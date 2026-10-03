# -*- coding: utf-8 -*-
"""Action-tree QA: scenario coverage, CN/EN uniqueness, gerund-first phrasing.

    python _shared/validate_actions.py [Module ...]
"""
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from toolkit import MODULES, load_actions, looks_like_gerund  # noqa: E402

MAX_WORDS = 6


def check_module(name: str):
    cats = load_actions(name)
    problems = []
    cn_counter, en_counter = Counter(), Counter()
    total = 0

    for cat in cats:
        if not cat.get("actions"):
            problems.append(f"category {cat['id']} '{cat['name_cn']}': empty")
        for cn, en in cat["actions"]:
            total += 1
            cn_counter[cn] += 1
            en_counter[en] += 1
            if not looks_like_gerund(en):
                problems.append(f"{cat['name_cn']} | {cn} — {en}: not a gerund form")
            if not re.search(r"[a-z]", en):
                problems.append(f"{cat['name_cn']} | {cn} — {en}: no latin letters")
            if len(en.split()) > MAX_WORDS:
                problems.append(f"{cat['name_cn']} | {cn} — {en}: longer than {MAX_WORDS} words")

    for cn, n in cn_counter.items():
        if n > 1:
            problems.append(f"DUPLICATE chinese action: {cn} x{n}")
    for en, n in en_counter.items():
        if n > 1:
            problems.append(f"DUPLICATE english phrase: {en} x{n}")
    return cats, total, problems


def main(argv):
    targets = argv[1:] or MODULES
    rc = 0
    for name in targets:
        try:
            cats, total, problems = check_module(name)
        except FileNotFoundError as exc:
            print(f"[{name}] SKIPPED - missing {exc}")
            continue
        print(f"[{name}] scenarios={len(cats)} actions={total}")
        for cat in cats:
            print(f"   {cat['id']}. {cat['name_cn']:<14} {len(cat['actions']):>3} 条")
        if problems:
            rc = 1
            print(f"  PROBLEMS ({len(problems)}):")
            for p in problems:
                print("   -", p)
        else:
            print("  All checks passed.")
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv))
