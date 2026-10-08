# Research Architecture v1.0

**Version:** 1.0 (DRAFT, pending Gate 1 approval) · **Last updated:** 08-Oct-2026 · **Gate:** 1

**Inputs used:**
- the Gate 0 architecture;
- the Gemini Gate 1 challenge (`01_gemini_research/00_architecture/2026-10-08_GATE1_architecture-challenge_gemini_v1.md`, Tier 6 lead);
- the ChatGPT / project-owner review of 08-Oct-2026.

How each Gemini recommendation was handled is recorded in `gate1_gemini_reconciliation.md`.

This document contains **no Guinea findings**. It defines how the research will be organised, sequenced, recorded, checked and integrated.

| Section | Content | Normative detail |
|---|---|---|
| A | Architecture overview and design principles | — |
| B | Final workstream list | `workstream_charters.md` |
| C | Workstream charters | `workstream_charters.md` |
| D | Research sequencing | This document |
| E | Gemini mission structure | `gemini_mission_briefs.md` |
| F | Gemini → Claude handoff protocol | This document |
| G | Register architecture | This document; field definitions in `methodology.md` §3, §4.2, §6.3 |
| H | Contradiction-resolution protocol | This document |
| I | Project-status framework | `methodology.md` §6 |
| J | Forecasting and scenario architecture | This document |
| K | Opportunity-screening architecture | This document |
| L | GIS architecture | This document |
| M | Regional benchmark framework | This document |

---

## A. Architecture overview

### A.1 Design principles

1. **Evidence before conclusions.** Gemini findings are hypotheses or leads until primary evidence is verified (D-026).
2. **Technology neutrality.** Every technically or economically plausible solution is assessed on evidence. This includes solar, wind, hydro, BESS, thermal, hybrids, grid reinforcement, demand-side measures, mini-grids and regional trade. No option is promoted or played down in advance (D-027).
3. **Country first, Alendei second.** WS-27 answers "what is attractive for Guinea?"; WS-28 then answers "where can Alendei participate?". WS-28 cannot alter WS-27's ranking (D-028).
4. **No premature thresholds or weights.** There are no universal GIS cut-offs, no frozen screening weights and no fixed time threshold for staleness or stalling. Thresholds are set later, per project or technology, with recorded justification.
5. **Site-level granularity where possible.** Mining, industrial, generation and network data are collected at the level of the asset, company or site.
6. **Seasonality is first-class.** Hydro dependable capacity and the supply–demand balance are analysed at least by season, and preferably by month.
7. **No workstream exists merely because Gemini listed it.** Each one has a distinct objective, boundary and set of downstream consumers (see `workstream_charters.md`).

### A.2 Specific non-assumptions (D-026)

Research must investigate the following, not assume them:

- **EDG:** its financial condition is to be evidenced. Distress is not presumed.
- **Offshore escrow / FX structures:** whether they are required, and which mechanisms are actually used, is to be evidenced.
- **OMVG / OMVS / ABN:** their relevance to Guinea hydropower is to be evidenced.
- **GIS slope (or any other) universal exclusion threshold:** not adopted. Constraint layers are built, and project-specific criteria are applied later.
- **Alumina refinery load:** researched separately for each plant or project. No generic MW figure is used.
- **Wind:** not de-prioritised. It is assessed in the same way as other technologies.
- **Opportunity weights:** Gemini's 25/20/20/20/15 weights are not adopted, and no weights are frozen at Gate 1.
- **Mining B2B:** not predetermined as the preferred commercial model.
- **Every other Gemini factual assertion:** logged as an unverified lead (`gate1_gemini_reconciliation.md` §4).

### A.3 Structural changes from Gate 0

| Change | Detail |
|---|---|
| Workstreams | 20 → 28. Ten new workstreams. The four origin/OEM workstreams are merged into WS-25. Mining and industrial demand are split by segment (WS-11 to WS-15). Opportunity work is split into WS-27 (country) and WS-28 (Alendei). |
| `01_gemini_research/` | Organised by **mission** (`GEM-NN_<slug>/`) instead of by workstream, because each mission spans several workstreams. `00_architecture/` is retained. |
| `03_evidence/` | Added `lead_register/`, `project_register/`, `entity_register/` and `assumption_register/`. |
| `04_analysis/` | Reorganised into `ws01_…` to `ws26_…`, plus `00_integrated_models/` (supply–demand balance, seasonal dispatch, scenarios). The Gate 0 domain folders were removed; they were empty. |
| `05_gis/` | Added `constraints/`, `logistics/` and `hydrology/`. |

---

## B. Final workstream list

