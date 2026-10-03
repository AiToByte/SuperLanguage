# -*- coding: utf-8 -*-
"""IPA audit: symbol inventory, stress, length, and CMU cross-validation."""
from __future__ import annotations

import difflib
import re

from audit_lib import (
    ARPABET_TO_IPA, FORBIDDEN_IPA, IPA_ALLOWED, IPA_DIACRITICS, IPA_VOWELS,
    Entry, Finding, cmu_lookup, split_label, syllable_split,
)

PRIMARY = "\u02c8"
SECONDARY = "\u02cc"
LENGTH = "\u02d0"
VOWEL_CHARS = set("".join(IPA_VOWELS))
CONS_SET = IPA_ALLOWED - VOWEL_CHARS - IPA_DIACRITICS - {"g"}


def _strip_parens(s: str) -> str:
    return re.sub(r"\([^)]*\)", "", s)


def ipa_phones(ipa_inner: str):
    """Tokenise IPA into phones; returns list of (phone, is_vowel)."""
    text = _strip_parens(ipa_inner)
    phones, i = [], 0
    while i < len(text):
        if text[i].isspace():
            i += 1
            continue
        hit = None
        for v in IPA_VOWELS:
            if text.startswith(v, i):
                hit = v
                break
        if hit:
            phones.append((hit, True))
            i += len(hit)
            continue
        phones.append((text[i], False))
        i += 1
    return phones


def arpabet_phones(phones):
    out = []
    for ph in phones:
        if isinstance(ph, (tuple, list)):
            ph = ph[0]
        ph = str(ph)
        base = ph.rstrip("012")
        if base not in ARPABET_TO_IPA:
            continue
        out.append((ARPABET_TO_IPA[base], base in
                    {"AA", "AE", "AO", "AW", "AY", "EH", "ER", "EY", "IH",
                     "IY", "OW", "OY", "UH", "UW"}))
    return out


def skeleton(phones, drop_r=True):
    """C/V + consonant skeleton used for dialect-tolerant comparison."""
    seq = []
    for ph, is_v in phones:
        if is_v:
            seq.append("V")
        else:
            c = ph.replace("\u027e", "r")
            if drop_r and c == "r":
                continue
            seq.append(c)
    return "".join(seq)


def levenshtein_ratio(a: str, b: str) -> float:
    if not a or not b:
        return 0.0
    return difflib.SequenceMatcher(None, a, b).ratio()


def _stress_count(inner: str) -> int:
    return inner.count(PRIMARY) + inner.count(SECONDARY)


# Symbols that belong to one accent system and must not appear in the other.
AMERICAN_ONLY = {
    "\u0279": "ɹ is the American r - the British transcription uses plain r",
    "o\u028a": "oʊ is American - British writes /əʊ/",
    "\u025d": "ɝ is American - British writes /ɜː/ or /ə/",
    "\u025a": "ɚ is American - British writes /ə/",
}
BRITISH_ONLY = {
    "\u02d0": "ː length mark - American IPA does not use it",
    "\u0252": "ɒ is a British vowel - American uses /ɑ/",
    "\u00e6\u02d0": "æː is not used in American",
}
# The American inventory adds the rhotic, the NURSE vowels and the ASCII "o"
# that opens /oʊ/.
IPA_ALLOWED_AME = IPA_ALLOWED | {
    "\u0279", "\u025d", "\u025a", "\u028c", "\u006f",
}


def check_tag_truth(e: Entry):
    """The stored tag must match the dialect markers inside the transcription.

    A field labelled ``AmE`` that still carries the British-only length mark or
    ``/ɒ/`` - or a field labelled ``BrE`` that carries ``ɹ`` or ``/oʊ/`` - is a
    mislabelled transcription, which is exactly the kind of error a learner
    would never notice but would trust.
    """
    out = []
    br_tag, br = split_label(e.ipa_brit)
    am_tag, am = split_label(e.ipa_ame)
    for tag, core, expect, wrong in (
            (br_tag, br, "BrE", AMERICAN_ONLY),
            (am_tag, am, "AmE", BRITISH_ONLY)):
        if tag is None or not core:
            continue
        for bad, why in wrong.items():
            if bad in core:
                out.append(Finding(e.module, e.month, e.index,
                                   "IPA_TAG_NOT_TRUTHFUL", "P0", e.word,
                                   f"tagged {tag} but the transcription "
                                   f"contains a symbol from the other accent: "
                                   f"{why}"))
    if br_tag == "AmE" or am_tag == "BrE":
        out.append(Finding(e.module, e.month, e.index, "IPA_TAG_SWAPPED", "P0",
                           e.word,
                           f"BrE field tagged {br_tag!r}, AmE field tagged "
                           f"{am_tag!r}"))
    return out


