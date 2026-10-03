# -*- coding: utf-8 -*-
"""Markdown renderers shared by every module (README, month files, action tree)."""
from __future__ import annotations

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from toolkit import build_day_index  # noqa: E402


def render_month_md(cfg, cats, mod, first_day: int, last_day: int) -> str:
    phase_cn, phase_en = cfg.phase_for(mod.MONTH)
    lines = []
    a = lines.append
    a(f"# Month {mod.MONTH:02d} · {mod.MONTH_NAME}")
    a("")
    a(f"> **年度主题（阶段 {mod.MONTH} / 共 {len(cfg.PHASES)} 阶段）**：{phase_cn}")
    a(">")
    a(f"> **Theme (EN)**：{phase_en}")
    a(">")
    a(f"> **Day {first_day:03d} – Day {last_day:03d}** ｜ 本月 {mod.DAYS} 天 ｜ "
      f"{mod.DAYS * 3} 个单词")
    a(">")
    a(f"> **难度**：{cfg.DIFFICULTY_NOTE}（{cfg.DIFFICULTY_SOURCES}）")
    a("")
    a("---")
    a("")
    a("## 模块一 · 每日单词")
    a("")
    a("格式：`[英文单词/短语] → [英式音标] ｜ [美式音标] → [中文释义]`，"
      "两条音标各自带有 `BrE` / `AmE` 标识，例句以该词或其变体开头。")
    a("")
    a("| 标识 | 含义 | 依据 |")
    a("| --- | --- | --- |")
    a("| `BrE` | 英国英语（RP） | 牛津 / 朗文 / 柯林斯高阶词典 |")
    a("| `AmE` | 美国英语（General American） | CMU 发音词典 |")
    a("")

    for d in range(mod.DAYS):
        a(f"### Day {first_day + d:03d}　（{mod.MONTH_NAME} {d + 1}）")
        a("")
        for i, (word, ipa_brE, ipa_AmE, meaning, example,
                translation) in enumerate(
                    mod.WORDS[d * 3:(d + 1) * 3], start=1
        ):
            a(f"{i}. **{word}** → `{ipa_brE}` ｜ `{ipa_AmE}` → {meaning}")
            a(f"   例句：{example}（{translation}）")
            a("")

    total_actions = sum(len(c["actions"]) for c in cats)
    a("---")
    a("")
    a("## 模块二 · 日常动作映射")
    a("")
    a(f"完整动作映射树（{len(cats)} 大场景 / {total_actions} 条）见 "
      "[`../actions/Daily_Actions_Mapping.md`](../actions/Daily_Actions_Mapping.md)。")
    a("")
    a("| 场景 | 本模块示例动作 |")
    a("| --- | --- |")
    for cat in [cats[0], cfg.office_category()]:
        for cn, en in cat["actions"][:3]:
            a(f"| {cat['name_cn']} | {cn} — {en} |")
    a("")
    return "\n".join(lines)


def render_actions_md(cfg, cats) -> str:
    total = sum(len(c["actions"]) for c in cats)
    lines = []
    a = lines.append
    a(f"# 模块二 · 全量日常动作分类映射树（{cfg.MODULE} 版）")
    a("")
    a("> **格式**：`中文动作 — 英文短语`（优先使用动名词 -ing 形式）")
    a(">")
    a(f"> **规模**：{len(cats)} 大核心场景 ｜ {total} 条动作 ｜ 中英条目均已去重")
    a("")
    a("---")
    a("")
    a("## 场景总览")
    a("")
    a("| # | 场景 | English | 条目数 |")
    a("| --- | --- | --- | --- |")
    for cat in cats:
        a(f"| {cat['id']} | {cat['name_cn']} | {cat['name_en']} | "
          f"{len(cat['actions'])} |")
    a(f"| | **合计** | | **{total}** |")
    a("")
    a("---")
    a("")
    for cat in cats:
        a(f"## {cat['id']}. {cat['name_cn']}　{cat['name_en']}")
        a("")
        if cat.get("note"):
            a(f"> {cat['note']}")
            a("")
        for cn, en in cat["actions"]:
            a(f"- {cn} — {en}")
        a("")
    a("---")
    a("")
    a("## 使用说明")
    a("")
    a("1. 口语中英文动作短语常省略人称代词，直接接在 *be* 动词后使用：*I'm + V-ing ...*")
    a("2. 书面与邮件中建议补足主语与时态标记。")
    a("3. 同一动作在不同语境常有更贴切的说法，选词时以本模块场景为准。")
    a("4. 后续补充未覆盖的动作将自动归入最接近的场景，并沿用同一格式。")
    a("")
    return "\n".join(lines)


