# Guinea Energy Intelligence 2026

**Owner:** Alendei Group (Alendei Green RE Pvt. Ltd.)
**Repository status:** see `00_project/research_status.md` (current gate and status)
**Classification:** Internal strategic research. Not for external distribution without approval.

---

## 1. Purpose

This repository is a durable, evidence-led research and intelligence asset on the electricity sector of the Republic of Guinea, set in its West African Power Pool (WAPP) regional context. It exists to:

1. Build an objective, independently verifiable understanding of Guinea's power system — institutions, generation, transmission, distribution, reliability, demand, mining and industrial loads, regional interconnection and resource potential.
2. Identify, test and rank potential energy-development opportunities **only after** that independent analysis is complete.
3. Evaluate whether, where and how Alendei could participate, under the working hypothesis that Alendei is a *strategic energy-development and ecosystem-integration partner* rather than solely a solar EPC contractor. This hypothesis is unvalidated.

It is not a one-shot report. It is built incrementally through explicit, approved quality gates.

## 2. Objectives

| # | Objective |
|---|-----------|
| O1 | Establish a verified, sourced baseline of Guinea's power system (historical period 2016–2026). |
| O2 | Characterise the near-term (2027–2030) and strategic (2030–2035) outlook, distinguishing confirmed from speculative developments. |
| O3 | Benchmark Guinea against relevant WAPP / neighbouring countries. |
| O4 | Map the international, DFI, OEM, EPC and IPP ecosystem active in or relevant to Guinea. |
| O5 | Record every material contradiction and data gap explicitly. |
| O6 | Develop an evidence-chained opportunity register, including "Do not pursue now" classifications. |
| O7 | Produce three final deliverables that contain no unsupported material numbers. |

## 3. Final deliverables

| Deliverable | Location | Status |
|---|---|---|
| Final PDF report | `07_report/final/` | NOT STARTED |
| Executive PowerPoint | `08_presentation/final/` | NOT STARTED |
| Interactive HTML intelligence platform | `09_html/final/` | NOT STARTED |

Supporting assets (source register, evidence register, contradiction register, data-gap register, analytical models, GIS data, opportunity register) are deliverables in their own right.

## 4. Folder structure

```
00_project/            Project operating system: scope, strategy, methodology, gates, decisions, status, agent instructions
01_gemini_research/    Raw Gemini outputs, by mission (GEM-NN_*) plus 00_architecture/ (UNVERIFIED LEADS — never edited after deposit)
02_sources/            Source documents and source notes, grouped by publisher / origin
03_evidence/           Source, lead, master data, project, entity, assumption, contradiction and data-gap registers
04_analysis/           Analysis by workstream (ws01_* – ws26_*) and integrated models (00_integrated_models/)
05_gis/                Geospatial opportunity, resource, infrastructure and constraint layers
06_opportunities/      WS-27 country opportunity portfolio; WS-28 Alendei participation, roadmap, due diligence
07_report/             PDF report drafts, figures, tables, final
08_presentation/       Executive deck drafts, figures, final
09_html/               Interactive platform source, data, assets, maps, build, final
```

## 5. Research workflow

```
Research architecture (Gate 1)
      │
      ▼
Discovery research — Gemini leads + Claude independent verification (Gate 2)
      │
      ▼
Evidence consolidation into registers (Gate 3)
      │
      ▼
Contradiction & data-gap audit (Gate 4)
      │
      ▼
Power-system analysis (Gate 5) → Geographic / resource / demand analysis (Gate 6)
      │
      ▼
Opportunity development — WS-27 country portfolio (Alendei-neutral, frozen) → WS-28 Alendei participation (Gate 7)
      │
      ▼
Adversarial review (Gate 8) → Final reconciliation (Gate 9)
      │
      ▼
Deliverable production (Gate 10) → Final QA (Gate 11)
```

Full gate definitions: `00_project/quality_gates.md`. Research architecture (28 workstreams, sequencing, missions, registers, protocols, scenarios, screening, GIS): `00_project/research_architecture.md` and `00_project/workstream_charters.md`. Research execution (mission lifecycle, verification, reconciliation, acceptance): `00_project/research_execution_protocol.md`. Register schema and data dictionary: `00_project/register_schema.md`. Executable Gemini mission packages: `01_gemini_research/00_architecture/mission_packages/`.

## 6. Roles

| Party | Role |
|---|---|
| **User (Alendei)** | Project sponsor and final authority. Sets scope, approves strategic gates, supplies any Alendei-internal facts (capabilities, partnerships, licences), decides on opportunities. |
| **ChatGPT** | Strategic co-reviewer. Co-approves strategic gates with the user, challenges framing, reviews structure and conclusions. |
| **Gemini** | Independent discovery researcher and adversarial reviewer. Produces research leads through defined missions; later attacks draft findings. Output is never treated as evidence on its own. |
| **Claude Code** | Primary engineering, research-verification and project agent. Maintains the repository, verifies claims against primary sources, populates registers, builds analysis, models, GIS layers and deliverables, and keeps status and decision logs current. |

