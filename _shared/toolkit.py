# -*- coding: utf-8 -*-
"""Shared build toolkit for every SuperLanguage profession module.

Single source of truth so IT / HR / Finance / Legal / Marketing cannot drift.

Per-module ``_build`` layout::

    config.py   -> `CONFIG = ModuleConfig(...)`
    actions.py  -> `CATEGORIES = [...]`
    data/mXX.py -> MONTH / MONTH_NAME / DAYS / THEME / THEME_EN / WORDS

Entry points::

    python _build/run_build.py                  # md + xlsx + html + pdf
    python _shared/validate.py <Module>         # vocabulary QA
    python _shared/validate_actions.py <Module> # action tree QA
    python _shared/audit.py                    # strict content audit (P0-P3)
    python _shared/set_words.py <Module> <N>   # patch entries safely
    python _shared/overlap_report.py            # cross-module duplicates
    python _shared/make_pdf.py <Module>         # headless-Chrome PDF
"""
from __future__ import annotations

import importlib.util
import re
from dataclasses import dataclass, field
from pathlib import Path

SHARED = Path(__file__).resolve().parent
ROOT = SHARED.parent
MODULES = ["IT", "HR", "Finance", "Legal", "Marketing"]


__all__ = [
    "ModuleConfig", "MODULES", "ROOT", "load_actions", "load_config",
    "load_months", "normalise", "opens_with_target", "singularise",
    "build_day_index", "split_label", "with_label",
]


@dataclass
class ModuleConfig:
    MODULE: str = ""
    PROJECT_TITLE: str = ""
    MODULE_TAG: str = ""
    STAGE_TITLE: str = ""
    DIFFICULTY_NOTE: str = "B2–C1"
    DIFFICULTY_SOURCES: str = "牛津高阶 / 朗文当代 / 柯林斯高阶"
    EXAMPLE_NOTE: str = "例句为真实职场场景，且以目标词或其变体开头。"
    REVIEW_CADENCE: str = "第 2 / 4 / 7 / 15 天各回看一次"
    ACCENT: str = "1F3864"
    ACCENT_SOFT: str = "F2F5FA"
    PHASES: list = field(default_factory=list)
    VOCAB_COLUMNS: list = field(default_factory=lambda: [
        "Day", "Month", "Theme", "Word", "Phonetic (BrE)", "Phonetic (AmE)",
        "Meaning (CN)", "Example (EN)", "Translation (CN)", "Review Round",
        "My Sentence",
    ])

    # --- paths -----------------------------------------------------------
    @property
    def module_dir(self) -> Path:
        return ROOT / self.MODULE

    @property
    def build_dir(self) -> Path:
        return self.module_dir / "_build"

    @property
    def data_dir(self) -> Path:
        return self.build_dir / "data"

    @property
    def vocab_dir(self) -> Path:
        return self.module_dir / "vocabulary"

    @property
    def actions_dir(self) -> Path:
        return self.module_dir / "actions"

    @property
    def html_dir(self) -> Path:
        return self.build_dir / "html"

    @property
    def html_path(self) -> Path:
        return self.html_dir / f"SuperLanguage_{self.MODULE}_365.html"

    @property
    def xlsx_path(self) -> Path:
        return self.module_dir / f"SuperLanguage_{self.MODULE}_365.xlsx"

    @property
    def pdf_path(self) -> Path:
        return self.module_dir / f"SuperLanguage_{self.MODULE}_365.pdf"

    # --- content ---------------------------------------------------------
    def phase_for(self, month_no: int):
        for lo, hi, cn, en in self.PHASES:
            if lo <= month_no <= hi:
                return cn, en
        raise ValueError(f"{self.MODULE}: no phase for month {month_no}")

    def office_category(self):
        for cat in load_actions(self.MODULE):
            if cat["id"] == 4:
                return cat
        raise ValueError(f"{self.MODULE}: action tree has no category id=4")


# --------------------------------------------------------------------------- #
# loading
# --------------------------------------------------------------------------- #
def _load(module: str, filename: str, attr_hint: str = ""):
    path = ROOT / module / "_build" / filename
    if not path.exists():
        raise FileNotFoundError(path)
    spec = importlib.util.spec_from_file_location(
        f"sl_{module}_{path.stem}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load_config(module: str) -> ModuleConfig:
    return _load(module, "config.py").CONFIG


def load_actions(module: str):
    return _load(module, "actions.py").CATEGORIES


def load_months(module: str):
    months = []
    for i in range(1, 13):
        months.append(_load(module, f"data/m{i:02d}.py"))
    return months


# --------------------------------------------------------------------------- #
# text helpers shared by validators and renderers
# --------------------------------------------------------------------------- #
# An accent tag is stored inside the phonetic field, e.g. "BrE /ˈkæt/".
# ``split_label("BrE /ˈkæt/") -> ("BrE", "/ˈkæt/")``
RE_ACCENT_LABEL = re.compile(r"^\s*(BrE|AmE)\s+(?=\S)")
ACCENT_TAGS = ("BrE", "AmE")


def split_label(value: str):
    """Return ``(tag_or_None, core)`` for a stored phonetic field."""
    m = RE_ACCENT_LABEL.match(value or "")
    if m:
        return m.group(1), value[m.end():].strip()
    return None, (value or "").strip()


def with_label(tag: str, core: str) -> str:
    """Attach an accent tag, refusing to double-tag."""
    _, bare = split_label(core)
    return f"{tag} {bare}"


IRREGULAR_GERUNDS = {
    "putting", "setting", "getting", "making", "taking", "sitting", "writing",
    "reading", "speaking", "breaking", "wearing", "choosing", "drawing",
    "swimming", "drinking", "singing", "ringing", "beginning", "running",
}


def normalise(word: str) -> str:
    """Lower-case and drop everything that is not a latin letter."""
    return re.sub(r"[^a-z]", "", word.lower())


def singularise(stem: str) -> str:
    """Best-effort de-pluralisation so 'spies' can match 'spy'."""
    if stem.endswith("ies") and len(stem) > 4:
        return stem[:-3] + "y"
    if stem.endswith("es") and len(stem) > 3:
        return stem[:-2]
    if stem.endswith("s") and not stem.endswith("ss") and len(stem) > 2:
        return stem[:-1]
    return stem


def opens_with_target(example: str, word: str) -> bool:
    """True when the example sentence starts with the target headword.

    Accepts inflections: plural, -ing/-ed, and multi-word headwords whose
    first token carries the meaning (e.g. 'candidate journey' -> 'Candidate').
    """
    first = example.strip().split()[0].lower().strip(".,:;!?\"'")
    stem = normalise(first)
    target = normalise(word.split()[0])
    if not target:
        return True
    if stem.startswith(target[:4]) or target.startswith(stem[:4]):
        return True
    alt = singularise(stem)
    return alt.startswith(target[:4]) or target.startswith(alt[:4])


def looks_like_gerund(phrase: str) -> bool:
    head = phrase.split()[0]
    return head in IRREGULAR_GERUNDS or head.endswith("ing")


def build_day_index(months):
    """Flatten months into (month, day_in_month, global_day, entry) rows."""
    rows, g = [], 0
    for mod in months:
        for d in range(mod.DAYS):
            for entry in mod.WORDS[d * 3:(d + 1) * 3]:
                g += 1
                rows.append((mod, d + 1, g, entry))
    return rows
