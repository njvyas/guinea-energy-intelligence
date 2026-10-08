# Gemini Mission Briefs — Discovery Missions GEM-01 to GEM-15

**Version:** 1.1 (DRAFT, pending Gate 1 approval) · **Last updated:** 08-Oct-2026 · **Gate:** 1

**Status:** all 15 missions are **APPROVED AS ARCHITECTURE ONLY. NOT STARTED.** Approval of a mission does not authorise running it. **Gate 2 must separately authorise research execution.** No mission may be issued before that.

- **GEM-01 to GEM-08** come from the Gemini Gate 1 challenge and form the initial discovery batch (D-034).
- **GEM-09 to GEM-15** were proposed by Claude Code to fill coverage gaps, and the owner accepted them as part of the architecture (D-051).
- More targeted missions may be created when the evidence shows important unresolved questions. Each new mission needs a decision-log entry.
- Where Gemini's mission titles or scopes assumed an answer, they have been reworded neutrally (`gate1_gemini_reconciliation.md` §5).
- The full prompt sent to Gemini for each mission consists of three parts: (a) `gemini_operating_instructions.md`, (b) the brief below, and (c) the mission output template (§4). Prompts are compiled when Gate 2 opens, and copies are archived in `01_gemini_research/00_architecture/`.

---

## 1. Mission overview

The "Primary WS" and "Secondary WS" columns are the authoritative mission-to-workstream mapping. §3 gives the same mapping inverted, by workstream.

| Mission | Title | Coverage area | Primary WS | Secondary WS | Wave | Deposit folder |
|---|---|---|---|---|---|---|
| GEM-01 | Fuel Logistics, Thermal Fleet & Landed Fuel Economics | Fuel supply, thermal fleet, delivered fuel cost | WS-03 | WS-05, WS-11, WS-13, WS-14 | 1 | `01_gemini_research/GEM-01_fuel-logistics-thermal/` |
| GEM-02 | Transboundary Basin Governance, Hydrology & Hydro Seasonality | Basin governance, hydrology, hydro seasonality | WS-17 | WS-05, WS-20 | 1 | `01_gemini_research/GEM-02_river-basins-hydrology/` |
| GEM-03 | Mining & Industrial Energy Baseline & Captive Supply Economics | Mining-site energy and captive supply | WS-11, WS-13 | WS-10, WS-12, WS-14 | 2 | `01_gemini_research/GEM-03_mining-industrial-energy/` |
| GEM-04 | Mining Legal Regime, Energy-Related Obligations & Private Supply Pathways | Mining law, obligations, private supply | WS-15 | WS-02 | 1 | `01_gemini_research/GEM-04_mining-legal-private-supply/` |
| GEM-05 | Utility Operations, Financial Condition & Network Constraints | Utility operations, finances, network, reliability | WS-06, WS-07, WS-08, WS-09 | — | 1 | `01_gemini_research/GEM-05_utility-operations-finance-network/` |
| GEM-06 | WAPP Interconnection & Cross-Border Trade Status | Interconnection and regional trade | WS-16 | WS-06 | 2 | `01_gemini_research/GEM-06_wapp-interconnection-trade/` |
| GEM-07 | International Finance, Bilateral Credit Lines & Country Ecosystems | Finance instruments and international ecosystem | WS-24, WS-25 | WS-04 | 1 | `01_gemini_research/GEM-07_international-finance-ecosystem/` |
| GEM-08 | Decentralised Energy, Mini-Grids & Rural Electrification | Mini-grids, off-grid, rural electrification | WS-22 | WS-07 | 2 | `01_gemini_research/GEM-08_decentralised-energy/` |
| GEM-09 | Macro, Political Economy, FX & Repatriation | Macro, political economy, currency & FX | WS-01, WS-04 | WS-09, WS-24 | 1 | `01_gemini_research/GEM-09_macro-political-fx/` |
| GEM-10 | Electricity Sector Institutions & Regulatory Framework | Electricity law, regulation & investment framework | WS-02 | WS-09, WS-22 | 1 | `01_gemini_research/GEM-10_electricity-law-regulation/` |
| GEM-11 | National Demand Baseline & Non-Mining Loads | Electricity demand, cities, industry & structural load | WS-10, WS-14 | WS-07, WS-08 | 2 | `01_gemini_research/GEM-11_demand-baseline-loads/` |
| GEM-12 | Simandou Corridor Energy (dedicated) | Simandou energy & infrastructure corridor | WS-12 | WS-06, WS-10, WS-15 | 2 | `01_gemini_research/GEM-12_simandou-corridor/` |
| GEM-13 | Technology-Neutral Resource Assessment (Solar, Wind, Hydro Sites, Storage Needs) | Resources, climate & site constraints | WS-18, WS-19, WS-20, WS-21 | WS-17, WS-26 | 2 | `01_gemini_research/GEM-13_resource-assessment/` |
| GEM-14 | Project Pipeline Consolidation & Status Verification | Existing, committed and planned project pipeline | WS-05, WS-23 | WS-06, WS-25 | 3 | `01_gemini_research/GEM-14_project-pipeline/` |
| GEM-15 | Land, Resettlement, Environmental & Biodiversity Framework | Land, environment, community & resettlement | WS-26 | WS-20 | 1 | `01_gemini_research/GEM-15_land-environment-social/` |

