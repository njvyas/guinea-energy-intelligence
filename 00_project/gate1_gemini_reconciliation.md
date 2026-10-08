# Gate 1 — Gemini Challenge Reconciliation

**Version:** 1.0 (DRAFT, pending Gate 1 approval) · **Last updated:** 08-Oct-2026

**Input:** `01_gemini_research/00_architecture/2026-10-08_GATE1_architecture-challenge_gemini_v1.md` (Tier 6 lead; SHA-256 recorded in its `.meta.md`).
**Governing decisions:** the ChatGPT / project-owner review of 08-Oct-2026, recorded as D-024 to D-040.

**Disposition codes:**
- `ACCEPTED`: adopted as recommended.
- `ACCEPTED-MODIFIED`: adopted, with changes.
- `REJECTED`: not adopted.
- `DEFERRED`: to be decided at a later gate.

---

## 1. Gemini's 27 workstreams → final 28

| Gemini WS | Gemini title | Final | Disposition and change |
|---|---|---|---|
| 01 | Macroeconomic & Political Economy Context | WS-01 | ACCEPTED-MODIFIED: country-risk scope added |
| 02 | Institutional, Legal & Regulatory Framework | WS-02 | ACCEPTED-MODIFIED: now also owns the legal pathways for private supply (moved from Gemini 15) |
| 03 | Primary Hydrocarbon Supply Chains, Depots & Fuel Logistics | WS-03 | ACCEPTED-MODIFIED: thermal and gas technology options added (technology neutrality) |
| 04 | Macro-Financial Framework, Currency (GNF) & FX Repatriation | WS-04 | ACCEPTED-MODIFIED: currency name not presumed; escrow requirement not presumed |
| 05 | Existing Generation Fleet & Operating Performance | WS-05 | ACCEPTED-MODIFIED: explicit seasonal dependable capacity added |
| 06 | Transmission Network Topology, Substations & Stability | WS-06 | ACCEPTED-MODIFIED: reinforcement options added |
| 07 | Distribution Network, Access, Losses & Metering | WS-07 | ACCEPTED-MODIFIED: demand-side measures added |
| 08 | System Reliability, Outages & Dispatch Operations | WS-08 | ACCEPTED |
| 09 | Utility Economics, Tariffs & EDG Financial Solvency | WS-09 | ACCEPTED-MODIFIED: renamed "Counterparty Condition & Bankability"; solvency not presumed |
| 10 | Electricity Demand & Structural Load Profiles | WS-10 | ACCEPTED-MODIFIED: suppressed and captive demand, and forecast inputs, added |
| 11 | Bauxite & Alumina Energy Nexus (Maritime Guinea) | WS-11 | ACCEPTED-MODIFIED: geographic qualifier removed (not presumed); extraction and refining kept separate |
| 12 | Simandou Iron Ore Megaproject & Infrastructure Corridor | WS-12 | ACCEPTED |
| 13 | Gold, Diamonds & Other Mining Energy Operations | WS-13 | ACCEPTED-MODIFIED: "other minerals" to be identified from evidence |
| 14 | Non-Mining Industrial, Port & Commercial Energy Demand | WS-14 | ACCEPTED |
| 15 | Mining Conventions, Refinery Mandates & B2B Legal Regimes | WS-15 | ACCEPTED-MODIFIED: renamed (the existence of "mandates" is not presumed); electricity-law pathways moved to WS-02 |
| 16 | WAPP Regional Electricity Market & Cross-Border Interconnections | WS-16 | ACCEPTED-MODIFIED: benchmark universe added |
| 17 | Supranational River Basin Commissions (OMVG, OMVS, ABN) & Cascade Hydrology | WS-17 | ACCEPTED-MODIFIED: basin relevance is investigated, not presumed; climate variability added (absorbs Gate 0 `04_analysis/climate`) |
| 18 | Solar Resource Potential & Environmental Constraints | WS-18 | ACCEPTED-MODIFIED: environmental constraints moved to WS-26 |
| 19 | Wind Resource Potential & Terrain Feasibility | WS-19 | ACCEPTED-MODIFIED: full parity with other technologies (Gemini's proposal to de-emphasise wind rejected) |
| 20 | Hydro Resource Potential, Cascade Engineering & Climate Variability | WS-20 | ACCEPTED-MODIFIED: limited to development potential; existing fleet in WS-05; hydrology and climate in WS-17 |
| 21 | BESS & Grid Stability Applications | WS-21 | ACCEPTED-MODIFIED: hybridisation added |
| 22 | Decentralized Energy, Mini-Grids & Rural Productive Uses | WS-22 | ACCEPTED |
| 23 | Committed, Planned & Pipeline Projects | WS-23 | ACCEPTED-MODIFIED: owns the master project register and the status framework |
| 24 | International Financing, DFIs & Bilateral Guarantees | WS-24 | ACCEPTED-MODIFIED: full list of instruments; no structure presumed |
| 25 | Country Ecosystems: India, China, Europe, ME, USA, Japan/Korea | WS-25 | ACCEPTED-MODIFIED: OEM/EPC/IPP register and five presence classes added |
| 26 | Land Tenure, Resettlement Safeguards & Community Risk | WS-26 | ACCEPTED-MODIFIED: environmental and biodiversity constraints and GIS constraint layers added |
| 27 | Commercial Opportunity Portfolio, Structuring & Alendei Positioning | WS-27 + WS-28 | ACCEPTED-MODIFIED: **split** into the country portfolio (WS-27) and Alendei participation (WS-28), as the owner directed |

---

## 2. Gemini "Top 20 architecture changes"

| # | Gemini recommendation | Disposition | Treatment |
|---|---|---|---|
| 1 | Fuel logistics workstream | ACCEPTED | WS-03 |
| 2 | River basin governance with OMVG/OMVS/ABN quotas | ACCEPTED-MODIFIED | WS-17; relevance and quotas to be investigated |
| 3 | Audit EDG solvency, subsidies and arrears | ACCEPTED-MODIFIED | WS-09; the utility's condition is evidenced, not presumed |
| 4 | Model FX convertibility and offshore escrow | ACCEPTED-MODIFIED | WS-04; escrow requirement not presumed |
| 5 | Dedicated Simandou workstream | ACCEPTED | WS-12 |
| 6 | Land tenure, IFC PS5/PS6, chimpanzee corridors | ACCEPTED-MODIFIED | WS-26, broadened; species and site specifics to be researched |
| 7 | Decentralised electrification | ACCEPTED | WS-22 |
| 8 | Seasonal hydro derating, wet vs dry | ACCEPTED | WS-05; `methodology.md` §5 |
| 9 | Separate bauxite mining from alumina refining | ACCEPTED-MODIFIED | WS-11; Gemini's characterisation of magnitudes ("low" / "enormous") not adopted; loads are site-specific |
| 10 | 3×2 scenario matrix | ACCEPTED-MODIFIED | Scenario architecture adopted (§J); matrix shape and all of Gemini's parameters left open |
| 11 | SLD-based transmission modelling | ACCEPTED-MODIFIED | WS-06 target, as far as the data allow; the data-availability gap will be logged |
| 12 | Partition technical and commercial losses | ACCEPTED | WS-07 |
| 13 | Mine-gate landed fuel cost | ACCEPTED-MODIFIED | WS-03; evidence-based with a documented method; Gemini's markup percentages rejected |
| 14 | WAPP commercial activation vs physical construction | ACCEPTED | WS-16; §H normalisation rule |
| 15 | GIS exclusion masks incl. slope >10% | ACCEPTED-MODIFIED | Constraint layers adopted; **universal slope threshold rejected** (§L.2) |
| 16 | Mining Code "Article 130" infrastructure sharing | ACCEPTED-MODIFIED | WS-15 research question; article reference treated as a lead (GL-22) |
| 17 | MW-DC vs MW-AC | ACCEPTED | Already in `methodology.md` §5 |
| 18 | 24-month expiry flag | ACCEPTED-MODIFIED | Recency becomes a quality dimension, with mandatory re-verification of volatile data classes before deliverables; **no fixed 24-month threshold** (D-048) |
| 19 | 0–100 multi-criteria scoring | ACCEPTED-MODIFIED | Framework adopted (§K); **weights, anchors and tier thresholds rejected at Gate 1**; Alendei fit moved to a separate lens (WS-28) |
| 20 | Five-stage sequencing | ACCEPTED-MODIFIED | Eight stages, mapped to gates (§D) |

---

## 3. Other Gemini sections

| Section | Content | Disposition | Treatment |
|---|---|---|---|
| Exec. summary | "Six blind spots" | ACCEPTED-MODIFIED | Each domain is incorporated; the factual premises are logged as leads (§4) |
| B | Subdomain questions | ACCEPTED-MODIFIED | Reworded neutrally in the charters (WS-05, 06, 11, 15, 16) |
| C | Institutions and primary sources | ACCEPTED-MODIFIED | Used as candidate source targets; names and statuses logged as leads (GL-16, GL-17) |
| D | Critical datasets matrix | ACCEPTED | Included in the charters' dataset lists, with limitations noted |
| E | GIS layer stack | ACCEPTED-MODIFIED | §L; slope cut-off rejected; constraints stored as attributes |
| F | Capacity → billed-energy cascade | ACCEPTED | Analytical framework (WS-05 to WS-09). The generic loss ranges and the illustrative "450 MW → 80 MW" example are **not data** (GL-24) |
| F.3 | Inertia / grid-forming analysis | ACCEPTED-MODIFIED | WS-06 and WS-21 question, where data allow; the conclusion that BESS is "mandatory" is rejected as premature |
| G | Mining site protocol | ACCEPTED-MODIFIED | SITE schema (§G). "Willingness / appetite for hybrid IPP" removed from Phase A discovery to keep it objective; may be considered in WS-27 only where publicly evidenced |
| H | WAPP realities | ACCEPTED | WS-16 questions |
| I | Finance de-risking stack | ACCEPTED-MODIFIED | Taxonomy of instruments (WS-24); no stack presumed to be required |
| J | Country ecosystems | ACCEPTED-MODIFIED | WS-25 origin sub-registers; every entity named is a lead (GL-18 to GL-21) |
| K | Contradiction taxonomy | ACCEPTED-MODIFIED | §H. "Disregard MoUs; require financial close" harmonised with the approved framework: MoUs count at most as Announced, and Financially committed requires a binding commitment |
| L | "Hidden" commercial information | ACCEPTED-MODIFIED | Converted into neutral research questions (WS-02, 03, 15, 17); numeric claims logged as leads (GL-23, GL-25) |
| M | Project schema | ACCEPTED-MODIFIED | PRJ schema (§G); approved lifecycle labels used; PPA terms recorded only where public; evidence ID for each field |
| N | Mining company schema | ACCEPTED-MODIFIED | SITE/ENT schema; "appetite" field removed; LCOE values labelled ESTIMATED with method |
| O | Scenario definitions | ACCEPTED-MODIFIED | §J architecture; **all numeric parameters rejected** (growth rates, tonnages, refinery MW) |
| P | Scoring algorithm, anchors and thresholds | REJECTED (numeric content) / ACCEPTED (concept) | §K. The 25/20/20/20/15 weights, the ">15% IRR" and "<10 km" anchors, the tier score thresholds and the 100-point score for "offshore escrow" are all rejected as premature |
| Q.1 | Staleness, 24 months | ACCEPTED-MODIFIED | D-048 |
| Q.2 | Spatial granularity index | ACCEPTED | `methodology.md` §3 |
| Q.3 | Discloser independence flag | ACCEPTED | `methodology.md` §3 |
| Q.4 | Analytical envelope for Tier 1/2 conflicts | ACCEPTED-MODIFIED | §H `RANGE-CARRIED` outcome; the hierarchy still applies first |
| R | Sequencing | ACCEPTED-MODIFIED | §D |
| S | Eight missions | ACCEPTED (initial batch only) | Titles neutralised (§5); coverage gaps closed by follow-up missions GEM-09 – GEM-15 (D-051); all approved as architecture only |
| T | Handoff protocol | ACCEPTED-MODIFIED | §F; adds a lead register, SHA-256 integrity, UNSUPPORTED status and a mission close report. The project keeps its **six** evidence tiers (Gemini used five) |
| Synth. §6 | Merge WS 17–20 (origins/OEM) | ACCEPTED | WS-25 |
| Synth. §6 | Merge mining and industrial into commodity clusters | ACCEPTED | WS-11 to WS-15 |
| Synth. §6 | De-emphasise wind | **REJECTED** | Owner directive D-026; WS-19 has full parity |
| Synth. §6 | Remove linear extrapolation | ACCEPTED-MODIFIED | Not used as the sole method; allowed as a reference line only (D-031) |

---

## 4. Gemini factual assertions: logged as unverified leads

**None of the following is evidence.** Each is a hypothesis to be verified or refuted at Gate 2. They will be transferred to the lead register (`LEAD-` IDs) when its template is created. They are recorded here so that no Gemini premise enters the architecture unexamined.

| GL | Assertion (Gemini, unverified) | Verify in |
|---|---|---|
| GL-01 | Guinea has no operating oil refinery; thermal and captive generation depends on imported liquid fuels through Conakry port and coastal depots | WS-03 |
| GL-02 | A major Conakry oil-depot explosion in December 2023 disrupted fuel supply | WS-03 |
| GL-03 | Wet season "July–October" in one place and "July–November" in another; dry season "December–May" and "December–June". **Internally inconsistent within the Gemini document** | WS-17 |
| GL-04 | Major dams fall under OMVG/OMVS/ABN treaties with multi-country quota allocations | WS-17 |
| GL-05 | Mining is >80% of export revenue and the majority of unconstrained power demand | WS-01, WS-10 |
| GL-06 | Statutory bauxite-to-alumina refining obligations exist under mining conventions | WS-15 |
| GL-07 | Simandou: 600+ km corridor; Compagnie du Transguinéen; Moribaya port; ownership split by blocks between named consortia | WS-12 |
| GL-08 | EDG is in severe financial distress with circular debt; rental and floating power plants are involved | WS-09, WS-05 |
| GL-09 | Currency, central bank and FX regime characteristics (non-CFA, FX scarcity, surrender rules) | WS-04 |
| GL-10 | An alumina refinery adds "200–400 MW" in one place and "250–350 MW" for 1–2 Mtpa in another. **Internally inconsistent; generic** | WS-11 |
| GL-11 | Named coastal barging points and LNG/FSRU studies at named ports | WS-03 |
| GL-12 | Named upstream storage and downstream run-of-river cascade relationships on a named basin | WS-05, WS-17 |
| GL-13 | Named basin asset-holding companies | WS-17 |
| GL-14 | Named utility thermal plants | WS-05 |
| GL-15 | Named substations, the 225 kV backbone, and the name of the national dispatch centre | WS-06, WS-08 |
| GL-16 | Names, mandates and current status of ministries, agencies, the regulator ("formerly AER/ARPT") and audit bodies | WS-02 |
| GL-17 | Named World Bank, AfDB and donor programmes | WS-07, WS-22, WS-24 |
| GL-18 | A 2017 USD 20 billion Guinea–China framework agreement; named Chinese contractors as builders of named dams; other named Chinese entities and their roles | WS-24, WS-25 |
| GL-19 | Named mining companies and their assets and nationalities | WS-11–13, WS-25 |
| GL-20 | Named Indian PSUs, EPCs and miners and their track records; EXIM Bank of India credit lines to Guinea | WS-24, WS-25 |
| GL-21 | Named Middle East, European, US and Japan/Korea entities and funds as active or relevant | WS-24, WS-25 |
| GL-22 | A mining-code article ("Article 130") mandates third-party access to infrastructure | WS-15 |
| GL-23 | Delivered fuel at mines is "30–50%" above coastal retail; thermal cost is "$0.25–0.38/kWh" | WS-03 |
| GL-24 | Loss ranges: "4–8%" transmission, "8–15%" distribution, "20–35%" commercial. Generic regional figures, not Guinea data | WS-07 |
| GL-25 | Wet-season spill occurs at named hydro plants | WS-17 |
| GL-26 | Organic demand growth of "5–6% p.a."; bauxite exports reaching "130+ Mtpa" | WS-10, WS-11 |
| GL-27 | Wind resource is limited outside coastal and ridge formations | WS-19 |
| GL-28 | Chimpanzee habitat corridors; a named UNESCO site; community protest risk in named regions | WS-26 |
| GL-29 | Named railways and ports | WS-12, WS-14 |
| GL-30 | Effects of the post-2021 political transition on concessions | WS-01 |
| GL-31 | Named interconnectors, border substations, regional counterparties and a regional transmission company | WS-16 |
| GL-32 | Network voltage levels (225/110/60/33 kV) | WS-06 |
| GL-33 | Exposure of Guinea mining exports to EU CBAM | WS-11 |

**Observation on lead reliability:** the Gemini document contains at least two internal numerical inconsistencies (GL-03, GL-10). This reinforces the D-026 rule that Gemini output is a hypothesis, not evidence.

---

## 5. Mission title changes (assumptions removed)

| Mission | Gemini title | Final title | Reason |
|---|---|---|---|
| GEM-01 | Hydrocarbon Logistics, Thermal Fleet & Landed Fuel Economics | Fuel Logistics, Thermal Fleet & Landed Fuel Economics | Broadened to cover any fuel or gas |
| GEM-02 | River Basin Treaties, Hydrology & Cascade Dispatch | Transboundary Basin Governance, Hydrology & Hydro Seasonality | "Treaties" and "cascade" presumed relevance and configuration |
| GEM-03 | Mining Sector Energy Baseline & Captive Economics | Mining & Industrial Energy Baseline & Captive Supply Economics | Industrial loads added |
| GEM-04 | Mining Conventions, Refinery Mandates & B2B Legal Architecture | Mining Legal Regime, Energy-Related Obligations & Private Supply Pathways | "Mandates" and the B2B framing presumed the answer |
| GEM-05 | EDG Utility Operations, Financial Solvency & Grid Bottlenecks | Utility Operations, Financial Condition & Network Constraints | "Solvency" and "bottlenecks" presumed the conclusion |
| GEM-06 | WAPP Cross-Border Reality & Regional Interconnections | WAPP Interconnection & Cross-Border Trade Status | Neutral wording |
| GEM-07 | International Finance, Bilateral LOCs & Country Ecosystems | International Finance, Bilateral Credit Lines & Country Ecosystems | Wording only |
| GEM-08 | Decentralized Energy, Mini-Grids & Rural Electrification | Decentralised Energy, Mini-Grids & Rural Electrification | Spelling only |

---

## 6. Gemini "Top 20 questions" → workstream questions

All 20 questions are kept, reworded neutrally and allocated to a workstream. Names of plants, substations and counterparties in them are treated as leads.

| Gemini Q | Topic | Allocated to |
|---|---|---|
| 1 | Delivered fuel cost at mine sites | WS-03 Q5 |
| 2 | Legality of a private IPP selling to mines | WS-02 Q4 |
| 3 | Dry-season dependable capacity of the hydro cascade | WS-05 Q2, WS-17 Q3 |
| 4 | Refinery power and steam requirements and deadlines | WS-11 Q4, WS-15 Q2 |
| 5 | Simandou captive power plans | WS-12 Q2 |
| 6 | Utility arrears on cross-border purchases and wheeling | WS-09 Q4, WS-16 Q3 |
| 7 | Collection rate by customer class | WS-09 Q3 |
| 8 | Wet-season spill volume | WS-17 Q5 |
| 9 | Credit enhancement required for financial close | WS-09 Q5, WS-24 Q2 |
| 10 | FX surrender rules | WS-04 Q2 |
| 11 | Synchronous vs islanded interconnector operation | WS-16 Q1, Q4 |
| 12 | Substation MVA and N-1 limits | WS-06 Q2 |
| 13 | Post-incident depot capacity | WS-03 Q2, Q3 |
| 14 | Enforcement of local-processing obligations | WS-15 Q2 |
| 15 | Reserve and frequency-response requirements | WS-08 Q3 |
| 16 | Precedents for infrastructure sharing | WS-15 Q3 |
| 17 | Land compensation rates and habitat buffers | WS-26 Q2, Q4 |
| 18 | Active Indian EXIM credit lines | WS-24 Q3 |
| 19 | Effect of the political transition on concessions | WS-01 Q3 |
| 20 | Viability of LNG/FSRU versus HFO | WS-03 Q6 |
