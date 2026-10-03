# -*- coding: utf-8 -*-
"""Text audit: headword orthography, English example grammar, Chinese fields."""
from __future__ import annotations

import re

from audit_lib import (
    RE_CJK, RE_CJK_PUNCT, RE_DIGIT, RE_LATIN_LETTER, Entry, Finding,
    cmu_lookup, cjk_count, has_mojibake,
)

EN_ALLOWED_PUNCT = set(".,;:!?'\"()-\u2019\u201c\u201d\u2014\u2013/&%")
# Full-width curly quotes and dashes are correct Chinese typography; only true
# ASCII marks are defects here.
ASCII_PUNCT_IN_CN = set(",.!?;:'\"()<>*%$")


FUNCTION_WORDS = {
    "the", "a", "an", "and", "or", "but", "of", "to", "in", "on", "for",
    "with", "at", "by", "from", "as", "is", "are", "be", "that", "this",
}

# A word beginning with a capital in mid-sentence is suspicious.  These are the
# only words allowed to stay capitalised inside our templates.
ALLOWED_MIDCAP = {
    "english", "british", "american", "chinese", "european", "asia",
    "q1", "q2", "q3", "q4", "ceo", "cfo", "coo", "cio", "crm", "erp",
    "hr", "it", "uk", "us", "eu", "api", "sla", "kpi", "roi", "saas",
}

PROPER_NOUNS = {
    "january", "february", "march", "april", "may", "june", "july", "august",
    "september", "october", "november", "december",
    "monday", "tuesday", "wednesday", "thursday", "friday", "saturday",
    "sunday", "britain", "british", "america", "american", "europe", "european",
    "china", "chinese", "japan", "japanese", "india", "asia", "asian",
    "london", "new", "york", "shanghai", "beijing", "hong", "kong", "singapore",
    "germany", "france", "spain", "italy", "canada", "australia",
    "jan", "feb", "mar", "apr", "jun", "jul", "aug", "sep", "sept", "oct",
    "nov", "dec",
    # named legal / parliamentary bodies and eponyms used in this corpus
    "parliament", "tomlin", "nice", "european", "eurozone",
}

RE_ABBREV = re.compile(
    r"\b(?:[A-Za-z]\.){2,}$|"
    r"\b(?:mr|mrs|ms|dr|prof|st|jr|sr|vs|etc|e\.g|i\.e|no|fig|approx|"
    r"inc|ltd|co|dept|est|vol|pp|ed|cf|al)\.$", re.I)

RE_BAD_APOSTROPHE = re.compile(
    r"\b(dont|doesnt|didnt|wont|cant|isnt|arent|wasnt|werent|hasnt|havent|"
    r"hadnt|shouldnt|wouldnt|couldnt|youd|youll|youre|"
    r"theyre|theyve|theyll|wed|weve|hell|shes|hes)\b",
    re.I)

RE_DOUBLE_WORD = re.compile(r"\b(\w+)\s+\1\b", re.I)
RE_SPACE_BEFORE_PUNCT = re.compile(r"\s+[.,;:!?]")
RE_MISSING_SPACE_AFTER = re.compile(r"[.,;:!?][A-Za-z]")
RE_TOKEN = r"[A-Za-z0-9]+(?:[./'\u2019-][A-Za-z0-9]+)*"
RE_MID_CAP = re.compile(r"(?<!^)(?<![.\"'])\b([A-Z][a-z]{2,})\b")
RE_SENTENCE_END = re.compile(r"[.!?][\"'\u2019\u201d)]*$")


def _is_acronym_head(word: str) -> bool:
    """True when a capitalised leading token is an acronym or a letter form."""
    first = word.split()[0] if word.split() else word
    if "/" in first or first.isupper():
        return True
    if len(first) <= 2 and first.isalpha():
        return True
    if first[0].isupper() and first[1:].islower() and first.lower() in {
            "boolean", "nice", "tomlin"}:
        return True
    return False


def _tokens(s: str):
    """Words, keeping digits and internal '/' or '-' compounds intact."""
    return re.findall(RE_TOKEN, s)