| ID | Workstream | Cluster |
|---|---|---|
| WS-01 | Macroeconomic, Political Economy & Country Risk Context | A |
| WS-02 | Electricity Sector Institutions, Law & Regulation | A |
| WS-03 | Fuel Supply, Logistics, Landed Fuel Economics & Thermal/Gas Options | A |
| WS-04 | Macro-Financial Framework, Currency, FX Convertibility & Repatriation | A |
| WS-05 | Existing Generation Fleet, Operating Performance & Seasonal Dependable Capacity | B |
| WS-06 | Transmission Network, Substations, System Stability & Reinforcement Options | B |
| WS-07 | Distribution, Access, Losses, Metering & Demand-Side Measures | B |
| WS-08 | Reliability, Outages & System Operations | B |
| WS-09 | Utility Economics, Tariffs, Counterparty Condition & Bankability | B |
| WS-10 | Electricity Demand Baseline, Load Profiles & Forecast Inputs | B |
| WS-11 | Bauxite Extraction & Alumina Refining Energy | C |
| WS-12 | Iron Ore / Simandou Megaproject & Infrastructure Corridor | C |
| WS-13 | Gold, Diamonds & Other Strategically Relevant Minerals | C |
| WS-14 | Non-Mining Industrial, Ports & Logistics, and Commercial Demand | C |
| WS-15 | Mining Legal Regime, Energy-Related Obligations & Infrastructure Access | C |
| WS-16 | WAPP, Regional Market & Cross-Border Interconnection | D |
| WS-17 | Transboundary River Basins, Hydrology & Climate Variability | D |
| WS-18 | Solar Resource & Technical Potential | E |
| WS-19 | Wind Resource & Technical Potential | E |
| WS-20 | Hydro Development Potential (New, Rehabilitation, Small Hydro) | E |
| WS-21 | BESS, Hybridisation & Grid-Stability Applications | E |
| WS-22 | Decentralised Energy, Mini-Grids & Productive Use | E |
| WS-23 | Generation & Transmission Project Pipeline | F |
| WS-24 | International Finance, DFI & Risk-Mitigation Instruments | F |
| WS-25 | International Commercial Ecosystem (by Origin) & OEM/EPC/IPP Register | F |
| WS-26 | Land Tenure, Resettlement, Environmental & Biodiversity Constraints | F |
| WS-27 | Commercial Opportunity Portfolio & Structuring | G (Phase B) |
| WS-28 | Alendei Strategic Participation & Ecosystem Role | G (Phase B, last) |

**Clusters:** A, Country, institutions and primary energy · B, Power-system baseline · C, Mining and industrial energy · D, Regional market and basin governance · E, Technology and resource options · F, Pipeline, finance, ecosystem and constraints · G, Opportunity and strategy.

**Why 28 workstreams and not 27:**

- Gemini's 27 workstreams combined country opportunity and Alendei positioning in one workstream (its WS-27). The owner review requires these to be separate, which gives WS-27 and WS-28.
- No other workstream was added beyond Gemini's set.
- Gemini's workstreams were re-scoped to remove overlap. The boundary statements are in each charter.

---

## D. Research sequencing

Discovery runs in parallel across missions. Analysis follows the dependency order below. Each stage maps to a quality gate.

| Stage | Content | Workstreams | Gate |
|---|---|---|---|
| **S1: Foundations** | Institutions, law, macro, FX, fuel, mining legal regime, basin governance | WS-01, 02, 03, 04, 15, 17 (governance part) | Discovery at Gate 2 → analysis at Gate 5 |
| **S2: Power-system baseline** | Fleet, network, distribution, reliability, utility economics, hydrology for dependable capacity | WS-05, 06, 07, 08, 09, 17 (hydrology part) | Gate 2 → Gate 5 |
| **S3: Regional & pipeline** | WAPP, project pipeline | WS-16, 23 | Gate 2 → Gate 5 |
| **S4: Demand, resources & constraints** | Demand segments, demand baseline, technology resources, decentralised energy, land and environment | WS-10–14, 18–22, 26 | Gate 2 → Gate 6 |
| **S5: Finance & ecosystem** | Finance instruments, international ecosystem | WS-24, 25 | Gate 2 → Gate 6 |
| **S6: Integration** | GIS integration, integrated scenario model, seasonal supply–demand balance | `04_analysis/00_integrated_models/`, `05_gis/` | Gate 6 |
| **S7: Country opportunities** | WS-27; the ratings are frozen at the end of this stage | WS-27 | Gate 7 (part 1) |
| **S8: Alendei participation** | WS-28 | WS-28 | Gate 7 (part 2) |

