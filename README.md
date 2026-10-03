# SuperLanguage

**A 365-day English study corpus for five professional domains, where every
entry carries a British *and* an American transcription — and both labels are
machine-verified.**

5 domains · 5,475 headwords · 1,470 workplace actions · dual-accent IPA ·
69 automated content checks

---

## Why this exists

Most professional-vocabulary decks fail in the same three ways:

1. **One accent only.** A learner who later hears the American pronunciation of
   `schedule` `/ˈskɛdʒʊl/` has been given `/ˈʃedjuːl/` with nothing that tells
   them the two are both correct.
2. **Phonetic errors nobody can see.** A single wrong glyph — `Ƀ` instead of `ʒ`,
   a Greek `α` instead of `ɑ`, a corrupted byte — is invisible in a PDF and
   quietly teaches the wrong sound.
3. **No way to check the content.** Spreadsheets do not validate themselves.

SuperLanguage treats the corpus as **data with a schema, a validator and an
audit pipeline**. The phonetic fields are tagged, the tags are cross-checked
against the transcriptions they label, and one command fails the build on any
defect.

---

## What is in the box

| Module | Months | Headwords | Actions | Phases |
| --- | --- | --- | --- | --- |
| IT | 12 | 1,095 | 230 | 6 |
| HR | 12 | 1,095 | 308 | 12 |
| Finance | 12 | 1,095 | 302 | 12 |
| Legal | 12 | 1,095 | 315 | 12 |
| Marketing | 12 | 1,095 | 315 | 12 |
| **Total** | **60** | **5,475** | **1,470** | — |

Each module ships a 365-day plan of **3 headwords per day**, placed on the real
calendar (a 31-day month holds 93 entries, a 28-day February holds 84), plus an
action tree of everyday workplace phrases organised by scenario.

Per module you get:

| Artefact | Format | Purpose |
| --- | --- | --- |
| `SuperLanguage_<Module>_365.xlsx` | 11-column workbook | Study tracker: review rounds and a `My Sentence` column |
| `SuperLanguage_<Module>_365.pdf` | A4 print layout | Readable handbook (~6.6 MB) |
| `SuperLanguage_<Module>_365.html` | print-ready HTML | Source for the PDF |
| `vocabulary/MonthXX_*.md` | Markdown | One file per month, diff-friendly |
| `actions/Daily_Actions_Mapping.md` | Markdown | Full action tree |
| `vocabulary/IPA_Provenance.json` | JSON | Where every American transcription came from |
| `README.md` | Markdown | Generated module guide |

All five modules total 36.6 MB of generated output.

---

## The dual-accent phonetic system

### Data shape

Every entry is a six-field tuple:

```python
("schedule", "BrE /ˈʃedjuːl/", "AmE /ˈskɛdʒʊl/",
 "日程安排；排期",
 "Schedule the design review before the sprint planning session.",
 "把设计评审安排在冲刺规划会之前。")
#  word     ipa_brE        ipa_AmE        meaning             example                     translation
```

The accent tag lives **inside the field**. It is not a rendering convention, so
it survives into Markdown, Excel, HTML, PDF and JSON, and — critically — it can
be checked.

### Tags are verified, not trusted

A tag that contradicts its own transcription is a defect a learner would never
notice and would trust:

| Check | Severity | Catches |
| --- | --- | --- |
| `IPA_LABEL_MISSING` | P0 | field with no accent tag |
| `IPA_LABEL_WRONG` | P0 | `AmE` stored in the BrE column |
| `IPA_TAG_SWAPPED` | P0 | BrE and AmE tags exchanged |
| `IPA_TAG_NOT_TRUTHFUL` | P0 | `AmE`-tagged transcription containing `ː` or `ɒ`; `BrE`-tagged containing `ɹ`, `oʊ`, `ɝ` or `ɚ` |
| `IPA_DIALECT_MISMATCH` | P1 | same, seen from the symbol side |
| `IPA_AME_MISSING_R` | P2 | compound part where CMU requires a rhotic and we have none |

Current state across all 5,475 entries:

```
BrE fields tagged 'BrE'        : 5475
AmE fields tagged 'AmE'        : 5475
BrE fields with a wrong tag    : 0
AmE fields with a wrong tag    : 0
BrE holding American symbols   : 0
AmE holding British symbols    : 0
RESULT: clean
```

### Where the American transcription comes from

| Source | Entries | Share | Method |
| --- | --- | --- | --- |
| `cmu` | 1,559 | 28.5% | Whole headword found in the CMU Pronouncing Dictionary; ARPABET converted to General American IPA |
| `parts` | 3,707 | 67.7% | Compound aligned part by part; each part the dictionary knows is taken from the dictionary |
| `manual` | 11 | 0.2% | Hand-checked entries in `_shared/ipa_overrides.json` |
| `derived` | 198 | 3.6% | Rule conversion, only for headwords no dictionary carries |
| **Dictionary-backed** | **5,277** | **96.4%** | |

### Why the last 3.6% cannot be automated

American **r-insertion is lexical, not rule-governed**:

| British | American | Why no rule works |
| --- | --- | --- |
| `short` /ʃɔːt/ | /ʃɔɹt/ | takes the rhotic |
| `claw` /klɔː/ | /klɔ/ | identical vowel, no rhotic |
| `hard` /hɑːd/ | /hɑɹd/ | takes the rhotic |
| `half` /hɑːf/ | /hæf/ | same British long vowel, becomes /æ/ |

So compound headwords take the dictionary's reading segment by segment, which
both supplies the rhotic and lets the dictionary settle cases no rule can. Only
198 headwords that no dictionary carries — `kanban`, `swimlane`, `tooltip`,
`wireframe` — fall back to conversion, and each of the risky ones was read by
hand.

### Transcriptions are dialect-pure

The audit enforces a two-way exclusion:

- British fields may not contain `ɹ`, `oʊ`, `ɝ`, `ɚ`
- American fields may not contain `ː`, `ɒ`, `æː`

Length marks are a British convention and are absent from every American field;
the linking-r notation `ə(r)` is preserved where the American form requires it.

---

## Quick start

**Requirements**

- Python 3.10+ (developed on 3.13)
- `pip install cmudict openpyxl`
- Chrome or Edge — only for PDF export

```bash
git clone <your-fork-url> SuperLanguage
cd SuperLanguage

python _shared/validate.py                 # schema, counts, uniqueness, both IPAs
python _shared/validate_actions.py         # action tree
python _shared/audit.py                    # 69 content checks; non-zero on P0/P1
python _shared/verify_accent_labels.py     # dual-accent labelling only
python _shared/overlap_report.py           # cross-module duplicate report
```

Build artefacts (one module, or all five):

```bash
python _shared/generate.py IT
python _shared/generate.py                    # every module
python _shared/generate.py --no-pdf Legal     # skip PDF if no browser
```

`generate.py` also runs standalone per module via `<Module>/_build/run_build.py`.

---

## Repository layout

```
SuperLanguage/
├── README.md                     ← this file
├── AUDIT_REPORT.md               ← what the audit found and what was fixed
├── _shared/                      ← the engine; no module-specific code here
│   ├── toolkit.py                config dataclass, module loader, text helpers
│   ├── validate.py               vocabulary schema + counts + uniqueness
│   ├── validate_actions.py       action tree
│   ├── audit.py                  severity-grouped audit entry point
│   ├── audit_lib.py              IPA inventory, CMU access, corpus loader
│   ├── audit_ipa.py              28 phonetic checks incl. accent-label checks
│   ├── audit_text.py             30 example-grammar, headword and CJK-field checks
│   ├── audit_consistency.py      terminology and gloss-pairing checks
│   ├── american_ipa.py           ARPABET → AmE IPA, BrE → AmE conversion
│   ├── migrate_dual_ipa.py       idempotent schema migration + accent labelling
│   ├── ipa_overrides.json        hand-checked American transcriptions
│   ├── verify_accent_labels.py   dual-accent labelling report
│   ├── overlap_report.py         cross-module duplicate report
│   ├── set_words.py              guarded, idempotent entry patcher
│   ├── append_words.py           bulk entry appender
│   ├── trim_month.py             trim a month to an exact count
│   ├── fix_examples.py           bulk example rewriter
│   ├── generate.py               build orchestrator
│   ├── render_md.py              Markdown
│   ├── render_excel.py           workbook
│   └── render_html.py            print-ready HTML
└── <Module>/
    ├── README.md                 generated module guide
    ├── SuperLanguage_<M>_365.{xlsx,pdf}
    ├── _build/
    │   ├── config.py             title, phases, palette
    │   ├── actions.py            action tree
    │   ├── run_build.py          module build entry point
    │   ├── data/m01.py … m12.py  the vocabulary, as Python literals
    │   └── html/                 print-ready HTML
    ├── vocabulary/               generated monthly Markdown + provenance
    └── actions/                  generated action mapping
```

