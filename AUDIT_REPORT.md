# SuperLanguage 内容审校报告

范围：IT / HR / Finance / Legal / Marketing 五个模块，
每模块 12 个月、1095 词条，合计 5475 条词条、1470 条日常动作。
每条词条均含英式（BrE）与美式（AmE）两套音标，并明确标注区分。

## 0. 双音标体系

数据条目为六元组：

```
(word, ipa_brE, ipa_AmE, meaning, example, translation)
```

音标来源分两类，逐条记录在 `<模块>/vocabulary/IPA_Provenance.json`：

| 来源 | 条数 | 占比 | 说明 |
|---|---|---|---|
| cmu | 1560 | 28.5% | CMU 发音词典精确命中，ARPABET 直转美国通用 IPA |
| derived | 3915 | 71.5% | 由精修英式音标按系统对应规则转换 |

分布：IT 738/357、HR 157/938、Finance 185/910、Legal 260/835、Marketing 220/875。

采用 derived 的原因：复合词与短语若按词块拼装词典读音，会丢失音节对齐并打乱重音
（实测出现 `/ˈˌædfətˈʌɡ/` 这类错标）。规则转换只改变元音音质、完整保留既有重音模式，
结果可预测。复合词与行业术语（如 kanban、tooltip）CMU 多无收录，也只能走此路径。

英式转美式的系统对应：

| 英式 | 美式 | 例 |
|---|---|---|
| ɪː iː uː ʊː ɔː ɑː ɜː | ɪ i u ʊ ɔ ɑ ɝ | 去长度标记 |
| ɒ | ɑ | cut-off → ˈkʌt ɑf |
| əʊ | oʊ | organisation |
| aː | æ | schedule |
| ɪə eə ʊə | ɪɹ ɛɹ ʊɹ | |
| r | ɹ | framework |
| (r) 连读 | 保留并显式化 | letter → ˈlɛtɚ |

刻意**不**推测美式的 r 插入：那是词汇性的，不是规则性的。
因此 derived 条目的辅音骨架与英式一致，仅元音音质变化。

两套音标的分工由 `_shared/audit_ipa.py` 双向校验：
美式不得出现 ː ɒ，英式不得出现 ɹ oʊ ɝ ɚ。

## 1. 审校方法

自动化只能把 5475 条收敛到可人工判断的量，因此本次审校分三层：

| 层 | 手段 | 依据 |
|---|---|---|
| 符号层 | IPA 字符白名单、重音与长音构型、括号与斜杠检查 | IPA 规范与本语料英式转写约定 |
| 交叉层 | 音节数、C/V 骨架、相似度与 CMU 逐音段比对 | CMU Pronouncing Dictionary（126,052 词条） |
| 文本层 | 例句语法、大小写、缩写、中文字段完整性、术语一致性 | 项目规则加人工分诊 |

工具链（均在 `_shared/`）：

| 文件 | 作用 |
|---|---|
| `audit.py` | 审校入口，按严重度输出，支持 `--sev` / `--code` / `--json` |
| `audit_lib.py` | IPA 音标表、CMU 查询与英美拼写桥接、语料载入 |
| `audit_ipa.py` | 音标结构、方言互斥与发音交叉校验 |
| `audit_text.py` | 词头正字法、例句语法、中文字段 |
| `audit_consistency.py` | 术语一致性、释义配对、混排检测 |
| `american_ipa.py` | ARPABET→美式 IPA、英式→美式规则转换 |
| `migrate_dual_ipa.py` | 六字段幂等迁移，`--refresh` 可重算美式列 |
| `set_words.py` | 安全幂等改词条工具（含字段数守卫） |

严重度定义：

- P0 数据损坏或不可用
- P1 与权威参考相抵触
- P2 语法、正字法、一致性缺陷
- P3 风格与打磨建议

## 2. 结果

| 严重度 | 审校前 | 审校后 |
|---|---|---|
| P0 | 55 | 0 |
| P1 | 65 | 0 |
| P2 | 203 | 0 |
| P3 | 2755 | 2666（均为可接受体例，见第 5 节） |

## 3. 已修复的 P0（数据损坏）

