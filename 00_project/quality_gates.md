# Quality Gates

**Version:** 1.0 (DRAFT — pending Gate 1 approval) · **Last updated:** 08-Oct-2026

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

## Standing governance check — evidence-data rule (controlled gate transition, D-077)

**Authoritative rule:** no populated evidence data before authorised research execution (Gate 2D).

How the check applies changes at Gate 2B. This is a planned gate transition, not a correction of Gate 1:

| Period | What the check verifies |
|---|---|
| **Before Gate 2B** | No evidence register files exist in `03_evidence/`, `05_gis/` or `06_opportunities/`. |
| **From Gate 2B until Gate 2D authorises research or data entry** | Only the approved empty register templates may exist. They must contain **zero data records** (the Gate 2B requirement). No other evidence data files may exist. |
| **From Gate 2D onwards** | Records may be entered only through the approved protocol, only after the register validator passes (D-075), and initially only with `acceptance_status = PROPOSED`. |

The separate Gate 2B requirement, **"All register templates must contain zero data records"**, remains in force until Gate 2D.

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
| **Objective** | Finalise Research Architecture v1.0: workstream structure and charters, sequencing, Gemini mission structure and handoff protocol, register architecture, contradiction protocol, status framework, scenario architecture, opportunity-screening architecture and GIS architecture — reconciled against the independent Gemini challenge and the owner review. |
| **Inputs** | Gate 0 outputs (D-001 – D-023); Gemini Gate 1 architecture challenge (Tier 6 lead, deposited in `01_gemini_research/00_architecture/`); ChatGPT / project-owner review of 08-Oct-2026. |
| **Expected outputs** | `research_architecture.md` (v1.0); `workstream_charters.md` (28 charters); `gemini_mission_briefs.md` (GEM-01 – GEM-15, approved as architecture only, with mission → workstream coverage matrix); `gate1_gemini_reconciliation.md` (dispositions + Gemini assertions logged as leads); updated methodology, scope, strategy, operating instructions, quality gates, status and decision log; folder structure aligned to the architecture. |
| **Acceptance criteria** | (1) Every workstream has objective, scope, principal questions, datasets, source priorities, dependencies, expected outputs, validation requirements and downstream consumers. (2) Workstream numbering is internally consistent across all governance documents and folders; no stale references to the Gate 0 numbering. (3) Every Gemini mission references valid workstreams. (4) Every Gemini recommendation has a recorded disposition; every Gemini factual assertion is logged as an unverified lead. (5) Register schemas implement `methodology.md` §2–§3, §4.2 and §6.3 (XLSX templates are generated from them when Gate 2 opens). (6) Technology-option coverage complete; no technology promoted or de-emphasised. (7) WS-27/WS-28 separation enforced. (8) No universal thresholds or frozen weights. (9) No Guinea factual research introduced; no register populated. (10) Regional benchmark metric framework defined. (11) Every research question carries a qualitative planning priority (CRITICAL / HIGH / MEDIUM / LOW) per `methodology.md` §12; no numerical materiality scores. (12) Mission → workstream coverage matrix shows a primary mission for every discovery workstream (WS-01 – WS-26), with the WS-27/WS-28 exception documented. |
| **Approver** | User + ChatGPT |

## GATE 2 — Discovery research

| Item | Definition |
|---|---|
| **Objective** | Gather research leads and candidate sources across all 26 Phase A workstreams (WS-01 – WS-26). |
| **Inputs** | Approved Gate 1 architecture; mission briefs; Research Execution Protocol (2A); XLSX register templates (2B); approved mission packages (2C). |
| **Expected outputs** | Gemini mission outputs in `01_gemini_research/GEM-NN_<slug>/` (immutable, with `.meta.md` sidecars incl. SHA-256); Claude independent discovery covering every Phase A workstream (including gaps not covered by the initial mission batch); lead register; draft source register; mission close reports; proposals for follow-up missions where warranted. |
| **Acceptance criteria** | All 26 Phase A workstreams have discovery coverage; every cited source is logged (unlocatable Gemini citations flagged); all GL-01 – GL-33 leads transferred to the lead register; Gemini outputs stored unaltered with date and prompt reference; no lead used in analysis. |
| **Approver** | User + ChatGPT |

### Gate 2 sub-gates (D-055)

Gate 2 is executed as four sequential sub-gates, each separately approved by User + ChatGPT. Detail: `research_execution_protocol.md` §0.

