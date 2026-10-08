# Workstream Charters — Research Architecture v1.0

**Version:** 1.0 (DRAFT — pending Gate 1 approval) · **Last updated:** 08-Oct-2026 · **Gate:** 1

This document defines each of the 28 research workstreams. It is a research design document and **contains no Guinea findings**. Wherever an institution, asset or company is named, the name is either a sponsor directive or a lead to be verified; it is not a confirmed fact.

**Conventions**

- Workstream IDs are written `WS-NN`. Analysis folders are `04_analysis/wsNN_<slug>/`. WS-27 and WS-28 outputs go in `06_opportunities/`.
- "Source priorities" lists source types in order of preference, using the evidence tiers in `methodology.md` §1.
- Every workstream follows these rules, which are not repeated in each charter:
  - the metric definitions (`methodology.md` §5);
  - the evidence states and confidence rules (`methodology.md` §2–§3);
  - the project-status framework (`methodology.md` §6);
  - the contradiction protocol (`research_architecture.md` §H);
  - technology neutrality (D-027).
- Research questions are worded neutrally. None of them assumes its answer.
- **Research-question priority.** Each question carries a qualitative planning tag: `[CRITICAL]`, `[HIGH]`, `[MEDIUM]` or `[LOW]` (rule: `methodology.md` §12).
  - The tag is a **research-planning classification only**. It is not an evidence-based conclusion, it is not evidence confidence, and it is not a factual finding about Guinea.
  - Priorities may be revised after evidence review. Gate 4 reassesses them against actual evidence gaps and decision impact.

---

## Workstream index

| ID | Workstream | Cluster | Phase | Analysis folder |
|---|---|---|---|---|
| WS-01 | Macroeconomic, Political Economy & Country Risk Context | A — Country, institutions & primary energy | A | `ws01_macro_political_economy` |
| WS-02 | Electricity Sector Institutions, Law & Regulation | A | A | `ws02_institutions_regulation` |
| WS-03 | Fuel Supply, Logistics, Landed Fuel Economics & Thermal/Gas Options | A | A | `ws03_fuel_thermal_gas` |
| WS-04 | Macro-Financial Framework, Currency, FX Convertibility & Repatriation | A | A | `ws04_macro_financial_fx` |
| WS-05 | Existing Generation Fleet, Operating Performance & Seasonal Dependable Capacity | B — Power-system baseline | A | `ws05_generation` |
| WS-06 | Transmission Network, Substations, System Stability & Reinforcement Options | B | A | `ws06_transmission` |
| WS-07 | Distribution, Access, Losses, Metering & Demand-Side Measures | B | A | `ws07_distribution_access` |
| WS-08 | Reliability, Outages & System Operations | B | A | `ws08_reliability_operations` |
| WS-09 | Utility Economics, Tariffs, Counterparty Condition & Bankability | B | A | `ws09_utility_economics` |
| WS-10 | Electricity Demand Baseline, Load Profiles & Forecast Inputs | B | A | `ws10_demand` |
| WS-11 | Bauxite Extraction & Alumina Refining Energy | C — Mining & industrial energy | A | `ws11_bauxite_alumina` |
| WS-12 | Iron Ore / Simandou Megaproject & Infrastructure Corridor | C | A | `ws12_simandou_corridor` |
| WS-13 | Gold, Diamonds & Other Strategically Relevant Minerals | C | A | `ws13_gold_diamonds_other_minerals` |
| WS-14 | Non-Mining Industrial, Ports & Logistics, and Commercial Demand | C | A | `ws14_nonmining_industrial_ports_commercial` |
| WS-15 | Mining Legal Regime, Energy-Related Obligations & Infrastructure Access | C | A | `ws15_mining_legal_regime` |
| WS-16 | WAPP, Regional Market & Cross-Border Interconnection | D — Regional market & basin governance | A | `ws16_wapp` |
| WS-17 | Transboundary River Basins, Hydrology & Climate Variability | D | A | `ws17_river_basins_hydrology_climate` |
| WS-18 | Solar Resource & Technical Potential | E — Technology & resource options | A | `ws18_solar` |
| WS-19 | Wind Resource & Technical Potential | E | A | `ws19_wind` |
| WS-20 | Hydro Development Potential (New, Rehabilitation, Small Hydro) | E | A | `ws20_hydro` |
| WS-21 | BESS, Hybridisation & Grid-Stability Applications | E | A | `ws21_bess_hybrid_stability` |
| WS-22 | Decentralised Energy, Mini-Grids & Productive Use | E | A | `ws22_decentralised_energy` |
| WS-23 | Generation & Transmission Project Pipeline | F — Pipeline, finance, ecosystem & constraints | A | `ws23_project_pipeline` |
| WS-24 | International Finance, DFI & Risk-Mitigation Instruments | F | A | `ws24_international_finance` |
| WS-25 | International Commercial Ecosystem (by Origin) & OEM/EPC/IPP Register | F | A | `ws25_international_ecosystem` |
| WS-26 | Land Tenure, Resettlement, Environmental & Biodiversity Constraints | F | A | `ws26_land_environment_social` |
| WS-27 | Commercial Opportunity Portfolio & Structuring | G — Opportunity & strategy | B | `06_opportunities/` |
| WS-28 | Alendei Strategic Participation & Ecosystem Role | G | B (last) | `06_opportunities/alendei_role/` |

**Phase A (WS-01 to WS-26)** is independent analysis of Guinea's energy system. No Alendei commercial lens is applied. **Phase B** applies WS-27 first, then WS-28 (D-028).

---

## Technology-option coverage (technology neutrality check)

Every option the sponsor named must have a workstream responsible for assessing it on evidence. No option is ranked or excluded in advance.

| Option | Assessed in | Integrated in |
|---|---|---|
| Solar PV | WS-18 | WS-27 |
| Wind | WS-19 | WS-27 |
| Hydro (new, rehabilitation, small) | WS-20 (existing fleet: WS-05) | WS-27 |
| BESS | WS-21 | WS-27 |
| Thermal (liquid fuels) and gas import options | WS-03 (existing fleet: WS-05) | WS-27 |
| Hybrid systems (any combination) | WS-21 | WS-27 |
| Grid reinforcement / transmission expansion | WS-06 | WS-27 |
| Regional imports/exports | WS-16 | WS-27 |
| Demand-side measures, efficiency, loss reduction | WS-07, WS-10 | WS-27 |
| Mini-grids and off-grid systems | WS-22 | WS-27 |
| Captive / self-generation (incumbent baseline) | WS-11–WS-14 | WS-27 |

---

## Mapping from the Gate 0 architecture (20 workstreams)

| Gate 0 workstream | Now covered by |
|---|---|
| 1 Country energy landscape | WS-01, plus WS-10 for the energy-demand context |
| 2 Institutions and regulation | WS-02 |
| 3 Generation | WS-05 |
| 4 Transmission | WS-06 |
| 5 Distribution | WS-07 |
| 6 Reliability | WS-08 |
| 7 Electricity demand | WS-10 |
| 8 Mining | WS-11, WS-12, WS-13, WS-15 |
| 9 Industrial energy | WS-14 |
| 10 WAPP | WS-16 |
| 11 Solar | WS-18 |
| 12 Wind | WS-19 |
| 13 Hydro | WS-20 (development potential), WS-05 (existing fleet, seasonal dependable capacity), WS-17 (hydrology) |
| 14 BESS | WS-21 |
| 15 Future project pipeline | WS-23 |
| 16 International / DFI ecosystem | WS-24 |
| 17 India, 18 China, 19 Europe/ME/USA/Japan/Korea, 20 OEM/EPC/IPP | WS-25 (consolidated, with origin sub-registers) |
| Gate 0 `04_analysis/climate` (cross-cutting) | WS-17 (climate effects on hydrology), WS-26 (physical hazard constraints) |
| *New* | WS-03, WS-04, WS-09, WS-12, WS-15, WS-17, WS-22, WS-26, WS-27, WS-28 |