Gate 3 (evidence consolidation) and Gate 4 (contradiction and data-gap audit) apply to everything that Stages S1–S5 discover. Gates 8–11 follow as defined in `quality_gates.md`.

**Critical-path dependencies:**
- WS-17 hydrology → WS-05 seasonal dependable capacity → integrated model.
- WS-11 to WS-14 and WS-22 → WS-10 demand → integrated model.
- WS-23 pipeline → integrated model (committed additions).
- Phase A complete → WS-27 → WS-27 rating freeze → WS-28.

---

## E. Gemini mission structure (summary)

Full briefs, the authoritative mission-to-workstream mapping and the coverage matrix are in `gemini_mission_briefs.md`.

- **GEM-01 to GEM-08:** the initial discovery batch (D-034).
- **GEM-09 to GEM-15:** follow-up missions that close the coverage gaps (D-051).
- All 15 are **approved as architecture only**. Running any mission requires separate authorisation at Gate 2.
- Further targeted missions may be added when the evidence reveals unresolved questions.

| Mission | Title | Primary WS | Secondary WS | Wave |
|---|---|---|---|---|
| GEM-01 | Fuel Logistics, Thermal Fleet & Landed Fuel Economics | WS-03 | WS-05, WS-11, WS-13, WS-14 | 1 |
| GEM-02 | Transboundary Basin Governance, Hydrology & Hydro Seasonality | WS-17 | WS-05, WS-20 | 1 |
| GEM-03 | Mining & Industrial Energy Baseline & Captive Supply Economics | WS-11, WS-13 | WS-10, WS-12, WS-14 | 2 |
| GEM-04 | Mining Legal Regime, Energy-Related Obligations & Private Supply Pathways | WS-15 | WS-02 | 1 |
| GEM-05 | Utility Operations, Financial Condition & Network Constraints | WS-06, WS-07, WS-08, WS-09 | — | 1 |
| GEM-06 | WAPP Interconnection & Cross-Border Trade Status | WS-16 | WS-06 | 2 |
| GEM-07 | International Finance, Bilateral Credit Lines & Country Ecosystems | WS-24, WS-25 | WS-04 | 1 |
| GEM-08 | Decentralised Energy, Mini-Grids & Rural Electrification | WS-22 | WS-07 | 2 |
| GEM-09 | Macro, Political Economy, FX & Repatriation | WS-01, WS-04 | WS-09, WS-24 | 1 |
| GEM-10 | Electricity Sector Institutions & Regulatory Framework | WS-02 | WS-09, WS-22 | 1 |
| GEM-11 | National Demand Baseline & Non-Mining Loads | WS-10, WS-14 | WS-07, WS-08 | 2 |
| GEM-12 | Simandou Corridor Energy (dedicated) | WS-12 | WS-06, WS-10, WS-15 | 2 |
| GEM-13 | Technology-Neutral Resource Assessment (Solar, Wind, Hydro Sites, Storage Needs) | WS-18, WS-19, WS-20, WS-21 | WS-17, WS-26 | 2 |
| GEM-14 | Project Pipeline Consolidation & Status Verification | WS-05, WS-23 | WS-06, WS-25 | 3 |
| GEM-15 | Land, Resettlement, Environmental & Biodiversity Framework | WS-26 | WS-20 | 1 |

**Coverage:**
- Every discovery workstream, WS-01 to WS-26, has at least one primary mission.
- WS-27 and WS-28 have no discovery mission by design. They are synthesis workstreams restricted to verified registers and, for WS-28, user-supplied Alendei evidence. Gemini's role for them is the Gate 8 adversarial review (`gemini_mission_briefs.md` §3).
- Claude's independent discovery also covers WS-01 to WS-26.

---

## F. Gemini → Claude handoff protocol

