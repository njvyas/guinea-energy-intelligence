# Research Status

**Last updated:** 08-Oct-2026

## Current status

| Field | Value |
|---|---|
| Current Gate | GATE 2C — CLOSED; awaiting Gate 2D authorisation |
| Status | Gates 2A, 2B, 2C approved and closed (D-057, D-085); checkpoint tag `gate-02c-mission-execution-readiness`. Sole Gate 2D prerequisite: confirm execution model (P-030). |
| Previous gates | GATE 0 — APPROVED (`5b1f6e7`, `gate-00-bootstrap`, pushed) · GATE 1 — APPROVED (`a255d4f`, `gate-01-research-architecture`, pushed) |
| Architecture | 28 workstreams (WS-01 – WS-28); 133 research questions with planning priorities; Gemini missions GEM-01 – GEM-15 approved as architecture only, NOT STARTED |
| Research started | NO |
| Substantive Guinea research performed by Claude | NO |
| Substantive Guinea research performed by Gemini | NO |
| Evidence register populated | NO — empty templates for the 11 logical registers exist (Entity/Site as two physical sheets); zero data records. Rule: no populated evidence data before authorised research execution (D-077) |
| Gemini missions started | NO |
| Gemini inputs received | Gate 1 architecture challenge only (Tier 6; assertions logged as leads GL-01 – GL-33) |
| Opportunity analysis started | NO |
| Final deliverables started | NO |

## Gate checklist

### GATE 0 — Repository bootstrap
- [x] Folder structure created
- [x] README.md created
- [x] `00_project/` documents created
- [x] `.gitignore` created
- [x] Decision log initialised
- [x] Pending decisions P-001 to P-006 reviewed by user (resolved as D-017 to D-022)
- [x] Gate 0 approved by User + ChatGPT
- [x] Gate 0 corrections applied
- [x] Gate 0 committed to `develop`
- [x] Gate 0 tagged `gate-00-bootstrap`
- [x] Pushed to `origin/develop` with tag

### GATE 1 — Research architecture
- [x] Gemini architecture challenge received and deposited verbatim (SHA-256 sidecar)
- [x] Owner review directives incorporated (D-024 – D-040)
- [x] Reconciliation log: every Gemini recommendation dispositioned; assertions logged as leads (GL-01 – GL-33)
- [x] Final workstream structure: 28 workstreams with full charters
- [x] Qualitative planning priority on every research question (CRITICAL / HIGH / MEDIUM / LOW)
- [x] Technology-option coverage matrix
- [x] Research sequencing mapped to gates
- [x] Gemini mission structure (GEM-01 – GEM-15, approved as architecture only) and mission → workstream coverage matrix
- [x] Gemini → Claude handoff protocol
- [x] Register architecture (11 logical registers, single-source-of-truth rules) and schema fields
- [x] Gemini artifact accepted as immutable operator-provided source (D-054)
- [x] Contradiction-resolution protocol
- [x] Project-status framework (retained; asset-specific rules added)
- [x] Forecasting / scenario architecture (no frozen matrix or parameters)
- [x] Opportunity-screening architecture (no frozen weights; WS-27/WS-28 separation)
- [x] GIS architecture (opportunity + constraint layers; no universal thresholds)
- [x] Regional benchmark metric framework
- [x] Folder structure aligned (mission-based raw research; WS-based analysis; new register and GIS folders)
- [x] Governance documents updated and consistency-checked
- [x] Gate 1 approved by User + ChatGPT (P-007)
- [x] P-008 resolved (D-051)
- [x] P-009 resolved — templates at Gate 2B (D-055)
- [x] Gate 1 committed (`a255d4f`), tagged `gate-01-research-architecture`, pushed

### GATE 2 — Discovery research

**2A — Research Execution Protocol**
- [x] `research_execution_protocol.md` drafted (lifecycle, evidence states, source/quantitative/temporal/geographic rules, terminology, status, contradictions, confidence, output contract, handoff, reconciliation, acceptance, stopping, failure, copyright, reproducibility)
- [x] Gate 2A pending decisions documented (P-013 – P-024)
- [x] Consistency audit against Gate 1 documents
- [x] Gate 2A approved by User + ChatGPT (D-057); P-013 – P-024 dispositioned (D-058 – D-065)

**2B — Register templates**
- [x] Register Schema v1.0 (`register_schema.md`) and generator (`00_project/tools/build_register_templates.py`)
- [x] EMPTY XLSX templates generated for the 11 logical registers (Entity/Site as two physical sheets; D-076), incl. 2A decisions; P-018 – P-020, P-023 resolved
- [x] Gate 2B schema/consistency audit
- [x] Register architecture approved by owner; D-071 approved; P-025 approved with boundary (D-074); P-026 approved and strengthened (D-075); D-072 final; D-076, D-077 recorded
- [x] Gate 2B approved and closed