---

# Cluster A — Country, Institutions & Primary Energy

## WS-01 — Macroeconomic, Political Economy & Country Risk Context

- **Objective:** Establish the macroeconomic, fiscal and political-economy context that bears on energy-sector investment and policy, 2016–2026, and the outlook to 2035.
- **Scope:** GDP and its structure; fiscal position and public debt; the export base; governance and institutional stability; changes of government and how they affected energy and mining contracts; country risk ratings; sanctions or donor-relationship constraints, where any exist. Excludes FX and convertibility mechanics, which belong to WS-04.
- **Principal questions:**
  1. **[HIGH]** What is the structure of the economy and the export base, and how concentrated is it?
  2. **[HIGH]** What are the fiscal and debt positions, and how much room do they leave for energy subsidies or sovereign guarantees?
  3. **[HIGH]** How have political transitions since 2016 affected existing energy and mining concessions, and investor confidence?
  4. **[MEDIUM]** What country-risk assessments do rating agencies, export credit agencies and DFIs publish, and what drives them?
  5. **[MEDIUM]** Which national development strategies set energy-sector priorities, and what targets do they contain?
- **Required datasets:** National accounts; IMF programme and Article IV documents; public debt statistics; export statistics by product; country risk ratings; the texts of national development plans.
- **Source priorities:** Government statistics and planning documents (T1) → IMF and World Bank (T2) → rating agencies and ECA country classifications (T3/T4) → reputable analysis (T5, context only).
- **Dependencies:** None. This is a foundation workstream.
- **Expected outputs:** A country context note; a country-risk factor table; macro inputs for scenarios (WS-10 and the integrated model).
- **Validation requirements:** Use the latest official vintage, and record which vintage was used. Flag any revisions. Take political-economy statements from documented events, not commentary.
- **Downstream consumers:** WS-04, WS-09, WS-10, WS-24, WS-27, the integrated scenario model, report chapter 1.

## WS-02 — Electricity Sector Institutions, Law & Regulation

- **Objective:** Map the legal, institutional and regulatory framework that governs electricity generation, transmission, distribution, trade, private participation and tariffs.
- **Scope:**
  - Sector legislation and implementing decrees.
  - Institutional mandates (ministry, utility or utilities, regulator, rural electrification agency, planning bodies). Whether each body currently exists and is operational is to be verified.
  - Licensing and concession regimes.
  - IPP, PPP and procurement rules.
  - Tariff-setting process.
  - Grid code and connection rules.
  - **The legal pathways for captive generation, private bilateral supply and third-party access over the network** (Gemini lead; to be researched, not assumed).
  - Net metering or embedded generation rules, if any.
  - Excludes mining-law provisions, which belong to WS-15.
- **Principal questions:**
  1. **[CRITICAL]** Which laws and decrees currently govern the electricity sector, and when were they last amended?
  2. **[HIGH]** Which institutions hold which mandates, and which of them are operational in practice?
  3. **[HIGH]** What licensing, concession and procurement routes exist for IPPs, and what have they been used for since 2016?
  4. **[CRITICAL]** Is private generation for self-use, or private sale to a third party, legally permitted? Under what conditions, and with or without the utility as intermediary?
  5. **[HIGH]** How are tariffs set, by whom, and how often? Are determinations published?
  6. **[MEDIUM]** What grid-connection and grid-code requirements apply to new generation?
- **Required datasets:** Legal texts (Journal Officiel or equivalent official publication); regulator decisions; procurement notices and awards; concession and PPA registries, where public.
- **Source priorities:** Official legal texts and regulator decisions (T1) → DFI legal and regulatory diagnostics (T2) → law-firm and academic analyses (T3/T4, interpretive only).
- **Dependencies:** None. This is a foundation workstream.
- **Expected outputs:** An institutional map; a legal-instrument register; a private-participation pathways matrix; a tariff-process description.
- **Validation requirements:** Each legal statement must cite the instrument, article and date, and must be checked against the latest amendment. Interpretations are labelled as inferences and carry the professional-verification caveat. Regulatory information carries a "may be outdated — verify against the current official text" flag.
- **Downstream consumers:** WS-09, WS-15, WS-16, WS-22, WS-23, WS-27, WS-28.

## WS-03 — Fuel Supply, Logistics, Landed Fuel Economics & Thermal/Gas Options

- **Objective:** Establish how liquid fuels (and any gas) reach power plants and mining or industrial sites, the delivered cost, the resilience of the supply chain, and the technical and economic case for thermal and gas-import options.
- **Scope:** Import volumes by product; port reception and storage infrastructure and its current status; inland and coastal distribution; fuel pricing, taxation and subsidy; delivered (landed) cost to representative locations; supply disruption history; LNG/gas import proposals, if any; thermal technology options (engines, turbines, dual-fuel) evaluated on equal terms with other technologies.
- **Principal questions:**
  1. **[HIGH]** What fuels are used for public and captive power generation, and in what volumes?
  2. **[HIGH]** What import, storage and distribution infrastructure exists? What is its operational status and redundancy?
  3. **[MEDIUM]** What supply disruptions have occurred since 2016, and what was their effect on generation? (A specific disruption event cited by Gemini is a lead to verify.)
  4. **[HIGH]** How are fuel prices set? What taxes and subsidies apply to power-sector and mining fuel?
  5. **[CRITICAL]** What is the evidenced delivered fuel cost at representative coastal and inland locations, and how does it break down?
  6. **[MEDIUM]** Are there documented gas or LNG import proposals, and at what lifecycle stage?
- **Required datasets:** Fuel import statistics; port throughput; depot capacities; price structures; delivered-cost evidence (company disclosures, ESIAs, DFI diagnostics); disruption records.
- **Source priorities:** Government, petroleum-agency, port and customs data (T1) → DFI and IMF diagnostics (T2) → IEA and trade data (T3) → company disclosures (T4).
- **Dependencies:** WS-02 (regulatory context); WS-01 (subsidy and fiscal context).
- **Expected outputs:** A fuel supply-chain map; a delivered-fuel-cost evidence table with stated method; a thermal/gas options note; the fuel-logistics GIS layer.
- **Validation requirements:** Every cost figure states its location, date, fuel grade, currency and cost components. Estimates of delivered cost follow a documented method and are labelled ESTIMATED. No markup percentage from Gemini may be used without primary support.
- **Downstream consumers:** WS-05, WS-09, WS-11–WS-14, WS-27, the integrated model.

## WS-04 — Macro-Financial Framework, Currency, FX Convertibility & Repatriation

