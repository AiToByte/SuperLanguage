# -*- coding: utf-8 -*-
"""Safe, idempotent entry patcher.

Loads a month module, applies field patches to ``WORDS`` **in memory**, then
rewrites only the ``WORDS`` block from those tuples.  Nothing is re-parsed from
the source text, so a patch can never corrupt an unrelated field.

    python _shared/set_words.py Finance 4 --set 63=translation=挑战性目标背后必须有写明责任人的支持。
    python _shared/set_words.py Legal 5 --set 76=word=thereafter --set 76=ipa=/ˌðeərˈɑːftə(r)/
    python _shared/set_words.py Marketing 11 --show 72

Reads the patch list from a JSON file with ``--json`` when the values contain
characters that are awkward to pass on a command line.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from toolkit import ROOT, _load  # noqa: E402

FIELDS = ("word", "ipa_brit", "ipa_ame", "meaning", "example", "translation")


def check_width(words, where):
    """Refuse to patch when the entry shape does not match FIELDS.

    Without this guard a patch written for the 6-field layout would silently
    overwrite the wrong field of a 5-field file.
    """
    if not words:
        raise SystemExit(f"{where}: no entries")
    bad = [i for i, e in enumerate(words) if len(e) != len(FIELDS)]
    if bad:
        widths = sorted({len(e) for e in words})
        raise SystemExit(
            f"{where}: expected {len(FIELDS)} fields per entry, found "
            f"{widths} (first offender index {bad[0]}). "
            f"Refusing to patch - migrate the data first.")


def read_block(path: Path):
    """Return (head_lines, words_start, words_end) for a month file."""
    lines = path.read_text(encoding="utf-8").split("\n")
    start = None
    for i, line in enumerate(lines):
        if line.startswith("WORDS"):
            start = i
            break
    if start is None:
        raise SystemExit(f"{path}: no WORDS assignment found")
    end = None
    for i in range(start, len(lines)):
        if lines[i].rstrip().endswith("]") and "[" not in lines[i]:
            end = i
            break
    if end is None:
        raise SystemExit(f"{path}: cannot find the end of the WORDS list")
    return lines, start, end


def serialise(entries):
    """Body of the WORDS list (the caller keeps the ``WORDS = [`` line)."""
    out = []
    for e in entries:
        cells = ", ".join('"%s"' % str(v).replace("\\", "\\\\").replace('"', '\\"')
                          for v in e)
        out.append("    (%s)," % cells)
    out.append("]")
    return out


def patch_one(module, month, patches, apply, show=()):
    path = ROOT / module / "_build" / "data" / f"m{month:02d}.py"
    lines, start, end = read_block(path)
    mod = _load(module, f"data/m{month:02d}.py")
    words = [list(e) for e in mod.WORDS]
    check_width(words, f"{module}/{path.name}")

    for index in show:
        if 0 <= index < len(words):
            label = " | ".join(f"{f}={v!r}" for f, v in zip(FIELDS, words[index]))
            print(f"  #{index} {label}")

    changed = []
    for index in sorted(patches):
        if not 0 <= index < len(words):
            raise SystemExit(
                f"{module} M{month:02d}: index {index} out of range "
                f"(0..{len(words) - 1})")
        for field, value in patches[index].items():
            pos = FIELDS.index(field)
            if words[index][pos] != value:
                changed.append(
                    f"  #{index} {field}: {words[index][pos]!r} -> {value!r}")
                words[index][pos] = value

    if changed and apply:
        new_lines = lines[:start + 1] + serialise(words) + lines[end + 1:]
        path.write_text("\n".join(new_lines), encoding="utf-8")
        print(f"{module}/{path.name}: applied {len(changed)} change(s)")
        for c in changed:
            print(c)
    elif changed:
        print(f"{module}/{path.name}: {len(changed)} change(s) pending")
        for c in changed:
            print(c)
    else:
        print(f"{module}/{path.name}: already up to date ({len(words)} entries)")
    return len(changed)


def main(argv):
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("module", nargs="?", default="")
    ap.add_argument("month", nargs="?", type=int)
    ap.add_argument("--set", action="append", default=[],
                    metavar="INDEX=FIELD=VALUE")
    ap.add_argument("--json", default="", metavar="PATH",
                    help='JSON list of {"module","month","index","fields"}')
    ap.add_argument("--show", action="append", type=int, default=[])
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args(argv[1:])

    if args.json:
        payload = json.loads(Path(args.json).read_text(encoding="utf-8"))
        grouped = {}
        default_module = args.module or None
        for item in payload:
            module = item.get("module") or default_module
            if not module:
                raise SystemExit("payload item has no 'module'")
            month = item.get("month", args.month)
            if month is None:
                raise SystemExit("payload item has no 'month'")
            grouped.setdefault((module, int(month)), {}).setdefault(
                item["index"], {}).update(item["fields"])
        total = 0
        for (module, month), patches in sorted(grouped.items()):
            total += patch_one(module, month, patches, args.apply, args.show)
        print(f"total changes: {total}")
        return 0

    if not args.module or args.month is None:
        raise SystemExit("give a module and month, or use --json")
    patches = {}
    for spec in args.set:
        index, field, value = spec.split("=", 2)
        if field not in FIELDS:
            raise SystemExit(f"unknown field {field!r}")
        patches.setdefault(int(index), {})[field] = value
    patch_one(args.module, args.month, patches, args.apply, args.show)
    return 0



if __name__ == "__main__":
    sys.exit(main(sys.argv))
