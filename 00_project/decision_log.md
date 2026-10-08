# Decision Log

**Version:** 1.0 (DRAFT — Gate 1 entries pending approval) · **Last updated:** 08-Oct-2026

Decisions recorded here are **project governance decisions**. They are not research findings. No entry in this log constitutes evidence about Guinea's energy sector.

Status values: `ACTIVE` · `PROPOSED` (Claude Code design choice awaiting approval) · `PENDING` · `SUPERSEDED` · `REVOKED`

---

## INITIAL PROJECT DECISIONS

| Decision ID | Date | Decision | Reason | Evidence | Owner | Status |
|---|---|---|---|---|---|---|
| D-001 | 08-Oct-2026 | Project name is "Guinea Energy Intelligence 2026". | Sponsor instruction. | User bootstrap brief | User | ACTIVE |
| D-002 | 08-Oct-2026 | Project is a durable, gated research asset, not a one-shot report. | Sponsor instruction. | User bootstrap brief | User | ACTIVE |
| D-003 | 08-Oct-2026 | Research periods: Historical 2016–2026; Near-term 2027–2030; Strategic 2030–2035. | Sponsor instruction. | User bootstrap brief | User | ACTIVE |
| D-004 | 08-Oct-2026 | Geographic scope: all of Guinea plus a minimum benchmark universe of Senegal, Mali, Côte d'Ivoire, Sierra Leone, Liberia, Guinea-Bissau, Ghana; additions require justification and a log entry. | Sponsor instruction. | User bootstrap brief | User | ACTIVE |
| D-005 | 08-Oct-2026 | Twenty research workstreams established (see `master_scope.md` §4). | Sponsor instruction. | User bootstrap brief | User | SUPERSEDED by D-041 (pending Gate 1 approval) |
| D-006 | 08-Oct-2026 | Twelve quality gates (Gate 0 – Gate 11) govern progression; no gate is skipped or auto-advanced. | Sponsor instruction. | User bootstrap brief | User | ACTIVE |
| D-007 | 08-Oct-2026 | Role model: User + ChatGPT approve strategic gates; Claude Code implements; Gemini performs independent research and adversarial review. | Sponsor instruction. | User bootstrap brief | User | ACTIVE |
| D-008 | 08-Oct-2026 | Gemini research is treated as an unverified lead (Tier 6), never as evidence. | Sponsor instruction; mitigates AI-generated error risk. | User bootstrap brief | User | ACTIVE |
| D-009 | 08-Oct-2026 | Confidence categories: VERIFIED, CORROBORATED, ESTIMATED, INDICATIVE, DATA GAP. | Sponsor instruction. | User bootstrap brief | User | ACTIVE |
| D-010 | 08-Oct-2026 | Independent Guinea system analysis (Gates 1–6) precedes and is separated from Alendei opportunity analysis (Gate 7 onward). | Sponsor instruction; objectivity. | User bootstrap brief | User | ACTIVE |
| D-011 | 08-Oct-2026 | Alendei positioning hypothesis: "strategic energy-development and ecosystem-integration partner". Hypothesis only; not a finding. | Sponsor instruction. | User bootstrap brief | User | ACTIVE (hypothesis) |
| D-012 | 08-Oct-2026 | "Do not pursue now" is a valid and mandatory opportunity classification. | Sponsor instruction. | User bootstrap brief | User | ACTIVE |
| D-013 | 08-Oct-2026 | Final deliverables: PDF report, executive PowerPoint, interactive HTML intelligence platform. | Sponsor instruction. | User bootstrap brief | User | ACTIVE |
| D-014 | 08-Oct-2026 | The following are explicitly deferred to evidence: best technology, geography, project, investment size, economics, tariff, IRR, NPV, DSCR, land requirement, final Alendei opportunity, partner, OEM, financing structure. | Sponsor instruction; avoids premature conclusions. | User bootstrap brief | User | ACTIVE |
| D-015 | 08-Oct-2026 | Raw research files (`01_gemini_research/`, original documents in `02_sources/`) are immutable once deposited. | Sponsor instruction; audit trail. | User bootstrap brief | User | ACTIVE |
| D-016 | 08-Oct-2026 | Git convention: `develop` = active development; `main` = approved/stable; descriptive gate tags = approved milestone snapshots (`gate-00-bootstrap`, `gate-01-research-architecture`, `gate-02-discovery`, `gate-03-evidence`, …). | Proposed by Claude Code; approved at Gate 0 review. | Gate 0 review instruction | User | ACTIVE |
| D-017 | 08-Oct-2026 | Source folder renamed from `02_sources/ireana/` to `02_sources/irena/` (International Renewable Energy Agency). | Correction of a typo in the folder name. | Gate 0 review instruction (resolves P-001) | User | ACTIVE |
| D-018 | 08-Oct-2026 | XLSX is the master working format for the human-facing evidence, data, source and opportunity registers. CSV/JSON may be added later as machine-readable derivatives (HTML platform, analytics). No duplicate register files until needed. | Usability for human reviewers; derivatives serve machine workflows. | Gate 0 review instruction (resolves P-002) | User | ACTIVE |
| D-019 | 08-Oct-2026 | Copyrighted third-party documents are not committed automatically. The source register preserves source ID, title, publisher, publication date, URL, access date, document type, relevant pages/sections, evidence extracted, access/copyright note and local-copy status. Licensed, public-domain, publicly redistributable government or otherwise shareable documents may be stored where appropriate. | Copyright compliance with full traceability. | Gate 0 review instruction (resolves P-005); `methodology.md` §4.2 | User | ACTIVE |
| D-020 | 08-Oct-2026 | Opportunity classification: Tier 1 — Pursue immediately; Tier 2 — Develop; Tier 3 — Monitor; Tier 4 — Do not pursue now. | Project-approved classification. | Gate 0 review instruction (resolves P-003); `methodology.md` §11 | User | ACTIVE |
| D-021 | 08-Oct-2026 | Initially, the project operator deposits Gemini research outputs manually into `01_gemini_research/`. Raw Gemini outputs are immutable after deposit. | Controlled intake and audit trail. | Gate 0 review instruction (resolves P-006) | User | ACTIVE |
| D-022 | 08-Oct-2026 | Project status is assigned from evidence of progress and commitment, not from a fixed time threshold. Lifecycle stage (Proposed, Announced, Active development, Financially committed, Under construction, Operational, Cancelled) is recorded separately from progress condition (On track, Delayed, Stalled, Unverified). | An arbitrary month threshold misclassifies projects; evidence-based status is more defensible. | Gate 0 review instruction (resolves P-004); `methodology.md` §6 | User | ACTIVE |
| D-023 | 08-Oct-2026 | Gate 0 (Repository bootstrap) approved, subject to the corrections recorded in D-016 to D-022. | Gate 0 review completed. | Gate 0 review instruction | User + ChatGPT | ACTIVE |