| Sub-gate | Objective | Expected outputs | Acceptance criteria |
|---|---|---|---|
| **2A — Research Execution Protocol** | Define mission execution, capture, verification, reconciliation, challenge and acceptance | `research_execution_protocol.md`; pointer updates; Gate 2A pending decisions | Consistent with Gate 1 architecture; no research, registers or data; pending decisions documented |
| **2B — Register templates** | Create empty XLSX templates from approved schemas incl. 2A decisions | Empty templates for the 11 logical registers (Entity/Site as two physical sheets; D-076): headers, enumerations, validation only; `register_schema.md`; generator | Schemas match `methodology.md` §3, §4.2, §6.3 and `research_architecture.md` §G; **all register templates contain zero data records** |
| **2C — Mission packages** | Compile and validate executable packages for GEM-01 – GEM-15; design and build the register validator (D-075) | Archived packages (instructions + brief + output contract + prompt version) in `01_gemini_research/00_architecture/`; register validator (CLI or equivalent) | Each package maps to valid WS/questions; contract per protocol §12; validator checks the D-075 capability list against the empty templates; no execution |
| **2D — Research execution authorisation** | Authorise mission execution and Claude independent discovery (by wave); accept discovery outputs | Raw artifacts with sidecars; lead and source registrations; Mission Reconciliation Reports | **Prerequisite: approved register validator in place and passing (D-075)**; protocol §15 acceptance criteria per mission; Gate 2 acceptance criteria above |

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
| **Expected outputs** | Contradiction register; data-gap register with materiality and next steps; reassessment of research-question priorities against actual evidence gaps and decision impact (`methodology.md` §12), with changes logged; audit summary. |
| **Acceptance criteria** | All conflicting values recorded with diagnosis and the reasoning for any governing value or carried range (`research_architecture.md` §H); material gaps have mitigation plans; research-question priorities reassessed against evidence and changes logged; no silent reconciliation. |
| **Approver** | User + ChatGPT |

## GATE 5 — Power-system analysis

| Item | Definition |
|---|---|
| **Objective** | Analyse the country context and power system: WS-01 – WS-09, WS-15 (legal context), WS-16, WS-17 and WS-23. |
| **Inputs** | Gate 3–4 registers. |
| **Expected outputs** | Workstream analyses in `04_analysis/wsNN_*`; capacity cascade (installed → available → dependable → dispatched) with seasonal hydro dependable capacity; counterparty assessment; interconnection status; project register with evidenced status; model platform decision (P-010). |
| **Acceptance criteria** | Every analytical claim traces to register entries; inferences labelled; seasonal dependable capacity stated for every hydro plant; status framework applied strictly; assumptions in the assumption register; no presumption about utility condition, FX structures or basin relevance; Alendei lens absent. |
| **Approver** | User + ChatGPT |

## GATE 6 — Geographic / resource / demand analysis

| Item | Definition |
|---|---|
| **Objective** | Demand (WS-10 – WS-14, WS-22), technology resources (WS-18 – WS-21), land/environment constraints (WS-26), finance and ecosystem mapping (WS-24, WS-25), GIS integration and the integrated scenario model. |
| **Inputs** | Gate 5 outputs; GIS sources; registers. |
| **Expected outputs** | GIS layers (opportunity and constraint) with catalogue entries; resource and demand analyses; site-level mining/industrial demand; scenario model and seasonal supply–demand balance for 2027–2030 and 2030–2035 (`research_architecture.md` §J); finance-instrument and entity registers. |
| **Acceptance criteria** | Every layer has source, date, CRS and licence recorded; constraints stored with attributes, no universal thresholds; technology assessments on equal footing; linear extrapolation not the sole method; scenario inclusion follows lifecycle-stage rules; entity presence classifications evidenced; Alendei lens absent. |
| **Approver** | User + ChatGPT |

## GATE 7 — Opportunity development

| Item | Definition |
|---|---|
| **Objective** | Part 1 — WS-27: derive, screen and rate country opportunities (Alendei-neutral). Part 2 — WS-28: assess Alendei participation and classify each opportunity Tier 1–4. |
| **Inputs** | Gates 5–6 outputs; user-supplied Alendei capability evidence (Part 2 only). |
| **Expected outputs** | Part 1: candidate opportunity register, fatal-flaw results, scoring with weight-sensitivity analysis, approved weights, attractiveness ratings (frozen), commercial-model notes. Part 2: Alendei participation register, Tier 1–4 classifications, roadmap, due-diligence lists. |
| **Acceptance criteria** | Every opportunity has an evidence chain; weights approved only after sensitivity testing; evidence confidence shown alongside scores; no commercial model predetermined; **WS-27 ratings frozen and recorded before Part 2 starts, and unchanged by Part 2**; Tier 1–4 classification per `methodology.md` §11 with "Tier 4 — Do not pursue now" applied where warranted; no unverified Alendei capability asserted; financial metrics only where evidence supports them. |
| **Approver** | User + ChatGPT (Part 1 freeze approved before Part 2 begins) |

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