| 类型 | 数量 | 说明 |
|---|---|---|
| 音标字形被破坏 | 14 | disclosure 家族的 /ʒ/ 被替换为 U+FFFD |
| 非法音标符号 | 6 | U+0243、U+0152、U+0279、希腊 alpha U+03B1、音标内连字符 |
| 音标斜杠数错误 | 5 | 早期修复脚本遗留的尾部双斜杠 |
| 中文译文乱码 | 4 | 责任人后缺字、上诉方案件事实后缺字等 |

修复示例：disclosure 改为 `/dɪsˈkləʊʒə(r)/`，consignment 改为 `/kənˈsɪnmənt/`，
permanent injunction 改为 `/ˈpɜːmənənt ɪnˈdʒʌŋkʃn/`，rightsizing 改为 `/ˈraɪtsaɪzɪŋ/`。

## 4. 已修复的 P1（与参考相抵触）

**音标错误（CMU 交叉校验发现）**

- chunking `/ˈtʌŋkɪŋ/` 改为 `/ˈtʃʌŋkɪŋ/`（CMU 证明为 /tʃ/）
- storytelling `/ˈstɔːrɪtɪŋ/` 改为 `/ˈstɔːritelɪŋ/`（漏音节）
- 双重主重音：notwithstanding、accord and satisfaction、
  request for information、ad fatigue
- 多词词头音标漏段：trade mark 系列、passing off of get-up、
  onboarding improvement、brand cannibalisation、such other relief 句
- and thereafter 是从句而非词条，已改为 thereafter

**例句未以目标词开头（18 项）**

- 真实缺陷：`So-what`、`You-said-we-d`、`Day-in-the-life`、`Pay-to-play`、
  `Add-to-cart` 等把首词连字符化；`fined` 的例句误用名词 `Fines`
- 已修正：`Set aside an award...`、`Fined for late filing...`、
  `Day in the life research...`、`Add to cart buttons...`

## 5. 保留的 P3 及理由

| 代码 | 数量 | 保留理由 |
|---|---|---|
| IPA_SYLLABLE_LONG | 983 | CMU 存弱读简式，英式谨慎读法保留词首 /ə/ 属正常 |
| TERM_GLOSS_CONFLICT | 575 | 跨模块同词不同义属正当，如 equity 在 IT 为公平、在 Finance 为所有者权益 |
| IPA_INITIAL_STRESS | 321 | 单音节标重音是本语料统一体例，牛津 learner 词典亦常见 |
| IPA_CMU_DIFFERENT | 315 | 英式与美式差异，如 schedule、version、opportunity |
| GLOSS_HEADWORD_CONFLICT | 192 | 一个中文释义对应近义词属正常 |
| CN_TRANS_LATIN / CN_MEAN_LATIN | 153 | offer、OKR、KPI、HRBP 等中文职场标准术语 |
| PHRASE_TOO_LONG | 87 | 法律固定搭配，如 such other relief as the court thinks fit |
| IPA_DOUBLE_SECONDARY | 10 | 长词多重次重音符合剑桥标注习惯 |
| GLOSS_MIXED_SCRIPT | 10 | Kubernetes、Transformer、robots.txt、SMART 属专有写法 |

英式音变豁免清单记录在 `audit_ipa.py` 的 `KNOWN_BRITISH_FORMS`，
每条附豁免理由，保证审校输出可复核。

## 6. 过程中的一次事故与恢复

修复过程中曾把同一份补丁错误地应用到全部 16 个月文件，导致大规模字段错位。
恢复方式：从 `vocabulary/Month*.md` 与 `_build/html/*.html` 两份**互相独立**的产物
分别解析 5475 条，逐字段比对一致后才回写；恢复后审校基线与事故前完全一致
（P0 55 / P1 65 / P2 225 / P3 2657），确认无损。

为此新增 `set_words.py`：在内存中修改 `WORDS` 后整体重新序列化，
不再从源文本反解析字段，从根本上消除同类风险。

## 7. 复审方式

```
python _shared/validate.py         # 数量、唯一性、双音标斜杠、例句开头
python _shared/validate_actions.py # 动作树
python _shared/audit.py            # 严格内容审校，P0/P1/P2 应为 0
python _shared/overlap_report.py   # 跨模块重合
python _shared/migrate_dual_ipa.py --refresh   # 重算全部美式音标
```

`audit.py` 以 P0 或 P1 存在时返回非零退出码，可直接接入流水线作为门禁。
`set_words.py` 在条目字段数与预期不符时拒绝写入，避免按错误列号覆盖字段。
