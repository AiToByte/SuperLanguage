# -*- coding: utf-8 -*-
"""Print-ready HTML renderer (A4 handbook layout) shared by every module."""
from __future__ import annotations

import html
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from toolkit import build_day_index, split_label  # noqa: E402

CSS = """
@page {{ size: A4; margin: 18mm 16mm 16mm 16mm; }}
* {{ box-sizing: border-box; }}
body {{ font-family: "Microsoft YaHei", "Segoe UI", "Noto Sans CJK SC", sans-serif;
       font-size: 10.2pt; line-height: 1.62; color: #1a1a1a; margin: 0; }}
h1 {{ font-size: 20pt; margin: 0 0 2mm; letter-spacing: .3px; }}
h2 {{ font-size: 13.5pt; margin: 9mm 0 3mm; padding-bottom: 1.6mm;
     border-bottom: 1.6px solid {accent}; color: {accent}; page-break-after: avoid; }}
h3 {{ font-size: 11.4pt; margin: 6mm 0 2mm; color: {accent}; page-break-after: avoid; }}
h4 {{ font-size: 10.6pt; margin: 4.5mm 0 1.5mm; color: #333; page-break-after: avoid; }}
.meta {{ color: #555; font-size: 9.2pt; margin-bottom: 1mm; }}
.meta-en {{ color: #777; font-size: 8.6pt; font-style: italic; }}
table {{ width: 100%; border-collapse: collapse; margin: 3mm 0; font-size: 9.4pt; }}
th {{ background: {accent}; color: #fff; padding: 1.6mm 2.2mm; text-align: left;
     font-weight: 600; border: 1px solid {accent}; }}
td {{ padding: 1.5mm 2.2mm; border: 1px solid #d6d6d6; vertical-align: top; }}
tr:nth-child(even) td {{ background: {soft}; }}
ul {{ margin: 1.5mm 0; padding-left: 6mm; columns: 2; column-gap: 8mm; }}
li {{ break-inside: avoid; margin-bottom: 0.8mm; }}
.w {{ font-weight: 700; }}
.ph {{ font-family: "Consolas", "Courier New", monospace; font-size: 9.4pt;
      color: #333; }}
.tag {{ font-family: "Segoe UI", sans-serif; font-size: 8pt; font-weight: 700;
       color: #C00000; background: #FCE4E4; border: 1px solid #C00000;
       border-radius: 2px; padding: 0 3px; margin-right: 3px;
       -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
.tag.ame {{ color: #7A5C1E; background: #F6EEDC; border-color: #7A5C1E; }}
.cn {{ color: #444; }}
.exzh {{ color: #666; font-size: 9.4pt; }}
.day {{ page-break-inside: avoid; }}
.note {{ background: {soft}; border-left: 3px solid {accent};
        padding: 2.4mm 3mm; margin: 3mm 0; font-size: 9.2pt; }}
.cover {{ text-align: center; padding-top: 46mm; page-break-after: always; }}
.cover .sub {{ color: #555; font-size: 12pt; margin-top: 3mm; }}
.cover .meta {{ margin-top: 12mm; font-size: 10pt; }}
.cover .facts {{ margin: 16mm auto 0; width: 78%; text-align: left; }}
.small {{ font-size: 8.6pt; color: #666; }}
"""


