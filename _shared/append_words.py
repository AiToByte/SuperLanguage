# -*- coding: utf-8 -*-
"""Append additional vocabulary entries to a month data file.

    python _shared/append_words.py <Module> mXX.py <records.txt>

``records.txt`` holds UTF-8 newline-separated records.  Six fields are the
current format and may omit the American IPA when it is filled in later by
``migrate_dual_ipa.py``::

    word|ipa_brE|ipa_AmE|meaning|example|translation

Five fields are also accepted for backwards compatibility, in which case the
American IPA is written as an empty cell::

    word|ipa_brE|meaning|example|translation
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main(argv):
    module, fname = argv[1], argv[2]
    path = ROOT / module / "_build" / "data" / fname
    lines = [l for l in Path(argv[3]).read_text(encoding="utf-8").splitlines()
             if l.strip()]
    records = []
    for raw in lines:
        parts = [x.strip() for x in raw.split("|")]
        if len(parts) == 5:
            w, i, m, e, t = parts
            records.append((w, i, "", m, e, t))
        elif len(parts) == 6:
            records.append(tuple(parts))
        else:
            print(f"SKIP (needs 5 or 6 fields): {raw[:60]}")
            continue

    text = path.read_text(encoding="utf-8").rstrip()
    block = "".join(
        '    ("%s", "%s", "%s", "%s", "%s", "%s"),\n' % r for r in records
    )
    if text.endswith("]"):
        text = text[:-1].rstrip() + "\n" + block + "]"
    else:
        raise SystemExit(f"{fname}: WORDS list not found")
    path.write_text(text + "\n", encoding="utf-8")
    print(f"appended {len(records)} entries to {module}/{fname}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))