The vocabulary lives in `.py` files rather than JSON or CSV for one reason: it
is ordinary Python, so it is reviewable in a pull request, importable by a test,
and writable by a patcher without a serialisation round-trip.

---

## Data model

`<Module>/_build/data/mXX.py`:

```python
# -*- coding: utf-8 -*-
MONTH = 1
MONTH_NAME = "January"
DAYS = 31
THEME = "团队协作、敏捷开发 (Agile/Scrum)、项目管理与日常沟通"
THEME_EN = "Team Collaboration, Agile/Scrum, Project Management & Everyday Communication"

WORDS = [
    ("schedule", "BrE /ˈʃedjuːl/", "AmE /ˈskɛdʒʊl/", "日程安排；排期", "...", "..."),
    # word    ipa_brE             ipa_AmE            meaning          example  translation
]
```

Invariants the validator enforces:

- every month holds `DAYS × 3` entries, and `DAYS` matches the real calendar
- 1,095 headwords per module, normalised unique
- both phonetic fields present, tagged, and wrapped in `/ /`
- the example opens with the headword or an accepted inflection of it
- the translation contains Chinese characters

---

## The QA pipeline

69 checks across four modules, graded in four severities:

| Area | Checks |
| --- | --- |
| Phonetics, accents, labelling | 28 |
| Example grammar and punctuation | 19 |
| Headword orthography | 11 |
| Chinese fields, glosses, terminology | 7 |
| Structural and cross-entry | 4 |
| **Total** | **69** |

| Severity | Meaning | Blocks the build |
| --- | --- | --- |
| **P0** | corrupt or unusable data | yes |
| **P1** | contradicts an authoritative reference | yes |
| **P2** | grammar, orthography, consistency | reported |
| **P3** | style and polish | reported |

`audit.py` exits non-zero when any P0 or P1 exists, so it drops straight into
CI as a gate.

Phonetic checks are cross-validated against the **CMU Pronouncing Dictionary**
(126,052 entries) on three axes: syllable count, C/V skeleton, and
consonant-cluster similarity. Because CMU is an American dictionary, those
checks are applied to the British field with a documented exemption list, and
to the American field directly.

```bash
python _shared/audit.py --sev P0 --sev P1          # gate only
python _shared/audit.py --code IPA_AME_MISSING_R   # one check
python _shared/audit.py --json findings.json      # machine-readable
python _shared/audit.py Marketing                 # one module
```

### Writing conventions

The corpus follows a few house rules that the checks reinforce:

- British non-rhotic with optional linking r: `/ˈsteɪkhəʊldə(r)/`
- American general American with a written rhotic: `/ˈsteɪkhəʊldɚ/`
- one primary stress per word; stress sits over the syllable onset
- compounds are transcribed with a space between words
- the example always opens with the headword, so a learner meets the word first

---

## Extending

### Add vocabulary to an existing module

```bash
python _shared/set_words.py Finance 4 --show 12          # inspect
python _shared/set_words.py Finance 4 \
    --set "12=meaning=备抵；计提准备" --apply
```

`set_words.py` refuses to write when the entry width does not match the schema,
so a patch written for one layout cannot silently corrupt another column. It
edits the tuple in memory and re-serialises the list rather than re-parsing
source text.

