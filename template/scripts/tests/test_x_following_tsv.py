import csv
import json
import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "x-following-to-tsv.sh"


class FollowingTsvTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / "users.jsonl"
        self.output = self.root / "users.tsv"

    def test_converts_selected_fields_in_input_order(self):
        records = [
            {
                "rest_id": "2",
                "core": {"screen_name": "second", "name": "Second\tUser", "created_at": "now"},
                "profile_bio": {"description": "line 1\nline 2"},
                "location": {"location": "Tokyo"},
                "relationship_counts": {"followers": 20, "following": 4},
                "tweet_counts": {"tweets": 8},
                "verification": {"verified": True},
                "is_blue_verified": False,
                "privacy": {"protected": False},
                "website": {"url": "https://example.com"},
            },
            {"rest_id": "1", "core": {"screen_name": "first", "name": "First"}},
        ]
        self.source.write_text("".join(json.dumps(record) + "\n" for record in records), encoding="utf-8")

        result = subprocess.run(
            ["bash", str(SCRIPT), str(self.source), str(self.output)],
            text=True,
            capture_output=True,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        with self.output.open(newline="", encoding="utf-8") as stream:
            rows = list(csv.DictReader(stream, delimiter="\t"))
        self.assertEqual([row["rest_id"] for row in rows], ["2", "1"])
        self.assertEqual(rows[0]["name"], "Second\\tUser")
        self.assertEqual(rows[0]["description"], "line 1\\nline 2")
        self.assertEqual(rows[0]["followers_count"], "20")
        self.assertEqual(rows[1]["verified"], "false")

    def test_rejects_invalid_jsonl_without_replacing_output(self):
        self.source.write_text('{"no_rest_id":true}\n', encoding="utf-8")
        self.output.write_text("keep\n", encoding="utf-8")

        result = subprocess.run(
            ["bash", str(SCRIPT), str(self.source), str(self.output)],
            text=True,
            capture_output=True,
        )

        self.assertEqual(result.returncode, 1)
        self.assertEqual(self.output.read_text(encoding="utf-8"), "keep\n")


if __name__ == "__main__":
    unittest.main()
