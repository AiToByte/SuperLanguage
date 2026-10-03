# -*- coding: utf-8 -*-
"""Excel workbook builder shared by every module (4 sheets)."""
from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from toolkit import build_day_index  # noqa: E402


def build_workbook(cfg, cats, months, out_path: Path):
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    from openpyxl.utils import get_column_letter

    hdr_fill = PatternFill("solid", fgColor=cfg.ACCENT)
    hdr_font = Font(color="FFFFFF", bold=True, size=11)
    title_font = Font(bold=True, size=12, color=cfg.ACCENT)
    thin = Side(style="thin", color="C8C8C8")
    border = Border(left=thin, right=thin, top=thin, bottom=thin)
    alt = PatternFill("solid", fgColor=cfg.ACCENT_SOFT)
    center = Alignment(horizontal="center", vertical="center")

    day_rows = build_day_index(months)

    def style_header(ws, headers, row=1):
        for c, h in enumerate(headers, start=1):
            cell = ws.cell(row=row, column=c, value=h)
            cell.fill, cell.font, cell.border = hdr_fill, hdr_font, border
            cell.alignment = center

    def widths(ws, values):
        for i, w in enumerate(values, start=1):
            ws.column_dimensions[get_column_letter(i)].width = w

    wb = Workbook()
    wb.remove(wb.active)

    # ---- Sheet 1: vocabulary -------------------------------------------
    ws = wb.create_sheet("每日单词")
    style_header(ws, cfg.VOCAB_COLUMNS)
    ncol = len(cfg.VOCAB_COLUMNS)
    r = 2
    for mod, d, g, (word, ipa_brE, ipa_AmE, meaning, example,
                    translation) in day_rows:
        vals = [f"Day {g:03d}", f"Month {mod.MONTH:02d} {mod.MONTH_NAME}",
                mod.THEME, word, ipa_brE, ipa_AmE, meaning, example,
                translation, "", ""]
        for c, v in enumerate(vals[:ncol], start=1):
            ws.cell(row=r, column=c, value=v)
        ws.cell(row=r, column=4).font = Font(bold=True)
        for col in (5, 6):
            cell = ws.cell(row=r, column=col)
            cell.font = Font(name="Consolas", size=10)
            cell.alignment = Alignment(horizontal="center", vertical="center")
        for c in range(1, ncol + 1):
            cell = ws.cell(row=r, column=c)
            cell.border = border
            cell.alignment = Alignment(vertical="center", wrap_text=(c in (8, 9)))
            if r % 2 == 0:
                cell.fill = alt
        r += 1
    widths(ws, [9, 20, 42, 26, 28, 28, 24, 62, 46, 13, 40])
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = f"A1:{get_column_letter(ncol)}{r - 1}"

    # ---- Sheet 2: action tree ------------------------------------------
    ws = wb.create_sheet("日常动作")
    style_header(ws, ["No.", "Category (CN)", "Category (EN)",
                      "Action (CN)", "Action (EN)"])
    r, n = 2, 1
    for cat in cats:
        start = r
        for cn, en in cat["actions"]:
            for c, v in enumerate([n, cat["name_cn"], cat["name_en"], cn, en], 1):
                cell = ws.cell(row=r, column=c, value=v)
                cell.border = border
                if r % 2 == 0:
                    cell.fill = alt
            r += 1
            n += 1
        if len(cat["actions"]) > 1:
            ws.merge_cells(start_row=start, start_column=2, end_row=r - 1, end_column=2)
            ws.merge_cells(start_row=start, start_column=3, end_row=r - 1, end_column=3)
            for col in (2, 3):
                ws.cell(row=start, column=col).alignment = Alignment(
                    horizontal="center", vertical="center", wrap_text=True)
    widths(ws, [6, 22, 30, 26, 42])
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = f"A1:E{r - 1}"

    # ---- Sheet 3: monthly themes ---------------------------------------
    ws = wb.create_sheet("月度主题")
    style_header(ws, ["Month", "Month Name", "Days", "Word Count",
                      "Day Range", "Theme (CN)", "Theme (EN)", "Module Theme"])
    first = 1
    for mod in months:
        last = first + mod.DAYS - 1
        phase_cn, phase_en = cfg.phase_for(mod.MONTH)
        row = mod.MONTH + 1
        for c, v in enumerate([f"Month {mod.MONTH:02d}", mod.MONTH_NAME, mod.DAYS,
                               mod.DAYS * 3, f"Day {first:03d}–{last:03d}",
                               phase_cn, phase_en, mod.THEME], start=1):
            cell = ws.cell(row=row, column=c, value=v)
            cell.border = border
            cell.alignment = Alignment(vertical="center", wrap_text=(c in (6, 7, 8)))
        first = last + 1
    widths(ws, [10, 14, 8, 12, 16, 46, 48, 46])

    # ---- Sheet 4: overview ---------------------------------------------
    total_actions = sum(len(c["actions"]) for c in cats)
    ws = wb.create_sheet("学习总览")
    ws.cell(row=1, column=1, value=cfg.PROJECT_TITLE).font = title_font
    ws.cell(row=2, column=1, value=cfg.MODULE_TAG)
    facts = [
        ("学习周期", "365 天"),
        ("每日单词", "3 个"),
        ("全年词条", f"{len(day_rows)} 个（无重复）"),
        ("动作映射", f"{total_actions} 条 / {len(cats)} 大场景"),
        ("难度区间", cfg.DIFFICULTY_NOTE),
        ("音标体系", "双音标：英式 RP（BrE）＋ 美式（AmE）；"
                     "英式参照牛津 / 朗文 / 柯林斯高阶词典，美式对照 CMU"),
        ("例句原则", cfg.EXAMPLE_NOTE),
        ("生成日期", date.today().isoformat()),
    ]
    r = 4
    for k, v in facts:
        ws.cell(row=r, column=1, value=k).font = Font(bold=True)
        ws.cell(row=r, column=2, value=v)
        r += 1
    r += 1
    ws.cell(row=r, column=1, value=cfg.STAGE_TITLE).font = title_font
    r += 1
    style_header(ws, ["Stage", "Months", "Theme (CN)", "Theme (EN)"], row=r)
    for i, (lo, hi, cn, en) in enumerate(cfg.PHASES, start=1):
        for c, v in enumerate([f"{lo:02d}", f"Month {lo:02d}", cn, en], start=1):
            cell = ws.cell(row=r + i, column=c, value=v)
            cell.border = border
            cell.alignment = Alignment(vertical="center", wrap_text=(c in (3, 4)))
    r += len(cfg.PHASES) + 3
    ws.cell(row=r, column=1, value="动作映射分布").font = title_font
    r += 1
    style_header(ws, ["#", "Category (CN)", "Category (EN)", "Count"], row=r)
    for i, cat in enumerate(cats):
        for c, v in enumerate([cat["id"], cat["name_cn"], cat["name_en"],
                               len(cat["actions"])], start=1):
            ws.cell(row=r + 1 + i, column=c, value=v).border = border
    widths(ws, [18, 46, 48, 48])

    out_path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(out_path)
    return len(day_rows), total_actions
