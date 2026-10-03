# -*- coding: utf-8 -*-
"""Vocabulary QA: completeness, uniqueness, IPA shape, example-opening rule.

    python _shared/validate.py [Module ...]
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from toolkit import (  # noqa: E402
    MODULES, ROOT, _load, normalise, opens_with_target, split_label, with_label,
)


def check_module(name: str):
    """Validate whatever month data files exist for the module.

    Returns (months_loaded, total_words, unique, problems, missing_months).
    """
    data_dir = ROOT / name / "_build" / "data"
    present = [i for i in range(1, 13) if (data_dir / f"m{i:02d}.py").exists()]
    missing = [i for i in range(1, 13) if i not in present]
    if not present:
        raise FileNotFoundError(data_dir)

    months, problems, seen, total = [], [], {}, 0
    for i in present:
        mod = _load(name, f"data/m{i:02d}.py")
        months.append(mod)
        words = mod.WORDS
        if len(words) != mod.DAYS * 3:
            problems.append(
                f"M{mod.MONTH:02d}: word count {len(words)} != DAYS*3 ({mod.DAYS * 3})")
        for j, entry in enumerate(words):
                total += 1
                if len(entry) != 6:
                    problems.append(
                        f"M{mod.MONTH:02d} #{j}: entry must have 6 fields "
                        f"(word, ipa_brE, ipa_AmE, meaning, example, "
                        f"translation), got {len(entry)}")
                    continue
                word, ipa_brit, ipa_ame, meaning, example, translation = entry

                key = normalise(word)
                if key in seen:
                    problems.append(
                        f"M{mod.MONTH:02d} #{j}: DUPLICATE '{word}' "
                        f"(already in M{seen[key][0]:02d})")
                else:
                    seen[key] = (mod.MONTH, word)

                for label, value, accent in (("BrE", ipa_brit, "BrE"),
                                           ("AmE", ipa_ame, "AmE")):
                    tag, core = split_label(value)
                    if not value:
                        problems.append(
                            f"M{mod.MONTH:02d} '{word}': empty {label} phonetic")
                        continue
                    if tag is None:
                        problems.append(
                            f"M{mod.MONTH:02d} '{word}': {label} phonetic "
                            f"has no accent tag -> {value!r} (expected "
                            f"'{accent} /.../')")
                        continue
                    if tag != accent:
                        problems.append(
                            f"M{mod.MONTH:02d} '{word}': {label} field is "
                            f"tagged {tag!r}")
                    if not core.startswith("/") or not core.endswith("/"):
                        problems.append(
                            f"M{mod.MONTH:02d} '{word}': {label} IPA must be "
                            f"wrapped in slashes")
                    if core.count("/") != 2:
                        problems.append(
                            f"M{mod.MONTH:02d} '{word}': {label} IPA has "
                            f"{core.count('/')} slashes: {core!r}")
                if not meaning.strip():
                    problems.append(f"M{mod.MONTH:02d} '{word}': empty meaning")
                if not opens_with_target(example, word):
                    problems.append(
                        f"M{mod.MONTH:02d} '{word}': example does not open "
                        f"with the word -> '{example[:60]}'")
                if not re.search(r"[\u4e00-\u9fff]", translation):
                    problems.append(
                        f"M{mod.MONTH:02d} '{word}': translation has no "
                        f"Chinese characters")

    return months, total, seen, problems, missing


def main(argv):
    targets = [a for a in argv[1:] if not a.startswith("--")] or MODULES
    rc = 0
    for name in targets:
        try:
            months, total, seen, problems, missing = check_module(name)
        except FileNotFoundError as exc:
            print(f"[{name}] SKIPPED - missing {exc}")
            continue
        head = f"[{name}] months={len(months)}/12 words={total} unique={len(seen)}"
        print(head + (f" (pending months: {missing})" if missing else ""))
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