**Waves** (dependencies of context, not hard blockers):
- **Wave 1** (GEM-01, 02, 04, 05, 07, 09, 10, 15): no dependencies.
- **Wave 2** (GEM-03, 06, 08, 11, 12, 13): receives the relevant Wave 1 outputs as context. Gemini proposed GEM-03 → GEM-01 and GEM-06/08 → GEM-05. In addition: GEM-11 → GEM-03 and GEM-05; GEM-12 → GEM-04; GEM-13 → GEM-02 and GEM-15.
- **Wave 3** (GEM-14): consolidates the projects identified by every other mission.

**Guardrails common to all missions:**

- Cite a source for every factual claim, or mark the claim "NO SOURCE — LEAD ONLY".
- Prefer primary and French-language official sources.
- Apply the metric definitions and the two-dimensional status framework.
- Report conflicting values side by side.
- List data gaps explicitly.
- Remain technology-neutral.
- Make no recommendations and no Alendei assessment.
- Do not treat any statement in the Gate 1 architecture challenge, including your own earlier statements, as established fact.

---

## 2. Mission briefs

### GEM-01 — Fuel Logistics, Thermal Fleet & Landed Fuel Economics

- **Workstreams:** WS-03 (primary); WS-05, WS-11, WS-13, WS-14 (secondary).
- **Objective:** Map the supply chain for liquid fuels and any gas used in public and captive power generation, the thermal generation fleet, and the evidence on delivered fuel cost.
- **Scope:**
  - import volumes by product;
  - port reception and storage infrastructure and its current status;
  - coastal and inland distribution;
  - pricing, taxation and subsidy;
  - delivered-cost evidence at representative locations;
  - supply disruptions since 2016;
  - utility thermal plants and their fuel use;
  - rental or emergency power contracts;
  - documented gas or LNG import proposals, with their lifecycle stage.
- **Key questions:** WS-03 Q1–Q6; WS-05 Q5–Q6.
- **Mission-specific guardrails:**
  - Verify, and do not assume, the specific disruption event and its effects mentioned in the Gate 1 challenge.
  - Do not apply generic markup percentages. Report delivered-cost components only where a source documents them.
- **Source priorities:** petroleum agency, port and customs data → ministry → DFI and IMF diagnostics → IEA and trade data → company disclosures.

### GEM-02 — Transboundary Basin Governance, Hydrology & Hydro Seasonality

- **Workstreams:** WS-17 (primary); WS-05, WS-20 (secondary).
- **Objective:** Establish which basin institutions and agreements actually affect hydropower in Guinea, the hydrological data available, and the seasonal behaviour of hydro output.
- **Scope:**
  - basin organisations and treaties, and their relevance to existing and planned Guinea hydro;
  - water allocation and operating rules;
  - streamflow and reservoir data inventories;
  - monthly hydro generation where available;
  - how interdependent plants are operated;
  - documented wet-season spill;
  - climate variability studies.
- **Key questions:** WS-17 Q1–Q5; WS-05 Q2 and Q4.
- **Mission-specific guardrails:**
  - Classify each basin organisation as relevant, partly relevant or not relevant, with evidence. Do not assume relevance.
  - Report seasonal dependable output separately from installed capacity.
  - Treat cascade relationships between specific plants as hypotheses to verify.