- **Objective:** Establish the actual currency, FX and capital-repatriation conditions that affect PPAs, debt service and dividends for energy projects.
- **Scope:**
  - The monetary regime and the central bank's FX regulations.
  - Surrender or repatriation requirements.
  - Conditions on FX availability.
  - Rules on the currency of contracts (PPA indexation).
  - How convertibility and transfer risk have been treated in actual energy and mining transactions.
  - **Whether offshore escrow or other structures are required or commonly used.** This is to be investigated, not assumed (D-026).
  - Excludes DFI instruments themselves, which belong to WS-24.
- **Principal questions:**
  1. **[MEDIUM]** What monetary and exchange-rate regime applies, and how has the exchange rate behaved over 2016–2026?
  2. **[CRITICAL]** Which FX regulations apply to export earnings, foreign-currency contracts, debt service and dividend repatriation?
  3. **[HIGH]** Has FX availability for transfers been constrained, and is that documented?
  4. **[HIGH]** In which currency have existing energy PPAs and concessions been denominated or indexed?
  5. **[HIGH]** What mechanisms (escrow, offshore accounts, guarantees, insurance) have actual Guinea energy or mining transactions used, and were they required by regulation or by lenders?
- **Required datasets:** Central-bank regulations and statistics; IMF reports; exchange-rate series; transaction disclosures (DFI project documents, company filings).
- **Source priorities:** Central-bank and government legal texts (T1) → IMF and World Bank (T2) → DFI project documents (T2) → law-firm and rating analyses (T3/T4).
- **Dependencies:** WS-01.
- **Expected outputs:** An FX and repatriation framework note; a matrix of transaction precedents; currency-risk inputs for WS-27 screening.
- **Validation requirements:** Regulatory statements cite the instrument and its date and carry the possibly-outdated flag. Any statement about what is "required" must be backed by a legal text or documented lender requirements.
- **Downstream consumers:** WS-09, WS-24, WS-27, WS-28.

---

# Cluster B — Power-System Baseline

## WS-05 — Existing Generation Fleet, Operating Performance & Seasonal Dependable Capacity

- **Objective:** Reconstruct the existing generation fleet, plant by plant, and its actual (not nameplate) contribution, including **explicit seasonal dependable capacity for hydro** (D-037).
- **Scope:**
  - All grid-connected public, IPP and rental/emergency generation.
  - For each plant: installed, available, dependable and dispatched capacity; gross and net generation; for thermal plant, heat rates and fuel use; ambient derating.
  - For hydro plant: dependable capacity by month or season.
  - Rental and emergency power contract terms, where public.
  - Captive generation is covered in WS-11–WS-14 but reconciled here.
- **Principal questions:**
  1. **[CRITICAL]** Which plants are operational, with what installed capacity, and in MW-AC or MW-DC for solar?
  2. **[CRITICAL]** What is each plant's available and dependable capacity, and how does hydro dependable capacity vary through the year?
  3. **[HIGH]** What was annual and monthly generation by plant over 2016–2026?
  4. **[HIGH]** How are interdependent hydro plants operated? Who decides dispatch priority, and under what rules? (Cascade coupling between specific plants, cited by Gemini, is a lead to verify.)
  5. **[MEDIUM]** What rental or emergency capacity has been contracted since 2016, on what terms and at what cost?
  6. **[MEDIUM]** What are the thermal heat rates, fuel types and derating factors, where documented?
- **Required datasets:** Plant-level generation and availability data; hydro monthly generation series; fuel consumption logs; rental contract disclosures; DFI supervision reports.
- **Source priorities:** Utility and system-operator reports (T1) → DFI appraisal and supervision documents (T2) → IEA/IRENA statistics (T3) → owner/OEM disclosures (T4).
- **Dependencies:** WS-02, WS-03, WS-17 (hydrology inputs).
- **Expected outputs:**
  - A plant register, linked to the project register. Operational plants are recorded as projects with lifecycle stage "Operational".
  - A capacity cascade: installed → available → dependable → dispatched.
  - Seasonal dependable-capacity tables for hydro.
  - A generation time series.
- **Validation requirements:**
  - Hydro plants carry both nameplate MW and seasonal dependable MW. An annual average is never used alone.
  - Each capacity figure carries its metric definition.
  - Rental capacity is distinguished from owned capacity.
- **Downstream consumers:** WS-08, WS-09, WS-16, WS-20, WS-21, WS-23, WS-27, the integrated model.

## WS-06 — Transmission Network, Substations, System Stability & Reinforcement Options

- **Objective:** Reconstruct the transmission network's topology, capacity and technical constraints, and identify the documented options for reinforcing it.
- **Scope:**
  - Lines by voltage, length and conductor rating.
  - Status of each line: constructed, energised or in commercial use.
  - Substations: transformer capacity and N-1 status, where documented.
  - Reactive power and voltage issues; system inertia and frequency stability, where evidenced.
  - SCADA and EMS capability.
  - Planned reinforcements.
  - Interconnector physical assets are recorded here; their commercial use belongs to WS-16.
- **Principal questions:**
  1. **[CRITICAL]** What is the transmission topology? Which lines and substations are energised versus only constructed?
  2. **[HIGH]** What are the substation transformer capacities and loading levels, and where are the documented constraints?
  3. **[MEDIUM]** Are voltage, reactive-power or stability problems documented, and what mitigation is installed or planned?
  4. **[MEDIUM]** What is the dispatch centre's monitoring and control capability?
  5. **[HIGH]** What reinforcement projects are planned, at what lifecycle stage?
- **Required datasets:** Network maps and single-line diagrams; substation data; grid studies; master plans; DFI transmission project documents.
- **Source priorities:** Utility and system-operator documents and master plans (T1) → WAPP master plans and DFI project documents (T1/T2) → engineering studies (T3).
- **Dependencies:** WS-02, WS-05.
- **Expected outputs:** A network topology dataset (GIS); a substation capacity table; a constraints register; a reinforcement-options list.
- **Validation requirements:** A line counts as "Operational" only with evidence that it is energised (`methodology.md` §6.4). Constructed, energised and commercially active kilometres are recorded separately.
- **Downstream consumers:** WS-08, WS-16, WS-21, WS-23, WS-27, GIS, the integrated model.

## WS-07 — Distribution, Access, Losses, Metering & Demand-Side Measures

- **Objective:** Characterise the distribution system, electricity access, losses and metering, and the documented demand-side and loss-reduction options.
- **Scope:**
  - Distribution network extent.
  - Connections by customer class.
  - Access rates, split by urban/rural and by access tier.
  - Technical versus non-technical losses.
  - Metering (including prepaid), billing and collection at the operational level.
  - Demand-side and efficiency programmes.
  - Financial collection analysis belongs to WS-09.
- **Principal questions:**
  1. **[HIGH]** What are access rates by geography and by access tier, and how do the sources define them?
  2. **[MEDIUM]** How many customers are there by class, and how has this changed since 2016?
  3. **[HIGH]** What are transmission, distribution-technical and commercial losses, and how is each measured?
  4. **[MEDIUM]** What metering and loss-reduction programmes exist, and what have their results been?
  5. **[LOW]** What demand-side or efficiency measures are documented?
