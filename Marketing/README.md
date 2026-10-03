# SuperLanguage 365-Day Marketing English Learning Plan

**模块**：Marketing · 市场营销英语

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
| 例句原则 | 真实营销职场场景（调研、品牌、内容、投放、销售、数据复盘），且以目标词开头 |

---

## 目录

### 模块一 · 365 天每日单词（按月分文件）

| 月份 | 文件 | 天数 | Day 区间 | 词条 | 本月主题 |
| --- | --- | --- | --- | --- | --- |
| 01 | [Month01_January.md](vocabulary/Month01_January.md) | 31 | Day 001–031 | 93 | 营销基础与市场调研（Marketing Fundamentals & Research） |
| 02 | [Month02_February.md](vocabulary/Month02_February.md) | 28 | Day 032–059 | 84 | 消费者行为与人群洞察（Consumer Behaviour & Segmentation） |
| 03 | [Month03_March.md](vocabulary/Month03_March.md) | 31 | Day 060–090 | 93 | 品牌定位与品牌管理（Brand Positioning & Brand Management） |
| 04 | [Month04_April.md](vocabulary/Month04_April.md) | 30 | Day 091–120 | 90 | 内容营销与故事表达（Content Marketing & Storytelling） |
| 05 | [Month05_May.md](vocabulary/Month05_May.md) | 31 | Day 121–151 | 93 | 社交媒体与社群运营（Social Media & Community） |
| 06 | [Month06_June.md](vocabulary/Month06_June.md) | 30 | Day 152–181 | 90 | 数字广告与效果投放（Digital Advertising & Paid Media） |
| 07 | [Month07_July.md](vocabulary/Month07_July.md) | 31 | Day 182–212 | 93 | SEO 与可发现性（SEO & Discoverability） |
| 08 | [Month08_August.md](vocabulary/Month08_August.md) | 31 | Day 213–243 | 93 | 公关、活动与整合传播（PR, Events & Integrated Communications） |
| 09 | [Month09_September.md](vocabulary/Month09_September.md) | 30 | Day 244–273 | 90 | 销售流程与客户关系（Sales Process & CRM） |
| 10 | [Month10_October.md](vocabulary/Month10_October.md) | 31 | Day 274–304 | 93 | 营销数据分析与度量（Marketing Analytics & Measurement） |
| 11 | [Month11_November.md](vocabulary/Month11_November.md) | 30 | Day 305–334 | 90 | 电商、渠道与增长运营（E-commerce, Channels & Growth） |
| 12 | [Month12_December.md](vocabulary/Month12_December.md) | 31 | Day 335–365 | 93 | 营销战略与高阶商务表达（Marketing Strategy & Executive Expression） |

### 模块二 · 全量日常动作分类映射树（9 大场景）

- [Daily_Actions_Mapping.md](actions/Daily_Actions_Mapping.md) — 9 大场景 / 315 条

### 打包产物

- `SuperLanguage_Marketing_365.xlsx` — Sheet 分为 每日单词 / 日常动作 / 月度主题 / 学习总览
- `SuperLanguage_Marketing_365.pdf` — 简洁学习手册排版（A4，可直接打印）

---

## 营销全链路 12 个月主题递进

| 阶段 | 月份 | 主题 |
| --- | --- | --- |
| 01 | Month 01 | 营销基础与市场调研（Marketing Fundamentals & Research） |
| 02 | Month 02 | 消费者行为与人群洞察（Consumer Behaviour & Segmentation） |
| 03 | Month 03 | 品牌定位与品牌管理（Brand Positioning & Brand Management） |
| 04 | Month 04 | 内容营销与故事表达（Content Marketing & Storytelling） |
| 05 | Month 05 | 社交媒体与社群运营（Social Media & Community） |
| 06 | Month 06 | 数字广告与效果投放（Digital Advertising & Paid Media） |
| 07 | Month 07 | SEO 与可发现性（SEO & Discoverability） |
| 08 | Month 08 | 公关、活动与整合传播（PR, Events & Integrated Communications） |
| 09 | Month 09 | 销售流程与客户关系（Sales Process & CRM） |
| 10 | Month 10 | 营销数据分析与度量（Marketing Analytics & Measurement） |
| 11 | Month 11 | 电商、渠道与增长运营（E-commerce, Channels & Growth） |
| 12 | Month 12 | 营销战略与高阶商务表达（Marketing Strategy & Executive Expression） |

---

## 每日使用节奏

1. **学**：先读 3 个新词，注意音标与例句语域。
2. **用**：用当天 3 个词各写 1 句自己的句子（Excel 中 `My Sentence` 列）。
3. **复习**：在 Excel `Review Round` 列打勾，第 2 / 4 / 7 / 15 天各回看一次。
4. **动作**：从模块二（尤其是场景 4「市场营销办公与工作日常」）挑 3 个当天高频动作，用新词复述一遍。

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
  --print-to-pdf="SuperLanguage_Marketing_365.pdf" _build/html/SuperLanguage_Marketing_365.html
```

校验：

```bash
python _shared/validate.py Marketing
python _shared/validate_actions.py Marketing
```