- **Source priorities:** treaties and basin-organisation documents → national hydrological service and utility → DFI hydro studies → peer-reviewed research.

### GEM-03 — Mining & Industrial Energy Baseline & Captive Supply Economics

- **Workstreams:** WS-11, WS-13 (primary); WS-10, WS-12, WS-14 (secondary). GEM-12 is the dedicated primary mission for WS-12.
- **Objective:** Build a site-by-site baseline of electrical and thermal demand, current supply source, captive capacity, fuel and evidenced cost for mining operations and major industrial sites.
- **Scope:**
  - all producing and advanced mining operations, identified from the cadastre and EITI data, not from a pre-set list;
  - bauxite extraction and alumina refining, kept separate;
  - the Simandou components (mines, rail, port);
  - gold, diamonds and other minerals;
  - major non-mining industrial and port loads;
  - expansion plans, with lifecycle stage;
  - operator and parent-company decarbonisation commitments.
- **Key questions:** WS-11 Q1–Q5; WS-12 Q1–Q3; WS-13 Q1–Q4; WS-14 Q1–Q3.
- **Mission-specific guardrails:**
  - Research each refinery's load individually from project-specific sources. Do not use generic MW figures.
  - Treat the company names, ownership and asset details given in the Gate 1 challenge as leads.
  - Do not assess companies' appetite for a PPA. This is factual discovery only.
- **Source priorities:** mining cadastre, EITI and ESIA filings → DFI documents → company statutory filings and reports → press (leads only).

### GEM-04 — Mining Legal Regime, Energy-Related Obligations & Private Supply Pathways

- **Workstreams:** WS-15 (primary); WS-02 (secondary).
- **Objective:** Establish what the mining and electricity legal frameworks actually provide on local-processing obligations, infrastructure sharing, captive generation and private bilateral power supply.
- **Scope:**
  - the mining code and its amendments;
  - published mining conventions;
  - local-processing or refining obligations, their enforcement and deadlines;
  - third-party access to mining infrastructure, and whether it has been used in practice;
  - electricity-law provisions on self-generation, private sale and third-party access to networks;
  - stabilisation clauses.
- **Key questions:** WS-15 Q1–Q4; WS-02 Q4.
- **Mission-specific guardrails:**
  - Cite instrument, article and date for every legal statement.
  - Treat the code article and obligations named in the Gate 1 challenge as leads.
  - Distinguish the text of the law from how it has been applied.
- **Source priorities:** official gazette and legal texts → published contracts and EITI → DFI legal reviews → legal analyses.

### GEM-05 — Utility Operations, Financial Condition & Network Constraints

- **Workstreams:** WS-06, WS-07, WS-08, WS-09 (primary).
- **Objective:** Evidence the national utility's operational and financial condition, and the technical constraints on the network, **without presuming the conclusion**.
- **Scope:**
  - financial statements, noting whether each is audited;
  - tariffs and subsidies;
  - billing and collection by customer class;
  - losses, partitioned by type;
  - payment record towards IPPs, fuel suppliers and regional counterparties;
  - substation capacity and loading;
  - voltage and stability issues;
  - dispatch-centre capability;
  - reliability indicators.
- **Key questions:** WS-09 Q1–Q5; WS-06 Q1–Q4; WS-07 Q3; WS-08 Q1–Q3.
- **Mission-specific guardrails:**
  - Do not describe the utility as distressed, insolvent or creditworthy unless a source states it and supports it with indicators. Report the indicators themselves.
  - Do not use generic regional loss ranges.
- **Source priorities:** audited statements and official audit reports → World Bank and IMF documents → utility statistics → rating or credit assessments.

### GEM-06 — WAPP Interconnection & Cross-Border Trade Status

- **Workstreams:** WS-16 (primary); WS-06 (secondary).
- **Objective:** Verify the physical status (constructed, energised, synchronised) and the commercial status (contracts, metered flows, settlement) of Guinea's interconnections.
- **Scope:**
  - interconnector assets and border substations;
  - commercial agreements;
  - metered trade;
  - wheeling and settlement arrangements and any documented arrears;
  - synchronisation and protection arrangements;
  - WAPP master-plan projects involving Guinea;
  - benchmark-country metrics, as available.