- **Required datasets:** Utility customer statistics; access surveys (multi-tier framework, household surveys); loss audits; DFI distribution project documents.
- **Source priorities:** Utility data and national surveys (T1) → World Bank access data and DFI project documents (T2) → IEA/IRENA (T3).
- **Dependencies:** WS-02, WS-06.
- **Expected outputs:** An access matrix (geography × tier); a loss-partition table; a summary of metering and programmes.
- **Validation requirements:**
  - Access rates are disaggregated by definition (grid connection versus multi-tier framework tier) and by urban/rural.
  - Losses are partitioned and the method is stated.
  - Generic regional loss ranges are never substituted for Guinea data.
- **Downstream consumers:** WS-09, WS-10, WS-22, WS-27.

## WS-08 — Reliability, Outages & System Operations

- **Objective:** Measure actual supply reliability and system-operations performance.
- **Scope:** Outage frequency and duration; load-shedding practice; unserved energy; system-wide disturbances; reserve and frequency-control practice; dispatch procedures; customer-side backup generation as an indicator of unreliability.
- **Principal questions:**
  1. **[HIGH]** What reliability indicators (e.g. SAIDI, SAIFI, hours of supply) are published, and what do they show by region and season?
  2. **[HIGH]** What is the evidence of load shedding and unserved energy, and what drives it?
  3. **[MEDIUM]** What reserve, frequency-control and load-shedding protection practices exist?
  4. **[MEDIUM]** How widespread is customer backup generation, and what does it imply about suppressed demand?
  5. **[LOW]** What independent indicators (e.g. night-time lights) corroborate the official reliability data?
- **Required datasets:** Utility outage statistics; enterprise surveys; DFI reports; satellite night-time light composites.
- **Source priorities:** Utility and system-operator data (T1) → World Bank enterprise surveys and DFI reports (T2) → remote sensing and peer-reviewed studies (T3).
- **Dependencies:** WS-05, WS-06, WS-07.
- **Expected outputs:** A reliability profile; an estimate of unserved and suppressed demand (with method); notes on system operations.
- **Validation requirements:**
  - Satellite-derived indicators are corroborating evidence only. Their limitations (e.g. cloud cover) must be stated.
  - Suppressed-demand estimates are labelled ESTIMATED, with the method shown.
- **Downstream consumers:** WS-10, WS-21, WS-27, the integrated model.

## WS-09 — Utility Economics, Tariffs, Counterparty Condition & Bankability

- **Objective:** Evidence the national utility's financial and operational condition as a counterparty, and the tariff and subsidy framework. **No conclusion about the utility's condition is assumed in advance** (D-026).
- **Scope:**
  - Utility financial statements: revenue, costs, cash collection, receivables, payables and arrears.
  - Tariff schedules by class, and cost recovery.
  - Government subsidies and transfers.
  - Payment record towards IPPs, fuel suppliers and cross-border counterparties.
  - Audit findings.
  - Bankability indicators used by lenders.
- **Principal questions:**
  1. **[CRITICAL]** What do the utility's audited (or otherwise published) financial statements show for 2016–2026?
  2. **[HIGH]** What are the tariffs by customer class? How do they compare with the cost of supply, and how are gaps funded?
  3. **[HIGH]** What are the collection rates by customer class, and the trends in receivables and arrears?
  4. **[CRITICAL]** What is the documented payment record towards IPPs, fuel suppliers and regional counterparties?
  5. **[HIGH]** What credit enhancement have lenders and DFIs required for utility-offtake projects, and why?
- **Required datasets:** Financial statements; tariff schedules; government budget and subsidy data; supreme audit institution reports; IMF and World Bank documents; DFI project documents.
- **Source priorities:** Audited statements and official audit reports (T1) → IMF and World Bank (T2) → rating or credit assessments (T3) → press (T5, leads only).
- **Dependencies:** WS-02, WS-04, WS-05, WS-07.
- **Expected outputs:** A counterparty assessment with explicit evidence; a tariff and subsidy note; bankability inputs for WS-27.
- **Validation requirements:**
  - Financial statements are noted as audited or unaudited.
  - Any characterisation (e.g. "distressed", "creditworthy") must be supported by stated indicators.
  - Discloser independence is recorded.
- **Downstream consumers:** WS-16, WS-24, WS-27, WS-28.

## WS-10 — Electricity Demand Baseline, Load Profiles & Forecast Inputs

- **Objective:** Establish the national demand baseline (served, suppressed and captive) and the structured inputs for the scenario architecture (`research_architecture.md` §J).
- **Scope:**
  - Energy consumption by customer class.
  - Served peak and average demand.
  - Daily, seasonal and annual load profiles.
  - Estimates of suppressed and unserved demand.
  - Household and residential urban demand.
  - Integration of the segment demand produced by WS-11–WS-14 and WS-22.
  - Demand drivers (population, urbanisation, GDP, electrification).
- **Principal questions:**
  1. **[CRITICAL]** What were served energy consumption and peak demand over 2016–2026, by class and region where available?
  2. **[HIGH]** What do load profiles look like by time of day and by season?
  3. **[HIGH]** How large are suppressed and captive demand, and by what method is each estimated?
  4. **[HIGH]** What drives demand growth, and which sources forecast it, with what methods and assumptions?
  5. **[MEDIUM]** How do existing official forecasts compare with each other and with outturn?
- **Required datasets:** Utility sales and load data; system-operator load curves; census and urbanisation data; existing master-plan forecasts; segment outputs from WS-11–WS-14.
- **Source priorities:** Utility, system-operator and national statistics (T1) → WAPP and DFI forecasts (T1/T2) → research (T3).
- **Dependencies:** WS-01, WS-07, WS-08, WS-11–WS-14, WS-22.
- **Expected outputs:** A demand baseline; a load-profile set; a register of forecast inputs; a review of existing forecasts.
- **Validation requirements:**
  - Served, suppressed and unconstrained demand are kept distinct.
  - Peak is distinguished from average.
  - Existing forecasts are recorded with their methods. They are not adopted without review.
- **Downstream consumers:** The integrated scenario model, WS-16, WS-27.

---

# Cluster C — Mining & Industrial Energy

All Cluster C workstreams collect data at **company, site and project level** wherever possible, using the entity register schema (`research_architecture.md` §G). Load magnitudes, including any alumina refinery load, are researched individually for each plant or project, and **no generic figure is assumed** (D-026, D-036).

## WS-11 — Bauxite Extraction & Alumina Refining Energy

- **Objective:** Quantify the electrical and thermal energy demand and supply arrangements of bauxite extraction and of alumina refining, treating the two separately.
- **Scope:**
  - Bauxite: mines, processing, rail and port loads.
  - Alumina refineries: existing, under construction and planned.
  - Captive generation (capacity, fuel, cost).
  - Process steam versus electrical demand.
  - Grid connection status.
  - Expansion plans, with their lifecycle stage.
  - Decarbonisation commitments of the operators and their parent companies.
- **Principal questions:**
  1. **[CRITICAL]** Which bauxite operations and alumina refineries exist or are planned, who operates them, and at what lifecycle stage is each?
  2. **[CRITICAL]** For each site, what are the documented electrical and thermal demand and the current supply source?
  3. **[HIGH]** What captive capacity and fuel are used, and at what evidenced cost?
  4. **[HIGH]** What refinery-specific energy requirements are documented in each project's own disclosures (ESIA, feasibility study, filings)?
  5. **[MEDIUM]** What decarbonisation targets or energy procurement policies apply at operator or parent level?
