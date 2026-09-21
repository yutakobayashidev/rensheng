import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "index.py"
spec = importlib.util.spec_from_file_location("index_helper", SCRIPT)
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)


class IndexWorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.put("AGENTS.md", "# Guidelines\n")
        self.put("philosophy.md", "# Philosophy\n")
        self.put("people/alice.md", '---\nupdated_at: "2026-01-15T18:30:00+09:00"\n---\n# Alice\n\nA fictional collaborator. Verified as of: 2026-01-14.\n')
        self.put("index.md", "# Index\n\n- [Alice](people/alice.md) — Collaboration context.\n")

    def put(self, name, text):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def run_command(self, *args, code=0):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--root", str(self.root), *args],
            capture_output=True, text=True, cwd=self.temp.name,
        )
        self.assertEqual(result.returncode, code, result.stdout + result.stderr)
        return result

    def pending(self):
        return json.loads(self.run_command("check", code=1).stdout)["pending"][0]

    def record(self, receipt=None, code=0):
        item = receipt or self.pending()
        return self.run_command("record", item["path"], "--sha256", item["sha256"],
                                "--entry-sha256", item["entry_sha256"], code=code)

    def test_review_then_content_change_and_noop_receipt(self):
        page = (self.root / "people/alice.md").read_bytes()
        index = (self.root / "index.md").read_bytes()
        item = self.pending()
        self.assertFalse((self.root / "index-state.json").exists())
        self.record(item)
        self.run_command("check")
        original_state = (self.root / "index-state.json").read_bytes()
        self.record(item)
        self.assertEqual((self.root / "index-state.json").read_bytes(), original_state)
        self.assertEqual((self.root / "people/alice.md").read_bytes(), page)
        self.assertEqual((self.root / "index.md").read_bytes(), index)
        self.put("people/alice.md", "# Alice\n\nReview received.\n")
        self.assertEqual(self.pending()["reasons"], ["page_changed"])
        self.record(item, code=2)
        self.assertEqual((self.root / "index-state.json").read_bytes(), original_state)
        self.record()
        self.run_command("check")

    def test_description_change_is_detected_independently(self):
        old = self.pending()
        self.record(old)
        self.put("index.md", "# Index\n\n- [Alice](people/alice.md) — Different description.\n")
        self.assertEqual(self.pending()["reasons"], ["entry_changed"])
        self.record(old, code=2)
        self.record()
        self.run_command("check")

    def test_add_rename_delete_and_missing_link(self):
        self.record()
        self.put("people/bob.md", "# Bob\n")
        report = json.loads(self.run_command("check", code=1).stdout)
        self.assertEqual(report["unlisted"], ["people/bob.md"])
        (self.root / "people/alice.md").rename(self.root / "people/alice-new.md")
        report = json.loads(self.run_command("check", code=1).stdout)
        self.assertEqual(report["missing"], ["people/alice.md"])
        self.put("index.md", "# Index\n\n- [Alice](people/alice-new.md) — Collaboration context.\n")
        self.run_command("prune", "people/alice-new.md", code=2)
        self.run_command("prune", "people/alice.md")
        self.record()
        (self.root / "people/bob.md").unlink()
        self.run_command("check")

    def test_guides_and_symlinks_are_excluded(self):
        self.record()
        for name in ("people/README.md", "people/index.md", "people/.private/note.md",
                     ".agents/skills/example/SKILL.md", "scripts/example.md"):
            self.put(name, "Not a personal page.\n")
        (self.root / "people/linked.md").symlink_to(self.root / "philosophy.md")
        (self.root / "people/linked-dir").symlink_to(self.root / "people", target_is_directory=True)
        self.run_command("check")

    def test_paths_with_spaces_and_unicode(self):
        self.put("people/あおい team.md", "# Aoi\n")
        self.put("index.md", "# Index\n\n- [Aoi](people/%E3%81%82%E3%81%8A%E3%81%84%20team.md) — Team context.\n")
        (self.root / "people/alice.md").unlink()
        self.record()
        self.run_command("check")

    def test_invalid_entries_and_state_fail_without_writes(self):
        self.record()
        original_state = (self.root / "index-state.json").read_bytes()
        for target in ("../outside.md", "people/../goals.md", "https://example.com/a.md", "people/README.md"):
            with self.subTest(target=target):
                self.put("index.md", f"# Index\n\n- [Bad]({target}) — Invalid.\n")
                self.run_command("check", code=2)
                self.assertEqual((self.root / "index-state.json").read_bytes(), original_state)
        self.put("index.md", "# Index\n\n- [Alice](people/alice.md) — Context.\n- [Again](people/alice.md) — Duplicate.\n")
        self.run_command("check", code=2)
        self.put("index.md", "# Index\n\n- [Alice](people/alice.md) — Context.\n")
        self.put("index-state.json", "{broken")
        self.run_command("check", code=2)
        self.assertEqual((self.root / "index-state.json").read_text(), "{broken")

    def test_lost_state_requires_review_and_timezone_is_written(self):
        self.record()
        state = json.loads((self.root / "index-state.json").read_text())
        self.assertTrue(state["pages"]["people/alice.md"]["indexed_at"].endswith("+00:00"))
        (self.root / "index-state.json").unlink()
        self.assertEqual(self.pending()["reasons"], ["unreviewed"])

    def test_state_symlink_is_not_overwritten(self):
        self.put("external.json", '{"pages": {}, "version": 1}\n')
        original = (self.root / "external.json").read_bytes()
        (self.root / "index-state.json").symlink_to(self.root / "external.json")
        self.run_command("check", code=2)
        self.assertEqual((self.root / "external.json").read_bytes(), original)

    def test_headings_do_not_invalidate_receipts_and_bad_dates_fail(self):
        self.record()
        self.put("index.md", "# New heading\n\n- [Alice](people/alice.md) — Collaboration context.\n")
        self.run_command("check")
        state = json.loads((self.root / "index-state.json").read_text())
        state["pages"]["people/alice.md"]["indexed_at"] = "2026-01-15T18:30:00"
        self.put("index-state.json", json.dumps(state))
        self.run_command("check", code=2)


if __name__ == "__main__":
    unittest.main()
