import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "x-following.sh"


def request():
    return {
        "method": "GET",
        "path": "/graphql/current/Following",
        "params": {
            "variables": json.dumps({"userId": "example", "count": 20}),
            "features": json.dumps({"current": True}),
        },
        "headers": {"content-type": "application/json"},
    }


def page(user_ids, cursor=None, typename="User"):
    entries = [
        {
            "content": {
                "itemContent": {
                    "user_results": {
                        "result": {
                            "__typename": "User",
                            "rest_id": user_id,
                            "core": {"screen_name": f"user{user_id}"},
                        }
                    }
                }
            }
        }
        for user_id in user_ids
    ]
    if cursor is not None:
        entries.append({"content": {"cursorType": "Bottom", "value": cursor}})
    if typename == "UserUnavailable":
        return {"data": {"user": {"result": {"__typename": typename}}}}
    return {
        "data": {
            "user": {
                "result": {
                    "__typename": typename,
                    "timeline": {"instructions": [{"entries": entries}]},
                }
            }
        }
    }


FAKE_CURL = r'''#!/usr/bin/env python3
import json
import os
import shutil
import sys
from pathlib import Path

args = sys.argv[1:]
output = Path(args[args.index("--output") + 1])
headers = Path(args[args.index("--dump-header") + 1])
encoded = [args[index + 1] for index, value in enumerate(args) if value == "--data-urlencode"]
variables = next(value.removeprefix("variables=") for value in encoded if value.startswith("variables="))
root = Path(os.environ["FAKE_CURL_ROOT"])
with (root / "args.log").open("a") as stream:
    stream.write(json.dumps(args) + "\n")
count_file = root / "count"
count = int(count_file.read_text()) + 1 if count_file.exists() else 1
count_file.write_text(str(count))
with (root / "variables.log").open("a") as stream:
    stream.write(variables + "\n")
response = root / f"{count}.json"
if not response.exists():
    print("unexpected request", file=sys.stderr)
    sys.exit(7)
shutil.copyfile(response, output)
headers.write_text("HTTP/1.1 200 OK\r\n\r\n")
print("200", end="")
'''


class FollowingShellTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.bin = self.root / "bin"
        self.bin.mkdir()
        curl = self.bin / "curl"
        curl.write_text(FAKE_CURL, encoding="utf-8")
        curl.chmod(0o755)
        self.request_file = self.root / "request.ndjson"
        self.request_file.write_text(json.dumps(request()) + "\n", encoding="utf-8")
        self.output = self.root / "output"
        self.fake = self.root / "fake"
        self.fake.mkdir()

    def run_script(self):
        env = os.environ.copy()
        env.update(
            {
                "PATH": f"{self.bin}:{env['PATH']}",
                "TWITTER_RELAY_BASE_URL": "https://relay.example",
                "TWITTER_PROFILE_NAME": "test-profile",
                "TWITTER_USER_ID": "99",
                "FAKE_CURL_ROOT": str(self.fake),
                "X_FOLLOWING_PAGE_INTERVAL": "0",
                "X_FOLLOWING_PAGE_JITTER": "0",
            }
        )
        return subprocess.run(
            [
                "bash",
                str(SCRIPT),
                "--request",
                str(self.request_file),
                "--output-dir",
                str(self.output),
            ],
            env=env,
            text=True,
            capture_output=True,
        )

    def write_response(self, number, payload):
        (self.fake / f"{number}.json").write_text(json.dumps(payload), encoding="utf-8")

    def test_collects_two_pages_and_completed_rerun_makes_no_request(self):
        self.write_response(1, page(["1", "2"], "next"))
        self.write_response(2, page(["2", "3"], "0|done"))

        first = self.run_script()
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(json.loads(first.stdout)["users"], 3)
        records = [json.loads(line) for line in (self.output / "users.jsonl").read_text().splitlines()]
        self.assertEqual([record["rest_id"] for record in records], ["1", "2", "3"])
        self.assertEqual((self.output / "users.jsonl").stat().st_mode & 0o777, 0o600)
        self.assertEqual((self.fake / "count").read_text(), "2")
        curl_args = json.loads((self.fake / "args.log").read_text().splitlines()[0])
        self.assertIn("x-profile-name: test-profile", curl_args)

        second = self.run_script()
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertEqual((self.fake / "count").read_text(), "2")

    def test_resumes_from_saved_cursor_and_deduplicates(self):
        self.output.mkdir()
        (self.output / "users.jsonl").write_text('{"rest_id":"1"}\n', encoding="utf-8")
        (self.output / "state.json").write_text(
            json.dumps(
                {
                    "version": 3,
                    "profileName": "test-profile",
                    "requestPath": "/graphql/current/Following",
                    "userId": "99",
                    "cursor": "saved",
                    "completed": False,
                    "pages": 1,
                    "users": 1,
                }
            ),
            encoding="utf-8",
        )
        self.write_response(1, page(["1", "2"], "0|done"))

        result = self.run_script()
        self.assertEqual(result.returncode, 0, result.stderr)
        variables = json.loads((self.fake / "variables.log").read_text().splitlines()[0])
        self.assertEqual(variables["cursor"], "saved")
        self.assertEqual((self.output / "users.jsonl").read_text().count("\n"), 2)

    def test_rejects_state_for_another_profile(self):
        self.output.mkdir()
        (self.output / "users.jsonl").write_text('{"rest_id":"1"}\n', encoding="utf-8")
        (self.output / "state.json").write_text(
            json.dumps(
                {
                    "version": 3,
                    "profileName": "another-profile",
                    "requestPath": "/graphql/current/Following",
                    "userId": "99",
                    "cursor": "saved",
                    "completed": False,
                    "pages": 1,
                    "users": 1,
                }
            ),
            encoding="utf-8",
        )

        result = self.run_script()
        self.assertEqual(result.returncode, 1)
        self.assertIn("invalid or mismatched state", result.stderr)
        self.assertFalse((self.fake / "count").exists())

    def test_user_unavailable_does_not_write_state(self):
        self.write_response(1, page([], typename="UserUnavailable"))
        result = self.run_script()
        self.assertEqual(result.returncode, 1)
        self.assertIn("UserUnavailable", result.stderr)
        self.assertFalse((self.output / "state.json").exists())

    def test_unknown_schema_does_not_mark_collection_complete(self):
        self.write_response(1, {"data": {}})
        result = self.run_script()
        self.assertEqual(result.returncode, 1)
        self.assertIn("unexpected Following response schema", result.stderr)
        self.assertFalse((self.output / "state.json").exists())

    def test_preserves_following_order(self):
        self.write_response(1, page(["2", "10", "1"], "0|done"))
        result = self.run_script()
        self.assertEqual(result.returncode, 0, result.stderr)
        records = [json.loads(line) for line in (self.output / "users.jsonl").read_text().splitlines()]
        self.assertEqual([record["rest_id"] for record in records], ["2", "10", "1"])

    def test_zero_bottom_cursor_marks_collection_complete(self):
        self.write_response(1, page(["1"], "0|terminal"))
        result = self.run_script()
        self.assertEqual(result.returncode, 0, result.stderr)
        state = json.loads((self.output / "state.json").read_text())
        self.assertTrue(state["completed"])
        self.assertIsNone(state["cursor"])
        self.assertEqual((self.fake / "count").read_text(), "1")

    def test_missing_bottom_cursor_does_not_mark_collection_complete(self):
        self.write_response(1, page(["1"]))
        result = self.run_script()
        self.assertEqual(result.returncode, 1)
        self.assertIn("no Bottom cursor", result.stderr)
        self.assertFalse((self.output / "state.json").exists())

    def test_requires_successful_request_file(self):
        self.request_file.write_text(json.dumps({"method": "GET", "path": "/graphql/Viewer"}) + "\n")
        result = self.run_script()
        self.assertEqual(result.returncode, 1)
        self.assertIn("no GET /Following", result.stderr)

    def test_refuses_output_symlink(self):
        self.output.mkdir()
        outside = self.root / "outside"
        outside.write_text("", encoding="utf-8")
        (self.output / "users.jsonl").symlink_to(outside)
        result = self.run_script()
        self.assertEqual(result.returncode, 1)
        self.assertIn("refusing symlink", result.stderr)
        self.assertEqual(outside.read_text(), "")

    def test_refuses_output_directory_symlink(self):
        outside = self.root / "outside"
        outside.mkdir()
        self.output.symlink_to(outside, target_is_directory=True)
        result = self.run_script()
        self.assertEqual(result.returncode, 1)
        self.assertIn("refusing symlink", result.stderr)

    def test_rejects_concurrent_collector(self):
        self.output.mkdir()
        lock = self.output / ".x-following.lock"
        lock.mkdir()
        (lock / "pid").write_text(str(os.getpid()), encoding="utf-8")
        result = self.run_script()
        self.assertEqual(result.returncode, 1)
        self.assertIn("another collector", result.stderr)

    def test_recovers_stale_collector_lock(self):
        self.output.mkdir()
        lock = self.output / ".x-following.lock"
        lock.mkdir()
        (lock / "pid").write_text("99999999", encoding="utf-8")
        self.write_response(1, page(["1"], "0|done"))
        result = self.run_script()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(lock.exists())


if __name__ == "__main__":
    unittest.main()