## GATE 1 DECISIONS — RESEARCH ARCHITECTURE

Entries D-024 – D-040 record directives from the ChatGPT / project-owner review of 08-Oct-2026 (ACTIVE on that authority). Entries D-041 – D-050 are Claude Code implementation choices (PROPOSED until Gate 1 approval). None of these entries is a research finding.

| Decision ID | Date | Decision | Reason | Evidence | Owner | Status |
|---|---|---|---|---|---|---|
| D-024 | 08-Oct-2026 | Gemini Gate 1 architecture challenge accepted as an input; deposited verbatim at `01_gemini_research/00_architecture/2026-10-08_GATE1_architecture-challenge_gemini_v1.md` with SHA-256 sidecar; treated as Tier 6 lead. All Gemini factual assertions logged as unverified leads GL-01 – GL-33. | Independent challenge of the architecture; evidence discipline. | Gemini file; `gate1_gemini_reconciliation.md` | User (deposit by Claude Code at operator's instruction) | ACTIVE |
| D-025 | 08-Oct-2026 | Expand toward Gemini's 27-workstream architecture; add/strengthen fuel logistics & landed fuel economics, macro-financial/FX/repatriation, utility economics & counterparty/bankability, dedicated Simandou & corridor research, mining/industrial segmentation, decentralised energy/mini-grids, land/resettlement/environment/biodiversity, transboundary basin governance & hydrology, explicit seasonal hydro dependable capacity. | Owner review items 1–2. | Owner review | User + ChatGPT | ACTIVE |
| D-026 | 08-Oct-2026 | Gemini findings are hypotheses/leads until primary evidence is verified. Do NOT assume: EDG financial distress; offshore escrow requirement; OMVG/OMVS/ABN relevance; universal GIS slope threshold (e.g. >10%); a 200–400 MW alumina load; wind unattractiveness; the 25/20/20/20/15 weights; mining B2B as the preferred commercial model. | Owner review item 3. | Owner review | User + ChatGPT | ACTIVE |
| D-027 | 08-Oct-2026 | Explicit technology neutrality: solar, wind, hydro, BESS, thermal, hybrids, grid reinforcement, demand-side measures, mini-grids and other justified solutions assessed on evidence; none promoted or de-emphasised in advance. | Owner review item 4. | Owner review | User + ChatGPT | ACTIVE |
| D-028 | 08-Oct-2026 | Separate WS-27 (Commercial Opportunity Portfolio & Structuring — "what is attractive for Guinea?") from WS-28 (Alendei Strategic Participation & Ecosystem Role — "where can Alendei participate?"); Alendei fit must not distort the country ranking. | Owner review item 5. | Owner review | User + ChatGPT | ACTIVE |
| D-029 | 08-Oct-2026 | Preliminary multi-criteria screening framework with the owner-listed dimensions; Alendei fit as a separate secondary lens; final weights NOT frozen at Gate 1 — validated later with sufficient evidence. | Owner review item 6. | Owner review | User + ChatGPT | ACTIVE |
| D-030 | 08-Oct-2026 | Two-dimensional project-status framework (D-022) retained; "stalled" never inferred from absence of news. | Owner review item 7. | Owner review | User + ChatGPT | ACTIVE |
| D-031 | 08-Oct-2026 | Linear demand extrapolation not to be the sole forecasting method; scenario architecture covering mining, industrial, processing/refining, urban/commercial, electrification, infrastructure, hydro seasonality, WAPP trade, committed additions and distributed/captive generation; matrix structure kept flexible until baseline evidence exists. | Owner review item 8. | Owner review | User + ChatGPT | ACTIVE |
| D-032 | 08-Oct-2026 | Strict evidence-state distinctions: raw lead, candidate source, extracted, verified, corroborated, estimate, analytical inference, unresolved contradiction, data gap; no material statistic in the master register without traceability. | Owner review item 9. | Owner review; `methodology.md` §2.2 | User + ChatGPT | ACTIVE |
| D-033 | 08-Oct-2026 | Per-claim source validation fields: original source, exact title, publisher, publication date, URL, access date, page/table/section, tier, confidence, cross-check, contradiction status. | Owner review item 10. | Owner review; `methodology.md` §3 | User + ChatGPT | ACTIVE |
| D-034 | 08-Oct-2026 | Gemini's eight missions (GEM-01 – GEM-08) approved as an INITIAL discovery batch only; additional targeted missions may be created as evidence reveals unresolved questions. | Owner review item 12. | Owner review | User + ChatGPT | ACTIVE |
| D-035 | 08-Oct-2026 | India, China, Europe, Middle East, USA, Japan/Korea and OEM/EPC/IPP research consolidated into one International Ecosystem workstream with origin registers and five Guinea-presence classes. | Owner review item 13. | Owner review | User + ChatGPT | ACTIVE |
| D-036 | 08-Oct-2026 | Commodity/site-specific mining and industrial analysis distinguishing bauxite extraction, alumina refining, gold, iron ore/Simandou, diamonds, other strategic minerals, non-mining industrial, ports & logistics, commercial/urban demand; company/site/project-level data where possible. | Owner review item 14. | Owner review | User + ChatGPT | ACTIVE |
| D-037 | 08-Oct-2026 | Transboundary basin institutions and agreements to be investigated without presuming relevance; hydro analysis to model seasonal dependable output explicitly. | Owner review item 15. | Owner review | User + ChatGPT | ACTIVE |
| D-038 | 08-Oct-2026 | GIS to include opportunity and exclusion/constraint layers; no universal project thresholds at Gate 1 unless evidence or engineering standards justify them. | Owner review item 16. | Owner review | User + ChatGPT | ACTIVE |
| D-039 | 08-Oct-2026 | Research DFIs, sovereign lending, guarantees, political-risk instruments, EXIM/LOC, bilateral, project, blended, PPP finance and technical assistance; no financing structure assumed before instruments and eligibility are researched. | Owner review item 17. | Owner review | User + ChatGPT | ACTIVE |
| D-040 | 08-Oct-2026 | Confidence framework strengthened with quality dimensions (source quality, recency, cross-source agreement, methodological quality, completeness, definition consistency); a high-confidence estimate is never presented as verified fact. | Owner review item 18. | Owner review; `methodology.md` §2.1 | User + ChatGPT | ACTIVE |
| D-041 | 08-Oct-2026 | Final architecture: **28 workstreams** (WS-01 – WS-28) in seven clusters, with charters in `workstream_charters.md`; supersedes D-005. Gemini's 27 re-scoped to remove overlap; Gemini WS-27 split into WS-27/WS-28. | Owner review items 1, 5, 11. | `workstream_charters.md`; `gate1_gemini_reconciliation.md` §1 | Claude Code (proposed) | PROPOSED |
| D-042 | 08-Oct-2026 | `01_gemini_research/` reorganised by mission (`GEM-NN_<slug>/`) rather than by workstream; the 20 empty Gate 0 workstream folders removed; `00_architecture/` retained. | Missions span multiple workstreams; avoids arbitrary placement or duplication. | `research_architecture.md` §A.3 | Claude Code (proposed) | PROPOSED |
| D-043 | 08-Oct-2026 | `04_analysis/` reorganised into `ws01_…` – `ws26_…` plus `00_integrated_models/`; the 17 empty Gate 0 domain folders removed (`climate` absorbed into WS-17/WS-26). | Traceability between workstreams and analysis. | `research_architecture.md` §A.3 | Claude Code (proposed) | PROPOSED |
| D-044 | 08-Oct-2026 | `05_gis/` gains `constraints/`, `logistics/`, `hydrology/`; `03_evidence/` gains `lead_register/`, `project_register/`, `entity_register/`, `assumption_register/`. | Owner review items 9, 14, 16; register architecture. | `research_architecture.md` §G, §L | Claude Code (proposed) | PROPOSED |
| D-045 | 08-Oct-2026 | [Superseded by D-053] Register architecture of 11 separate XLSX workbooks (source, lead, master data, contradiction, data gap, project, entity/site, assumption, GIS catalogue, opportunity, Alendei participation) with defined ID formats. | D-018; owner review items 9–10. | `research_architecture.md` §G | Claude Code (proposed) | SUPERSEDED by D-053 |
| D-046 | 08-Oct-2026 | Contradiction protocol with outcomes RESOLVED-DEFINITIONAL / RESOLVED-HIERARCHY / RESOLVED-ERROR / RANGE-CARRIED / OPEN; RANGE-CARRIED adopted from Gemini's "analytical envelope" proposal, applied after the evidence hierarchy. | Never silently reconcile; preserve uncertainty. | `research_architecture.md` §H | Claude Code (proposed) | PROPOSED |
| D-047 | 08-Oct-2026 | Scenario inclusion rules by lifecycle stage (operational/under construction in all scenarios; financially committed central+; active development high only; announced/proposed sensitivity only; stalled excluded from central). | Links forecasts to evidence of commitment. | `research_architecture.md` §J.2 | Claude Code (proposed; confirm at Gate 6) | PROPOSED |
| D-048 | 08-Oct-2026 | Recency handled as a quality dimension, with mandatory Gate 9 re-verification of volatile data classes (tariffs, laws/regulations, mandates, FX rules, project status, ownership); Gemini's fixed 24-month expiry not adopted. | Consistent with rejecting arbitrary time thresholds (cf. D-022). | `methodology.md` §2.1 | Claude Code (proposed) | PROPOSED |
| D-049 | 08-Oct-2026 | Research sequencing in eight stages mapped to gates (`research_architecture.md` §D); Gate 5/6/7 scopes updated accordingly (WS-24/WS-25 analysed at Gate 6; Gate 7 split into WS-27 then WS-28 with an approved freeze between). | Dependency order; owner review item 5. | `research_architecture.md` §D; `quality_gates.md` | Claude Code (proposed) | PROPOSED |
| D-050 | 08-Oct-2026 | Gemini mission titles neutralised where wording presumed conclusions (GEM-02, GEM-04, GEM-05, GEM-06); missions deposit into mission folders; mission output template defined. | Owner review item 3. | `gate1_gemini_reconciliation.md` §5; `gemini_mission_briefs.md` | Claude Code (proposed) | PROPOSED |

### Gate 1 correction pass — owner directives (08-Oct-2026)

| Decision ID | Date | Decision | Reason | Evidence | Owner | Status |
|---|---|---|---|---|---|---|
| D-051 | 08-Oct-2026 | Follow-up missions GEM-09 – GEM-15 accepted as part of the research architecture: macro, political economy, currency & FX (GEM-09); electricity law, regulation & investment framework (GEM-10); electricity demand, cities, industry & structural load (GEM-11); Simandou energy & infrastructure corridor (GEM-12); resource, climate & site constraints (GEM-13); existing/committed/planned project pipeline (GEM-14); land, environment, community & resettlement (GEM-15). **Approved as architecture only; execution requires separate Gate 2 authorisation.** Primary assignments revised so every discovery workstream (WS-01 – WS-26) has a primary mission; WS-27/WS-28 have none by design. | Close coverage gaps of the initial batch. | Owner correction instruction; `gemini_mission_briefs.md` §1, §3 | User + ChatGPT | ACTIVE |
| D-052 | 08-Oct-2026 | Every research question carries a qualitative architectural research priority (CRITICAL / HIGH / MEDIUM / LOW). Priority is a planning classification only — not evidence confidence, not a finding about Guinea; revisable after evidence review; reassessed at Gate 4. No numerical materiality scores before evidence. | Retain prioritisation without false precision. | Owner correction instruction; `methodology.md` §12 | User + ChatGPT | ACTIVE |
| D-053 | 08-Oct-2026 | Register architecture confirmed with single-source-of-truth rules: XLSX authoritative; CSV/JSON generated derivatives only; no manually maintained duplicates; every material quantitative value stored only in the Master Data Register and referenced elsewhere by `DAT-` ID; each register has a defined maintainer/authority, ID convention, purpose and MDR relationship; no data at Gate 1. Eleven registers retained after duplication review (supersedes the register list in D-045). | Owner correction instruction; avoid competing sources of truth. | `research_architecture.md` §G | User + ChatGPT (structure proposed by Claude Code) | ACTIVE (subject to Gate 1 approval) |
| D-054 | 08-Oct-2026 | The deposited Gemini Gate 1 challenge is accepted as an immutable operator-provided source artifact: original preserved unchanged; SHA-256 retained; not evidence; its claims remain leads until independently sourced and validated; its presence does not constitute research completion. | Owner correction instruction. | `.meta.md` sidecar; `research_architecture.md` §F | User + ChatGPT | ACTIVE |

## PENDING DECISIONS (require user / ChatGPT input)

| Decision ID | Date raised | Question | Raised by | Status |
|---|---|---|---|---|
| P-001 | 08-Oct-2026 | Rename `02_sources/ireana/` to `irena/`? | Claude Code | RESOLVED → D-017 |
| P-002 | 08-Oct-2026 | Register file format. | Claude Code | RESOLVED → D-018 |
| P-003 | 08-Oct-2026 | Opportunity classification taxonomy. | Claude Code | RESOLVED → D-020 |
| P-004 | 08-Oct-2026 | Definition of "Stalled". | Claude Code | RESOLVED → D-022 |
| P-005 | 08-Oct-2026 | Handling of copyrighted source documents. | Claude Code | RESOLVED → D-019 |
| P-006 | 08-Oct-2026 | Mechanism for depositing Gemini outputs. | Claude Code | RESOLVED → D-021 |

| P-007 | 08-Oct-2026 | Approve Research Architecture v1.0 (as corrected by D-051 – D-054) and Gate 1 PROPOSED decisions D-041 – D-050. | Claude Code | PENDING |
| P-008 | 08-Oct-2026 | Approve, amend or reject proposed follow-up missions GEM-09 – GEM-15 (coverage gaps in the initial batch). | Claude Code | RESOLVED → D-051 |
| P-009 | 08-Oct-2026 | Confirm that XLSX register templates are generated when Gate 2 opens (not at Gate 1). | Claude Code | PENDING |
| P-010 | 08-Oct-2026 | Modelling platform for the integrated scenario model (Python, XLSX or both) — to be decided at Gate 5. | Claude Code | PENDING (Gate 5) |
| P-011 | 08-Oct-2026 | WS-27 Alendei-neutral attractiveness labels (proposed: Highly attractive / Attractive / Conditionally attractive / Not currently attractive) and the proposed rule that Alendei Tier 1–2 requires at least "Conditionally attractive". | Claude Code | PENDING (confirm by Gate 7) |
| P-012 | 08-Oct-2026 | GIS storage: GeoPackage master + GeoJSON derivatives; handling of large rasters (Git LFS vs kept outside git). | Claude Code | PENDING (Gate 6) |

---

## Change history

| Date | Change | By |
|---|---|---|
| 08-Oct-2026 | Log initialised at Gate 0. | Claude Code |
| 08-Oct-2026 | Gate 0 review: D-016 approved; D-017 to D-023 added; P-001 to P-006 resolved. | Claude Code (per user instruction) |
| 08-Oct-2026 | Gate 1 reconciliation: D-024 – D-040 (owner directives) and D-041 – D-050 (proposed) added; D-005 superseded; P-007 – P-012 raised. | Claude Code (per user instruction) |
| 08-Oct-2026 | Gate 1 correction pass: D-051 – D-054 added; P-008 resolved; D-045 register list superseded by D-053. | Claude Code (per user instruction) |