- **Key questions:** WS-16 Q1–Q6.
- **Mission-specific guardrails:** Distinguish physical completion from energisation and from commercial activation.
- **Source priorities:** WAPP, regional regulator and interconnector-operator documents → DFI interconnection documents → IEA/IRENA.

### GEM-07 — International Finance, Bilateral Credit Lines & Country Ecosystems

- **Workstreams:** WS-24, WS-25 (primary); WS-04 (secondary).
- **Objective:** Map the financing and risk-mitigation instruments actually used for, or available to, Guinea energy projects, and build the register of international entities by origin, classified by evidence of their Guinea presence.
- **Scope:**
  - DFIs, sovereign lending, guarantees, political-risk insurance, ECA/EXIM and lines of credit, bilateral and blended finance, PPP instruments, technical assistance;
  - entities from India, China, Europe, the Middle East, the USA, Japan and Korea, Africa, and others;
  - entity types: developer, IPP, EPC, OEM, financier;
  - FX and convertibility treatment observed in actual transactions.
- **Key questions:** WS-24 Q1–Q5; WS-25 Q1–Q4; WS-04 Q5.
- **Mission-specific guardrails:**
  - Use the five presence classes (WS-25). Global presence does not imply Guinea presence.
  - Treat the entity lists and the bilateral framework agreements named in the Gate 1 challenge as leads.
  - Do not propose a financing structure.
- **Source priorities:** institutional project databases and official agreements → research databases → company disclosures → press (leads only).

### GEM-08 — Decentralised Energy, Mini-Grids & Rural Electrification

- **Workstreams:** WS-22 (primary); WS-07 (secondary).
- **Objective:** Evaluate the policy, regulatory and market framework for mini-grids and off-grid supply, and the deployment so far.
- **Scope:**
  - the rural electrification institution(s) and their current status;
  - mini-grid licensing, tariffs and subsidies;
  - deployment record;
  - solar home system markets;
  - anchor-load and productive-use models;
  - donor and DFI programmes and their eligibility rules;
  - access statistics by tier.
- **Key questions:** WS-22 Q1–Q5; WS-07 Q1.
- **Mission-specific guardrails:** Treat the programme names given in the Gate 1 challenge as leads. Report programme status using the lifecycle framework.
- **Source priorities:** agency and regulatory documents → DFI and donor programme documents → IRENA, ESMAP and research.

---

### GEM-09 — Macro, Political Economy, FX & Repatriation

- **Workstreams:** WS-01, WS-04 (primary); WS-09, WS-24 (secondary).
- **Objective:** Establish the macroeconomic, fiscal, political-economy and currency/FX conditions relevant to energy investment.
- **Scope:**
  - the structure of the economy and exports;
  - fiscal and debt position, and room for subsidies or guarantees;
  - political transitions and their documented effects on concessions;
  - country risk ratings;
  - the monetary regime, exchange-rate history, FX and repatriation regulations;
  - currency treatment in actual energy and mining transactions.
- **Key questions:** WS-01 Q1–Q5; WS-04 Q1–Q5.
- **Mission-specific guardrails:**
  - Do not presume FX scarcity, escrow requirements or the currency regime.
  - Cite legal instruments and their dates.
  - Distinguish documented events from commentary.
- **Source priorities:** central bank and government legal texts and statistics → IMF and World Bank → DFI project documents → rating agencies and ECA classifications.

### GEM-10 — Electricity Sector Institutions & Regulatory Framework

- **Workstreams:** WS-02 (primary); WS-09, WS-22 (secondary).
- **Objective:** Map the electricity law, institutions, regulation and investment framework.
- **Scope:**
  - sector legislation and decrees;
  - institutional mandates, and whether each body is operational;
  - licensing, concession, IPP, PPP and procurement routes, and their use since 2016;
  - the tariff-setting process;
  - grid code and connection rules;
  - captive, private-supply and third-party-access provisions;
  - net metering or embedded generation rules;
  - mini-grid regulation (cross-reference to GEM-08).
- **Key questions:** WS-02 Q1–Q6; WS-09 Q2.
- **Mission-specific guardrails:**
  - Cite instrument, article and date for every legal statement.
  - Distinguish the text of the law from how it is applied.
  - Treat institution names and statuses from the Gate 1 challenge as leads.
- **Source priorities:** official gazette and regulator decisions → DFI legal and regulatory diagnostics → legal analyses.

