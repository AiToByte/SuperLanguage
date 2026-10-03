# -*- coding: utf-8 -*-
"""Bulk-rewrite vocabulary examples so each opens with its target headword.

    python _shared/fix_examples.py <patches.json>

The JSON file maps a data-file name (e.g. ``m03.py``) to a dict of
``{"old sentence": "new sentence"}`` pairs. Every ``old`` must be present or
the script exits non-zero, so nothing is silently skipped.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    module = argv[1]
    patches_file = Path(argv[2])
    patches = json.loads(patches_file.read_text(encoding="utf-8"))

    data_dir = ROOT / module / "_build" / "data"
    failures, applied = [], 0
    for fname, pairs in patches.items():
        path = data_dir / fname
        if not path.exists():
            failures.append(f"{fname}: file not found")
            continue
        text = path.read_text(encoding="utf-8")
        for old, new in pairs.items():
            if old not in text:
                failures.append(f"{fname}: NOT FOUND -> {old[:60]}")
                continue
            text = text.replace(old, new, 1)
            applied += 1
        path.write_text(text, encoding="utf-8")
        print(f"  patched {fname}: {len(pairs)} pair(s)")

    print(f"\napplied {applied} replacement(s)")
    if failures:
        print("FAILURES:")
        for f in failures:
            print("  -", f)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))