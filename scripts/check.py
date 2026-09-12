#!/usr/bin/env python3
"""Fail if a who-approved record claims accepted without a human."""

from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
RECORDS = ROOT / "records"


def fields(text: str) -> dict[str, str]:
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    out: dict[str, str] = {}
    for line in parts[1].splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        out[key.strip()] = value.strip()
    return out


def main() -> int:
    if not RECORDS.is_dir():
        print("no records/ directory", file=sys.stderr)
        return 1
    errors = 0
    found = 0
    for path in sorted(RECORDS.glob("*.md")):
        if path.name.upper() == "TEMPLATE.MD":
            continue
        found += 1
        data = fields(path.read_text(encoding="utf-8"))
        ident = data.get("id", "")
        status = data.get("status", "")
        accepted_by = data.get("accepted_by", "")
        accepted_at = data.get("accepted_at", "")
        if not ident.startswith("WA-"):
            print(f"{path.name}: missing id WA-NNNN", file=sys.stderr)
            errors += 1
        if status not in {"proposed", "accepted"}:
            print(f"{path.name}: status must be proposed or accepted", file=sys.stderr)
            errors += 1
        if status == "accepted" and (not accepted_by or not accepted_at):
            print(
                f"{path.name}: accepted without accepted_by and accepted_at",
                file=sys.stderr,
            )
            errors += 1
        if status == "proposed" and (accepted_by or accepted_at):
            print(
                f"{path.name}: proposed record must not have accept fields",
                file=sys.stderr,
            )
            errors += 1
    if found == 0:
        print("no records to check (template only is ok)", file=sys.stderr)
    if errors:
        return 1
    print(f"ok ({found} record(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