```
[0] Mission brief issued (gemini_mission_briefs.md) ─ operator runs Gemini
        │
[1] INTAKE ─ operator deposits output verbatim into 01_gemini_research/GEM-NN_<slug>/
        │      file name: YYYY-MM-DD_GEM-NN_<slug>_gemini_vN.md
        │      Claude writes a <file>.meta.md sidecar (date, model if known, prompt ref, SHA-256)
        │      raw file is immutable from this point
        │
[2] LEAD EXTRACTION ─ each material claim → lead register (LEAD-NNNNN)
        │      evidence_state = RAW_LEAD; the Gemini-cited source is recorded as stated
        │
[3] SOURCE REGISTRATION ─ each cited source → source register (SRC-NNNN)
        │      evidence_state = CANDIDATE_SOURCE until retrieved and checked
        │      Gemini citations that cannot be found → flagged "CITATION NOT FOUND"
        │      local copy stored only if the copyright basis is recorded (methodology §4.2)
        │
[4] INDEPENDENT VERIFICATION ─ Claude reads the original source
        │      confirms the exact text/table/figure, page and definition
        │      assigns tier, discloser independence and quality dimensions
        │
[5] REGISTRATION ─ verified items → master data / project / entity register
        │      evidence_state = EXTRACTED | VERIFIED | CORROBORATED | ESTIMATE
        │      lead register entry updated: VERIFIED / PARTLY VERIFIED / CONTRADICTED /
        │                                   UNSUPPORTED / NOT YET CHECKED
        │
[6] CONTRADICTION & GAP LOGGING ─ conflicts → contradiction register (§H)
        │      unverifiable material claims → data-gap register
        │
[7] MISSION CLOSE REPORT ─ GEM-NN_close_report.md in the mission folder (Claude-authored): coverage by WS,
        │      leads verified / contradicted / unsupported, new gaps, proposed follow-up missions
        │
[8] ANALYTICAL INTEGRATION ─ only register entries (never leads) feed 04_analysis/ and 05_gis/
```

**Operator-provided Gemini artifacts:**

These rules apply to every Gemini artifact. The Gate 1 architecture challenge is accepted as an immutable artifact provided by the operator (D-054).

1. **The original is preserved unchanged.** It is never edited, renamed or deleted.
2. **The fingerprint is retained.** A SHA-256 and the deposit metadata are kept in the `.meta.md` sidecar, and integrity is checked at each gate.
3. **The artifact is not evidence.** It is a Tier 6 source artifact.
4. **Its claims remain research leads** until they have been independently sourced and validated through steps 2–6 above.
5. **Its presence does not mean research is complete.** Depositing an artifact completes nothing beyond intake (step 1).

**Rules:**

- A lead never enters an analysis, a model or a deliverable directly.
- When a Gemini claim cites a source that Claude cannot locate or that does not support the claim, the lead is marked UNSUPPORTED. It is not silently dropped.
- Claude's independent discovery uses the same pipeline from step 3 onward. Its source is recorded as "Claude discovery".
- A mission is closed only when every material lead from it has a status other than NOT YET CHECKED, or is logged as a data gap.

---

## G. Register architecture

### G.1 Single-source-of-truth rules

1. **XLSX is authoritative.** Each register is one XLSX workbook, and that workbook is the human-facing master (D-018).
2. **Derivatives only.** CSV or JSON files may be generated from the XLSX master when needed (e.g. for the HTML platform or analysis scripts). They are written by a script, never edited by hand, and labelled as derived. They are regenerated whenever the master changes.
3. **No competing copies.** No manually maintained duplicate, extract or parallel version of any register may exist. A filtered view (e.g. the priority portfolio) is produced from the master, not kept separately.
4. **Each value is stored once.** Every material quantitative value is stored **only** in the Master Data Register (MDR). Other registers refer to it by `DAT-` ID. Any number they display is a derived lookup, not a separately maintained value.
5. **No data at Gate 1.** No register is created or populated at Gate 1. Templates are generated from these schemas when Gate 2 opens (P-009).
6. **Authority.** Claude Code maintains every register (except where stated), and the User and ChatGPT approve register states at each gate. Alendei capability facts come only from the user.

### G.2 Registers