### GEM-11 — National Demand Baseline & Non-Mining Loads

- **Workstreams:** WS-10, WS-14 (primary); WS-07, WS-08 (secondary).
- **Objective:** Establish the national electricity demand baseline, its structure (cities, industry, commercial and residential) and load profiles, and the energy arrangements of non-mining loads.
- **Scope:**
  - served consumption and peak by class and region;
  - load profiles by time of day and by season;
  - suppressed, unserved and captive demand, and how each is estimated;
  - urban demand centres;
  - non-mining industry, ports and logistics, telecoms and large commercial loads;
  - backup generation;
  - existing official forecasts and their methods.
- **Key questions:** WS-10 Q1–Q5; WS-14 Q1–Q4; WS-08 Q4.
- **Mission-specific guardrails:**
  - Keep served, suppressed and unconstrained demand separate.
  - Record official forecasts with their methods; do not adopt them.
  - Do not apply generic growth rates.
- **Source priorities:** utility and system-operator data and national statistics → WAPP and DFI studies → enterprise surveys → company disclosures.

### GEM-12 — Simandou Corridor Energy (dedicated)

- **Workstreams:** WS-12 (primary); WS-06, WS-10, WS-15 (secondary).
- **Objective:** Dedicated discovery on the Simandou project and its corridor as an energy-demand and energy-infrastructure system.
- **Scope:**
  - project components (mines, rail, port), the lifecycle stage of each, and the ownership structure;
  - documented power demand and supply arrangements;
  - grid or community power commitments;
  - infrastructure-sharing provisions;
  - implications for transmission and for supply chains.
- **Key questions:** WS-12 Q1–Q4.
- **Mission-specific guardrails:**
  - Give each component its own lifecycle stage and progress condition.
  - Treat ownership, distances and asset names from the Gate 1 challenge as leads.
  - Corroborate company progress claims.
- **Source priorities:** official agreements and ESIAs → company statutory filings → investor materials → press (leads only).

### GEM-13 — Technology-Neutral Resource Assessment (Solar, Wind, Hydro Sites, Storage Needs)

- **Workstreams:** WS-18, WS-19, WS-20, WS-21 (primary); WS-17, WS-26 (secondary).
- **Objective:** Assemble resource, climate and site-constraint evidence for solar, wind and hydro development options, and for storage and hybrid needs, on an equal footing.
- **Scope:**
  - solar and wind resource datasets and any measured data;
  - seasonal profiles and how they complement each other;
  - climate effects on resource (cross-reference to GEM-02);
  - studied hydro sites (new, rehabilitation, small) and their study status;
  - documented system needs for storage;
  - existing and planned storage or hybrid projects;
  - site-constraint data sources (cross-reference to GEM-15).
- **Key questions:** WS-18 Q1–Q4; WS-19 Q1–Q4; WS-20 Q1–Q4; WS-21 Q1–Q4; WS-17 Q4.
- **Mission-specific guardrails:**
  - Apply the same method and depth to every technology.
  - Do not rank or play down any technology.
  - Do not apply universal site-exclusion thresholds.
  - Record dataset versions.
- **Source priorities:** ground measurements and national data → global resource atlases and reanalysis → DFI and WAPP studies → peer-reviewed research.

### GEM-14 — Project Pipeline Consolidation & Status Verification

- **Workstreams:** WS-05, WS-23 (primary); WS-06, WS-25 (secondary).
- **Objective:** Consolidate and verify the status of all existing (operational), committed and planned generation, storage and transmission projects.
- **Scope:**
  - operational plants (the existing-fleet register);
  - projects under construction, financially committed, in active development, announced or proposed;
  - delayed, stalled and cancelled projects;
  - de-duplication of re-announced projects;
  - sponsors, EPCs, OEMs, financiers and offtakers linked to each project.
- **Key questions:** WS-23 Q1–Q4; WS-05 Q1 and Q3.
- **Mission-specific guardrails:**
  - Apply the two-dimensional status framework strictly, citing evidence and its date for each assignment.
  - MoUs count at most as Announced.
  - Never infer "Stalled" from an absence of news.
- **Source priorities:** official project lists and DFI records → procurement records → company disclosures (corroborated) → press (leads only).

### GEM-15 — Land, Resettlement, Environmental & Biodiversity Framework

