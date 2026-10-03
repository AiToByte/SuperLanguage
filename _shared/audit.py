# -*- coding: utf-8 -*-
"""Strict content audit across every SuperLanguage module.

    python _shared/audit.py                 # all modules, report only
    python _shared/audit.py --fix           # report + exit code
    python _shared/audit.py Marketing       # one module
    python _shared/audit.py --sev P0 --sev P1
    python _shared/audit.py --code IPA_BAD_SYMBOL
    python _shared/audit.py --json out.json
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import audit_consistency  # noqa: E402
import audit_ipa  # noqa: E402
import audit_text  # noqa: E402
from audit_lib import MODULES, SEV_LABEL, SEV_ORDER, Entry, load_corpus  # noqa: E402

CHECKERS = (
    ("ipa", audit_ipa.run),
    ("text", audit_text.run),
    ("consistency", audit_consistency.run),
    ("phrases", audit_consistency.phrase_audit),
)


def audit(modules=None):
    entries = load_corpus(modules)
    findings = []
    for _, fn in CHECKERS:
        findings += fn(entries)
    findings.sort(key=lambda f: (SEV_ORDER[f.sev], f.module, f.month, f.index))
    return entries, findings


def report(entries, findings, sevs, codes, verbose_limit, stream=sys.stdout):
    entries_by_module = Counter(e.module for e in entries)
    w = stream.write
    w("=" * 74 + "\n")
    w("SuperLanguage strict content audit\n")
    w("=" * 74 + "\n")
    w("corpus: " + "  ".join(f"{m}={entries_by_module[m]}" for m in entries_by_module)
      + f"   total={len(entries)}\n\n")

    selected = [f for f in findings
                if (not sevs or f.sev in sevs) and (not codes or f.code in codes)]
    blocking = [f for f in selected if f.sev in ("P0", "P1")]

    by_code = Counter(f.code for f in selected)
    by_sev = Counter(f.sev for f in selected)
    w("severity totals\n")
    for sev in ("P0", "P1", "P2", "P3"):
        w(f"  {sev}  {by_sev.get(sev, 0):>5}   {SEV_LABEL[sev]}\n")
    w("\nfindings by code\n")
    for code, n in by_code.most_common():
        sev = next(f.sev for f in selected if f.code == code)
        w(f"  {sev}  {code:<28} {n:>5}\n")
    if not selected:
        w("  (clean)\n")
        return 0

    w("\ndetail\n" + "-" * 74 + "\n")
    grouped = defaultdict(list)
    for f in selected:
        grouped[f.code].append(f)
    shown = Counter()
    for code, group in sorted(grouped.items(),
                              key=lambda kv: (SEV_ORDER[kv[1][0].sev], -len(kv[1]))):
        sev = group[0].sev
        w(f"\n[{sev}] {code}  ({len(group)})\n")
        for f in group[:verbose_limit]:
            w(f"   {f.where:<18} {f.headword:<28} {f.detail}\n")
        if len(group) > verbose_limit:
            w(f"   ... {len(group) - verbose_limit} more "
              f"(use --limit 0 or --code {code})\n")
    if blocking:
        w(f"\nBLOCKING: {len(blocking)} P0/P1 finding(s) must be fixed.\n")
    return 1 if blocking else 0


def main(argv):
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("modules", nargs="*")
    ap.add_argument("--sev", action="append", default=[])
    ap.add_argument("--code", action="append", default=[])
    ap.add_argument("--limit", type=int, default=25)
    ap.add_argument("--json", default="")
    args = ap.parse_args(argv[1:])

    modules = args.modules or MODULES
    entries, findings = audit(modules)
    sevs = set(args.sev)
    codes = set(args.code)

    rc = report(entries, findings, sevs, codes, args.limit)

    if args.json:
        payload = [
            {"where": f.where, "module": f.module, "month": f.month,
             "index": f.index, "code": f.code, "sev": f.sev,
             "word": f.headword, "detail": f.detail}
            for f in findings
            if (not sevs or f.sev in sevs) and (not codes or f.code in codes)
        ]
        Path(args.json).write_text(
            json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"\njson -> {args.json} ({len(payload)} findings)")

    hard = any(f.sev in ("P0", "P1") for f in findings
               if (not sevs or f.sev in sevs) and (not codes or f.code in codes))
    return 1 if (hard or rc) else 0



if __name__ == "__main__":
    sys.exit(main(sys.argv))