| # | Register | Workbook | ID | Purpose | Maintained by / authority | Relationship to the MDR |
|---|---|---|---|---|---|---|
| 1 | **Master Data Register (MDR)** | `03_evidence/master_data_register/master_data_register.xlsx` | `DAT-WSNN-NNNNN` | The **single store of material quantitative statistics**, with full metadata (`methodology.md` §3) | Claude Code; approved at Gates 3, 4 and 9 | Is the hub |
| 2 | Source register | `03_evidence/source_register/source_register.xlsx` | `SRC-NNNN` | Bibliographic and copyright record of each source (`methodology.md` §4.2) | Claude Code | Each MDR record cites a `SRC-` ID |
| 3 | Lead register | `03_evidence/lead_register/lead_register.xlsx` | `LEAD-NNNNN` | Verification queue for unverified claims (Gemini, discovery notes, GL-01 to GL-33) | Claude Code | A verified lead points to the `DAT-`/`PRJ-`/`ENT-` record it produced. Leads are **never** used as data |
| 4 | Contradiction register | `03_evidence/contradictions/contradiction_register.xlsx` | `CON-NNNN` | Conflicting values and their resolution (§H) | Claude Code; material items reviewed by the owner at Gate 4 | References two or more `DAT-` IDs; the MDR records carry `contradiction_id` |
| 5 | Data-gap register | `03_evidence/data_gaps/data_gap_register.xlsx` | `GAP-NNNN` | Questions sought but not answered; materiality; next steps; priority reassessment (`methodology.md` §12) | Claude Code; reviewed at Gate 4 | Records the absence of an MDR value |
| 6 | Project register | `03_evidence/project_register/project_register.xlsx` | `PRJ-NNNN` | Identity, technology, location, lifecycle stage and progress condition (`methodology.md` §6.3), and links to entities, for every generation, storage, transmission and infrastructure project | Claude Code (WS-23 owner) | Holds status and descriptive attributes. Capacities, output and costs are **`DAT-` references** |
| 7 | Entity register | `03_evidence/entity_register/entity_register.xlsx` (two sheets: organisations and sites) | `ENT-NNNN` / `SITE-NNNN` | Organisations (type, origin, Guinea-presence class) and mining or industrial sites (operator, segment, location, stage, power source) | Claude Code (WS-25 and WS-11 to WS-14 owners) | Demand, captive MW and fuel cost are **`DAT-` references** |
| 8 | Assumption register | `03_evidence/assumption_register/assumption_register.xlsx` | `ASM-NNNN` | Modelling assumptions: value, basis, sensitivity range, scenario | Claude Code; approved at Gates 6 and 7 | Each assumption cites its `DAT-` basis or a documented method. An assumption is never written back into the MDR as data |
| 9 | GIS layer catalogue | `05_gis/gis_layer_catalogue.xlsx` | `GIS-NNNN` | Provenance of each layer: source, date, licence, CRS, processing, constraint class | Claude Code | Cites `SRC-` IDs. Layer features carry `PRJ-`, `SITE-` or `OPP-` IDs |
| 10 | Opportunity register (WS-27) | `06_opportunities/candidate_opportunities/opportunity_register.xlsx` | `OPP-NNNN` | Country opportunities: evidence chain, fatal-flaw result, dimension scores, attractiveness rating (frozen) | Claude Code; User and ChatGPT approve the freeze at Gate 7 part 1 | The evidence chain cites `DAT-`, `PRJ-`, `ENT-` and `ASM-` IDs |
| 11 | Alendei participation register (WS-28) | `06_opportunities/alendei_role/alendei_participation_register.xlsx` | `ALP-NNNN` | Alendei roles, capability gaps, partners, Tier 1–4 classification | Claude Code. **Capability evidence is supplied only by the user**; User and ChatGPT approve | References `OPP-` IDs (read-only). Contains no Guinea statistics of its own |

### G.3 Review of the 11-register structure

The structure was reviewed for duplication. **Each register has a distinct function that no other register performs**, so no further consolidation is warranted:

- **Consolidations already applied:**
  - organisations and sites share one entity workbook;
  - the priority portfolio, the benchmark tables and the pipeline summaries are views generated from registers, not separate registers.
- **Duplication of values is prevented by G.1 rule 4:** the project, entity, opportunity and assumption registers store references, not copies.
- **Separations kept deliberately:**
  - the lead register is kept apart from the MDR so that unverified claims cannot contaminate it (D-032);
  - the opportunity register is kept apart from the Alendei participation register to enforce D-028;
  - the contradiction register is kept apart from the data-gap register because they have different fields, triggers and review paths.

### G.4 Evidence states

Defined in `methodology.md` §2.2 (D-032):

`RAW_LEAD` → `CANDIDATE_SOURCE` → `EXTRACTED` → `VERIFIED` / `CORROBORATED`; separately `ESTIMATE`, `INFERENCE`, `CONTRADICTED_UNRESOLVED`, `DATA_GAP`.

| State | Where it may appear |
|---|---|
| RAW_LEAD | Lead register only |
| CANDIDATE_SOURCE | Source register only |
| INFERENCE | Analysis documents only, labelled as inference. Never stored as a data point |

---

## H. Contradiction-resolution protocol

**Trigger:** two or more values for the same metric, entity, geography and period that differ by more than the tolerance set for that metric class. Tolerances are set in the register template at Gate 2. Any difference in a status or a categorical value counts as a contradiction.

**Steps:**

1. **Log** every value with its full metadata (`CON-NNNN`). Each value keeps its own data ID.
2. **Normalise and diagnose the cause.** The categories are:
   - definition (e.g. installed vs dependable; MW-DC vs MW-AC; grid connection vs access tier);
   - period or season;
   - geographic scope;
   - unit or currency;
   - status interpretation (e.g. line constructed vs energised; MoU vs commitment);
   - duplication (the same project under different names);
   - transcription error;
   - genuine disagreement.