To append a batch, write a UTF-8 file of pipe-separated records and use
`append_words.py`; to trim an over-full month, use `trim_month.py`.

### Add a module

1. `mkdir -p New/_build/data && cp -r IT/_build/config.py New/_build/`
2. Edit `MODULE`, `PROJECT_TITLE`, `MODULE_TAG`, `STAGE_TITLE`, `ACCENT`, `PHASES`
3. Write `New/_build/actions.py` with the `CATEGORIES` tree (one category must
   have `id = 4`; it becomes the office category)
4. Write `New/_build/data/m01.py … m12.py`
5. Register the name in `_shared/toolkit.py:MODULES`
6. `python _shared/migrate_dual_ipa.py --apply New` — adds the American column
   and the accent tags
7. `python _shared/validate.py New && python _shared/audit.py New`
8. `python _shared/generate.py New`

Steps 6 and 7 are the point of the whole design: you never hand-write the
American transcription, and the audit tells you which of them the dictionaries
could not supply.

---

## Data provenance and licensing

**This repository does not yet have a licence file. That must be settled before
publication** — the choice determines whether the corpus can be redistributed
and whether a `LICENSE` file, `SPDX` headers and a `CITATION.cff` are needed.

Sources and their status:

| Asset | Origin | Status |
| --- | --- | --- |
| British transcriptions | Hand-curated with reference to Oxford / Longman / Collins advanced dictionaries | Derivative; dictionary content is copyrighted and is **not** included as extracted text |
| American transcriptions | CMU Pronouncing Dictionary, converted to IPA by this project | The CMU dict file ships with a permissive notice; the conversion and this project's IPA conventions are original work |
| Glosses, examples, translations | Original, written for this project | Original work |
| Action phrases | Original | Original work |

The CMU dictionary is a data source, not a source of prose; no dictionary
entries are vendored into this repository. The `cmudict` package is a runtime
dependency, not a bundled file.

---

## Contributing

Content changes are welcome and are reviewed by the audit, not by eye:

1. Make the change with `set_words.py` or `append_words.py`
2. Run `validate.py` and `audit.py`; both must be clean
3. If the audit flags something you believe is wrong, add a documented exemption
   rather than deleting the check — every exemption carries its reason inline
4. Run `generate.py` for the affected module and commit the regenerated
   artefacts, so the repository never contains output that its data cannot
   reproduce

Style expectations for new entries:

- British English, B2–C1 professional register
- the gloss is a learner-facing Chinese equivalent; `；` separates senses
- the example is a real workplace sentence, never a definition
- jargon stays in Latin script only where that is how the industry writes it
  (`offer`, `OKR`, `ATS`); everything else gets a Chinese equivalent

---

## Roadmap

- [ ] Choose and add a `LICENSE`
- [ ] `requirements.txt` / `pyproject.toml` with pinned dependencies
- [ ] GitHub Actions running `validate` + `audit` as a gate on every push
- [ ] `.gitignore` covering `__pycache__` and scratch files (deliverables stay
      tracked so learners can download them straight from the repository)
- [ ] Remove or wire up `_shared/common_actions.py` (currently unreferenced)
- [ ] Corpus translations (zh-CN ↔ other locales) alongside the English
- [ ] Anki/Quizlet export from the workbook
- [ ] A fourth accent (AusE) reusing the `parts` alignment approach

---

## Acknowledgements

- The **CMU Pronouncing Dictionary** (cmudict), for making a
  dictionary-validated American transcription possible at this scale
- **Oxford Advanced Learner's Dictionary**, **Longman Dictionary of
  Contemporary English** and **Collins Advanced Learner's Dictionary**, as the
  reference points for British pronunciation and B2–C1 calibration
- Everyone who has read a phonetic transcription carefully enough to notice
  that `ˈdɒkjumenˈteɪʃn` and `ˈdɒkumenˈteɪʃn` are not the same thing

---

## Licence

Not yet determined — see [Data provenance and licensing](#data-provenance-and-licensing).