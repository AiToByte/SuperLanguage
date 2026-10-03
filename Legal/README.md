# SuperLanguage 365-Day Legal English Learning Plan

**模块**：Legal · 法律英语

---

## 概览

| 项目 | 数值 |
| --- | --- |
| 学习周期 | 365 天 |
| 每日单词 | 3 个 |
| 全年词条 | 1095 个（已校验无重复） |
| 难度区间 | B2–C1 |
| 动作映射条目 | 315 条 / 9 大场景 |
| 音标体系 | 双音标：英式 RP（BrE）＋ 美式（AmE），英式参照牛津 / 朗文 / 柯林斯高阶词典，美式对照 CMU 发音词典 |
| 例句原则 | 真实法律实务场景（合同、诉讼、合规、谈判、知识产权），且以目标词开头 |

---

## 目录

### 模块一 · 365 天每日单词（按月分文件）

| 月份 | 文件 | 天数 | Day 区间 | 词条 | 本月主题 |
| --- | --- | --- | --- | --- | --- |
| 01 | [Month01_January.md](vocabulary/Month01_January.md) | 31 | Day 001–031 | 93 | 法律体系与法院结构（Legal System & Court Structure） |
| 02 | [Month02_February.md](vocabulary/Month02_February.md) | 28 | Day 032–059 | 84 | 合同基础与条款语言（Contract Fundamentals & Clauses） |
| 03 | [Month03_March.md](vocabulary/Month03_March.md) | 31 | Day 060–090 | 93 | 合同起草与修订（Contract Drafting & Revision） |
| 04 | [Month04_April.md](vocabulary/Month04_April.md) | 30 | Day 091–120 | 90 | 违约救济与争议解决（Breach, Remedies & Dispute Resolution） |
| 05 | [Month05_May.md](vocabulary/Month05_May.md) | 31 | Day 121–151 | 93 | 诉讼程序与证据（Litigation Procedure & Evidence） |
| 06 | [Month06_June.md](vocabulary/Month06_June.md) | 30 | Day 152–181 | 90 | 合规、监管与监管调查（Compliance, Regulation & Enforcement） |
| 07 | [Month07_July.md](vocabulary/Month07_July.md) | 31 | Day 182–212 | 93 | 公司治理与商事交易（Corporate Governance & Commercial Transactions） |
| 08 | [Month08_August.md](vocabulary/Month08_August.md) | 31 | Day 213–243 | 93 | 知识产权与技术保护（Intellectual Property & Technology） |
| 09 | [Month09_September.md](vocabulary/Month09_September.md) | 30 | Day 244–273 | 90 | 劳动用工与雇佣法（Employment & Labour Law） |
| 10 | [Month10_October.md](vocabulary/Month10_October.md) | 31 | Day 274–304 | 93 | 数据保护与网络安全（Data Protection & Cybersecurity） |
| 11 | [Month11_November.md](vocabulary/Month11_November.md) | 30 | Day 305–334 | 90 | 并购、融资与交易文件（Mergers, Financing & Transaction Documents） |
| 12 | [Month12_December.md](vocabulary/Month12_December.md) | 31 | Day 335–365 | 93 | 法律谈判、诉讼策略与高阶表达（Negotiation, Strategy & Advocacy） |

### 模块二 · 全量日常动作分类映射树（9 大场景）

- [Daily_Actions_Mapping.md](actions/Daily_Actions_Mapping.md) — 9 大场景 / 315 条

### 打包产物

- `SuperLanguage_Legal_365.xlsx` — Sheet 分为 每日单词 / 日常动作 / 月度主题 / 学习总览
- `SuperLanguage_Legal_365.pdf` — 简洁学习手册排版（A4，可直接打印）

---

## 法律实务 12 个月主题递进

| 阶段 | 月份 | 主题 |
| --- | --- | --- |
| 01 | Month 01 | 法律体系与法院结构（Legal System & Court Structure） |
| 02 | Month 02 | 合同基础与条款语言（Contract Fundamentals & Clauses） |
| 03 | Month 03 | 合同起草与修订（Contract Drafting & Revision） |
| 04 | Month 04 | 违约救济与争议解决（Breach, Remedies & Dispute Resolution） |
| 05 | Month 05 | 诉讼程序与证据（Litigation Procedure & Evidence） |
| 06 | Month 06 | 合规、监管与监管调查（Compliance, Regulation & Enforcement） |
| 07 | Month 07 | 公司治理与商事交易（Corporate Governance & Commercial Transactions） |
| 08 | Month 08 | 知识产权与技术保护（Intellectual Property & Technology） |
| 09 | Month 09 | 劳动用工与雇佣法（Employment & Labour Law） |
| 10 | Month 10 | 数据保护与网络安全（Data Protection & Cybersecurity） |
| 11 | Month 11 | 并购、融资与交易文件（Mergers, Financing & Transaction Documents） |
| 12 | Month 12 | 法律谈判、诉讼策略与高阶表达（Negotiation, Strategy & Advocacy） |

---

## 每日使用节奏

1. **学**：先读 3 个新词，注意音标与例句语域。
2. **用**：用当天 3 个词各写 1 句自己的句子（Excel 中 `My Sentence` 列）。
3. **复习**：在 Excel `Review Round` 列打勾，第 2 / 4 / 7 / 15 天各回看一次。
4. **动作**：从模块二（尤其是场景 4「法律办公与工作日常」）挑 3 个当天高频动作，用新词复述一遍。

---

## 质量控制

词库已通过自动化校验（`_shared/validate.py`）：

- 每月词条数 = 当月天数 × 3，全量 1095 条
- 全年 1095 个词条 **无重复**
- 每条例句均以目标单词/短语或其分词/变体开头
- 音标均以 `/ /` 包裹，英式与美式双音标均已标注（`BrE` / `AmE`），中文释义与中文翻译均非空

动作树已通过 `_shared/validate_actions.py`：9 大场景、中英条目均无重复、英文短语全部为动名词优先形式。

## 重新生成

```bash
python _build/run_build.py                       # md / xlsx / html
chrome --headless --disable-gpu --no-pdf-header-footer \
  --print-to-pdf="SuperLanguage_Legal_365.pdf" _build/html/SuperLanguage_Legal_365.html
```

校验：

```bash
python _shared/validate.py Legal
python _shared/validate_actions.py Legal
```