3. **Apply the standing normalisation rules:**
   - solar is recorded in both MW-DC and MW-AC;
   - hydro is recorded as nameplate plus seasonal dependable capacity;
   - access is recorded by tier and by urban/rural;
   - transmission is recorded as constructed, energised and commercially active;
   - the pipeline is de-duplicated by location, capacity and sponsor;
   - MoUs never count above Announced.
4. **Resolve**, choosing one outcome:

| Outcome | When | Effect |
|---|---|---|
| `RESOLVED-DEFINITIONAL` | The values measure different things | Both are retained as separate metrics |
| `RESOLVED-HIERARCHY` | The evidence hierarchy clearly favours one value (higher tier → more recent → more specific → better defined) | A governing value is set; the others are retained, with the reasoning |
| `RESOLVED-ERROR` | A transcription or calculation error is identified | The corrected value is used and the error documented |
| `RANGE-CARRIED` | Credible sources of comparable tier disagree and cannot be reconciled | A low/high envelope is carried into analysis, with a sensitivity flag. No single value is chosen silently |
| `OPEN` | The investigation is not complete | The value cannot be used in a deliverable headline |

5. **Rate materiality** as Material, Moderate or Minor. A contradiction is Material when it could change a conclusion, a ranking or a decision.
6. **Escalate.** Material contradictions that are OPEN or RANGE-CARRIED are listed for owner review at Gate 4, and disclosed in the deliverables at Gate 10.
7. **Never reconcile silently.** Every resolution records who resolved it, the date, and the reasoning.

---

## I. Project-status framework

The approved two-dimensional framework (D-022, reaffirmed by D-030) is defined in `methodology.md` §6:

- **Lifecycle stage:** Proposed · Announced · Active development · Financially committed · Under construction · Operational · Cancelled.
- **Progress condition:** On track · Delayed · Stalled · Unverified.

Gate 1 adds the following evidence rules for particular asset types (`methodology.md` §6.4):

- **Transmission and interconnectors:**
  - "Operational" requires evidence of energisation. Mechanical completion is not enough.
  - Commercial activation of an interconnector is recorded separately, in the project register.
- **Multi-component projects** (e.g. mine + rail + port): each component carries its own stage and condition.
- **Re-announced projects** are de-duplicated (§H). The history of names is kept in `alternative_names`.
- **"Stalled" is never inferred from an absence of news.** In that case the condition is Unverified and a data gap is raised.

---

## J. Forecasting and scenario architecture

**Principle:** linear extrapolation is never the sole forecasting method (D-031). It may appear only as a reference line. The structure of the scenarios stays flexible until the baseline evidence is in (Gate 6).

### J.1 Model structure

```
Baseline (Gate 5–6 verified)                    Driver modules (each with evidence-linked trajectories)
 ├ served demand by class & season               ├ D1 Mining expansion (site-level, WS-11–13)
 ├ suppressed / captive demand (estimated)       ├ D2 Processing / refining (project-level, WS-11)
 ├ fleet: seasonal dependable capacity           ├ D3 Industrial expansion (WS-14)
 ├ network transfer limits                       ├ D4 Urban / commercial growth (WS-10, WS-14)
 └ regional trade position                       ├ D5 Electrification (grid + decentralised, WS-07, WS-22)
                                                 ├ D6 Infrastructure projects (e.g. corridors, ports; WS-12, WS-14)
                                                 ├ S1 Hydro seasonality & climate variability (WS-17, WS-05)
                                                 ├ S2 Committed generation / transmission additions (WS-23)
                                                 ├ S3 WAPP imports / exports (WS-16)
                                                 └ S4 Distributed / captive generation (WS-11–14, WS-22)
                                  │
                                  ▼
               Scenario assembly (combinations of driver trajectories)
                                  │
                                  ▼
       Seasonal (monthly preferred; minimum wet/dry) supply–demand balance,
       2027–2030 and 2030–2035: energy, peak, dependable-capacity margin, unserved energy
```

### J.2 Evidence-linked inclusion rules

Projects enter scenarios according to their lifecycle stage. The rules below are proposed and will be confirmed at Gate 6.

| Lifecycle stage | Included in |
|---|---|
| Operational, Under construction | All scenarios, with the progress condition reflected in the timing |
| Financially committed | Central and higher scenarios. Delay sensitivity is applied if the project is Delayed |
| Active development | Higher scenarios only |
| Announced, Proposed | Sensitivity cases only |
| Stalled (any stage) | Excluded from central. Sensitivity only |

