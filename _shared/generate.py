# -*- coding: utf-8 -*-
"""Build every artefact for one module: md + xlsx + html.

    python _shared/generate.py [Module ...]
"""
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from toolkit import MODULES, load_actions, load_config, load_months  # noqa: E402
from render_md import render_actions_md, render_month_md, render_readme  # noqa: E402
from render_excel import build_workbook  # noqa: E402
from render_html import render_html  # noqa: E402

CHROME_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]


def find_browser():
    for path in CHROME_CANDIDATES:
        if Path(path).exists():
            return path
    return None


def make_pdf(cfg) -> bool:
    browser = find_browser()
    if not browser:
        print("  pdf  SKIPPED - no Chrome/Edge found")
        return False
    cmd = [
        browser,
        "--headless",
        "--disable-gpu",
        "--no-sandbox",
        "--no-pdf-header-footer",
        f"--print-to-pdf={cfg.pdf_path}",
        cfg.html_path.as_uri(),
    ]
    subprocess.run(cmd, check=False, capture_output=True)
    if cfg.pdf_path.exists():
        size = cfg.pdf_path.stat().st_size
        print(f"  pdf  {cfg.pdf_path.name}  ({size / 1024 / 1024:.2f} MB)")
        return True
    print(f"  pdf  FAILED - {cfg.pdf_path.name} not produced")
    return False


def build(module: str, want_pdf: bool = True):
    cfg = load_config(module)
    cats = load_actions(module)
    months = load_months(module)

    cfg.vocab_dir.mkdir(parents=True, exist_ok=True)
    cfg.actions_dir.mkdir(parents=True, exist_ok=True)
    cfg.html_dir.mkdir(parents=True, exist_ok=True)

    first = 1
    for mod in months:
        last = first + mod.DAYS - 1
        path = cfg.vocab_dir / f"Month{mod.MONTH:02d}_{mod.MONTH_NAME}.md"
        path.write_text(render_month_md(cfg, cats, mod, first, last), encoding="utf-8")
        print(f"  md   {path.name}  (Day {first:03d}-{last:03d}, {mod.DAYS * 3} words)")
        first = last + 1

    apath = cfg.actions_dir / "Daily_Actions_Mapping.md"
    apath.write_text(render_actions_md(cfg, cats), encoding="utf-8")
    print(f"  md   {apath.relative_to(cfg.module_dir)}  "
          f"({sum(len(c['actions']) for c in cats)} actions)")

    rpath = cfg.module_dir / "README.md"
    rpath.write_text(render_readme(cfg, cats, months), encoding="utf-8")
    print(f"  md   {rpath.relative_to(cfg.module_dir)}")

    n_words, n_actions = build_workbook(cfg, cats, months, cfg.xlsx_path)
    print(f"  xlsx {cfg.xlsx_path.name}  ({n_words} words, {n_actions} actions)")

    cfg.html_path.write_text(render_html(cfg, cats, months), encoding="utf-8")
    print(f"  html {cfg.html_path.name}")

    if want_pdf:
        make_pdf(cfg)

    print(f"\n[{module}] OK  words={n_words}  actions={n_actions}\n")


def main(argv):
    want_pdf = "--no-pdf" not in argv
    targets = [a for a in argv[1:] if not a.startswith("--")] or MODULES
    for module in targets:
        try:
            build(module, want_pdf=want_pdf)
        except FileNotFoundError as exc:
            print(f"[{module}] SKIPPED - {exc}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))