# -*- coding: utf-8 -*-
"""Trim a month's WORDS list to an exact row count.

Usage:
    python _shared/trim_month.py <Module> <mXX.py> [count]

Keeps the first `count` rows (default: DAYS * 3) and rewrites the file so the
list is well formed. Rows after the kept ones are dropped, which is the
preferred behaviour when extra candidate rows were appended.
"""
import importlib.util
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROW = re.compile(r'^    \("')


def load_days(module: str, path: Path) -> int:
    spec = importlib.util.spec_from_file_location("_days", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return int(mod.DAYS)


def main(argv: list[str]) -> int:
    if not 2 <= len(argv) <= 3:
        print(__doc__.strip())
        return 2

    module, name = argv[0], argv[1]
    path = ROOT / module / "_build" / "data" / name
    limit = int(argv[2]) if len(argv) == 3 else load_days(module, path) * 3

    lines = path.read_text(encoding="utf-8").splitlines()
    start = next(i for i, l in enumerate(lines) if l.startswith("WORDS = ["))
    try:
        end = next(i for i, l in enumerate(lines) if i > start and l.strip() == "]")
        tail = [l for l in lines[end + 1:] if l.strip()]
    except StopIteration:
        tail = []
        end = len(lines)

    rows = [l for l in lines[start + 1:] if ROW.match(l)]
    kept = rows[:limit]
    if len(kept) < limit:
        print("FAIL: only %d rows available, need %d" % (len(rows), limit))
        return 1

    path.write_text("\n".join(lines[:start + 1] + kept + ["]"] + tail) + "\n",
                    encoding="utf-8")
    print("%s/%s: kept %d rows (dropped %d)" % (module, name, len(kept), len(rows) - len(kept)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