### J.3 Method rules

- **Mining and industrial demand** is built bottom-up, site by site and project by project. Each site has its own discrete timing trajectory.
- **Residential and commercial demand** uses top-down driver relationships where the data allow. These are cross-checked against benchmark countries and against how earlier official forecasts compared with outturn.
- **Seasonality:**
  - hydro dependable capacity is set by month or season, from WS-17 and WS-05;
  - solar and wind seasonal profiles come from WS-18 and WS-19;
  - load seasonality comes from WS-10.
- **Every assumption** goes in the assumption register (`ASM-`), with its basis and sensitivity range.
- **Scenario matrix:** a matrix such as Gemini's 3 demand × 2 season structure may be adopted at Gate 6. The number of scenarios, their definitions and their values are **not fixed now**, and none of Gemini's numeric parameters are adopted (e.g. growth rates, export tonnages, refinery MW).
- **Platform** (Python, XLSX or both) is to be decided at Gate 5 (P-010).

---

## K. Opportunity-screening architecture (preliminary, weights not frozen)

### K.1 Separation of the two questions

```
Phase A evidence ──► WS-27 COUNTRY OPPORTUNITY SCREEN ──► Attractiveness rating (Alendei-neutral) ──► FREEZE
                                                                                                      │
                     Alendei capability evidence (user) ──► WS-28 PARTICIPATION LENS ◄────────────────┘
                                                                     │
                                                                     ▼
                                                     Tier 1–4 Alendei pursuit classification
```

### K.2 WS-27 screening steps

1. **Candidate generation.** Opportunities are derived from evidenced needs, resources, constraints and policy, across all solution types.
2. **Fatal-flaw screen** (pass / fail / unresolved). The tests are:
   - a legal prohibition;
   - no credible offtaker or payment pathway;
   - a legal exclusion constraint on the site;
   - a technical impossibility;
   - evidence too weak to assess. A candidate failing on this ground is held as "Unresolved"; it is not rejected.
3. **Multi-criteria scoring** of the candidates that pass, on the dimensions below. Each dimension uses a common ordinal scale, proposed as 1–5. The scale anchors are defined at Gate 7 from the evidence, and numeric anchor thresholds are not set now.
4. **Weighting.** No weights are frozen at Gate 1 (D-029). At Gate 7, candidate weight sets are tested, including equal weights and weights elicited from the owner. Robustness of the ranking is checked by sensitivity analysis. The final weights are approved by the User and ChatGPT.
5. **Evidence-confidence overlay.** Evidence confidence is reported **alongside** the score, not blended into it, so that a high score on weak evidence remains visible as such.
6. **Attractiveness rating**, Alendei-neutral. The proposed labels are *Highly attractive / Attractive / Conditionally attractive / Not currently attractive* (P-011). The ratings are frozen before WS-28 begins.

**WS-27 screening dimensions:**

