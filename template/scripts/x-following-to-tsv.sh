#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: x-following-to-tsv.sh INPUT.jsonl OUTPUT.tsv

Convert an x-following users.jsonl export to a tab-separated table.
EOF
}

if (($# != 2)); then
  usage >&2
  exit 2
fi

input=$1
output=$2
output_dir=$(dirname "$output")

[[ -f $input ]] || { echo "x-following-to-tsv: input file not found: $input" >&2; exit 2; }
[[ -d $output_dir ]] || { echo "x-following-to-tsv: output directory not found: $output_dir" >&2; exit 2; }
[[ ! -L $output ]] || { echo "x-following-to-tsv: refusing symlink: $output" >&2; exit 1; }
command -v jq >/dev/null || { echo "x-following-to-tsv: jq is required" >&2; exit 2; }

jq -e -s 'all(.[]; type == "object" and (.rest_id | type == "string"))' "$input" >/dev/null || {
  echo "x-following-to-tsv: invalid following JSONL: $input" >&2
  exit 1
}

temporary=$(mktemp "$output_dir/.x-following.tsv.XXXXXX")
cleanup() {
  [[ ! -e $temporary ]] || unlink "$temporary"
}
trap cleanup EXIT INT TERM

{
  printf 'rest_id\tscreen_name\tname\tdescription\tlocation\tfollowers_count\tfollowing_count\ttweet_count\tcreated_at\tverified\tblue_verified\tprotected\twebsite_url\n'
  jq -r '[
    .rest_id,
    (.core.screen_name // ""),
    (.core.name // ""),
    (.profile_bio.description // ""),
    (.location.location // ""),
    (.relationship_counts.followers // ""),
    (.relationship_counts.following // ""),
    (.tweet_counts.tweets // ""),
    (.core.created_at // ""),
    (.verification.verified // false),
    (.is_blue_verified // false),
    (.privacy.protected // false),
    (.website.url // "")
  ] | @tsv' "$input"
} >"$temporary"

mv -f -- "$temporary" "$output"
