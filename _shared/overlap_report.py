# -*- coding: utf-8 -*-
"""Cross-module vocabulary overlap report.

    python _shared/overlap_report.py [Module ...]
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from toolkit import MODULES, load_months, normalise  # noqa: E402


def words_of(module):
    out = []
    for mod in load_months(module):
        out += [w[0] for w in mod.WORDS]
    return out


def main(argv):
    targets = [a for a in argv[1:] if not a.startswith("--")] or MODULES
    table = {}
    for module in targets:
        try:
            table[module] = words_of(module)
        except FileNotFoundError as exc:
            print(f"[{module}] SKIPPED - {exc}")

    print(f"{'module':<12}{'words':>7}{'unique':>8}   overlap with earlier modules")
    print("-" * 78)
    seen = {}
    for module in targets:
        words = table.get(module)
        if not words:
            continue
        keys = {normalise(w) for w in words}
        overlap = sorted({w for w in words if normalise(w) in seen})
        print(f"{module:<12}{len(words):>7}{len(keys):>8}   "
              f"{len(overlap)} ({len(overlap) / len(words) * 100:.1f}%)")
        for w in overlap:
            print(f"                        · {w}  (first in {seen[normalise(w)]})")
        for w in words:
            seen.setdefault(normalise(w), module)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))