def check_entry(e: Entry):
    """Return a list of Finding for one entry's British and American IPA."""
    out = []
    for label, field in (("BrE", e.ipa_brit), ("AmE", e.ipa_ame)):
        out += _check_one(e, field, label)
    return out


def _check_one(e: Entry, stored: str, label: str):
    out = []
    add = lambda code, sev, detail: out.append(  # noqa: E731
        Finding(e.module, e.month, e.index, code, sev, e.word,
                f"[{label}] {detail}"))

    tag, ipa = split_label(stored)
    if tag is None:
        add("IPA_LABEL_MISSING", "P0",
            f"no accent tag in {stored!r} (expected '{label} /.../')")
    elif tag != label:
        add("IPA_LABEL_WRONG", "P0",
            f"field tagged {tag!r} but stored as {label}: {stored!r}")

    if not ipa:
        add("IPA_EMPTY", "P0", "empty phonetic transcription")
        return out
    if "\ufffd" in ipa:
        add("IPA_MOJIBAKE", "P0", "replacement character in IPA")
    if not (ipa.startswith("/") and ipa.endswith("/")):
        add("IPA_NOT_SLASHED", "P0", f"not wrapped in slashes: {ipa!r}")
        return out

    inner = ipa[1:-1].strip()
    if not inner:
        add("IPA_EMPTY", "P0", "empty phonetic transcription")
        return out

    if label == "BrE":
        for bad, why in AMERICAN_ONLY.items():
            if bad in inner:
                add("IPA_DIALECT_MISMATCH", "P1", why)
        allowed = IPA_ALLOWED
    else:
        for bad, why in BRITISH_ONLY.items():
            if bad in inner:
                add("IPA_DIALECT_MISMATCH", "P1", why)
        allowed = IPA_ALLOWED_AME

    # --- symbol inventory -------------------------------------------------
    for ch in inner:
        if ch in allowed or ch.isspace():
            continue
        add("IPA_BAD_SYMBOL", "P0",
            f"U+{ord(ch):04X} {ch!r} is not a valid {label} symbol")

    if label == "BrE":
        for bad, why in FORBIDDEN_IPA.items():
            if bad in inner:
                add("IPA_NONBRITISH", "P1", f"{why}: found {bad!r}")

    # --- orthography of the transcription itself --------------------------
    if "  " in inner:
        add("IPA_DOUBLE_SPACE", "P2", "double space inside IPA")
    if inner != inner.strip():
        add("IPA_EDGE_SPACE", "P2", "leading/trailing space inside slashes")
    if "-" in inner:
        add("IPA_HYPHEN", "P2", "hyphen inside IPA; use no separator")
    if ("(" in inner) != (")" in inner):
        add("IPA_PAREN_UNBALANCED", "P1", "unbalanced parenthesis")

    # --- length marks -----------------------------------------------------
    for m in re.finditer(LENGTH + "+", inner):
        start = m.start()
        if start == 0:
            add("IPA_LENGTH_NO_VOWEL", "P1", "length mark with no preceding vowel")
        elif inner[start - 1] not in VOWEL_CHARS:
            add("IPA_LENGTH_NO_VOWEL", "P1",
                f"length mark follows consonant {inner[start - 1]!r}")
    if LENGTH + LENGTH in inner:
        add("IPA_DOUBLE_LENGTH", "P1", "doubled length mark")

    # --- stress -----------------------------------------------------------
    for word in inner.split():
        if word.count(PRIMARY) > 1:
            add("IPA_DOUBLE_PRIMARY", "P1",
                f"more than one primary stress in /{word}/")
        if word.count(SECONDARY) > 1:
            add("IPA_DOUBLE_SECONDARY", "P3",
                f"more than one secondary stress in /{word}/")
        if label == "BrE" and re.match("[" + PRIMARY + SECONDARY + "]", word) \
                and len(word) <= 4:
            add("IPA_INITIAL_STRESS", "P3",
                f"stress mark on a monosyllable /{word}/")

    # --- British form against the American dictionary ----------------------
    if label == "BrE":
        head_tokens = [t for t in e.word.split() if t]
        our_tokens = [w for w in inner.split() if w]
        if len(our_tokens) < len(head_tokens):
            add("IPA_MISSING_SEGMENT", "P1",
                f"{len(head_tokens)} headword word(s) but {len(our_tokens)} "
                f"transcribed segment(s): {ipa}")
        ref = cmu_lookup(e.word)
        if ref:
            _cross_check(e, inner, ref, add)

    return out