| # | Dimension | Principal evidence source |
|---|---|---|
| 1 | Demand quality | WS-10–14, WS-22 |
| 2 | Offtaker / counterparty quality | WS-09, WS-11–14 |
| 3 | Technical feasibility | WS-05, WS-06, WS-18–21 |
| 4 | Resource quality | WS-17–20 |
| 5 | Grid proximity / capacity | WS-06, GIS |
| 6 | Land / permitting / environment | WS-26, WS-02 |
| 7 | Commercial economics | WS-03, WS-09, assumption register |
| 8 | FX / currency exposure | WS-04 |
| 9 | Financing availability | WS-24 |
| 10 | Implementation complexity | Multiple |
| 11 | Development timeline | WS-23, WS-26 |
| 12 | Strategic importance (to Guinea's power system) | Integrated model |
| 13 | Scalability / replicability | Multiple |
| 14 | Competitive alternatives | WS-03, WS-16, WS-23, WS-25 |
| 15 | Evidence confidence (reported as an overlay, not a weighted dimension) | Registers |

### K.3 WS-28 participation lens (secondary)

- **What is assessed:**
  - Alendei strategic fit;
  - role options (from the D-011 hypothesis);
  - capability gaps, scored against user-supplied evidence only;
  - partner requirements (WS-25);
  - financing pathway (WS-24).
- **Rules:**
  - WS-28 cannot change a WS-27 rating.
  - A Tier 1 or Tier 2 classification for Alendei requires a WS-27 rating of at least *Conditionally attractive*. The threshold is proposed and to be confirmed at Gate 7.
  - "Tier 4 — Do not pursue now" is mandatory where warranted.

---

## L. GIS architecture

### L.1 Layer families and folders

| Family | Folder | Example layers (to be sourced at Gates 2–6) |
|---|---|---|
| Base & administrative | `base_maps/` | Boundaries, administrative units, DEM |
| Settlements & demand | `cities/` | Settlements, population, night-time lights |
| Generation | `generation/` | Plants (linked to PRJ IDs) |
| Transmission & substations | `transmission/`, `substations/` | Lines by voltage and status, substations with capacity |
| Regional interconnection | `wapp/` | Interconnectors and border substations |
| Mining & industrial | `mining/`, `industrial/` | Cadastre polygons, sites (linked to SITE IDs) |
| Logistics | `logistics/` | Roads, rail, ports, fuel depots and routes |
| Hydrology | `hydrology/` | Basins, rivers, gauges, reservoirs |
| Resources | `solar/`, `wind/`, `hydro/` | Resource rasters, hydro sites |
| Storage | `bess/` | Candidate or planned storage sites |
| **Constraints** | `constraints/` | Protected areas, forests, biodiversity and critical habitat, settlements, agricultural land, customary land (where data exist), resettlement precedents, flood risk, terrain and slope, existing corridors, mining and industrial areas |
| Opportunities | `opportunities/` | Opportunity zones (linked to OPP IDs) |

### L.2 Constraint treatment (D-038)

Each constraint layer is stored **with its attributes and continuous values** (e.g. slope in degrees or percent, distance surfaces), not as a pre-applied binary mask. Each layer is classified into one of three classes:

| Constraint class | Meaning | When applied |
|---|---|---|
| Legal exclusion | Development legally prohibited. The legal basis must be cited from WS-26 or WS-02 | Gate 6, once the legal basis is verified |
| Regulatory / technical constraint | Development is possible subject to conditions | Gate 7, per project and technology |
| Risk flag | Increases cost, risk or time | Gate 7, as a scoring input |

**No universal numeric threshold is set at Gate 1** (no slope cut-off, no buffer distance). Thresholds are set per technology and project at Gates 6–7, citing an engineering standard or other evidence, and recorded in the assumption register.

### L.3 Data standards

- Each layer has a catalogue entry (`GIS-NNNN`) recording source, date, licence and redistribution terms, CRS, resolution and processing steps.
- **Storage CRS** is EPSG:4326. The analysis CRS will be a projected CRS selected at Gate 6.
- **Proposed master format** is GeoPackage, with GeoJSON derivatives for the HTML platform. How large rasters are stored (Git LFS or kept out of git) is an open decision (P-012).
- **Licensing:** dataset licence terms vary. The copyright rule (`methodology.md` §4.2) applies to GIS data. A layer that cannot be redistributed is recorded in the catalogue but not committed.
- Every spatial feature that represents a project, site or entity carries the corresponding register ID.

---

## M. Regional benchmark framework

**Benchmark universe:** Senegal, Mali, Côte d'Ivoire, Sierra Leone, Liberia, Guinea-Bissau and Ghana, as the sponsor-specified minimum (D-004). Other countries are added only with a logged justification.

**Owner:** WS-16. Each metric is collected for Guinea and for every benchmark country using an identical definition. Where a source's definition differs, the difference is recorded in the register, not silently normalised.

| # | Metric | Definition basis |
|---|---|---|
| B1 | Installed capacity, total and by technology (MW; solar in both MW-DC and MW-AC) | `methodology.md` §5 |
| B2 | Dependable or available capacity, where published | §5 |
| B3 | Annual generation by source (GWh) and generation mix (%) | §5 |
| B4 | Served peak demand (MW) | §5 |
| B5 | Electricity consumption per capita (kWh/person) | Consumption ÷ population, both sourced |
| B6 | Access rate: grid and total, urban and rural | §5 (definition stated) |
| B7 | Losses: transmission, distribution and commercial | §5 |
| B8 | Average end-user tariff by customer class (local currency and USD; date and exchange rate stated) | WS-09 |
| B9 | Reliability indicators (SAIDI/SAIFI or hours of supply) | WS-08 |
| B10 | Cross-border interconnection: capacity, energised status and traded volumes | §5 |
| B11 | Share of private / IPP capacity | WS-23 |
| B12 | Share of renewable capacity and generation | §5 |
| B13 | Utility cost recovery or financial indicators, where comparable | WS-09 |

Metrics B1 to B13 form the **initial** list. Metrics may be added at Gate 5. A metric that cannot be sourced for a country is recorded as DATA GAP for that country and is not estimated by analogy.
