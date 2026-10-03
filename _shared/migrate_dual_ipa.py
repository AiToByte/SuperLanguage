# -*- coding: utf-8 -*-
"""Migrate and maintain the dual-accent phonetic fields.

    python _shared/migrate_dual_ipa.py            # dry run, prints a plan
    python _shared/migrate_dual_ipa.py --apply    # rewrite the month files
    python _shared/migrate_dual_ipa.py --refresh --apply

Entry layout, before
    (word, ipa_brE, meaning, example, translation)
Entry layout, after
    (word, "BrE /.../", "AmE /.../", meaning, example, translation)

The accent tag is stored **inside** the field, so every consumer shows it and
the audit can verify that the tag matches the transcription it labels.

The transform is idempotent: tags are stripped and re-applied on every pass,
so running it twice changes nothing.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from american_ipa import american_for  # noqa: E402
from audit_lib import split_label, with_label  # noqa: E402
from set_words import check_width, read_block, serialise  # noqa: E402
from toolkit import MODULES, ROOT, _load  # noqa: E402

WIDTH_BEFORE = 5
WIDTH_AFTER = 6


def rebuild(word, brit_val, ame_val):
    """Return (brE_field, amE_field, source, note) with both tags applied."""
    _, brit_core = split_label(brit_val)
    ame_core = split_label(ame_val)[1]
    fresh, source, note = american_for(word, brit_core)
    return with_label("BrE", brit_core), with_label("AmE", fresh or ame_core), \
        source, note


def migrate(module: str, apply: bool):
    report = {}
    stats = Counter()
    changed = 0
    for month in range(1, 13):
        rel = f"data/m{month:02d}.py"
        path = ROOT / module / "_build" / rel
        mod = _load(module, rel)
        words = [list(e) for e in mod.WORDS]
        widths = {len(e) for e in words}
        if widths == {WIDTH_BEFORE}:
            rows, prov = [], []
            for entry in words:
                word, brit, meaning, example, translation = entry
                b, a, source, note = rebuild(word, brit, "")
                rows.append([word, b, a, meaning, example, translation])
                prov.append({"word": word, "ipa_brE": b, "ipa_AmE": a,
                             "source": source, "note": note})
                stats[source] += 1
            report[f"m{month:02d}"] = prov
            if apply:
                lines, start, end = read_block(path)
                path.write_text(
                    "\n".join(lines[:start + 1] + serialise(rows)
                              + lines[end + 1:]), encoding="utf-8")
            changed += 1
            continue
        if widths != {WIDTH_AFTER}:
            raise SystemExit(
                f"{module}/{path.name}: unexpected entry widths {widths}")
        check_width(words, f"{module}/{path.name}")
        rows, prov, touched = [], [], False
        for word, brit, ame, meaning, example, translation in words:
            nb, na, source, note = rebuild(word, brit, ame)
            if (nb, na) != (brit, ame):
                touched = True
            rows.append([word, nb, na, meaning, example, translation])
            prov.append({"word": word, "ipa_brE": nb, "ipa_AmE": na,
                         "source": source, "note": note})
            stats[source] += 1
        report[f"m{month:02d}"] = prov
        if touched:
            if apply:
                lines, start, end = read_block(path)
                path.write_text(
                    "\n".join(lines[:start + 1] + serialise(rows)
                              + lines[end + 1:]), encoding="utf-8")
            changed += 1
    return stats, report, changed


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--refresh", action="store_true",
                    help="recompute the American transcription (default)")
    ap.add_argument("modules", nargs="*")
    args = ap.parse_args(argv[1:])
    targets = args.modules or MODULES
    grand = Counter()
    for module in targets:
        stats, report, files = migrate(module, args.apply)
        grand += stats
        vocab = ROOT / module / "vocabulary"
        vocab.mkdir(parents=True, exist_ok=True)
        if args.apply and report:
            (vocab / "IPA_Provenance.json").write_text(
                json.dumps(report, ensure_ascii=False, indent=1),
                encoding="utf-8")
        state = f"{files} month file(s) updated" if files else "already labelled"
        print(f"[{module}] {state}: "
              + " ".join(f"{k}={v}" for k, v in sorted(stats.items())))
    print(f"\ntotal: {dict(grand)}  sum={sum(grand.values())}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))