LATIN_PLURAL = {
    "hypotheses": "hypothesis", "hypothesis": "hypotheses",
    "addenda": "addendum", "consortia": "consortium",
    "synopses": "synopsis", "appendices": "appendix",
    "memoranda": "memorandum", "criteria": "criterion",
    "phenomena": "phenomenon", "data": "datum", "media": "medium",
    "indices": "index", "matrices": "matrix", "vertices": "vertex",
    "analyses": "analysis", "diagnoses": "diagnosis", "theses": "thesis",
    "crises": "crisis", "axes": "axis", "bases": "basis",
}

IRREGULAR_FORMS = {
    "children": "child", "people": "person", "men": "man", "women": "woman",
    "feet": "foot", "teeth": "tooth", "mice": "mouse", "geese": "goose",
    "liable": "liability", "insurance": "insurer",
    "insurers": "insurance", "insurer": "insurance",
}


def _is_inflection(word: str, head: str) -> bool:
    w, h = word.lower(), head.lower()
    if w == h:
        return True
    if LATIN_PLURAL.get(w) == h or LATIN_PLURAL.get(h) == w:
        return True
    if IRREGULAR_FORMS.get(w) == h or IRREGULAR_FORMS.get(h) == w:
        return True
    # anonymisation -> anonymised / anonymising / anonymise
    for suf in ("isation", "ization"):
        if h.endswith(suf):
            stem = h[: -len(suf)]
            if w in (stem + "ise", stem + "ised", stem + "ises",
                     stem + "ising", stem + "ize", stem + "ized",
                     stem + "izes", stem + "izing", stem + "e",
                     stem + "ations", h, h + "s"):
                return True
    # gerund as headword:  backloading -> backloaded / backloader
    if h.endswith("ing") and len(h) > 5:
        stem = h[:-3]
        if w in (stem + "ed", stem + "er", stem + "ers", stem + "es"):
            return True
    # -ise/-ised/-ising (British) <-> -ize/-ized/-izing
    for suf, rep in (("ise", "ize"), ("ised", "ized"), ("ises", "izes"),
                     ("ising", "izing"), ("isation", "ization")):

        if h.endswith(suf):
            alt = h[: -len(suf)] + rep
            for base in {h, alt}:
                for tail in ("s", "es", "ed", "ing", "d"):
                    if w == base + tail:
                        return True
    # nominalisations:  certification -> certificate/certificates
    if h.endswith("ation"):
        stem = h[:-5]
        if w in (stem + "ate", stem + "ates", stem + "ated",
                 stem + "ating", stem + "ation"):
            return True
    if h.endswith("ibility"):
        return w == h[:-7] + "able"
    if h.endswith("ible"):
        return w in (h[:-2] + "ility", h + "s", h + "d")
    if h.endswith("e"):
        return w in (h[:-1] + "ing", h[:-1] + "ed", h[:-1] + "es", h + "d",
                     h[:-1] + "er", h[:-1] + "est", h[:-1] + "ion",
                     h[:-1] + "ive", h[:-1] + "al", h[:-1] + "ation")
    if h.endswith("y"):
        return w in (h[:-1] + "ies", h[:-1] + "ied", h[:-1] + "ier",
                     h[:-1] + "iest", h[:-1] + "ily", h[:-1] + "ing")
    return w in (
        h + "s", h + "es", h + "ed", h + "ing", h + "er", h + "est", h + "ly",
        h + "'s", h + "'", h + "ment", h + "ers", h + "ion", h + "ions",
        h + "al", h + "ive", h + "ity", h + "ies", h + "ied", h + "ier",
        h + "age", h + "ance", h + "ence", h + "s",
    )




