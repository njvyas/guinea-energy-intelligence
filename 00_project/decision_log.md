# Decision Log

**Version:** 0.1 · **Last updated:** 08-Oct-2026

Decisions recorded here are **project governance decisions**. They are not research findings. No entry in this log constitutes evidence about Guinea's energy sector.

Status values: `ACTIVE` · `PENDING` · `SUPERSEDED` · `REVOKED`

---

## INITIAL PROJECT DECISIONS

| Decision ID | Date | Decision | Reason | Evidence | Owner | Status |
|---|---|---|---|---|---|---|
| D-001 | 08-Oct-2026 | Project name is "Guinea Energy Intelligence 2026". | Sponsor instruction. | User bootstrap brief | User | ACTIVE |
| D-002 | 08-Oct-2026 | Project is a durable, gated research asset, not a one-shot report. | Sponsor instruction. | User bootstrap brief | User | ACTIVE |
| D-003 | 08-Oct-2026 | Research periods: Historical 2016–2026; Near-term 2027–2030; Strategic 2030–2035. | Sponsor instruction. | User bootstrap brief | User | ACTIVE |
| D-004 | 08-Oct-2026 | Geographic scope: all of Guinea plus a minimum benchmark universe of Senegal, Mali, Côte d'Ivoire, Sierra Leone, Liberia, Guinea-Bissau, Ghana; additions require justification and a log entry. | Sponsor instruction. | User bootstrap brief | User | ACTIVE |
| D-005 | 08-Oct-2026 | Twenty research workstreams established (see `master_scope.md` §4). | Sponsor instruction. | User bootstrap brief | User | ACTIVE |
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

## PENDING DECISIONS (require user / ChatGPT input)

| Decision ID | Date raised | Question | Raised by | Status |
|---|---|---|---|---|
| P-001 | 08-Oct-2026 | Rename `02_sources/ireana/` to `irena/`? | Claude Code | RESOLVED → D-017 |
| P-002 | 08-Oct-2026 | Register file format. | Claude Code | RESOLVED → D-018 |
| P-003 | 08-Oct-2026 | Opportunity classification taxonomy. | Claude Code | RESOLVED → D-020 |
| P-004 | 08-Oct-2026 | Definition of "Stalled". | Claude Code | RESOLVED → D-022 |
| P-005 | 08-Oct-2026 | Handling of copyrighted source documents. | Claude Code | RESOLVED → D-019 |
| P-006 | 08-Oct-2026 | Mechanism for depositing Gemini outputs. | Claude Code | RESOLVED → D-021 |

No decisions are currently pending.

---

## Change history

| Date | Change | By |
|---|---|---|
| 08-Oct-2026 | Log initialised at Gate 0. | Claude Code |
| 08-Oct-2026 | Gate 0 review: D-016 approved; D-017 to D-023 added; P-001 to P-006 resolved. | Claude Code (per user instruction) |
