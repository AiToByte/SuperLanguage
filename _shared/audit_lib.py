# -*- coding: utf-8 -*-
"""Shared primitives for the strict SuperLanguage content audit.

Severity ladder
---------------
P0  corrupt / unusable / wrong data            -> must fix
P1  contradicts an authoritative reference      -> must fix
P2  grammar, orthography, consistency defect    -> should fix
P3  style, polish, learnability nit              -> optional

Every finding carries a stable ``code`` so that fixes can be verified by
re-running the audit and diffing code counts.
"""
from __future__ import annotations

import re
import sys
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from toolkit import ROOT, MODULES, _load, normalise  # noqa: E402

# --------------------------------------------------------------------------- #
# findings
# --------------------------------------------------------------------------- #
SEV_ORDER = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
SEV_LABEL = {
    "P0": "P0 corrupt/unusable",
    "P1": "P1 contradicts reference",
    "P2": "P2 grammar/orthography/consistency",
    "P3": "P3 style/polish",
}


@dataclass(frozen=True)
class Finding:
    module: str
    month: int
    index: int
    code: str
    sev: str
    headword: str
    detail: str

    @property
    def where(self) -> str:
        return f"{self.module}/M{self.month:02d}#{self.index}"

    def __str__(self) -> str:
        return f"[{self.sev}] {self.code:<26} {self.where:<18} {self.headword}"


@dataclass
class Entry:
    module: str
    month: int
    index: int
    word: str
    ipa_brit: str
    ipa_ame: str
    meaning: str
    example: str
    translation: str

    @property
    def where(self) -> str:
        return f"{self.module}/M{self.month:02d}#{self.index}"

    @property
    def ipa(self) -> str:
        """Backwards-compatible alias for the British transcription."""
        return self.ipa_brit


# --------------------------------------------------------------------------- #
# character classes
# --------------------------------------------------------------------------- #
RE_CJK = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")
RE_CJK_PUNCT = re.compile(r"[\u3000-\u303f\uff00-\uffef]")
RE_LATIN_LETTER = re.compile(r"[A-Za-z]")
RE_DIGIT = re.compile(r"[0-9]")
RE_MOJIBAKE = re.compile(r"[\ufffd\u001a]")
RE_IPA_SLASH = re.compile(r"/[^/]*/")

REPLACEMENT = "\ufffd"

# --- accent label carried inside the phonetic field -------------------------
# The label lives in the data so that every consumer - Markdown, Excel, HTML,
# PDF, JSON - shows it, and so the audit can check the label is truthful.
RE_ACCENT_LABEL = re.compile(r"^\s*(BrE|AmE)\s+(?=\S)")
ACCENT_TAGS = ("BrE", "AmE")


def split_label(value: str):
    """Return ``(tag_or_None, core)`` for a phonetic field."""
    m = RE_ACCENT_LABEL.match(value or "")
    if m:
        return m.group(1), value[m.end():].strip()
    return None, (value or "").strip()


def with_label(tag: str, core: str) -> str:
    """Attach an accent tag, refusing to double-tag."""
    _, bare = split_label(core)
    return f"{tag} {bare}"

# British English IPA inventory accepted in this corpus.
# Longest-first so that greedy syllabification is correct.
IPA_VOWELS = [
    # two-syllable diphthongs first (the corpus writes these as base letter + ɪ/ʊ)
    "\u0061\u026a", "\u0061\u028a", "\u0065\u026a", "\u0254\u026a",
    # stressed long vowels and rhotic vowels
    "\u0254\u02d0", "\u0251\u02d0", "\u028a\u02d0", "\u028c\u02d0", "\u026a\u02d0",
    "\u0259\u02d0", "\u026a\u0259", "\u0259\u028a", "\u0259\u028c", "\u0254\u026a",
    "\u0251\u026a", "\u00e0\u028a", "\u00e9\u026a", "\u0259\u028a", "\u025b\u0259",
    "\u0259\u0259", "\u0065\u0259", "\u0061\u02d0", "\u028a\u0259",
    # plain vowels
    "\u025b", "\u0254", "\u026a", "\u0252", "\u0259",
    "\u028a", "\u028c", "\u0250", "\u0251", "\u00e6", "\u0065", "\u0069",
    "\u0075", "\u0061", "\u025c", "\u025a", "\u025d",
]

IPA_CONSONANTS = {
    "p", "b", "t", "d", "k", "\u0261", "g", "t\u0283", "d\u0292", "f", "v",
    "\u03b8", "\u00f0", "s", "z", "\u0283", "\u0292", "h", "m", "n", "\u014b",
    "l", "r", "\u027e", "j", "w",
}
IPA_DIACRITICS = {
    "\u02c8",  # primary stress
    "\u02cc",  # secondary stress
    "\u02d0",  # length
    "\u02d1",  # half length
    "\u0303",  # tilde
    "\u0329",  # syllabic
    "\u02b0", "\u02b1",  # aspirated / palatalised modifiers
    "(", ")",  # optional linking r, e.g. /'stei kh -əu ld -ə(r)/ -> /...ə(r)/
}
IPA_MODIFIER_LETTERS = {"\u02b0", "\u02b1"}