- **Required datasets:** Mining cadastre; EITI reports; company annual reports and filings; ESIAs; project feasibility disclosures.
- **Source priorities:** Mining cadastre, EITI and ESIA filings (T1) → DFI documents (T2) → company disclosures (T4, authoritative for the company's own facts) → press (T5).
- **Dependencies:** WS-03, WS-15.
- **Expected outputs:** Site-level entity records; a segment demand table (served, captive, potential); inputs to the scenario drivers.
- **Validation requirements:**
  - Demand from extraction and from refining is kept separate.
  - Planned refinery loads are classified by lifecycle stage.
  - Each load figure cites a project-specific source.
- **Downstream consumers:** WS-10, WS-21, WS-27, the integrated model, GIS.

## WS-12 — Iron Ore / Simandou Megaproject & Infrastructure Corridor

- **Objective:** Dedicated research on the Simandou project (named by the sponsor) and its associated rail, port and corridor infrastructure, as an energy demand and energy-infrastructure system.
- **Scope:**
  - Project ownership and structure.
  - Lifecycle stage of each component (mines, rail, port).
  - Power requirements and supply plans (captive, grid, hybrid).
  - Corridor-related grid or community electrification commitments.
  - Infrastructure-sharing provisions.
  - Ownership, distances and asset names given by Gemini are leads to verify.
- **Principal questions:**
  1. **[HIGH]** What are the project's components and ownership structure, and what is the current lifecycle stage of each component?
  2. **[CRITICAL]** What are the documented power demand and supply arrangements for the mines, rail and port?
  3. **[HIGH]** Do any commitments exist to supply or share power or infrastructure with the national grid or with communities?
  4. **[MEDIUM]** What effect could the project have on regional demand, on transmission needs, and on supply chains (fuel, equipment)?
- **Required datasets:** Government conventions and agreements (where public); company filings and investor materials; ESIAs; DFI or ECA documents, if any.
- **Source priorities:** Official agreements and ESIAs (T1) → company statutory filings (T1/T4) → investor presentations (T4) → press (T5).
- **Dependencies:** WS-15, WS-03.
- **Expected outputs:** A Simandou energy profile; component status table; demand scenario inputs; corridor GIS layer.
- **Validation requirements:** Each component carries its own lifecycle stage and progress condition. Company claims about progress are corroborated before the component is staged at Financially committed or later.
- **Downstream consumers:** WS-06, WS-10, WS-27, the integrated model, GIS.

## WS-13 — Gold, Diamonds & Other Strategically Relevant Minerals

- **Objective:** Quantify the energy demand and supply arrangements of gold, diamond and other strategically relevant mining (industrial and, where material, artisanal).
- **Scope:** Operations, their lifecycle stages and captive supply; energy intensity of processing; expansion plans; other minerals, to be identified from the cadastre and EITI data, not assumed.
- **Principal questions:**
  1. **[HIGH]** Which gold, diamond and other mineral operations are producing or advancing, and where?
  2. **[HIGH]** What are their documented power demand, supply source and cost?
  3. **[MEDIUM]** Are any other minerals strategically relevant for future energy demand, on the evidence?
  4. **[LOW]** Is artisanal mining a material energy-demand segment?
- **Required datasets:** Mining cadastre; EITI; company disclosures; ESIAs.
- **Source priorities:** As for WS-11.
- **Dependencies:** WS-03, WS-15.
- **Expected outputs:** Site-level entity records; a segment demand table.
- **Validation requirements:** As for WS-11.
- **Downstream consumers:** WS-10, WS-22, WS-27, GIS.

## WS-14 — Non-Mining Industrial, Ports & Logistics, and Commercial Demand

- **Objective:** Quantify demand and supply arrangements outside mining: manufacturing, agro-processing, ports and logistics, telecoms, and large commercial and urban loads.
- **Scope:** Industrial zones and large consumers; port electricity demand and supply; telecom tower energy; commercial and institutional loads; captive generation in these segments.
- **Principal questions:**
  1. **[HIGH]** Who are the largest non-mining consumers, and what is their demand and supply source?
  2. **[MEDIUM]** What are the energy demand and supply arrangements at the principal ports and logistics hubs?
  3. **[MEDIUM]** How much captive and backup generation do non-mining industrial and commercial customers use?
  4. **[MEDIUM]** What industrial or special-economic-zone developments are planned, and at what stage?
- **Required datasets:** Industrial registries; utility large-customer data; port authority reports; enterprise surveys; telecom regulator data.
- **Source priorities:** Government, utility and port data (T1) → DFI and enterprise surveys (T2) → company disclosures (T4).
- **Dependencies:** WS-03, WS-07.
- **Expected outputs:** Segment entity records; a segment demand table.
- **Validation requirements:** Site-level figures are sourced individually. Aggregates show how they were built up.
- **Downstream consumers:** WS-10, WS-22, WS-27, GIS.

## WS-15 — Mining Legal Regime, Energy-Related Obligations & Infrastructure Access

- **Objective:** Establish what the mining legal framework actually requires or enables with respect to energy, local processing and infrastructure sharing.
- **Scope:**
  - The mining code and its amendments.
  - Mining conventions, where public.
  - Any local-processing or refining obligations, and how they are enforced.
  - Third-party access to mining infrastructure (ports, rail, power lines). A specific code article cited by Gemini is a lead to verify.
  - Energy-related obligations on concessionaires.
  - Stabilisation clauses.
  - Excludes electricity-law pathways for private supply, which belong to WS-02.
- **Principal questions:**
  1. **[HIGH]** What does the current mining code provide on energy, local processing and infrastructure sharing?
  2. **[HIGH]** Do refining or local-processing obligations exist? In which instruments, with what deadlines, and how have they been enforced?
  3. **[MEDIUM]** Have infrastructure-sharing or third-party access provisions ever been applied in practice?
  4. **[HIGH]** How do mining conventions treat power supply (captive rights, grid obligations, fuel tax treatment)?
- **Required datasets:** Legal texts; published conventions; EITI contract disclosures; arbitration records.
- **Source priorities:** Official legal texts and published contracts (T1) → EITI and DFI legal reviews (T1/T2) → legal analyses (T3/T4).
- **Dependencies:** WS-02.
- **Expected outputs:** A matrix of mining-law energy provisions; an obligations and enforcement record.
- **Validation requirements:** As for WS-02 (instrument, article and date; possibly-outdated flag; professional-verification caveat).
- **Downstream consumers:** WS-11–WS-13, WS-27.

---

# Cluster D — Regional Market & Basin Governance

## WS-16 — WAPP, Regional Market & Cross-Border Interconnection

- **Objective:** Establish the physical and commercial status of Guinea's regional interconnections and its position in the WAPP market, and benchmark Guinea against the regional universe.
- **Scope:**
  - Interconnector assets and whether each is energised and synchronised.
  - Commercial agreements (power purchase, transmission service).
  - Actual metered trade flows.
  - Wheeling charges and settlement.
  - Regional market rules and regulator decisions.
  - WAPP master-plan projects involving Guinea.
  - Benchmark metrics for the seven benchmark countries.
- **Principal questions:**
  1. **[CRITICAL]** Which interconnectors are constructed, energised, synchronised and commercially active?
  2. **[HIGH]** What cross-border trade (MWh) has actually taken place, in which direction, and under what contracts?
  3. **[HIGH]** What wheeling and settlement arrangements apply, and is any arrears position documented?
  4. **[MEDIUM]** What technical conditions govern synchronous operation and protection against system separation?
  5. **[MEDIUM]** What role do the WAPP master plans assign to Guinea, and how have those plans changed over time?
  6. **[MEDIUM]** How does Guinea compare with the benchmark countries on agreed metrics?
- **Required datasets:** WAPP master plans and reports; regional regulator decisions; interconnector operator reports; trade and metering data; benchmark-country statistics.
- **Source priorities:** WAPP, ECOWAS regional regulator and interconnector-operator documents (T1) → DFI interconnection project documents (T2) → IEA/IRENA (T3).
- **Dependencies:** WS-05, WS-06, WS-09.
- **Expected outputs:** An interconnection status table; a trade-flow series; a regional market note; a benchmark table.
- **Validation requirements:**
  - Physical completion, energisation and commercial activation are recorded separately.
  - Benchmark metrics use identical definitions across countries, and any difference is recorded.
- **Downstream consumers:** WS-27, the integrated model (import/export scenarios).

## WS-17 — Transboundary River Basins, Hydrology & Climate Variability

- **Objective:** Investigate which transboundary basin institutions and agreements actually affect hydropower in Guinea, and establish the hydrological basis (flows, seasonality, variability, climate trends) for dependable hydro capacity.
- **Scope:**
  - Basin organisations and treaties. **OMVG, OMVS and ABN were named by the sponsor or Gemini; their relevance is to be investigated, not assumed** (D-037).
  - Water allocation and operating rules.
  - Basin asset-holding companies.
  - Streamflow and reservoir data.
  - Seasonal and inter-annual variability.
  - Climate-change projections relevant to hydrology.
  - Wet-season spill or curtailment, if documented.
- **Principal questions:**
  1. **[HIGH]** Which basin organisations and agreements have jurisdiction over rivers with existing or planned Guinea hydropower, and what obligations do they impose?
  2. **[CRITICAL]** What streamflow, reservoir and gauge data exist, for which periods, and of what quality?
  3. **[CRITICAL]** What are the seasonal and inter-annual flow patterns at existing and candidate hydro sites?
  4. **[MEDIUM]** What do climate studies project for hydrological variability over 2030–2035?
  5. **[MEDIUM]** Is wet-season spill or curtailment documented, and why does it occur?
- **Required datasets:** Basin-organisation documents; treaties; hydrological gauge series; reanalysis and climate projection datasets; dam operating reports.
- **Source priorities:** Treaties and basin-organisation documents (T1) → national hydrological services (T1) → DFI hydro studies (T2) → peer-reviewed hydrology and climate research (T3) → global reanalysis datasets (T3).
- **Dependencies:** WS-02.
- **Expected outputs:** A basin-relevance matrix (relevant / partly relevant / not relevant, with evidence); a hydrological data inventory; seasonal flow profiles; climate variability inputs.
- **Validation requirements:** Basin relevance is classified on evidence. Data gaps in the hydrological records are disclosed. Climate projections cite model and scenario.
- **Downstream consumers:** WS-05, WS-20, WS-21, WS-27, the integrated model, GIS.

---

# Cluster E — Technology & Resource Options

All Cluster E workstreams are **technology-neutral and evidence-led**. No technology is promoted, ranked or played down before evidence supports it (D-027). The resource and technical-potential method is applied consistently across technologies.

## WS-18 — Solar Resource & Technical Potential

- **Objective:** Assess the solar resource and technical potential on the same basis as other technologies.
- **Scope:** Global horizontal and plane-of-array irradiance; seasonal profiles; soiling and aerosol effects; temperature; grid-proximate technical potential (with constraints from WS-26 applied as layers, not fixed thresholds); existing and planned solar projects (staged in WS-23).
- **Principal questions:**
  1. **[HIGH]** What is the solar resource across Guinea, and how does it vary by season and region?
  2. **[MEDIUM]** What factors reduce yield (cloud, aerosols, dust, temperature), and by how much on the evidence?
  3. **[MEDIUM]** What ground-measured data exist to validate satellite or reanalysis estimates?
  4. **[HIGH]** What is the technical potential near load centres and network infrastructure?
- **Required datasets:** Global solar resource datasets; reanalysis; ground measurement records, if any; aerosol datasets.
- **Source priorities:** Ground measurements and national data (T1) → World Bank/ESMAP resource atlases and reanalysis (T2/T3) → research (T3).
- **Dependencies:** WS-26 (constraint layers), WS-06 (network).
- **Expected outputs:** Solar resource layers and seasonal profiles; yield assumptions with sources; a technical-potential method note.
- **Validation requirements:** Every capacity figure records MW-DC and MW-AC. The resource dataset version is recorded. Satellite estimates are flagged when they have not been ground-validated.
- **Downstream consumers:** WS-21, WS-27, GIS, the integrated model.

## WS-19 — Wind Resource & Technical Potential

- **Objective:** Assess the wind resource and technical potential with the same rigour as other technologies. **Wind is not given lower priority in advance** (D-026).
- **Scope:** Wind speed at hub height; seasonal profiles; terrain and coastal effects; measurement campaigns; technical potential with constraint layers; existing or proposed wind projects, if any.
- **Principal questions:**
  1. **[HIGH]** What does the wind resource look like across Guinea, including at coastal and elevated sites?
  2. **[MEDIUM]** What measured data exist, and how do they compare with modelled datasets?
  3. **[MEDIUM]** How does the wind seasonal profile relate to the hydro and solar seasonal profiles?
  4. **[HIGH]** Where, if anywhere, is technical potential evidenced near load or network?
- **Required datasets:** Global wind atlas data; reanalysis; measurement campaigns, if any.
- **Source priorities:** As for WS-18.
- **Dependencies:** WS-26, WS-06.
- **Expected outputs:** Wind resource layers; a seasonal complementarity analysis; a technical-potential note.
- **Validation requirements:** Model versus measurement status is recorded. No conclusion on attractiveness is drawn before the analysis.
- **Downstream consumers:** WS-21, WS-27, GIS, the integrated model.

## WS-20 — Hydro Development Potential (New, Rehabilitation, Small Hydro)

- **Objective:** Assess hydro development options: new large and medium sites, rehabilitation or uprating of existing plant, and small hydro. Each option is assessed on its seasonal dependable output, not only installed capacity.
- **Scope:** Identified hydro sites and studies; lifecycle stage (via WS-23); seasonal dependable output (from WS-17 hydrology); environmental and social sensitivity (from WS-26); transboundary constraints (from WS-17); cost evidence.
- **Principal questions:**
  1. **[HIGH]** Which hydro sites have been studied, to what level, and with what results?
  2. **[HIGH]** For each candidate, what are the expected seasonal dependable output and firm energy?
  3. **[MEDIUM]** What rehabilitation or uprating opportunities exist at existing plants?
  4. **[HIGH]** What transboundary, environmental and resettlement constraints apply to each site?
- **Required datasets:** Hydro master plans and feasibility studies; basin-organisation project documents; DFI studies.
- **Source priorities:** Government and basin-organisation studies (T1) → DFI studies (T2) → research (T3).
- **Dependencies:** WS-17, WS-26, WS-23.
- **Expected outputs:** A hydro options register with seasonal output; a constraints summary.
- **Validation requirements:** Seasonal dependable output is required for every option. When projects are re-announced under different names, they are de-duplicated (§H).
- **Downstream consumers:** WS-21, WS-27, the integrated model.

## WS-21 — BESS, Hybridisation & Grid-Stability Applications

- **Objective:** Assess where storage and hybrid configurations are technically and economically justified, on evidence. This covers energy shifting, firming, frequency and stability services, and the hybridisation of captive generation.
- **Scope:**
  - BESS and other storage use cases.
  - Hybrid configurations of any technologies: solar, wind, hydro, thermal or storage.
  - System stability needs from WS-06 and WS-08.
  - Existing or planned storage projects.
  - Cost and performance benchmarks (technology data, not Guinea facts).
- **Principal questions:**
  1. **[HIGH]** What system needs (firming, reserves, frequency response, congestion relief) does the evidence from WS-06 and WS-08 identify?
  2. **[MEDIUM]** Do any storage or hybrid projects exist or are any planned in Guinea, and at what stage?
  3. **[HIGH]** For which use cases do storage or hybrids compete with alternatives (thermal, network, demand-side)?
  4. **[LOW]** What grid-code or technical requirements would apply to storage and hybrid plants?
- **Required datasets:** System studies; project disclosures; technology cost and performance benchmarks.
- **Source priorities:** System studies and grid code (T1) → DFI and WAPP studies (T2) → IEA, IRENA and NREL technology data (T3).
- **Dependencies:** WS-05, WS-06, WS-08, WS-18–WS-20.
- **Expected outputs:** A use-case matrix; a hybrid-configuration assessment framework.
- **Validation requirements:** Use cases must be grounded in an identified system need. Generic global benchmarks are labelled as such.
- **Downstream consumers:** WS-27, the integrated model.

## WS-22 — Decentralised Energy, Mini-Grids & Productive Use

- **Objective:** Assess the policy, regulatory and market framework for mini-grids and off-grid supply, together with productive-use and anchor-load models.
- **Scope:**
  - The rural electrification agency framework. The agency's name and current status are to be verified.
  - Mini-grid licensing and tariffs.
  - Subsidy and results-based financing programmes.
  - Existing mini-grid portfolio.
  - Solar home systems.
  - Anchor loads (telecom, agro-processing, artisanal mining).
  - Donor programmes. Programme names given by Gemini are leads to verify.
- **Principal questions:**
  1. **[HIGH]** Which institutions, laws and regulations govern mini-grids and off-grid supply?
  2. **[MEDIUM]** How are mini-grid tariffs set, and what subsidy mechanisms exist?
  3. **[MEDIUM]** What mini-grid and off-grid deployment has occurred, by whom and with what results?
  4. **[MEDIUM]** Which anchor-load and productive-use models are documented as viable?
  5. **[HIGH]** What donor or DFI programmes are active, and what are their eligibility rules?
- **Required datasets:** Agency publications; regulatory texts; donor programme documents; deployment data.
- **Source priorities:** Agency and regulatory documents (T1) → DFI and donor programme documents (T2) → IRENA, ESMAP and research (T3).
- **Dependencies:** WS-02, WS-07.
- **Expected outputs:** A decentralised-energy framework note; a deployment register; a list of programme eligibility rules.
- **Validation requirements:** Programme status follows the lifecycle framework. Statistics on deployment state their definitions.
- **Downstream consumers:** WS-10, WS-27.

---

# Cluster F — Pipeline, Finance, Ecosystem & Constraints

## WS-23 — Generation & Transmission Project Pipeline

- **Objective:** Maintain the master project register: every identified generation, storage and transmission project, with its lifecycle stage, progress condition and the evidence for both.
- **Scope:** All projects identified by any workstream; de-duplication; lifecycle and progress assessments (`methodology.md` §6); links to sponsors, EPCs, OEMs, financiers and offtakers (WS-25 entity IDs).
- **Principal questions:**
  1. **[CRITICAL]** Which projects exist in the pipeline, and what is the evidenced lifecycle stage and progress condition of each?
  2. **[HIGH]** Which projects are duplicates or re-announcements of one another?
  3. **[CRITICAL]** What capacity is operational, under construction, financially committed or in active development, by technology and by year?
  4. **[MEDIUM]** What patterns of delay, stalling or cancellation appear, and what causes them?
- **Required datasets:** Outputs of all workstreams; official project lists; DFI project databases; procurement records.
- **Source priorities:** Official documents and DFI records (T1/T2) → company disclosures (T4, corroborated) → press (T5, leads only).
- **Dependencies:** WS-05, WS-06, WS-18–WS-22.
- **Expected outputs:** The project register (XLSX); a pipeline summary by stage and technology; the inputs on committed additions for the scenario model.
- **Validation requirements:**
  - The status rules of `methodology.md` §6 are applied strictly.
  - De-duplication uses location, capacity and sponsor.
  - Every stage assignment cites its evidence.
- **Downstream consumers:** The integrated model, WS-27, GIS, the HTML platform.

## WS-24 — International Finance, DFI & Risk-Mitigation Instruments

- **Objective:** Map the financing and risk-mitigation instruments actually available for Guinea energy projects, and their eligibility conditions, **without assuming any financing structure** (D-039).
- **Scope:**
  - DFIs: multilateral and bilateral.
  - Sovereign lending.
  - Guarantees: partial risk, partial credit, sovereign.
  - Political-risk insurance.
  - ECA, EXIM and line-of-credit programmes.
  - Bilateral financing.
  - Project finance precedents.
  - Blended and climate finance.
  - PPP instruments.
  - Technical assistance and project-preparation facilities.
- **Principal questions:**
  1. **[HIGH]** Which financing institutions have financed Guinea energy projects since 2016, with which instruments and on what terms (where public)?
  2. **[HIGH]** What guarantee and insurance instruments are available for Guinea? What are their eligibility rules, and have they been used?
  3. **[MEDIUM]** What lines of credit or bilateral programmes are active, and what conditions apply (for example sourcing requirements)?
  4. **[MEDIUM]** What project-preparation and technical-assistance facilities are available?
  5. **[HIGH]** What do completed transactions show about the financing structures lenders actually require?
- **Required datasets:** DFI project databases; ECA and EXIM disclosures; guarantee agency project lists; climate fund portfolios.
- **Source priorities:** Institutional project databases and official agreements (T1/T2) → research databases (T3) → press (T5).
- **Dependencies:** WS-01, WS-04, WS-09.
- **Expected outputs:** A register of financing instruments; a list of transaction precedents; an eligibility matrix.
- **Validation requirements:** Each instrument's availability for Guinea is evidenced, not inferred from the institution's general mandate. Each instrument's status is recorded (active, closed or pipeline).
- **Downstream consumers:** WS-27, WS-28.

## WS-25 — International Commercial Ecosystem (by Origin) & OEM/EPC/IPP Register

- **Objective:** Build a structured register of the developers, IPPs, EPCs, OEMs, utilities, investors and agencies from each origin that are relevant to Guinea's energy sector, classified strictly by evidence of their Guinea presence (D-035).
- **Scope:**
  - Origin sub-registers: India; China; Europe; Middle East; USA; Japan and Korea; Africa (regional); other.
  - Entity types: developer, IPP, EPC, OEM, financier, utility, government agency, mining company with an energy role.
- **Presence classification (one per entity):**
  - Confirmed operational presence in Guinea.
  - Confirmed Guinea project supplied or executed.
  - Confirmed Guinea pipeline.
  - Regional presence only.
  - Potential future supplier or partner.
- **Principal questions:**
  1. **[HIGH]** Which international entities have evidenced activity in Guinea's energy or mining-energy sector, and in what role?
  2. **[MEDIUM]** For each origin, what government-backed instruments and strategies are relevant (cross-referenced with WS-24)?
  3. **[LOW]** Which entities have regional presence only, and in which benchmark countries?
  4. **[MEDIUM]** What competitive landscape do the entities form in each technology and service segment?
- **Required datasets:** Project register links (WS-23); company disclosures; procurement awards; DFI project documents; government bilateral agreements.
- **Source priorities:** Procurement awards, contracts and official records (T1) → DFI documents (T2) → company disclosures (T4) → press (T5, leads only).
- **Dependencies:** WS-23, WS-24.
- **Expected outputs:** The entity register with origin sub-registers; competitive landscape maps.
- **Validation requirements:**
  - Global presence never implies presence in Guinea.
  - Every presence classification cites Guinea-specific evidence.
  - Entities named by Gemini enter the register only after verification.
- **Downstream consumers:** WS-27, WS-28.

## WS-26 — Land Tenure, Resettlement, Environmental & Biodiversity Constraints

- **Objective:** Establish the land, social, environmental and biodiversity framework and the spatial constraints that affect energy projects, and build the GIS constraint layers (D-038).
- **Scope:**
  - Statutory and customary land tenure.
  - Expropriation and compensation.
  - Resettlement precedents.
  - The ESIA process and authority.
  - IFC Performance Standards applicability.
  - Protected areas, forests and biodiversity, including critical habitats and species of concern. Species and site specifics are to be researched.
  - Agricultural land.
  - Flood and other physical climate hazards.
  - Community conflict history.
- **Principal questions:**
  1. **[HIGH]** What land tenure regimes apply, and how is land acquired for energy projects?
  2. **[HIGH]** What expropriation, compensation and resettlement frameworks and precedents exist?
  3. **[HIGH]** What is the ESIA process? Which authority runs it, and how long does it take in practice?
  4. **[HIGH]** Which protected areas, critical habitats and biodiversity-sensitive zones exist, and what legal status does each have?
  5. **[MEDIUM]** Where are flood and other physical climate hazards documented?
  6. **[MEDIUM]** What community conflict around energy or mining projects is documented, and what caused it?
- **Required datasets:** Legal texts; ESIA registries; protected-area and biodiversity datasets; land-cover and agricultural data; flood hazard data; resettlement plans.
- **Source priorities:** Legal texts and official registries (T1) → DFI safeguard documents (T2) → global environmental datasets and research (T3) → NGO reports (T4/T5, corroborated).
- **Dependencies:** WS-02, WS-15, WS-17.
- **Expected outputs:** A land and ESIA framework note; constraint layers with attributes (GIS); a precedent register.
- **Validation requirements:**
  - Each constraint layer records its legal status (legal exclusion, regulatory constraint or risk flag), source, date and licence.
  - **No universal numeric threshold** (for example a slope cut-off) is applied at this stage.
- **Downstream consumers:** WS-18–WS-20, WS-27, GIS.

---

# Cluster G — Opportunity & Strategy (Phase B)

## WS-27 — Commercial Opportunity Portfolio & Structuring

- **Objective:** Answer the question: **"What opportunities are technically, commercially and strategically attractive for Guinea?"** This is done independently of Alendei's interests or capabilities (D-028).
- **Scope:**
  - Generating candidate opportunities from Phase A evidence, across all technology options and all solution types (generation, network, storage, demand-side, decentralised, regional).
  - A fatal-flaw screen and multi-criteria screening (`research_architecture.md` §K).
  - Commercial model options (utility PPA, private B2B, captive, BOO/BOOT, concession, PPP, mini-grid), each assessed on evidence.
  - Structuring requirements.
  - Sensitivity analysis.
  - **No commercial model is predetermined as preferred** (D-026).
- **Principal questions:**
  1. **[CRITICAL]** Which opportunities does the Phase A evidence support, and through what evidence chain?
  2. **[CRITICAL]** Which candidates fail on a fatal flaw (legal, offtake, constraint, evidence)?
  3. **[HIGH]** How do the remaining candidates score across the screening dimensions? How robust is the ranking to changes in weights?
  4. **[HIGH]** Which commercial and financing structures are feasible for each opportunity, on evidence from WS-02, WS-04, WS-09 and WS-24?
- **Required datasets:** Outputs of Phase A; the assumption register.
- **Source priorities:** The project's own registers. No new unsourced inputs.
- **Dependencies:** All Phase A workstreams (Gates 5–6 complete).
- **Expected outputs:** Candidate opportunity register; screening results; an Alendei-neutral attractiveness rating for each opportunity; commercial model notes; sensitivity analysis. Stored in `06_opportunities/candidate_opportunities/`, `priority_portfolio/` and `commercial_models/`.
- **Validation requirements:**
  - Every opportunity has an evidence chain.
  - The ratings are frozen and recorded before WS-28 begins.
  - Financial metrics are included only where the evidence supports them.
  - Weights are validated at Gate 7 with sensitivity analysis.
- **Downstream consumers:** WS-28, the report, the presentation, the HTML platform.

## WS-28 — Alendei Strategic Participation & Ecosystem Role

- **Objective:** Answer the question: **"Where can Alendei participate?"** WS-28 assesses Alendei's possible roles in the frozen WS-27 portfolio. **It does not alter the country opportunity ranking** (D-028).
- **Scope:**
  - Testing the positioning hypothesis (D-011) against WS-27 opportunities.
  - Gap analysis between candidate roles and user-supplied evidence of Alendei's capabilities.
  - Partner requirements (from WS-25).
  - Financing pathways (from WS-24).
  - Tier 1–4 pursuit classification (`methodology.md` §11).
  - Roadmap and due-diligence lists.
- **Principal questions:**
  1. **[CRITICAL]** For each WS-27 opportunity, what roles could Alendei credibly play, given the capability evidence supplied by the user?
  2. **[HIGH]** Which capability, licence, partnership or financing gaps would have to be closed, and how?
  3. **[MEDIUM]** Which partners (from the evidenced WS-25 register) would be needed?
  4. **[CRITICAL]** Which classification (Tier 1–4) does each opportunity merit for Alendei, and why?
- **Required datasets:** The frozen WS-27 outputs; user-supplied evidence of Alendei capabilities; WS-24 and WS-25 registers.
- **Source priorities:** The project registers; Alendei evidence supplied by the user (the only valid source of Alendei facts).
- **Dependencies:** WS-27 (frozen); user-supplied capability evidence.
- **Expected outputs:** Alendei participation assessment; Tier 1–4 classifications; roadmap; due-diligence lists. Stored in `06_opportunities/alendei_role/`, `roadmap/` and `due_diligence/`.
- **Validation requirements:**
  - No Alendei capability, licence, partnership or financing commitment is asserted without user-supplied evidence.
  - "Tier 4 — Do not pursue now" is applied wherever warranted.
  - The WS-27 rating cannot be changed by WS-28.
- **Downstream consumers:** The report, the presentation, the HTML platform, Alendei decision-makers.
