# -*- coding: utf-8 -*-
"""Cross-entry audit: terminology consistency and bilingual pairing."""
from __future__ import annotations

import re
from collections import defaultdict

from audit_lib import (
    RE_CJK, Entry, Finding, cmu_lookup, cjk_count, normalise,
)


RE_LATIN_SANDWICH = re.compile(r"[\u4e00-\u9fff][A-Za-z][A-Za-z ]{2,}[\u4e00-\u9fff]")


def _spelling_variant(a: str, b: str) -> bool:
    """True when two headwords are only British/American spellings of one word."""
    from audit_lib import BRITISH_WHOLES
    x, y = a.strip().lower(), b.strip().lower()
    if x == y:
        return True
    if BRITISH_WHOLES.get(x) == y or BRITISH_WHOLES.get(y) == x:
        return True
    for suf, rep in (("isation", "ization"), ("ised", "ized"),
                     ("ising", "izing"), ("ise", "ize"), ("our", "or"),
                     ("ogue", "og"), ("yse", "yze")):
        if x.endswith(suf) and x[:-len(suf)] + rep == y:
            return True
        if y.endswith(suf) and y[:-len(suf)] + rep == x:
            return True
    return False


def run(entries):
    out = []

    def add(e, code, sev, detail):
        out.append(Finding(e.module, e.month, e.index, code, sev, e.word, detail))

    # --- same headword -> one gloss ---------------------------------------
    by_word = defaultdict(list)
    for e in entries:
        by_word[e.word.strip().lower()].append(e)
    for w, group in by_word.items():
        if len(group) < 2:
            continue
        glosses = {g.meaning.strip() for g in group}
        if len(glosses) <= 1:
            continue
        # Same senses, different order -> a hard inconsistency.
        seg_sets = [frozenset(re.split(r"[；;、]", x)) for x in glosses]
        seg_sets = [s for s in seg_sets if s]
        if seg_sets and all(s == seg_sets[0] for s in seg_sets):
            where = " vs ".join(f"{g.where}={g.meaning!r}" for g in group)
            for g in group:
                add(g, "TERM_GLOSS_ORDER", "P2",
                    f"{w!r} gloss segments are the same but ordered "
                    f"differently -> {where}")
            continue
        where = ", ".join(f"{g.where}={g.meaning!r}" for g in group)
        for g in group:
            add(g, "TERM_GLOSS_CONFLICT", "P3",
                f"{w!r} has {len(glosses)} different glosses -> {where}")


    # --- same gloss -> one headword ---------------------------------------
    by_gloss = defaultdict(list)
    for e in entries:
        g = e.meaning.strip()
        if cjk_count(g) >= 2:
            by_gloss[g].append(e)
    for g, group in by_gloss.items():
        heads = {x.word.strip().lower() for x in group}
        if len(heads) > 1:
            where = ", ".join(sorted(f"{x.word!r}@{x.where}" for x in group))
            for x in group:
                add(x, "GLOSS_HEADWORD_CONFLICT", "P3",
                    f"gloss {g!r} is shared by {len(heads)} headwords -> {where}")

    # --- transliteration / untranslated gloss -----------------------------
    for e in entries:
        g = e.meaning.strip()
        if not g:
            continue
        if re.fullmatch(r"[A-Za-z0-9 .\-&/]+", g):
            add(e, "GLOSS_NOT_TRANSLATED", "P1",
                f"gloss is Latin script, not Chinese: {g!r}")
        elif re.search(r"[A-Za-z]{4,}", g):
            add(e, "GLOSS_MIXED_SCRIPT", "P3",
                f"long Latin run inside gloss: {g!r}")

    # --- a Latin run wedged between Chinese is always a broken gloss ------
    for e in entries:
        for field, label in ((e.meaning, "MEAN"), (e.translation, "TRANS")):
            m = RE_LATIN_SANDWICH.search(field)
            if m:
                code = "CN_MEAN" if label == "MEAN" else "CN_TRANS"
                add(e, code + "_LATIN_SANDWICH", "P2",
                    f"Latin run wedged between Chinese in {label}: "
                    f"...{field[max(0, m.start() - 4):m.end() + 4]}...")

    # --- translation must not be a verbatim copy of the English example --

    for e in entries:
        ex = re.sub(r"[^a-z ]", " ", e.example.lower())
        tr = e.translation.strip()
        if len(tr) > 6 and tr.lower() in ex:
            add(e, "TRANS_COPIES_EXAMPLE", "P2",
                "translation appears inside the English example")

    # --- IPA identical for different words is almost always a copy-paste --
    by_ipa = defaultdict(list)
    for e in entries:
        if e.ipa.strip():
            by_ipa[e.ipa.strip()].append(e)
    for ipa, group in by_ipa.items():
        if len(group) < 2:
            continue
        if len({normalise(g.word) for g in group}) == len(group):
            heads = [g.word for g in group]
            if all(_spelling_variant(heads[0], h) for h in heads[1:]):
                continue          # same word, British vs American spelling
            detail = ", ".join(f"{g.word!r}@{g.where}" for g in group[:6])
            for g in group:
                add(g, "IPA_SHARED_BY_MANY", "P3",
                    f"{len(group)} different words share {ipa}: {detail}")


    # --- headword attested by a pronunciation dictionary ------------------
    for e in entries:
        heads = [h for h in re.split(r"[-\s]+", e.word.lower()) if h]
        unknown = [h for h in heads if not cmu_lookup(h)]
        if unknown and len(heads) > 1:
            if all(not cmu_lookup(u) for u in unknown) and len(unknown) == len(heads):
                add(e, "HEADWORD_UNATTESTED", "P1",
                    f"not in CMU dict: {', '.join(unknown)}")

    # --- every field present ---------------------------------------------
    for e in entries:
        if not all([e.word.strip(), e.ipa.strip(), e.meaning.strip(),
                    e.example.strip(), e.translation.strip()]):
            add(e, "FIELD_EMPTY", "P0", "one or more fields are empty")

    # --- ordering inside a day: alphabetical-ish sanity -------------------
    for e in entries:
        if e.ipa.count("/") != 2:
            add(e, "IPA_SLASH_COUNT", "P1",
                f"{e.ipa.count('/')} slash characters in IPA: {e.ipa!r}")

    return out


def phrase_audit(entries):
    """Report headwords that are really sentences, not vocabulary items."""
    out = []
    for e in entries:
        w = e.word
        if len(w.split()) >= 4:
            out.append(Finding(e.module, e.month, e.index, "PHRASE_TOO_LONG",
                               "P3", e.word,
                               f"{len(w.split())} words in headword"))
        if re.match(r"^(and|or|but|the|a|an|of|to|for|if|when|that|which)\b",
                    w.strip().lower()) and not re.match(r"^[A-Za-z]/", w.strip()):
            out.append(Finding(e.module, e.month, e.index, "PHRASE_FUNCTION_LEAD",
                               "P2", e.word,
                               "headword begins with a function word"))

    return out