def check_headword(e: Entry, add):
    w = e.word
    if not w.strip():
        add("HW_EMPTY", "P0", "empty headword")
        return
    if has_mojibake(w):
        add("HW_MOJIBAKE", "P0", f"replacement character in headword: {w!r}")
    if w != w.strip():
        add("HW_WHITESPACE", "P2", "leading/trailing whitespace")
    if "  " in w:
        add("HW_DOUBLE_SPACE", "P2", "double space")
    if re.search(r"[\u4e00-\u9fff]", w):
        add("HW_HAS_CJK", "P1", "headword contains Chinese characters")
    if w[0].isupper() and " " in w and not _is_acronym_head(w):
        add("HW_CAPITALISED", "P3", "multi-word headword starts upper-case")

    if re.search(r"\s-\s|\s-$", w):
        add("HW_BAD_HYPHEN", "P2", "space before hyphen")
    if re.search(r"[.,;:!?]$", w):
        add("HW_TRAILING_PUNCT", "P2", "headword ends with punctuation")
    if len(w) > 34:
        add("HW_TOO_LONG", "P3", f"{len(w)} characters")
    if w.lower() in FUNCTION_WORDS:
        add("HW_FUNCTION_WORD", "P2", "headword is a function word")
    parts = [p for p in re.split(r"[-\s]", w) if p]
    if len(parts) > 4:
        add("HW_TOO_MANY_PARTS", "P3", f"{len(parts)} components")


def check_example(e: Entry, add):
    s = e.example
    if not s.strip():
        add("EX_EMPTY", "P0", "empty example")
        return
    if has_mojibake(s):
        add("EX_MOJIBAKE", "P0", "replacement character in example")
    if s != s.strip():
        add("EX_WHITESPACE", "P2", "leading/trailing whitespace")
    if "  " in s:
        add("EX_DOUBLE_SPACE", "P2", "double space")
    if RE_CJK.search(s):
        add("EX_HAS_CJK", "P1", "Chinese characters inside the English example")
    for ch in s:
        if ch in "\u2018\u201c\u201d\u2014\u2013\u2026" or ord(ch) > 0x2100:
            add("EX_EXOTIC_PUNCT", "P2", f"non-ASCII punctuation {ch!r}")
        elif ch.isalpha() and not ("a" <= ch <= "z" or "A" <= ch <= "Z"):
            add("EX_NON_LATIN", "P2", f"non-Latin letter {ch!r}")
    if not RE_SENTENCE_END.search(s):
        add("EX_NO_TERMINAL", "P2", "example does not end with . ! or ?")
    if not s[:1].isalpha() and not s[:1].isdigit():
        add("EX_NO_CAPITAL", "P2", "example does not start with a capital")
    elif s[:1].isalpha() and not s[:1].isupper():
        add("EX_NO_CAPITAL", "P2", "example does not start with a capital")

    if RE_SPACE_BEFORE_PUNCT.search(s):
        add("EX_SPACE_BEFORE_PUNCT", "P2", "space before punctuation")
    for m in RE_MISSING_SPACE_AFTER.finditer(s):
        left = s.rfind(" ", 0, m.start()) + 1
        token = s[left:m.end() + 1]
        if RE_ABBREV.match(token):
            continue          # p.m. / a.m. / e.g. / i.e.
        add("EX_MISSING_SPACE_AFTER", "P2",
            f"missing space after {s[m.start():m.end() + 4]!r}")


    if re.search(r"\.{2,}", s):
        add("EX_MULTI_STOP", "P2", "repeated full stops")
    m = RE_DOUBLE_WORD.search(s)
    if m and m.group(1).lower() not in {"that", "had", "in"}:
        add("EX_REPEATED_WORD", "P2", f"repeated word {m.group(1)!r}")
    if RE_BAD_APOSTROPHE.search(s):
        add("EX_MISSING_APOSTROPHE", "P2",
            "missing apostrophe in contraction: "
            + RE_BAD_APOSTROPHE.search(s).group(0))
    if s.count("'") and s.count("\u2019"):
        add("EX_APOSTROPHE_STYLE", "P3", "mixed straight and curly apostrophes")

    toks = _tokens(s)
    if len(toks) < 4:
        add("EX_TOO_SHORT", "P3", f"{len(toks)} word(s)")
    if len(toks) > 24:
        add("EX_TOO_LONG", "P3", f"{len(toks)} words")
    for mm in RE_MID_CAP.finditer(s[1:]):
        tok = mm.group(1)
        low = tok.lower()
        if low in ALLOWED_MIDCAP or low in PROPER_NOUNS:
            continue
        if cmu_lookup(tok) and not cmu_lookup(tok.lower()):
            continue
        add("EX_MID_SENTENCE_CAP", "P2", f"mid-sentence capital: {tok!r}")

    # --- must open with the target word ----------------------------------
    head = e.word.split()[0].strip(",.:;")
    first = toks[0] if toks else ""
    if not _is_inflection(first, head):
        stem = re.sub(r"[^a-z]", "", first.lower())
        base = re.sub(r"[^a-z]", "", head.lower())
        if not (stem.startswith(base) or base.startswith(stem)) or len(base) < 4:
            add("EX_NOT_OPENING", "P1",
                f"example starts with {first!r}, not a form of {head!r}")


