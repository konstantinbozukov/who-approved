from __future__ import annotations

import importlib.util
import io
import pathlib
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
CHECK_PATH = REPO_ROOT / "scripts" / "check.py"


def load_check_module():
    spec = importlib.util.spec_from_file_location("who_approved_check", CHECK_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


check = load_check_module()

PROPOSED = """---
id: WA-9001
title: test proposed
status: proposed
date: 2026-01-01
irreversible: other
proposed_by: agent
proposed_at: 2026-01-01T00:00:00Z
accepted_by:
accepted_at:
---

## Decision

Test.
"""

ACCEPTED = """---
id: WA-9002
title: test accepted
status: accepted
date: 2026-01-01
irreversible: other
proposed_by: agent
proposed_at: 2026-01-01T00:00:00Z
accepted_by: Example Human
accepted_at: 2026-01-02T00:00:00Z
---

## Decision

Test.
"""


class CheckRecordsTests(unittest.TestCase):
    def write_record(self, directory: pathlib.Path, name: str, body: str) -> None:
        (directory / name).write_text(body, encoding="utf-8")

    def run_validate(self, records_dir: pathlib.Path) -> tuple[int, str, str]:
        out = io.StringIO()
        err = io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = check.validate_records(records_dir)
        return code, out.getvalue(), err.getvalue()

    def test_valid_proposed_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            records = pathlib.Path(tmp)
            self.write_record(records, "TEMPLATE.md", PROPOSED)
            self.write_record(records, "WA-9001-test.md", PROPOSED)
            code, out, err = self.run_validate(records)
            self.assertEqual(code, 0)
            self.assertIn("ok (1 record(s))", out)
            self.assertEqual(err, "")

    def test_valid_accepted_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            records = pathlib.Path(tmp)
            self.write_record(records, "WA-9002-test.md", ACCEPTED)
            code, out, _ = self.run_validate(records)
            self.assertEqual(code, 0)
            self.assertIn("ok (1 record(s))", out)

    def test_accepted_missing_accept_fields_fails(self) -> None:
        body = ACCEPTED.replace("accepted_by: Example Human", "accepted_by:")
        with tempfile.TemporaryDirectory() as tmp:
            records = pathlib.Path(tmp)
            self.write_record(records, "WA-9002-test.md", body)
            code, out, err = self.run_validate(records)
            self.assertEqual(code, 1)
            self.assertEqual(out, "")
            self.assertIn("accepted without accepted_by and accepted_at", err)

    def test_accepted_missing_accepted_at_fails(self) -> None:
        body = ACCEPTED.replace(
            "accepted_at: 2026-01-02T00:00:00Z", "accepted_at:"
        )
        with tempfile.TemporaryDirectory() as tmp:
            records = pathlib.Path(tmp)
            self.write_record(records, "WA-9002-test.md", body)
            code, _, err = self.run_validate(records)
            self.assertEqual(code, 1)
            self.assertIn("accepted without accepted_by and accepted_at", err)

    def test_proposed_with_accept_fields_fails(self) -> None:
        body = PROPOSED.replace(
            "accepted_by:",
            "accepted_by: Someone",
        )
        with tempfile.TemporaryDirectory() as tmp:
            records = pathlib.Path(tmp)
            self.write_record(records, "WA-9001-test.md", body)
            code, _, err = self.run_validate(records)
            self.assertEqual(code, 1)
            self.assertIn("proposed record must not have accept fields", err)

    def test_invalid_status_fails(self) -> None:
        body = PROPOSED.replace("status: proposed", "status: draft")
        with tempfile.TemporaryDirectory() as tmp:
            records = pathlib.Path(tmp)
            self.write_record(records, "WA-9001-test.md", body)
            code, _, err = self.run_validate(records)
            self.assertEqual(code, 1)
            self.assertIn("status must be proposed or accepted", err)

    def test_malformed_frontmatter_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            records = pathlib.Path(tmp)
            (records / "WA-9001-test.md").write_text(
                "# no frontmatter\n", encoding="utf-8"
            )
            code, _, err = self.run_validate(records)
            self.assertEqual(code, 1)
            self.assertIn("missing id WA-NNNN", err)
            self.assertIn("status must be proposed or accepted", err)

    def test_repo_records_directory_passes(self) -> None:
        code, out, err = self.run_validate(REPO_ROOT / "records")
        self.assertEqual(code, 0)
        self.assertIn("ok (1 record(s))", out)
        self.assertEqual(err, "")

    def test_main_uses_repo_records(self) -> None:
        out = io.StringIO()
        with redirect_stdout(out):
            code = check.main()
        self.assertEqual(code, 0)
        self.assertIn("ok (1 record(s))", out.getvalue())


if __name__ == "__main__":
    unittest.main()