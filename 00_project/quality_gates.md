# Quality Gates

**Version:** 0.1 · **Last updated:** 08-Oct-2026

## Approval model

| Party | Responsibility |
|---|---|
| User + ChatGPT | Approve strategic gates. |
| Claude Code | Performs implementation; self-checks acceptance criteria before requesting approval. |
| Gemini | Independent research (Gate 2) and adversarial review (Gate 8; optionally others). |

**Rules:** No gate is auto-advanced. Claude Code stops at the end of each gate, reports against acceptance criteria and waits for explicit approval. Each approved gate is recorded in `decision_log.md` and `research_status.md`, and snapshotted with a descriptive git tag.

| Gate | Tag |
|---|---|
| 0 | `gate-00-bootstrap` |
| 1 | `gate-01-research-architecture` |
| 2 | `gate-02-discovery` |
| 3 | `gate-03-evidence` |
| 4 | `gate-04-contradiction-gap-audit` |
| 5 | `gate-05-power-system` |
| 6 | `gate-06-geo-resource-demand` |
| 7 | `gate-07-opportunities` |
| 8 | `gate-08-adversarial-review` |
| 9 | `gate-09-reconciliation` |
| 10 | `gate-10-deliverables` |
| 11 | `gate-11-final-qa` |

Tags for Gates 4–11 follow the approved pattern and may be refined when each gate is reached.

---

## GATE 0 — Repository bootstrap

| Item | Definition |
|---|---|
| **Objective** | Establish repository structure and project operating system. |
| **Inputs** | User bootstrap brief. |
| **Expected outputs** | Folder structure; README; `00_project/` documents; `.gitignore`; initial decision log; status tracker. |
| **Acceptance criteria** | All specified folders and files exist; no invented Guinea data; `DATA NOT YET RESEARCHED` used where applicable; no secrets committed; research not started. |
| **Approver** | User + ChatGPT |

## GATE 1 — Research architecture

| Item | Definition |
|---|---|
| **Objective** | Define the detailed research questions, source targets, metric definitions and register schemas for each workstream. |
| **Inputs** | Gate 0 outputs; resolved decisions D-016 to D-022. |
| **Expected outputs** | Per-workstream research question sets and Gemini prompts in `01_gemini_research/00_architecture/`; XLSX register templates; benchmark metric list; source-targeting plan. |
| **Acceptance criteria** | Every workstream has prioritised questions with materiality ratings; XLSX register schemas implement `methodology.md` §3, §4.2 and §6.3; Gemini prompts require source citation. |
| **Approver** | User + ChatGPT |

## GATE 2 — Discovery research

| Item | Definition |
|---|---|
| **Objective** | Gather research leads and sources across all workstreams. |
| **Inputs** | Gate 1 architecture and prompts. |
| **Expected outputs** | Gemini lead documents in `01_gemini_research/<workstream>/` (immutable); Claude independent discovery notes; sources captured in `02_sources/`; draft source register. |
| **Acceptance criteria** | All 20 workstreams have discovery coverage; every cited source is logged; Gemini outputs stored unaltered with date and prompt reference. |
| **Approver** | User + ChatGPT |

## GATE 3 — Evidence consolidation

| Item | Definition |
|---|---|
| **Objective** | Verify material claims and populate the master data register. |
| **Inputs** | Gate 2 leads and sources. |
| **Expected outputs** | Populated master data register and source register with full metadata and confidence categories. |
| **Acceptance criteria** | Every material data point carries all mandatory fields; no Tier 6 item marked above DATA GAP without independent verification; metric and status taxonomies applied. |
| **Approver** | User + ChatGPT |

## GATE 4 — Contradiction and data-gap audit

| Item | Definition |
|---|---|
| **Objective** | Systematically surface, diagnose and record contradictions and gaps. |
| **Inputs** | Gate 3 registers. |
| **Expected outputs** | Contradiction register; data-gap register with materiality and next steps; audit summary. |
| **Acceptance criteria** | All conflicting values recorded with diagnosis and governing-value reasoning; material gaps have mitigation plans; no silent reconciliation. |
| **Approver** | User + ChatGPT |

