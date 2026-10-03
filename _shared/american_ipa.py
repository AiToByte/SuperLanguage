# -*- coding: utf-8 -*-
"""British / American IPA conversion.

Two independent routes produce the American transcription:

``from_cmu``
    The CMU Pronouncing Dictionary is an American dictionary, so its ARPABET
    transcription is converted directly.  This is the authoritative route and
    is used whenever the headword (or every part of a compound headword) is in
    the dictionary.

``derived``
    For headwords CMU does not carry - mostly domain jargon - the American form
    is derived from the curated British IPA with systematic sound
    correspondences.  Derived entries are reported separately so they can be
    reviewed.

Both routes emit General American style: no length marks, ``ɹ`` for the
rhotic, ``oʊ`` for GOAT, ``ɝ``/``ɚ`` for NURSE.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from audit_lib import cmu_lookup  # noqa: E402

# --------------------------------------------------------------------------- #
# ARPABET -> General American IPA
# --------------------------------------------------------------------------- #
ARPABET_TO_IPA = {
    "AA": "\u0251", "AE": "\u00e6", "AH": "\u028c", "AO": "\u0254",
    "AW": "\u00e0\u028a", "AY": "\u0251\u026a", "B": "b", "CH": "t\u0283",
    "D": "d", "DH": "\u00f0",
    "EH": "\u025b", "ER": "\u025d", "EY": "\u00e9\u026a", "F": "f",
    "G": "\u0261", "HH": "h", "IH": "\u026a", "IY": "i", "JH": "d\u0292",
    "K": "k", "L": "l", "M": "m", "N": "n", "NG": "\u014b", "OW": "o\u028a",
    "OY": "\u0254\u026a", "P": "p", "R": "\u0279", "S": "s", "SH": "\u0283",
    "T": "t", "TH": "\u03b8", "UH": "\u028a", "UW": "u", "V": "v",
    "W": "w", "Y": "j", "Z": "z", "ZH": "\u0292",
}
VOWEL_PHONES = {"AA", "AE", "AH", "AO", "AW", "AY", "EH", "ER", "EY", "IH",
                "IY", "OW", "OY", "UH", "UW"}
PRIMARY, SECONDARY = "\u02c8", "\u02cc"


def shift_stress(text: str) -> str:
    """Move every stress mark onto the syllable boundary.

    CMU attaches the stress digit to the vowel, which renders as ``lˈɛtɚ`` or
    ``skˈɛdʒʊl``.  Standard IPA wants the mark over the syllable onset, so the
    mark is shifted left across the consonants of its own syllable only.
    """
    from audit_ipa import ipa_phones
    toks = [list(t) for t in ipa_phones(text)]
    for i, (phone, _vowel) in enumerate(toks):
        if phone not in (PRIMARY, SECONDARY):
            continue
        j = i - 1
        while j >= 0 and not toks[j][1] and toks[j][0] not in (PRIMARY, SECONDARY):
            j -= 1
        target = j + 1
        if target < i:
            toks[i] = ["", False]
            toks.insert(target, [phone, False])
            i += 1
    return "".join(p for p, _v in toks)


def arpabet_to_ipa(phones):
    """Convert one CMU pronunciation (list of phoneme strings) to IPA."""
    out = []
    for raw in phones:
        ph = str(raw[0] if isinstance(raw, (list, tuple)) else raw)
        stress = ""
        while ph and ph[-1].isdigit():
            stress = ph[-1] + stress
            ph = ph[:-1]
        sym = ARPABET_TO_IPA.get(ph)
        if sym is None:
            return None
        if ph in VOWEL_PHONES:
            if ph == "AH" and stress in ("", "0"):
                sym = "\u0259"              # unstressed AH is schwa
            elif stress == "1":
                sym = PRIMARY + sym
            elif stress == "2":
                sym = SECONDARY + sym
            elif ph == "ER":
                sym = "\u025a"              # unstressed NURSE -> /ɚ/
        out.append(sym)
    return shift_stress("".join(out))


# --------------------------------------------------------------------------- #
# British -> American correspondences, applied phone by phone
# --------------------------------------------------------------------------- #
BRE_PHONE_TO_AME = {
    # long -> short (American does not mark length)
    "i\u02d0": "i", "u\u02d0": "u", "\u028a\u02d0": "\u028a",
    "\u026a\u02d0": "\u026a", "\u0254\u02d0": "\u0254",
    "\u0251\u02d0": "\u0251", "a\u02d0": "\u00e6",
    # monophthongs
    "i": "\u026a", "u": "\u028a", "\u0065": "\u025b", "\u0061": "\u00e6",
    "\u0250": "\u0251", "\u0252": "\u0251", "\u0259": "\u0259",
    "\u025c": "\u025d", "\u025c\u02d0": "\u025d",
    # diphthongs and rhotic vowels
    "\u0259\u028a": "o\u028a", "\u026a\u0259": "\u026a\u0279",
    "\u0259\u0259": "\u025b\u0279", "\u028a\u0259": "\u028a\u0279",
    # unchanged
    "a\u026a": "a\u026a", "a\u028a": "a\u028a", "e\u026a": "e\u026a",
    "\u0254\u026a": "\u0254\u026a",
    "\u0065\u0259": "\u025b\u0279",          # eə -> ɛɹ
    "\u00e6": "\u00e6", "\u025b": "\u025b", "\u0254": "\u0254",
    "\u0251": "\u0251", "\u026a": "\u026a", "\u028a": "\u028a",
    "\u028c": "\u028c", "\u028c\u02d0": "\u028c",
    "\u027e": "\u0279",
}

# Long British vowels map to their short American counterpart.
LONG_TO_SHORT = {
    "i": "i", "u": "u", "\u028a": "\u028a", "\u026a": "\u026a",
    "\u0254": "\u0254", "\u0251": "\u0251", "a": "\u00e6",
    "\u025c": "\u025d",
}


def bre_to_ame(inner: str) -> str:
    """Derive an American IPA string from a curated British one.

    Only systematic vowel-quality and rhotic correspondences are applied.
    American r-insertion is deliberately *not* guessed: it is lexical, not
    rule-governed, so consonant structure is carried over unchanged and the
    caller reports the entry as derived for review.
    """
    from audit_ipa import ipa_phones

    GLIDE = {"j", "w"}
    out_words = []
    # British linking-r is phonetic in American English: keep it.
    for word in inner.replace("(r)", "r").split(" "):
        phones = ipa_phones(word)
        # attach a following length mark to the vowel it belongs to
        merged = []
        for phone, is_vowel in phones:
            if phone == "\u02d0" and merged and merged[-1][1]:
                merged[-1] = (merged[-1][0] + "\u02d0", True)
                continue
            merged.append((phone, is_vowel))
        chunk, prev = [], None
        for phone, is_vowel in merged:
            if not is_vowel:
                chunk.append("\u0279" if phone == "r" else phone)
                prev = phone
                continue
            key = phone
            if key.endswith("\u02d0"):
                long = True
                base = key[:-1]
            else:
                long = False
                base = key
            if prev in GLIDE and base in ("i", "u"):
                mapped = base
            elif long:
                mapped = LONG_TO_SHORT.get(base, BRE_PHONE_TO_AME.get(base, base))
            else:
                mapped = BRE_PHONE_TO_AME.get(base, base)
            chunk.append(mapped)
            prev = base
        text = "".join(chunk)
        # word-final unstressed /ər/ is written /ɚ/ in American IPA
        text = re.sub("\u0259\u0279$", "\u025a", text)
        # a rhotic already inside the vowel must not double up
        while "\u0279\u0279" in text:
            text = text.replace("\u0279\u0279", "\u0279")
        out_words.append(shift_stress(text))
    return " ".join(out_words)


# --------------------------------------------------------------------------- #
# entry-level resolution
# --------------------------------------------------------------------------- #
def _decompose(word: str):
    parts = [p for p in re.split(r"[-\s]+", word.lower()) if p]
    return parts or [word.lower()]


def _syllable_stress(inner: str):
    """Stress mark of each syllable of a transcription: '', '1' or '2'."""
    from audit_ipa import ipa_phones
    out = []
    for word in inner.split(" "):
        mark = ""
        buf = ""
        for phone, is_vowel in ipa_phones(word):
            if phone == PRIMARY and not mark:
                mark = "1"
            elif phone == SECONDARY and not mark:
                mark = "2"
            if is_vowel:
                out.append((mark, buf))
                mark, buf = "", ""
            else:
                buf += phone
    return out


def _apply_stress(phones_str: str, pattern):
    """Rebuild ``phones_str`` with the syllable stress of ``pattern``."""
    from audit_ipa import ipa_phones
    out, pi = [], 0
    for phone, is_vowel in ipa_phones(phones_str):
        if not is_vowel:
            out.append(phone)
            continue
        mark = pattern[pi][0] if pi < len(pattern) else ""
        pi += 1
        out.append((PRIMARY if mark == "1" else SECONDARY if mark == "2" else "")
                   + phone)
    return "".join(out)


def _keep_first_primary(text: str) -> str:
    """A single headword carries one primary stress; demote any later one."""
    seen = False
    out = []
    for ch in text:
        if ch == PRIMARY:
            if seen:
                out.append(SECONDARY)
                continue
            seen = True
        out.append(ch)
    return "".join(out)


def _pick_pronunciation(candidates, target_syllables=None):
    """Choose the CMU variant for a headword.

    Preference order:
      1. the variant whose syllable count matches the curated British
         transcription - CMU often lists a slow four-syllable variant first
         (``viable`` as /ˈvɑɪəbəl/ instead of the usual /ˈvaɪəbl/);
      2. otherwise the variant with the fewest non-syllabic /r/.
    """
    from audit_ipa import ipa_phones
    best, best_score, fallback = None, None, None
    for cand in candidates:
        ipa = arpabet_to_ipa(cand)
        if not ipa:
            continue
        phones = ipa_phones(ipa)
        orphan_r = sum(1 for i, (p, _v) in enumerate(phones)
                       if p == "\u0279" and not (
                           i + 1 < len(phones) and phones[i + 1][1]))
        score = orphan_r
        if best_score is None or score < best_score:
            fallback, best_score = ipa, score
        if target_syllables:
            n = sum(1 for _, v in phones if v)
            if n == target_syllables and (best is None or orphan_r < 0):
                best = ipa
                if orphan_r == 0:
                    break
    chosen = best or fallback
    return _keep_first_primary(chosen) if chosen else None


def _segment_count(ipa: str) -> int:
    from audit_ipa import ipa_phones
    return sum(1 for _, v in ipa_phones(ipa) if v)


def _br_syllables(inner: str) -> int:
    from audit_ipa import ipa_phones
    return sum(1 for _, v in ipa_phones(inner.replace("(r)", "r")) if v)


def refine_with_cmu(word: str, ame_inner: str):
    """Replace each segment with the dictionary's American pronunciation.

    Compound and phrase headwords are aligned part by part.  Wherever CMU knows
    the part, its American transcription wins, which is what supplies the
    rhotic that British drops (``keyboard`` -> /'ki.bɔɹd/, not /'kibɔd/) and
    settles lexical pairs such as start /stɑɹt/ versus half /hæf/ that no rule
    can decide.  Parts CMU does not know keep the rule-converted form.
    """
    parts = _decompose(word)
    segs = [s for s in ame_inner.split(" ") if s]
    if len(parts) != len(segs):
        return ame_inner, 0
    out, replaced = [], 0
    for part, seg in zip(parts, segs):
        ref = _pick_pronunciation(
            cmu_lookup(part, strip_suffix=False) or [],
            target_syllables=_segment_count(seg))
        if ref:
            out.append(ref)
            replaced += 1
        else:
            out.append(seg)
    return " ".join(out), replaced


OVERRIDES_FILE = Path(__file__).with_name("ipa_overrides.json")
_OVERRIDES: dict = {}


def load_overrides() -> dict:
    """Manual American corrections that no rule can produce.

    American r-insertion after a vowel is lexical, not rule-governed:
    ``short`` becomes /ʃɔɹt/ while ``claw`` stays /klɔ/, and ``hard`` takes
    the rhotic while ``half`` loses the vowel.  Headwords that CMU does not
    carry therefore need a hand-checked value, recorded here so that
    ``migrate_dual_ipa.py --refresh`` never silently reverts them.
    """
    global _OVERRIDES
    if not _OVERRIDES:
        if OVERRIDES_FILE.exists():
            import json
            _OVERRIDES = json.loads(
                OVERRIDES_FILE.read_text(encoding="utf-8"))
        else:
            _OVERRIDES = {}
    return _OVERRIDES


def american_for(word: str, brit_ipa: str):
    """Return (american_ipa, source, note).

    ``source`` records how the transcription was built:

    ``manual``  a hand-checked entry from ``ipa_overrides.json``
    ``cmu``      the whole single-word headword is in the CMU dictionary
    ``parts``    at least one part of a compound came from the dictionary
    ``derived``  purely rule-converted from the British transcription
    """
    override = load_overrides().get(word.strip().lower())
    if override:
        return override, "manual", "hand-checked override"

    single = " " not in word and "-" not in word
    if single:
        inner_for_target = brit_ipa.strip("/")
        ipa = _pick_pronunciation(
            cmu_lookup(word, strip_suffix=False) or [],
            target_syllables=(_br_syllables(inner_for_target)
                              if inner_for_target else None))
        if ipa:
            return "/" + ipa + "/", "cmu", ""

    inner = brit_ipa.strip("/")
    if not inner:
        return "", "derived", "no British IPA available"
    converted = bre_to_ame(inner)
    refined, replaced = refine_with_cmu(word, converted)
    if replaced:
        return "/" + refined + "/", "parts", f"{replaced} part(s) from CMU"
    return "/" + converted + "/", "derived", "no CMU entry"