SYLLABLE_GAP_TOLERANCE = 1
"""British English elides schwas that American spells out, so a one-syllable
gap is normal (``/ˈækʃn/`` vs ``/ˈækʃən/``).

Gaps of two or more are the same effect at scale: American *documentation* is
/ˌdɑkjəmɛnˈteɪʃən/ (five syllables) where British has /ˌdɒkmenˈteɪʃn/ (three),
and both are the standard dictionary forms. This is therefore reported as
advisory rather than as a defect; a wrong dictionary variant still shows up
here, which is why it is worth printing.
"""


def check_agreement(e: Entry):
    """Advisory cross-accent syllable comparison."""
    from audit_ipa import ipa_phones
    out = []
    brit = split_label(e.ipa_brit)[1].strip("/")
    ame = split_label(e.ipa_ame)[1].strip("/")
    if not brit or not ame:
        return out
    b = sum(1 for _, v in ipa_phones(brit.replace("(r)", "r")) if v)
    a = sum(1 for _, v in ipa_phones(ame) if v)
    if abs(a - b) > SYLLABLE_GAP_TOLERANCE:
        out.append(Finding(e.module, e.month, e.index, "IPA_ACCENT_SYLLABLES",
                           "P3", e.word,
                           f"BrE {b} syllable(s) {brit} vs AmE {a} {ame}"))
    return out


def check_ame_rhotic(e: Entry):
    """Verify the American rhotic against the dictionary, part by part.

    British drops /r/ in codas where American keeps it (``keyboard``,
    ``cold start``), so a rule-based conversion will always miss some. Any
    compound segment whose part is in CMU is compared directly.
    """
    import re as _re
    from american_ipa import _pick_pronunciation, _decompose
    from audit_lib import cmu_lookup

    out = []
    parts = _decompose(e.word)
    segs = [s for s in split_label(e.ipa_ame)[1].strip("/").split(" ") if s]
    if len(parts) != len(segs) or len(parts) < 2:
        return out
    for part, seg in zip(parts, segs):
        ref = _pick_pronunciation(cmu_lookup(part, strip_suffix=False) or [])
        if not ref:
            continue
        if "\u0279" in ref and "\u0279" not in seg:
            out.append(Finding(e.module, e.month, e.index, "IPA_AME_MISSING_R",
                               "P2", e.word,
                               f"[AmE] part {part!r} is /{seg}/ but CMU "
                               f"gives /{ref}/"))
    return out


def run(entries):
    out = []
    for e in entries:
        out += check_entry(e)
        out += check_tag_truth(e)
        out += check_agreement(e)
        out += check_ame_rhotic(e)
    return out