## GATE 5 — Power-system analysis

| Item | Definition |
|---|---|
| **Objective** | Analyse generation, transmission, distribution, reliability, demand, regulation and WAPP position. |
| **Inputs** | Gate 3–4 registers. |
| **Expected outputs** | Domain analyses in `04_analysis/`; supply-demand balance and related models with documented assumptions. |
| **Acceptance criteria** | Every analytical claim traces to register entries; assumptions sourced and labelled; Alendei lens absent. |
| **Approver** | User + ChatGPT |

## GATE 6 — Geographic / resource / demand analysis

| Item | Definition |
|---|---|
| **Objective** | Spatial analysis of resources (solar, wind, hydro), demand centres, mining and industrial loads, network infrastructure. |
| **Inputs** | Gate 5 outputs; GIS sources. |
| **Expected outputs** | GIS layers in `05_gis/` with provenance metadata; resource and demand maps; spatial findings. |
| **Acceptance criteria** | Every layer has source, date, CRS and licence recorded; technology comparisons evidence-based; no technology presumed. |
| **Approver** | User + ChatGPT |

## GATE 7 — Opportunity development

| Item | Definition |
|---|---|
| **Objective** | Derive, screen and classify opportunities; test Alendei's role. |
| **Inputs** | Gates 5–6 outputs; user-supplied Alendei capability evidence. |
| **Expected outputs** | Candidate and priority opportunity registers; commercial model options; Alendei role assessment; roadmap; due-diligence lists. |
| **Acceptance criteria** | Every opportunity has an evidence chain and a Tier 1–4 classification (`methodology.md` §11); "Tier 4 — Do not pursue now" applied where warranted; no unverified Alendei capability asserted; financial metrics only where evidence supports them. |
| **Approver** | User + ChatGPT |

## GATE 8 — Adversarial review

| Item | Definition |
|---|---|
| **Objective** | Independently challenge findings and opportunities. |
| **Inputs** | Gates 5–7 outputs. |
| **Expected outputs** | Gemini adversarial review; Claude response log (accepted / rejected with reasoning). |
| **Acceptance criteria** | Every challenge addressed; changes logged; residual disagreements disclosed. |
| **Approver** | User + ChatGPT |

## GATE 9 — Final reconciliation

| Item | Definition |
|---|---|
| **Objective** | Lock the evidence base and conclusions for production. |
| **Inputs** | Gate 8 outputs. |
| **Expected outputs** | Frozen registers; reconciled numbers list; final findings and opportunity portfolio. |
| **Acceptance criteria** | All material numbers reconciled or disclosed as contradictions; staleness of policy/tariff data flagged; sign-off list complete. |
| **Approver** | User + ChatGPT |

## GATE 10 — Deliverable production

| Item | Definition |
|---|---|
| **Objective** | Produce PDF report, executive PowerPoint and interactive HTML platform. |
| **Inputs** | Gate 9 frozen evidence base. |
| **Expected outputs** | Drafts and finals in `07_report/`, `08_presentation/`, `09_html/`. |
| **Acceptance criteria** | Every material number traces to a register ID; confidence visibly shown where below CORROBORATED; formal register for senior audience; consistent DD-MMM-YYYY dates and Indian number formatting for INR. |
| **Approver** | User + ChatGPT |

## GATE 11 — Final QA

| Item | Definition |
|---|---|
| **Objective** | Confirm accuracy, traceability, consistency and presentation quality across all deliverables. |
| **Inputs** | Gate 10 deliverables. |
| **Expected outputs** | QA report; number-trace audit; cross-deliverable consistency check; release tag. |
| **Acceptance criteria** | Zero untraceable material numbers; zero inconsistencies across deliverables; no secrets or personal data; release approved. |
| **Approver** | User + ChatGPT |