IPA_ALLOWED = IPA_CONSONANTS | set("".join(IPA_VOWELS)) | IPA_DIACRITICS
IPA_VOWEL_SET = set("".join(IPA_VOWELS))

# Symbols that must never appear in a British-English transcription.
FORBIDDEN_IPA = {
    "\u025a": "American rhotic schwa /\u025a/ - not used in British IPA",
    "o\u028a": "American /o\u028a/ - British writes this as /\u0259\u028a/",
    "\u027e": "American /r/ glyph - this corpus uses plain r",
    "\u0243": "invalid symbol (b with stroke)",
    "\u0152": "invalid symbol (OE ligature)",
    "\u03b1": "invalid symbol (Greek alpha) - use U+0251",
    "\u0250\u02d0": "invalid long turned-a - use \u0251\u02d0 (U+0251 U+02D0)",
}


# --------------------------------------------------------------------------- #
# CMU pronouncing dictionary
# --------------------------------------------------------------------------- #
ARPABET_TO_IPA = {
    "AA": "\u0251\u02d0", "AE": "\u00e6", "AO": "\u0254\u02d0", "AW": "\u00e0\u028a",
    "AY": "\u0251\u026a", "B": "b", "CH": "t\u0283", "D": "d", "DH": "\u00f0",
    "EH": "\u025b", "ER": "\u025c\u02d0", "EY": "\u00e9\u026a", "F": "f",
    "G": "\u0261", "HH": "h", "IH": "\u026a", "IY": "\u028c\u02d0", "JH": "d\u0292",
    "K": "k", "L": "l", "M": "m", "N": "n", "NG": "\u014b", "OW": "o\u028a",
    "OY": "\u0254\u026a", "P": "p", "R": "\u027e", "S": "s", "SH": "\u0283",
    "T": "t", "TH": "\u03b8", "UH": "\u028a", "UW": "u\u02d0", "V": "v",
    "W": "w", "Y": "j", "Z": "z", "ZH": "\u0292",
}

_CMU: dict = {}
_CMU_INDEX: dict = {}


def cmu_lookup(word: str, strip_suffix: bool = True):
    """Return the CMU pronunciation(s) for ``word`` or None.

    Handles case, possessives and the British/American spelling gap.  With
    ``strip_suffix=False`` only the literal spelling and its British/American
    equivalents are tried, which is what the American-IPA route needs: a
    morphological guess would silently truncate the transcription
    ("chunking" must not become "chunk").
    """
    if not _CMU:
        _load_cmu()
    w = word.lower().strip()
    for cand in _cmu_candidates(w, strip_suffix=strip_suffix):
        if cand in _CMU:
            return _CMU[cand]
    return None


def cmu_index(word: str):
    """Return the CMU pronunciations keyed by word, with base-form fallback."""
    if not _CMU:
        _load_cmu()
    return _cmu_candidates(word.lower().strip())


BRITISH_SUFFIX = [
    ("isation", "ization"), ("isations", "izations"), ("ised", "ized"),
    ("ising", "izing"), ("ise", "ize"), ("ises", "izes"), ("ising", "izing"),
    ("yse", "yze"), ("ysed", "yzed"), ("ysing", "yzing"),
    ("ogue", "og"), ("our", "or"), ("ours", "ors"), ("oured", "ored"),
    ("ll", "l"), ("mme", "me"), ("cce", "ce"),
    ("tised", "tized"), ("tising", "tizing"), ("tise", "tize"),
    ("use", "use"), ("tt", "t"), ("ll", "l"),
]

BRITISH_WHOLES = {
    "programme": "program", "programmes": "programs", "favour": "favor",
    "favours": "favors", "favoured": "favored", "flavour": "flavor",
    "honour": "honor", "honours": "honors", "labour": "labor",
    "neighbour": "neighbor", "neighbours": "neighbors", "rumour": "rumor",
    "behaviour": "behavior", "colour": "color", "colours": "colors",
    "favourite": "favorite", "favourites": "favorites", "harbour": "harbor",
    "armour": "armor", "savour": "savor", "vapour": "vapor", "vigour": "vigor",
    "endeavour": "endeavor", "defence": "defense", "offence": "offense",
    "licence": "license", "practise": "practice", "catalogue": "catalog",
    "dialogue": "dialog", "analogue": "analog", "aluminium": "aluminum",
    "grey": "gray", "greyed": "grayed", "greyish": "grayish",
    "plough": "plow", "draught": "draft", "cheque": "check", "storey": "story",
    "storeys": "stories", "tyre": "tire", "kerb": "curb", "pyjamas": "pajamas",
    "mould": "mold", "moulding": "molding", "smoulder": "smolder",
    "judgement": "judgment", "acknowledgement": "acknowledgment",
    "enrolment": "enrollment", "fulfil": "fulfill", "fulfilment": "fulfillment",
    "traveler": "traveler", "traveller": "traveler", "travellers": "travelers",
    "travelled": "traveled", "modelling": "modeling", "modelled": "modeled",
    "cancelled": "canceled", "cancelling": "canceling", "counsellor": "counselor",
    "labelled": "labeled", "fuelled": "fueled", "signalling": "signaling",
    "jewellery": "jewelry", "woollen": "woolen", "greyish": "grayish",
    "speciality": "specialty", "practise": "practice", "sulphate": "sulfate",
    "sulphur": "sulfur", "metre": "meter", "litre": "liter", "tonne": "ton",
    "aeroplane": "airplane", "tyre": "tire", "kerb": "curb", "plait": "braid",
    "gaol": "jail", "gaol": "jail", "instalment": "installment",
    "skilful": "skillful", "wilful": "willful", "enrol": "enroll",
    "counsellor": "counselor", "marvellous": "marvelous", "appalling": "appalling",
    "cancelled": "canceled", "totally": "totally", "levy": "levy",
}