Agent-specific instructions: `00_project/claude_operating_instructions.md`, `00_project/gemini_operating_instructions.md`.

## 7. Evidence hierarchy

From most to least authoritative:

1. **Tier 1 — Guinea government / primary institutional:** laws, decrees, official gazette, ministry, regulator, utility and system-operator publications.
2. **Tier 2 — WAPP / ECOWAS / regional institutional:** WAPP, ECOWAS, regional regulator, interconnector operators, river-basin organisations.
3. **Tier 3 — World Bank / IFC / AfDB / EIB / IMF / UN / other DFIs.**
4. **Tier 4 — Data institutions, science and engineering:** IRENA, IEA, Global Energy Monitor, Ember, NREL, Global Solar/Wind Atlas, NASA, NOAA, Copernicus, scientific literature, engineering studies.
5. **Tier 5 — Corporate and project disclosures:** OEM/EPC/IPP/mining-company disclosures, investor presentations, project-finance disclosures, tenders, corporate statutory filings (issuer's own disclosed facts only). Media and trade press are secondary reporting/discovery sources, not an evidence tier; they never independently establish a material quantitative or legal claim (D-086).
6. **Tier 6 — AI-generated or otherwise unsourced material:** LEAD ONLY, **never evidence**.

A lower-tier source can corroborate but cannot override a higher-tier source without a recorded contradiction entry and reasoning.

## 8. Non-negotiable rules

1. **Raw research must never be overwritten.** Files deposited in `01_gemini_research/` and original documents in `02_sources/` are immutable. Corrections, annotations and verifications are written to new files or registers.
2. **Gemini research is an unverified research lead.** No Gemini claim enters an evidence register or deliverable until independently verified against a Tier 1–5 source (Tier 5 only for the issuer's own facts; D-082).
3. **Primary evidence is the ultimate authority.** Where sources disagree, the highest-tier, most recent, most specific source governs — and the disagreement is still recorded.
4. **Material contradictions must be recorded** in `03_evidence/contradictions/`. They are never silently reconciled.
5. **Unsupported numbers must not enter final deliverables.** Every material number in a deliverable must trace to an evidence-register entry with a confidence category.
6. **No invented Guinea data.** Where information is not yet known, write `DATA NOT YET RESEARCHED`.
7. **No unverified Alendei claims.** Alendei capabilities, licences, partnerships and financing commitments are not asserted unless evidenced by the user.

## 9. Quality-control principles

- Evidence before conclusions; technology-neutral assessment — no technology is promoted or de-emphasised before the evidence supports it.
- Every material statistic carries: value, unit, geography, date/year, metric definition, source, source publication date, URL/reference, confidence, cross-check.
- Confidence categories: `VERIFIED`, `CORROBORATED`, `ESTIMATED`, `INDICATIVE`, `DATA GAP` (definitions in `00_project/methodology.md`).
- Capacity, energy and demand metrics are strictly distinguished (installed vs available vs dependable vs dispatched; generation vs delivered vs consumed; peak vs average).
- Project status is assigned from evidence of progress and commitment, not elapsed time. Lifecycle stage (proposed, announced, active development, financially committed, under construction, operational, cancelled) is recorded separately from progress condition (on track, delayed, stalled, unverified).
- Opportunities are classified Tier 1 — Pursue immediately, Tier 2 — Develop, Tier 3 — Monitor, or Tier 4 — Do not pursue now.
- Registers are maintained in XLSX as the master working format. CSV/JSON derivatives are generated only where needed.
- Copyrighted third-party documents are not committed automatically. The source register preserves traceability.
- Independent Guinea analysis precedes, and is kept separate from, Alendei opportunity analysis.
- Every gate has written acceptance criteria and a named approver.

## 10. Versioning principles

- Git is the system of record.
- Branching: `develop` is for active development; `main` holds approved, stable states.
- Approved gates are snapshotted with descriptive tags: `gate-00-bootstrap`, `gate-01-research-architecture`, `gate-02-discovery`, `gate-03-evidence`, and so on (full list in `00_project/quality_gates.md`).
- Project documents carry a version and last-updated date (DD-MMM-YYYY).
- Registers are append-oriented: entries are superseded (with a pointer to the replacement), not deleted.
- Deliverable drafts are versioned by filename (`_v0.1`, `_v0.2`, …); only approved versions move to `final/`.
- Decisions are logged in `00_project/decision_log.md` with ID, date, reason, evidence, owner and status.
- No secrets, credentials, API keys or personal data are ever committed (see `.gitignore`).