**2C — Mission packages**
- [x] Mission packages GEM-01 – GEM-15 (Pv1) compiled and validated (`01_gemini_research/00_architecture/mission_packages/`; D-078 – D-081)
- [x] Register validator built and passing against empty templates (D-083; 63 tests passing)
- [x] Gemini prompt compatibility test: GEM-05 and GEM-12 control 10/10 PASS (D-084); no split required
- [x] Gate 2C approved and closed (D-085); P-029 resolved (D-086); model pinning prepared (D-087)

**2D — Research execution**
- [ ] GL-01 – GL-33 transferred to lead register
- [x] Register validator approved and passing (prerequisite, D-075; D-083)
- [ ] Execution model confirmed by owner (P-030; tested option gemini-3.8-flash-high, D-087)
- [ ] Gate 2D research execution authorised (missions may not run before this)
- [ ] Wave 1 missions deposited: GEM-01, GEM-02, GEM-04, GEM-05, GEM-07, GEM-09, GEM-10, GEM-15
- [ ] Wave 2 missions deposited: GEM-03, GEM-06, GEM-08, GEM-11, GEM-12, GEM-13
- [ ] Wave 3 mission deposited: GEM-14
- [ ] Claude independent discovery completed for all 26 Phase A workstreams
- [ ] Sources captured and source register drafted
- [ ] Mission Reconciliation Reports (`GEM-NN_close_report.md`) with challenge logs
- [ ] Gate 2 approved

### GATE 3 — Evidence consolidation
- [ ] Material claims verified
- [ ] Master data register populated with full metadata
- [ ] Confidence categories assigned
- [ ] Metric and status taxonomies applied
- [ ] Gate 3 approved

### GATE 4 — Contradiction and data-gap audit
- [ ] Contradiction register populated and diagnosed
- [ ] Data-gap register populated with materiality and next steps
- [ ] Audit summary written
- [ ] Gate 4 approved

### GATE 5 — Power-system analysis
- [ ] Country, macro and FX context (WS-01, WS-04)
- [ ] Institutions, law and mining legal regime (WS-02, WS-15)
- [ ] Fuel supply and thermal/gas options (WS-03)
- [ ] Generation fleet and seasonal dependable capacity (WS-05, WS-17)
- [ ] Transmission, distribution, reliability (WS-06 – WS-08)
- [ ] Utility economics and counterparty assessment (WS-09)
- [ ] WAPP and interconnection status (WS-16)
- [ ] Project register with evidenced status (WS-23)
- [ ] Model platform decision (P-010)
- [ ] Gate 5 approved

### GATE 6 — Geographic / resource / demand analysis
- [ ] Demand baseline and segment demand (WS-10 – WS-14, WS-22)
- [ ] Resource assessments on equal footing (WS-18 – WS-21)
- [ ] Land, environment and biodiversity constraints (WS-26)
- [ ] Finance instruments and international ecosystem registers (WS-24, WS-25)
- [ ] GIS opportunity and constraint layers with catalogue entries
- [ ] Integrated scenario model and seasonal supply–demand balance
- [ ] Gate 6 approved

### GATE 7 — Opportunity development
- [ ] Part 1 — WS-27: candidates, fatal-flaw screen, scoring, weight sensitivity, approved weights
- [ ] Part 1 — WS-27 attractiveness ratings frozen and approved
- [ ] Alendei capability evidence received from user
- [ ] Part 2 — WS-28: participation assessment and Tier 1–4 classifications (incl. "Tier 4 — Do not pursue now")
- [ ] Roadmap and due-diligence lists drafted
- [ ] Gate 7 approved

### GATE 8 — Adversarial review
- [ ] Gemini adversarial review received
- [ ] Response log completed
- [ ] Gate 8 approved

### GATE 9 — Final reconciliation
- [ ] Registers frozen
- [ ] Reconciled numbers list
- [ ] Final findings and portfolio locked
- [ ] Gate 9 approved

### GATE 10 — Deliverable production
- [ ] PDF report
- [ ] Executive PowerPoint
- [ ] Interactive HTML platform
- [ ] Gate 10 approved

### GATE 11 — Final QA
- [ ] Number-trace audit
- [ ] Cross-deliverable consistency check
- [ ] Secrets / personal-data scan
- [ ] QA report
- [ ] Release approved and tagged

## Workstream status

