#!/usr/bin/env bash
set -euo pipefail
umask 077

page_interval=${X_FOLLOWING_PAGE_INTERVAL:-10}
page_jitter=${X_FOLLOWING_PAGE_JITTER:-20}
backoff_base=${X_FOLLOWING_BACKOFF_BASE:-60}
max_retries=${X_FOLLOWING_MAX_RETRIES:-5}
timeout=${X_FOLLOWING_TIMEOUT:-30}
profile_name=${TWITTER_PROFILE_NAME:-}

usage() {
  cat <<'EOF'
Usage: x-following.sh --request FILE --profile NAME [--user-id ID] [--output-dir DIR]

Collect an X account's following list through TWITTER_RELAY_BASE_URL.

Options:
  --request FILE    Successful Following request in JSON or NDJSON format
  --profile NAME    Relay profile name (default: TWITTER_PROFILE_NAME)
  --user-id ID      Numeric X user ID (default: TWITTER_USER_ID)
  --output-dir DIR  Output directory (default: repository records/x-following)
  -h, --help        Show this help
EOF
}

request_file=
user_id=${TWITTER_USER_ID:-}
script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
output_dir=${X_FOLLOWING_OUTPUT_DIR:-$(dirname "$script_dir")/records/x-following}

while (($#)); do
  case $1 in
    --request)
      (($# >= 2)) || { echo "x-following: --request needs a file" >&2; exit 2; }
      request_file=$2
      shift 2
      ;;
    --user-id)
      (($# >= 2)) || { echo "x-following: --user-id needs an ID" >&2; exit 2; }
      user_id=$2
      shift 2
      ;;
    --profile)
      (($# >= 2)) || { echo "x-following: --profile needs a name" >&2; exit 2; }
      profile_name=$2
      shift 2
      ;;
    --output-dir)
      (($# >= 2)) || { echo "x-following: --output-dir needs a directory" >&2; exit 2; }
      output_dir=$2
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "x-following: unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

[[ -n ${TWITTER_RELAY_BASE_URL:-} ]] || { echo "x-following: TWITTER_RELAY_BASE_URL is required" >&2; exit 2; }
[[ -n $profile_name ]] || { echo "x-following: --profile or TWITTER_PROFILE_NAME is required" >&2; exit 2; }
[[ $user_id =~ ^[0-9]+$ ]] || { echo "x-following: --user-id or TWITTER_USER_ID must be numeric" >&2; exit 2; }
[[ -n $request_file && -f $request_file ]] || { echo "x-following: --request must be a readable file" >&2; exit 2; }
command -v curl >/dev/null || { echo "x-following: curl is required" >&2; exit 2; }
command -v jq >/dev/null || { echo "x-following: jq is required" >&2; exit 2; }
for setting in page_interval page_jitter max_retries; do
  value=${!setting}
  [[ $value =~ ^[0-9]+$ ]] || { echo "x-following: $setting must be a non-negative integer" >&2; exit 2; }
done
for setting in backoff_base timeout; do
  value=${!setting}
  [[ $value =~ ^[1-9][0-9]*$ ]] || { echo "x-following: $setting must be a positive integer" >&2; exit 2; }
done

template=$(jq -c 'select(.method == "GET" and (.path | endswith("/Following")))' "$request_file" | tail -n 1)
[[ -n $template ]] || { echo "x-following: no GET /Following request in $request_file" >&2; exit 1; }

request_path=$(jq -r '.path' <<<"$template")
base_variables=$(jq -r '.params.variables' <<<"$template")
request_features=$(jq -r '.params.features' <<<"$template")
jq -e 'type == "object" and (.userId | type == "string")' <<<"$base_variables" >/dev/null || {
  echo "x-following: Following variables must contain a string userId" >&2
  exit 1
}

if [[ -L $output_dir ]]; then
  echo "x-following: refusing symlink: $output_dir" >&2
  exit 1
elif [[ -e $output_dir ]]; then
  [[ -d $output_dir ]] || { echo "x-following: output path is not a directory: $output_dir" >&2; exit 1; }
else
  mkdir -p "$output_dir"
  chmod 700 "$output_dir"
fi
output=$output_dir/users.jsonl
state_file=$output_dir/state.json
for target in "$output" "$state_file"; do
  [[ ! -L $target ]] || { echo "x-following: refusing symlink: $target" >&2; exit 1; }
done

lock_dir=$output_dir/.x-following.lock
if ! mkdir "$lock_dir" 2>/dev/null; then
  lock_pid=$(cat "$lock_dir/pid" 2>/dev/null || true)
  if [[ $lock_pid =~ ^[0-9]+$ ]] && kill -0 "$lock_pid" 2>/dev/null; then
    echo "x-following: another collector is using $output_dir (pid=$lock_pid)" >&2
    exit 1
  fi
  [[ ! -e $lock_dir/pid ]] || unlink "$lock_dir/pid"
  rmdir "$lock_dir" 2>/dev/null || { echo "x-following: cannot recover stale lock: $lock_dir" >&2; exit 1; }
  mkdir "$lock_dir"
fi
printf '%s\n' "$$" >"$lock_dir/pid"
work_dir=
cleanup() {
  if [[ -n ${work_dir:-} && $work_dir == "$output_dir"/.x-following.* ]]; then
    rm -rf -- "$work_dir"
  fi
  [[ ! -e $lock_dir/pid ]] || unlink "$lock_dir/pid"
  rmdir "$lock_dir" 2>/dev/null || true
}
trap cleanup EXIT INT TERM

if [[ -f $output ]]; then
  jq -e -s 'all(.[]; type == "object" and (.rest_id | type == "string"))' "$output" >/dev/null || {
    echo "x-following: invalid output file: $output" >&2
    exit 1
  }
else
  : >"$output"
fi

if [[ -s $output && ! -f $state_file ]]; then
  echo "x-following: non-empty output has no state file: $output" >&2
  exit 1
fi

declare -A seen=()
user_count=0
while IFS= read -r id; do
  if [[ -z ${seen[$id]+present} ]]; then
    seen[$id]=1
    ((user_count += 1))
  fi
done < <(jq -r '.rest_id' "$output")

cursor=
pages=0
if [[ -f $state_file ]]; then
  jq -e \
    --arg profile_name "$profile_name" \
    --arg request_path "$request_path" \
    --arg user_id "$user_id" '
    .version == 3 and
    .profileName == $profile_name and
    .requestPath == $request_path and
    .userId == $user_id and
    (.completed | type == "boolean") and
    (.pages | type == "number") and
    (.users | type == "number") and
    (if .completed then .cursor == null else (.cursor | type == "string" and length > 0) end)
  ' "$state_file" >/dev/null || { echo "x-following: invalid or mismatched state file: $state_file" >&2; exit 1; }
  saved_users=$(jq -r '.users' "$state_file")
  ((user_count >= saved_users)) || { echo "x-following: output has fewer users than the saved state" >&2; exit 1; }
  if [[ $(jq -r '.completed' "$state_file") == true ]]; then
    jq -c '.' "$state_file"
    exit 0
  fi
  cursor=$(jq -r '.cursor' "$state_file")
  pages=$(jq -r '.pages' "$state_file")
  echo "resuming after page=$pages with $user_count users" >&2
fi

work_dir=$(mktemp -d "$output_dir/.x-following.XXXXXX")

write_state() {
  local completed=$1
  local temporary
  temporary=$(mktemp "$output_dir/.state.XXXXXX")
  jq -n \
    --arg profile_name "$profile_name" \
    --arg request_path "$request_path" \
    --arg user_id "$user_id" \
    --arg cursor "$cursor" \
    --argjson completed "$completed" \
    --argjson pages "$pages" \
    --argjson users "$user_count" \
    '{
      version: 3,
      profileName: $profile_name,
      requestPath: $request_path,
      userId: $user_id,
      cursor: (if $completed then null else $cursor end),
      completed: $completed,
      pages: $pages,
      users: $users
    }' \
    >"$temporary"
  mv -f -- "$temporary" "$state_file"
}

fetch_page() {
  local variables=$1
  local attempt=0
  local code curl_status delay retry_after jitter
  while ((attempt <= max_retries)); do
    : >"$work_dir/headers"
    : >"$work_dir/body.json"
    set +e
    code=$(curl --silent --show-error --get \
      --max-time "$timeout" \
      --user-agent 'Mozilla/5.0 (X11; Linux x86_64; rv:156.0) Gecko/20100101 Firefox/156.0' \
      --header 'accept: */*' \
      --header 'content-type: application/json' \
      --header "x-profile-name: $profile_name" \
      --dump-header "$work_dir/headers" \
      --output "$work_dir/body.json" \
      --write-out '%{http_code}' \
      "${TWITTER_RELAY_BASE_URL%/}/i/api${request_path}" \
      --data-urlencode "variables=$variables" \
      --data-urlencode "features=$request_features")
    curl_status=$?
    set -e

    if ((curl_status == 0)) && [[ $code =~ ^2[0-9][0-9]$ ]]; then
      return 0
    fi
    if ((curl_status == 0)) && [[ $code != 429 && ! $code =~ ^5[0-9][0-9]$ ]]; then
      echo "x-following: HTTP $code from relay" >&2
      return 1
    fi
    if ((attempt == max_retries)); then
      echo "x-following: relay request failed after $((max_retries + 1)) attempts (curl=$curl_status, HTTP=$code)" >&2
      return 1
    fi

    delay=$((backoff_base * (2 ** attempt)))
    retry_after=$(awk 'tolower($1) == "retry-after:" {gsub("\\r", "", $2); print $2; exit}' "$work_dir/headers")
    if [[ $retry_after =~ ^[0-9]+$ ]] && ((retry_after > delay)); then
      delay=$retry_after
    fi
    jitter=$((RANDOM % (page_jitter + 1)))
    delay=$((delay + jitter))
    echo "request failed (curl=$curl_status, HTTP=$code); retrying in ${delay}s" >&2
    sleep "$delay"
    ((attempt += 1))
  done
}

echo "using $request_path" >&2
while :; do
  if [[ -n $cursor ]]; then
    variables=$(jq -c --arg user_id "$user_id" --arg cursor "$cursor" '.userId=$user_id | .cursor=$cursor' <<<"$base_variables")
  else
    variables=$(jq -c --arg user_id "$user_id" '.userId=$user_id | del(.cursor)' <<<"$base_variables")
  fi

  fetch_page "$variables"
  if jq -e '.errors? | type == "array" and length > 0' "$work_dir/body.json" >/dev/null; then
    echo "x-following: GraphQL errors: $(jq -c '.errors' "$work_dir/body.json")" >&2
    exit 1
  fi
  if jq -e '.data.user.result.__typename == "UserUnavailable"' "$work_dir/body.json" >/dev/null; then
    echo "x-following: Following returned UserUnavailable" >&2
    exit 1
  fi
  jq -e '
    .data.user.result as $root
    | ($root | type == "object")
      and ($root.__typename == "User")
      and ([$root | .. | objects | .instructions? | select(type == "array")] | length > 0)
  ' "$work_dir/body.json" >/dev/null || {
    echo "x-following: unexpected Following response schema" >&2
    exit 1
  }

  jq -c '
    .. | objects | .user_results?.result?
    | select(type == "object" and .__typename == "User" and (.rest_id | type == "string"))
  ' "$work_dir/body.json" >"$work_dir/users.jsonl"
  next_cursor=$(jq -r 'first(.. | objects | select(.cursorType? == "Bottom" and (.value | type == "string")) | .value) // empty' "$work_dir/body.json")
  [[ -n $next_cursor ]] || { echo "x-following: Following response has no Bottom cursor" >&2; exit 1; }
  if [[ $next_cursor == 0\|* ]]; then
    next_cursor=
  fi
  [[ -z $next_cursor || $next_cursor != "$cursor" ]] || { echo "x-following: Following returned the same Bottom cursor" >&2; exit 1; }

  received=0
  added=0
  while IFS= read -r user; do
    ((received += 1))
    id=$(jq -r '.rest_id' <<<"$user")
    if [[ -z ${seen[$id]+present} ]]; then
      printf '%s\n' "$user"
      seen[$id]=1
      ((user_count += 1))
      ((added += 1))
    fi
  done <"$work_dir/users.jsonl" >>"$output"

  ((pages += 1))
  cursor=$next_cursor
  if [[ -z $cursor ]]; then
    write_state true
  else
    write_state false
  fi
  echo "page=$pages received=$received added=$added total=$user_count" >&2

  if [[ -z $cursor ]]; then
    jq -c '.' "$state_file"
    exit 0
  fi
  delay=$((page_interval + RANDOM % (page_jitter + 1)))
  echo "waiting ${delay}s" >&2
  sleep "$delay"
done