def check_chinese(field: str, label: str, e: Entry, add, maxlen: int):
    v = e.meaning if label == "MEAN" else e.translation
    code = "CN_MEAN" if label == "MEAN" else "CN_TRANS"
    if not v.strip():
        add(f"{code}_EMPTY", "P0", f"empty {label} field")
        return
    if has_mojibake(v):
        add(f"{code}_MOJIBAKE", "P0", f"replacement character in {label}")
    if v != v.strip():
        add(f"{code}_WHITESPACE", "P2", "leading/trailing whitespace")
    if RE_LATIN_LETTER.search(v):
        bad = RE_LATIN_LETTER.findall(v)
        add(f"{code}_LATIN", "P3",
            f"Latin letters {''.join(sorted(set(bad)))} in {label}: {v!r}")

    for i, ch in enumerate(v):
        if ch not in ASCII_PUNCT_IN_CN:
            continue
        near_digit = (RE_DIGIT.search(v[max(0, i - 1):i])
                      or RE_DIGIT.search(v[i + 1:i + 2]))
        near_latin = (RE_LATIN_LETTER.search(v[max(0, i - 1):i])
                      or RE_LATIN_LETTER.search(v[i + 1:i + 2]))
        if near_digit:
            continue              # ratios like 4.5:1, percentages like 200%
        if near_latin and ch in ".-/":
            continue              # technical names like robots.txt or A/B
        add(f"{code}_ASCII_PUNCT", "P2",
            f"ASCII {ch!r} in {label} (use full-width): {v!r}")


    if "  " in v:
        add(f"{code}_DOUBLE_SPACE", "P2", "double space")
    if not RE_CJK.search(v):
        add(f"{code}_NO_CJK", "P1", f"no Chinese characters in {label}")
    n = cjk_count(v)
    if label == "MEAN":
        if n > 16:
            add(f"{code}_TOO_LONG", "P3", f"{n} characters in gloss: {v!r}")
        if n == 0 and RE_DIGIT.search(v):
            add(f"{code}_NUMERIC", "P3", f"gloss is only digits: {v!r}")
    else:
        if n > 46:
            add(f"{code}_TOO_LONG", "P3", f"{n} characters in translation")
    if RE_CJK_PUNCT.search(v):
        for mm in RE_CJK_PUNCT.finditer(v):
            if mm.group(0) in "\uff0c\u3002\u3001\uff1b\uff1a\uff01\uff1f\uff08\uff09":
                continue
            add(f"{code}_CJK_PUNCT", "P2",
                f"punctuation {mm.group(0)!r} in {label}: {v!r}")
    if re.search(r"([\uff0c\u3002\uff1b\uff01\uff1f])\1", v):
        add(f"{code}_DOUBLE_PUNCT", "P2", f"repeated Chinese punctuation: {v!r}")



def run(entries):
    out = []
    for e in entries:
        local = []

        def add(code, sev, detail, _l=local):
            _l.append(Finding(e.module, e.month, e.index, code, sev, e.word, detail))

        check_headword(e, add)
        check_example(e, add)
        check_chinese(e.meaning, "MEAN", e, add, 16)
        check_chinese(e.translation, "TRANS", e, add, 46)
        if e.meaning.strip() and e.meaning.strip() == e.translation.strip():
            add("CN_TRANS_EQ_MEAN", "P2",
                "translation is identical to the gloss")
        out += local
    return out