def render_readme(cfg, cats, months) -> str:
    day_rows = build_day_index(months)
    total_actions = sum(len(c["actions"]) for c in cats)
    total_words = len(day_rows)
    lines = []
    a = lines.append
    a(f"# {cfg.PROJECT_TITLE}")
    a("")
    a(f"**模块**：{cfg.MODULE_TAG}")
    a("")
    a("---")
    a("")
    a("## 概览")
    a("")
    a("| 项目 | 数值 |")
    a("| --- | --- |")
    a("| 学习周期 | 365 天 |")
    a("| 每日单词 | 3 个 |")
    a(f"| 全年词条 | {total_words} 个（已校验无重复） |")
    a(f"| 难度区间 | {cfg.DIFFICULTY_NOTE} |")
    a(f"| 动作映射条目 | {total_actions} 条 / {len(cats)} 大场景 |")
    a("| 音标体系 | 双音标：英式 RP（BrE）＋ 美式（AmE），"
      "英式参照牛津 / 朗文 / 柯林斯高阶词典，美式对照 CMU 发音词典 |")
    a(f"| 例句原则 | {cfg.EXAMPLE_NOTE} |")
    a("")
    a("---")
    a("")
    a("## 目录")
    a("")
    a("### 模块一 · 365 天每日单词（按月分文件）")
    a("")
    a("| 月份 | 文件 | 天数 | Day 区间 | 词条 | 本月主题 |")
    a("| --- | --- | --- | --- | --- | --- |")
    first = 1
    for mod in months:
        last = first + mod.DAYS - 1
        phase_cn, _ = cfg.phase_for(mod.MONTH)
        a(f"| {mod.MONTH:02d} | [Month{mod.MONTH:02d}_{mod.MONTH_NAME}.md]"
          f"(vocabulary/Month{mod.MONTH:02d}_{mod.MONTH_NAME}.md) | {mod.DAYS} | "
          f"Day {first:03d}–{last:03d} | {mod.DAYS * 3} | {phase_cn} |")
        first = last + 1
    a("")
    a(f"### 模块二 · 全量日常动作分类映射树（{len(cats)} 大场景）")
    a("")
    a("- [Daily_Actions_Mapping.md](actions/Daily_Actions_Mapping.md) — "
      f"{len(cats)} 大场景 / {total_actions} 条")
    a("")
    a("### 打包产物")
    a("")
    a(f"- `{cfg.xlsx_path.name}` — Sheet 分为 每日单词 / 日常动作 / 月度主题 / 学习总览")
    a(f"- `{cfg.pdf_path.name}` — 简洁学习手册排版（A4，可直接打印）")
    a("")
    a("---")
    a("")
    a(f"## {cfg.STAGE_TITLE}")
    a("")
    a("| 阶段 | 月份 | 主题 |")
    a("| --- | --- | --- |")
    for lo, hi, cn, en in cfg.PHASES:
        a(f"| {lo:02d} | Month {lo:02d} | {cn} |")
    a("")
    a("---")
    a("")
    a("## 每日使用节奏")
    a("")
    a("1. **学**：先读 3 个新词，注意音标与例句语域。")
    a("2. **用**：用当天 3 个词各写 1 句自己的句子（Excel 中 `My Sentence` 列）。")
    a(f"3. **复习**：在 Excel `Review Round` 列打勾，{cfg.REVIEW_CADENCE}。")
    a(f"4. **动作**：从模块二（尤其是场景 4「{cfg.office_category()['name_cn']}」）"
      "挑 3 个当天高频动作，用新词复述一遍。")
    a("")
    a("---")
    a("")
    a("## 质量控制")
    a("")
    a("词库已通过自动化校验（`_shared/validate.py`）：")
    a("")
    a("- 每月词条数 = 当月天数 × 3，全量 1095 条")
    a("- 全年 1095 个词条 **无重复**")
    a("- 每条例句均以目标单词/短语或其分词/变体开头")
    a("- 音标均以 `/ /` 包裹，英式与美式双音标均已标注（`BrE` / `AmE`），"
      "中文释义与中文翻译均非空")
    a("")
    a("动作树已通过 `_shared/validate_actions.py`："
      f"{len(cats)} 大场景、中英条目均无重复、英文短语全部为动名词优先形式。")
    a("")
    a("## 重新生成")
    a("")
    a("```bash")
    a("python _build/run_build.py                       # md / xlsx / html")
    a(f'chrome --headless --disable-gpu --no-pdf-header-footer \\')
    a(f'  --print-to-pdf="{cfg.pdf_path.name}" '
      f'_build/html/SuperLanguage_{cfg.MODULE}_365.html')
    a("```")
    a("")
    a("校验：")
    a("")
    a("```bash")
    a(f"python _shared/validate.py {cfg.MODULE}")
    a(f"python _shared/validate_actions.py {cfg.MODULE}")
    a("```")
    a("")
    return "\n".join(lines)