def render_html(cfg, cats, months) -> str:
    day_rows = build_day_index(months)
    total_actions = sum(len(c["actions"]) for c in cats)
    office = cfg.office_category()["name_cn"]
    e = html.escape
    out = []
    a = out.append

    a("<!DOCTYPE html><html lang='zh-CN'><head><meta charset='utf-8'>")
    a(f"<title>{e(cfg.PROJECT_TITLE)}</title><style>")
    a(CSS.format(accent=cfg.ACCENT, soft=cfg.ACCENT_SOFT))
    a("</style></head><body>")

    # ---- cover ----------------------------------------------------------
    a("<div class='cover'>")
    a(f"<h1>{e(cfg.PROJECT_TITLE)}</h1>")
    a(f"<div class='sub'>{e(cfg.MODULE_TAG)}</div>")
    a(f"<div class='meta'>365 天 × 3 词 = {len(day_rows)} 个高频专业词"
      f"（{e(cfg.DIFFICULTY_NOTE)}）<br>"
      f"＋ {len(cats)} 大场景日常动作映射树</div>")
    a("<div class='facts'><table>")
    a("<tr><th>学习周期</th><td>365 天（Day 001 – Day 365）</td></tr>")
    a(f"<tr><th>每日词条</th><td>3 个，全年 {len(day_rows)} 个，已校验无重复</td></tr>")
    a(f"<tr><th>动作映射</th><td>{total_actions} 条，覆盖 {len(cats)} 大日常场景</td></tr>")
    a(f"<tr><th>难度区间</th><td>{e(cfg.DIFFICULTY_NOTE)}</td></tr>")
    a("<tr><th>音标体系</th><td>每条词条两套音标并各自带标识："
      "<span class='tag'>BrE</span> 英国英语（RP，参照牛津 / 朗文 / "
      "柯林斯高阶词典），"
      "<span class='tag ame'>AmE</span> 美国英语（General American，"
      "对照 CMU 发音词典）</td></tr>")
    a(f"<tr><th>例句原则</th><td>{e(cfg.EXAMPLE_NOTE)}</td></tr>")
    a("</table></div></div>")

    # ---- contents -------------------------------------------------------
    a("<h2>目录</h2><table><tr><th>月份</th><th>Day 区间</th>"
      "<th>词条</th><th>本月主题</th></tr>")
    first = 1
    for mod in months:
        last = first + mod.DAYS - 1
        phase_cn, _ = cfg.phase_for(mod.MONTH)
        a(f"<tr><td>Month {mod.MONTH:02d} · {e(mod.MONTH_NAME)}</td>"
          f"<td>Day {first:03d}–{last:03d}</td><td>{mod.DAYS * 3}</td>"
          f"<td>{e(phase_cn)}</td></tr>")
        first = last + 1
    a("</table>")
    a("<div class='note'><b>每日节奏</b>：① 读 3 个新词（音标 + 例句）　"
      "② 用每个词各造 1 句　"
      f"③ {e(cfg.REVIEW_CADENCE)}　"
      f"④ 从场景 4「{e(office)}」挑 3 个动作，用新词复述一遍</div>")

    # ---- vocabulary -----------------------------------------------------
    first = 1
    for mod in months:
        phase_cn, phase_en = cfg.phase_for(mod.MONTH)
        a("<h2 style='page-break-before: always'>"
          f"Month {mod.MONTH:02d} · {e(mod.MONTH_NAME)}</h2>")
        a(f"<div class='meta'>年度主题：{e(phase_cn)}</div>")
        a(f"<div class='meta-en'>{e(phase_en)}</div>")
        a(f"<div class='meta'>Day {first:03d} – Day {first + mod.DAYS - 1:03d}"
          f" ｜ {mod.DAYS} 天 ｜ {mod.DAYS * 3} 词</div>")
        a("<h3>模块一 · 每日单词</h3>")
        for d in range(mod.DAYS):
            a(f"<h4 class='day'>Day {first + d:03d}　"
              f"{e(mod.MONTH_NAME)} {d + 1}</h4>")
            a("<table><tr><th>#</th><th>Word</th>"
              "<th>英式音标 <span class='tag'>BrE</span></th>"
              "<th>美式音标 <span class='tag ame'>AmE</span></th>"
              "<th>中文释义</th><th>例句 / Example</th></tr>")
            for i, (w, ipa_brE, ipa_AmE, meaning, example,
                    translation) in enumerate(
                        mod.WORDS[d * 3:(d + 1) * 3], start=1
            ):
                _, core_br = split_label(ipa_brE)
                _, core_am = split_label(ipa_AmE)
                a(f"<tr><td>{i}</td><td class='w'>{e(w)}</td>"
                  f"<td class='ph'><span class='tag'>BrE</span>{e(core_br)}</td>"
                  f"<td class='ph'><span class='tag ame'>AmE</span>"
                  f"{e(core_am)}</td><td class='cn'>{e(meaning)}</td>"
                  f"<td>{e(example)}<br>"
                  f"<span class='exzh'>（{e(translation)}）</span></td></tr>")
            a("</table>")
        first += mod.DAYS

    # ---- action tree ----------------------------------------------------
    a("<h2 style='page-break-before: always'>"
      f"模块二 · 全量日常动作分类映射树（{len(cats)} 大场景）</h2>")
    a("<div class='meta'>格式：中文动作 — 英文短语（优先动名词 -ing 形式）｜"
      f" 共 {total_actions} 条，中英条目均无重复</div>")
    for cat in cats:
        a(f"<h3>{cat['id']}. {e(cat['name_cn'])}　"
          f"<span class='small'>{e(cat['name_en'])}</span></h3>")
        if cat.get("note"):
            a(f"<div class='note'>{e(cat['note'])}</div>")
        a("<ul>")
        for cn, en in cat["actions"]:
            a(f"<li>{e(cn)} — {e(en)}</li>")
        a("</ul>")

    a("<h4>使用说明</h4><ul style='columns:1'>")
    a("<li>口语中英文动作短语常省略人称代词，直接接在 <i>be</i> 动词后使用。</li>")
    a("<li>书面与邮件中建议补足主语与时态标记。</li>")
    a("<li>同一动作在不同语境常有更贴切的说法，选词时以本模块场景为准。</li>")
    a("<li>后续补充未覆盖的动作将自动归入最接近的场景，并沿用同一格式。</li>")
    a("</ul>")
    a("</body></html>")
    return "\n".join(out)