- **Workstreams:** WS-26 (primary); WS-20 (secondary).
- **Objective:** Establish the framework for land tenure, expropriation, resettlement, ESIA, environment, biodiversity and community issues, and the sources of spatial constraint data.
- **Scope:**
  - statutory and customary tenure;
  - expropriation and compensation;
  - resettlement precedents;
  - the ESIA authority, its process and timelines;
  - applicability of IFC Performance Standards;
  - protected areas, critical habitats and species of concern, and their legal status;
  - agricultural land;
  - flood and other physical climate hazards;
  - documented community conflict.
- **Key questions:** WS-26 Q1–Q6.
- **Mission-specific guardrails:**
  - Classify each constraint as a legal exclusion, a regulatory constraint or a risk flag, citing the legal basis.
  - Set no numeric thresholds.
  - Treat the species, sites and regions named in the Gate 1 challenge as leads.
- **Source priorities:** legal texts and official registries → DFI safeguard documents → global environmental datasets → NGO reports (corroborated).

---

## 3. Mission → workstream coverage matrix

The matrix is the inverse of the §1 mapping, and the Gate 1 consistency check verifies it automatically. Every discovery workstream (WS-01 to WS-26) has at least one primary mission.

| WS | Primary mission(s) | Secondary mission(s) |
|---|---|---|
| WS-01 | GEM-09 | — |
| WS-02 | GEM-10 | GEM-04 |
| WS-03 | GEM-01 | — |
| WS-04 | GEM-09 | GEM-07 |
| WS-05 | GEM-14 | GEM-01, GEM-02 |
| WS-06 | GEM-05 | GEM-06, GEM-12, GEM-14 |
| WS-07 | GEM-05 | GEM-08, GEM-11 |
| WS-08 | GEM-05 | GEM-11 |
| WS-09 | GEM-05 | GEM-09, GEM-10 |
| WS-10 | GEM-11 | GEM-03, GEM-12 |
| WS-11 | GEM-03 | GEM-01 |
| WS-12 | GEM-12 | GEM-03 |
| WS-13 | GEM-03 | GEM-01 |
| WS-14 | GEM-11 | GEM-01, GEM-03 |
| WS-15 | GEM-04 | GEM-12 |
| WS-16 | GEM-06 | — |
| WS-17 | GEM-02 | GEM-13 |
| WS-18 | GEM-13 | — |
| WS-19 | GEM-13 | — |
| WS-20 | GEM-13 | GEM-02, GEM-15 |
| WS-21 | GEM-13 | — |
| WS-22 | GEM-08 | GEM-10 |
| WS-23 | GEM-14 | — |
| WS-24 | GEM-07 | GEM-09 |
| WS-25 | GEM-07 | GEM-14 |
| WS-26 | GEM-15 | GEM-13 |
| WS-27 | NONE (by design) | NONE (by design) |
| WS-28 | NONE (by design) | NONE (by design) |

**Why WS-27 and WS-28 have no discovery mission (by design, not a gap):** they are Phase B synthesis workstreams. WS-27 may use only the project's verified registers, with "no new unsourced inputs" (charter). WS-28 may use only those registers plus the Alendei capability evidence supplied by the user, which is the only valid source of Alendei facts. Assigning them a Gemini discovery mission would bring unverified inputs into the opportunity analysis. Gemini's role for these two workstreams is the **Gate 8 adversarial review** of their outputs (`gemini_operating_instructions.md` §3).

Claude's independent discovery at Gate 2 also covers every Phase A workstream (WS-01 to WS-26).

## 4. Mission output template (required structure for every Gemini deposit)

1. **Mission metadata:** mission ID, date, workstreams covered, Gemini model and version, prompt reference.
2. **Summary of findings:** bullet points, each carrying a citation or "NO SOURCE — LEAD ONLY".
3. **Structured data table:** one row per claim, with these columns: claim · value · unit · geography · period · metric definition · lifecycle stage / progress condition (for projects) · source title · publisher · publication date · URL · page/table/section · Gemini's self-assessed confidence and reason.
4. **Source roster:** every publication cited, with its exact title, issuer, date, URL and language.
5. **Contradictions observed:** conflicting values between sources, shown side by side and not resolved.
6. **Data gaps:** the questions for which no primary evidence was found, and the sources that were tried.
7. **Leads for follow-up:** further unresolved questions that might justify a targeted mission.