MORPH_SUFFIX = ["s", "es", "ed", "d", "ing", "er", "est", "ly", "ers", "ies",
                "ied", "ier", "iest", "'s", "'", "ness", "ment", "ments"]


def _cmu_candidates(w: str, strip_suffix: bool = True):
    """Ordered candidate spellings for dictionary lookup."""
    out = [w]
    if w in BRITISH_WHOLES:
        out.append(BRITISH_WHOLES[w])
    for suf, rep in BRITISH_SUFFIX:
        if w.endswith(suf) and len(w) > len(suf) + 1:
            out.append(w[: -len(suf)] + rep)
    if "-" in w:
        out.append(w.replace("-", ""))
    if not strip_suffix:
        return list(dict.fromkeys(c for c in out if c))
    if w.endswith("ies") and len(w) > 4:
        out.append(w[:-3] + "y")
    if w.endswith("ied") and len(w) > 4:
        out.append(w[:-3] + "y")
    if w.endswith("ises") and len(w) > 5:
        out.append(w[:-4] + "y")
    if w.endswith("ising") and len(w) > 6:
        out.append(w[:-5] + "y")
    if w.endswith("yse") and len(w) > 4:
        out.append(w[:-3] + "ize")
    if w.endswith("ll") and len(w) > 2:
        out.append(w[:-1])
    for suf in MORPH_SUFFIX:
        if w.endswith(suf) and len(w) - len(suf) >= 3:
            base = w[: -len(suf)]
            out.append(base)
            if suf == "ies":
                out.append(base + "y")
            if suf in ("es", "ied"):
                out.append(w[:-2])
            if suf in ("s", "'s", "'"):
                out.append(w.rstrip("s'"))
    if w.endswith("e"):
        out.append(w[:-1])
    if w.endswith("ing") and len(w) > 5:
        out.append(w[:-3])
        out.append(w[:-3] + "e")
    if w.endswith("ed") and len(w) > 4:
        out.append(w[:-2])
        out.append(w[:-1])
    return list(dict.fromkeys(c for c in out if c))


def _load_cmu():
    global _CMU, _CMU_INDEX
    import cmudict
    _CMU = {}
    for key, prons in cmudict.dict().items():
        base = key.split(" ")[0].lower()
        _CMU.setdefault(base, []).extend(
            list(p) for p in prons if isinstance(p, (list, tuple)))
    _CMU_INDEX = _CMU


# --------------------------------------------------------------------------- #
# corpus loading
# --------------------------------------------------------------------------- #
def load_corpus(modules=None):
    """Flatten every month file into Entry objects."""
    entries = []
    for module in (modules or MODULES):
        data_dir = ROOT / module / "_build" / "data"
        for i in range(1, 13):
            path = data_dir / f"m{i:02d}.py"
            if not path.exists():
                continue
            mod = _load(module, f"data/m{i:02d}.py")
            for j, e in enumerate(mod.WORDS):
                    if len(e) != 6:
                        entries.append(Entry(module, mod.MONTH, j,
                                            *map(str, e), "", "", ""))
                        continue
                    entries.append(Entry(module, mod.MONTH, j,
                                         *(str(v) for v in e[:3]),
                                         str(e[3]), str(e[4]), str(e[5])))
    return entries


# --------------------------------------------------------------------------- #
# small text helpers
# --------------------------------------------------------------------------- #
def cjk_count(s: str) -> int:
    return len(RE_CJK.findall(s))


def has_mojibake(s: str) -> bool:
    return bool(RE_MOJIBAKE.search(s))


def nfkc(s: str) -> str:
    return unicodedata.normalize("NFKC", s)


def strip_accents(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", s)
                   if unicodedata.category(c) != "Mn")


def syllable_split(ipa_inner: str):
    """Split an IPA string into syllables.

    Returns (list_of_syllables, [unparsed_tokens]).
    """
    text = ipa_inner.strip()
    syllables, cur = [], ""
    i = 0
    while i < len(text):
        ch = text[i]
        if ch.isspace():
            if cur:
                syllables.append(cur)
                cur = ""
            i += 1
            continue
        matched = None
        for v in IPA_VOWELS:
            if text.startswith(v, i):
                matched = v
                break
        if matched:
            if cur:
                syllables.append(cur)
                cur = ""
            cur = matched
            i += len(matched)
            continue
        cur += ch
        i += 1
    if cur:
        syllables.append(cur)
    return syllables, []