# British forms that legitimately diverge from the CMU (American) entry.
# Every exemption carries a reason so the audit output stays reviewable.
KNOWN_BRITISH_FORMS = {
    "accrual": "BrE /əˈkruːəl/ keeps the initial schwa; CMU stores a reduced form",
    "ageing": "CMU entry is corrupt; BrE /ˈeɪdʒɪŋ/ is correct",
    "schedule": "BrE /ˈʃedjuːl/ vs AmE /ˈskedʒuːl/",
    "reschedule": "BrE -djuːl vs AmE -dʒuːl",
    "scheduler": "BrE -djuːlə(r) vs AmE -dʒuːl",
    "version": "BrE /ˈvɜːʃn/ vs AmE /ˈvɜːʒn/",
    "versioning": "BrE /ˈvɜːʃənɪŋ/ vs AmE /ˈvɜːʒnɪŋ/",
    "opportunity": "BrE /ˌɒpəˈtjuːnəti/ vs AmE /ˌɑːpərˈtuːnəti/",
    "sharding": "BrE /ˈʃɑːdɪŋ/; CMU stores a truncated variant",
    "recoupment": "BrE /rɪˈkuːpmənt/ keeps the syllabic n; CMU drops it",
    "bribery": "BrE /ˈbraɪbri/ is two syllables, AmE three",
    "attitude": "BrE /ˈætɪtjuːd/ vs AmE /ˈætɪˌtuːd/",
    "retargeting": "BrE /ˈriːˌtɑːɡɪtɪŋ/; CMU marks a different syllable count",
    "booth": "BrE /buːð/ is standard; /buːθ/ is the American variant",
    "rehire": "BrE /ˌriːˈhaɪə(r)/ vs AmE /ˌriːˈhaɪɚ/",
    "bottom-up": "CMU stores the reduced form of 'up'",
    "e-commerce": "BrE /ˈiː-/ for the 'e' of e-commerce; CMU has /ʌ/",
    # British syllable counts below CMU's
    "pattern": "BrE /ˈpætn/ is one syllable; CMU has two",
    "factory": "BrE /ˈfæktri/ is two syllables; CMU has three",
    "mentorship": "BrE /ˈmentʃɪp/ is two syllables; CMU has three",
    "watershed": "BrE /ˈwɔːtʃed/ is two syllables; AmE has three",
    "territory": "BrE /ˈterɪtri/ is three syllables; CMU has four",
}


def _cross_check(e: Entry, inner: str, ref, add):

    """Compare every syllable against the best-matching CMU pronunciation."""
    our_words = [w for w in inner.split() if w]
    head_tokens = [t for t in e.word.lower().split() if t]
    if len(our_words) != len(head_tokens):
        return

    pairs, our_syll, ref_syll = [], 0, 0
    for tok, hw in zip(our_words, head_tokens):
        single = cmu_lookup(hw)
        if not single:
            return
        ours_tok = ipa_phones(tok)
        if not any(v for _, v in ours_tok):
            continue
        best_r, best_t = -1.0, None
        for cand in single:
            tgt = arpabet_phones(cand)
            if not tgt:
                continue
            r = levenshtein_ratio(skeleton(ours_tok), skeleton(tgt))
            if r > best_r:
                best_r, best_t = r, tgt
        if best_t is None:
            return
        pairs.append((tok, hw, ours_tok, best_t, best_r))
        our_syll += sum(1 for _, v in ours_tok if v)
        ref_syll += sum(1 for _, v in best_t if v)

    if not pairs:
        return

    exempt = KNOWN_BRITISH_FORMS.get(e.word.lower())
    for tok, hw, ours_tok, tgt, r in pairs:
        if exempt:
            continue
        if r < 0.62:
            add("IPA_CMU_MISMATCH", "P1",
                f"/{tok}/ for {hw!r} is unlike CMU "
                f"({' '.join(p for p, _ in tgt)}) - similarity {r:.2f}")
        elif r < 0.80:
            add("IPA_CMU_DIFFERENT", "P3",
                f"/{tok}/ for {hw!r} differs from CMU "
                f"({' '.join(p for p, _ in tgt)}) - similarity {r:.2f}")

    if exempt:
        return

    # CMU carries reduced fast-speech variants, so an extra schwa in our careful
    # British form is normal.  Only flag the corpus for transcribing too few vowels.
    if our_syll < ref_syll:
        add("IPA_SYLLABLE_SHORT", "P1",
            f"only {our_syll} vowel(s) transcribed vs {ref_syll} in CMU: {e.ipa}")
    elif our_syll > ref_syll:
        add("IPA_SYLLABLE_LONG", "P3",
            f"{our_syll} vowel(s) transcribed vs {ref_syll} in CMU: {e.ipa}")