| WS | Workstream | Primary mission(s) | Secondary mission(s) | Claude verification | Status |
|---|---|---|---|---|---|
| WS-01 | Macroeconomic, Political Economy & Country Risk Context | GEM-09 | — | NOT STARTED | DATA NOT YET RESEARCHED |
| WS-02 | Electricity Sector Institutions, Law & Regulation | GEM-10 | GEM-04 | NOT STARTED | DATA NOT YET RESEARCHED |
| WS-03 | Fuel Supply, Logistics, Landed Fuel Economics & Thermal/Gas Options | GEM-01 | — | NOT STARTED | DATA NOT YET RESEARCHED |
| WS-04 | Macro-Financial Framework, Currency, FX Convertibility & Repatriation | GEM-09 | GEM-07 | NOT STARTED | DATA NOT YET RESEARCHED |
| WS-05 | Existing Generation Fleet, Operating Performance & Seasonal Dependable Capacity | GEM-14 | GEM-01, GEM-02 | NOT STARTED | DATA NOT YET RESEARCHED |
| WS-06 | Transmission Network, Substations, System Stability & Reinforcement Options | GEM-05 | GEM-06, GEM-12, GEM-14 | NOT STARTED | DATA NOT YET RESEARCHED |
| WS-07 | Distribution, Access, Losses, Metering & Demand-Side Measures | GEM-05 | GEM-08, GEM-11 | NOT STARTED | DATA NOT YET RESEARCHED |
| WS-08 | Reliability, Outages & System Operations | GEM-05 | GEM-11 | NOT STARTED | DATA NOT YET RESEARCHED |
| WS-09 | Utility Economics, Tariffs, Counterparty Condition & Bankability | GEM-05 | GEM-09, GEM-10 | NOT STARTED | DATA NOT YET RESEARCHED |
| WS-10 | Electricity Demand Baseline, Load Profiles & Forecast Inputs | GEM-11 | GEM-03, GEM-12 | NOT STARTED | DATA NOT YET RESEARCHED |
| WS-11 | Bauxite Extraction & Alumina Refining Energy | GEM-03 | GEM-01 | NOT STARTED | DATA NOT YET RESEARCHED |
| WS-12 | Iron Ore / Simandou Megaproject & Infrastructure Corridor | GEM-12 | GEM-03 | NOT STARTED | DATA NOT YET RESEARCHED |
| WS-13 | Gold, Diamonds & Other Strategically Relevant Minerals | GEM-03 | GEM-01 | NOT STARTED | DATA NOT YET RESEARCHED |
| WS-14 | Non-Mining Industrial, Ports & Logistics, and Commercial Demand | GEM-11 | GEM-01, GEM-03 | NOT STARTED | DATA NOT YET RESEARCHED |
| WS-15 | Mining Legal Regime, Energy-Related Obligations & Infrastructure Access | GEM-04 | GEM-12 | NOT STARTED | DATA NOT YET RESEARCHED |
| WS-16 | WAPP, Regional Market & Cross-Border Interconnection | GEM-06 | — | NOT STARTED | DATA NOT YET RESEARCHED |
| WS-17 | Transboundary River Basins, Hydrology & Climate Variability | GEM-02 | GEM-13 | NOT STARTED | DATA NOT YET RESEARCHED |
| WS-18 | Solar Resource & Technical Potential | GEM-13 | — | NOT STARTED | DATA NOT YET RESEARCHED |
| WS-19 | Wind Resource & Technical Potential | GEM-13 | — | NOT STARTED | DATA NOT YET RESEARCHED |
| WS-20 | Hydro Development Potential (New, Rehabilitation, Small Hydro) | GEM-13 | GEM-02, GEM-15 | NOT STARTED | DATA NOT YET RESEARCHED |
| WS-21 | BESS, Hybridisation & Grid-Stability Applications | GEM-13 | — | NOT STARTED | DATA NOT YET RESEARCHED |
| WS-22 | Decentralised Energy, Mini-Grids & Productive Use | GEM-08 | GEM-10 | NOT STARTED | DATA NOT YET RESEARCHED |
| WS-23 | Generation & Transmission Project Pipeline | GEM-14 | — | NOT STARTED | DATA NOT YET RESEARCHED |
| WS-24 | International Finance, DFI & Risk-Mitigation Instruments | GEM-07 | GEM-09 | NOT STARTED | DATA NOT YET RESEARCHED |
| WS-25 | International Commercial Ecosystem (by Origin) & OEM/EPC/IPP Register | GEM-07 | GEM-14 | NOT STARTED | DATA NOT YET RESEARCHED |
| WS-26 | Land Tenure, Resettlement, Environmental & Biodiversity Constraints | GEM-15 | GEM-13 | NOT STARTED | DATA NOT YET RESEARCHED |
| WS-27 | Commercial Opportunity Portfolio & Structuring | NONE (by design) | NONE (by design) | NOT STARTED | Not started (Gate 7) |
| WS-28 | Alendei Strategic Participation & Ecosystem Role | NONE (by design) | NONE (by design) | NOT STARTED | Not started (Gate 7) |

## Gemini mission status

| Mission | Status |
|---|---|
| GEM-01 – GEM-15 | APPROVED AS ARCHITECTURE; executable packages Pv1 prepared (Gate 2C, pending approval) — NOT STARTED. Execution requires Gate 2D authorisation and the D-075 validator. |
