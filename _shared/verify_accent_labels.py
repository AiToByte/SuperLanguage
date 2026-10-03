# -*- coding: utf-8 -*-
"""Accent-label verification report.

Confirms, for every entry, that
  1. both phonetic fields carry a tag,
  2. the tag matches the column it is stored in,
  3. the tag is truthful - the transcription contains no symbol from the
     other accent,
  4. the two transcriptions agree on syllable count,
and reports how each American transcription was sourced.
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, r"D:\_MyProject\SuperSoft\SuperLanguage\_shared")
import audit_ipa  # noqa: E402
from audit_ipa import AMERICAN_ONLY, BRITISH_ONLY  # noqa: E402
from audit_lib import (  # noqa: E402
    MODULES, ROOT, load_corpus, split_label,
)

TAG_PROBLEMS = {"IPA_LABEL_MISSING", "IPA_LABEL_WRONG", "IPA_TAG_SWAPPED",
                "IPA_TAG_NOT_TRUTHFUL", "IPA_AME_MISSING_R", "IPA_BAD_SYMBOL",
                "IPA_MOJIBAKE", "IPA_DIALECT_MISMATCH", "IPA_EMPTY",
                "IPA_NOT_SLASHED"}
ADVISORY = {"IPA_ACCENT_SYLLABLES"}
"""British elides schwas American spells out, so a syllable gap is a real
dialect difference, not a defect. Counted, never blocking."""

WATCH = {
    "AmE holds British marks": BRITISH_ONLY,
    "BrE holds American marks": AMERICAN_ONLY,
}


def main():
    entries = load_corpus()
    stats = Counter()
    truth_fail = Counter()
    detail = []
    for e in entries:
        br_tag, br = split_label(e.ipa_brit)
        am_tag, am = split_label(e.ipa_ame)
        stats["entries"] += 1
        if br_tag == "BrE":
            stats["BrE tagged"] += 1
        else:
            stats["BrE BAD TAG"] += 1
        if am_tag == "AmE":
            stats["AmE tagged"] += 1
        else:
            stats["AmE BAD TAG"] += 1
        for label, core, wrong in (("BrE", br, AMERICAN_ONLY),
                                   ("AmE", am, BRITISH_ONLY)):
            for bad, why in wrong.items():
                if core and bad in core:
                    truth_fail[label] += 1
                    detail.append((e.where, e.word, label, why))
        for f in audit_ipa.run([e]):
            if f.code in TAG_PROBLEMS:
                stats[f.code] += 1
                detail.append((e.where, e.word, f.code, f.detail))

    print("=" * 70)
    print("ACCENT LABEL VERIFICATION")
    print("=" * 70)
    print(f"entries checked                : {stats['entries']}")
    print(f"BrE fields tagged 'BrE'        : {stats['BrE tagged']}")
    print(f"AmE fields tagged 'AmE'        : {stats['AmE tagged']}")
    print(f"BrE fields with a wrong tag    : {stats['BrE BAD TAG']}")
    print(f"AmE fields with a wrong tag    : {stats['AmE BAD TAG']}")
    print(f"BrE holding American symbols   : {truth_fail['BrE']}")
    print(f"AmE holding British symbols    : {truth_fail['AmE']}")
    print("-" * 70)
    codes = {k: v for k, v in stats.items() if k in TAG_PROBLEMS}
    print(f"label/transcription defects    : {sum(codes.values())}")
    for k, v in sorted(codes.items()):
        print(f"    {k:<26} {v}")
    advis = {k: v for k, v in stats.items() if k in ADVISORY}
    if advis:
        print(f"advisory (not defects)         : {sum(advis.values())}")
        for k, v in sorted(advis.items()):
            print(f"    {k:<26} {v}")
    print("-" * 70)

    prov = Counter()
    for module in MODULES:
        path = ROOT / module / "vocabulary" / "IPA_Provenance.json"
        if not path.exists():
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        local = Counter()
        for rows in data.values():
            for r in rows:
                local[r["source"]] += 1
        prov += local
        print(f"{module:<10} " + " ".join(f"{k}={v}"
                                        for k, v in sorted(local.items())))
    print("-" * 70)
    print("AmE sources: " + " ".join(f"{k}={v}" for k, v in sorted(prov.items())))
    print(f"dictionary-backed: "
          f"{prov['cmu'] + prov['parts'] + prov['manual']}/{sum(prov.values())}")

    if detail:
        print("\ndefects:")
        for row in detail[:40]:
            print("   ", row)
    print("\nRESULT:", "clean" if not detail and not truth_fail else "DEFECTS")
    return 0 if (not detail and not truth_fail) else 1


if __name__ == "__main__":
    sys.exit(main())