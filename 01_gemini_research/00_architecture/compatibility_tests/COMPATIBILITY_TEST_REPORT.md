# Gemini Prompt Compatibility Test — Report

**Date:** 08-Oct-2026 · **Gate:** 2C · **Decisions:** D-084, D-087 · **Tool:** `00_project/tools/gemini_compat_test.py`

> **NON-RESEARCH TEST ARTIFACTS.** These were format and compatibility tests only. No Guinea research was requested or performed, and no mission was executed. The replies contain placeholder text (`TEST`) only. They are not evidence and must not be entered in any register.

## Method

1. `gemini_compat_test.py build` wraps a package's **complete** prompt block, from `<!-- PROMPT START -->` to `<!-- PROMPT END -->` verbatim, in test instructions. These forbid tools, web search and any factual content. They ask Gemini only to echo the boundary lines, every section heading and every question heading, to count the hypothesis traps, to reproduce the evidence-table column list, and to return an **empty** 17-section skeleton with placeholder claim and source IDs.
2. **Execution:** Antigravity CLI `agy` v1.3.1, print mode, `--sandbox`, run from an empty scratch working directory.
3. `gemini_compat_test.py check` verifies each reply against the owner's nine criteria, plus a tenth check that the reply contains no research content.

## Runs

| Run | Model | Packages tested | Status |
|---|---|---|---|
| Run 1 | CLI default — confirmed from CLI logs as **Gemini 3.8 Flash (High)** (`gemini-3.8-flash-high`) | GEM-05 and GEM-12 before the P-029 wording update | 10/10 and 10/10 (superseded by run 2 because the package text has since changed) |
| **Run 2 (current)** | **Pinned explicitly:** `agy --model gemini-3.8-flash-high`; the CLI log records `model="gemini-3.8-flash-high"` | **Current** GEM-05 and GEM-12 Pv1 packages, after P-029 (D-086) | **10/10 and 10/10** |

## Run 2 — current packages, pinned model

| Mission | Package SHA-256 (current; trailing-newline normalisation only, prompt block byte-identical to the tested prompt) | Test prompt size | Prompt SHA-256 | Reply SHA-256 |
|---|---|---|---|---|
| GEM-05 | `d6e3e17ee3d95eb7…` | 36,450 characters (~9,112 tokens, estimated) | `ab7bceee57dc87ef…` | `543a23c6f58fce73…` |
| GEM-12 | `72f574f9c6f913fc…` | 24,092 characters (~6,023 tokens, estimated) | `ba4cf2934207a3e6…` | `bd3b2a387641dd36…` |

### GEM-05 (run 2)

```
PASS | 1 complete prompt accepted | reply completed with the closing line
PASS | 2 PROMPT START / END intact | both boundary lines echoed exactly
PASS | 3 all mission instructions retained | 23/23 section headings echoed exactly; T8 = YES
PASS | 4 all 18 questions visible | 18/18 question headings echoed with identical ID, priority and reference
PASS | 5 17-section output contract usable | 17/17 contract section headings produced in order
PASS | 6 claim-ID requirement usable | GEM-05-C001, GEM-05-S01 and the NO SOURCE — LEAD ONLY line present
PASS | 7 quantitative evidence table usable | column list echoed exactly (18 columns) and used in the skeleton header
PASS | 8 no truncation | T7 = NO; trap count echoed ['13'] vs 13
PASS | 9 no instruction loss | all sections, questions and contract sections survived intact
PASS | 10 no research content in reply | no Guinea names or quantities in the reply
SUMMARY: 10/10 PASS
```

### GEM-12 (run 2)

```
PASS | 1 complete prompt accepted | reply completed with the closing line
PASS | 2 PROMPT START / END intact | both boundary lines echoed exactly
PASS | 3 all mission instructions retained | 23/23 section headings echoed exactly; T8 = YES
PASS | 4 all 4 questions visible | 4/4 question headings echoed with identical ID, priority and reference
PASS | 5 17-section output contract usable | 17/17 contract section headings produced in order
PASS | 6 claim-ID requirement usable | GEM-12-C001, GEM-12-S01 and the NO SOURCE — LEAD ONLY line present
PASS | 7 quantitative evidence table usable | column list echoed exactly (18 columns) and used in the skeleton header
PASS | 8 no truncation | T7 = NO; trap count echoed ['11'] vs 11
PASS | 9 no instruction loss | all sections, questions and contract sections survived intact
PASS | 10 no research content in reply | no Guinea names or quantities in the reply
SUMMARY: 10/10 PASS
```

## Run 1 — earlier package text, default model (record only)

| Mission | Prompt SHA-256 | Reply SHA-256 |
|---|---|---|
| GEM-05 | `136b84fd4f30facd…` | `aba033cdb479aade…` |
| GEM-12 | `212c0c6374516816…` | `edd93117c8c59d3f…` |

## Findings

- Both packages were accepted **intact** in both runs. All 23 prompt sections, every question (18 for GEM-05, 4 for GEM-12), the trap count, the 18-column evidence table, the 17-section contract, the claim-ID format and the NO SOURCE — LEAD ONLY convention were reproduced exactly. Gemini reported no truncation and confirmed that all instructions were visible.
- **GEM-05 does not need to be split.**
- **Model pinning is reproducible:** `--model gemini-3.8-flash-high` is honoured, and the model is recorded in the CLI log.

## Caveats

- The Gemini CLI (`gemini`) could not be used: Google refused the account tier ("no longer supported for Gemini Code Assist for individuals … migrate to the Antigravity suite").
- `--mode plan` has no effect alongside `--disable-slash-commands`. Protection came from the sandbox, the empty working directory and the no-tools / no-search instructions. The replies show no tool use and no factual content.
- **Whether `gemini-3.8-flash-high` is the intended execution model is an owner decision (P-030).** If another model is chosen, repeat run 2 with `--model <id>` before any mission is executed.
- In run 1 the checker first mis-parsed the GEM-12 reply (instruction text repeated before the answers). The checker was corrected; Gemini's answers were correct.
