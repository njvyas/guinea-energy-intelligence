#!/usr/bin/env python3
"""Build the 15 executable Gemini mission packages (Gate 2C).

Single source for the mission packages (D-078). Common rules (source hierarchy,
output contract, handoff, metadata) are defined once here; mission-specific
content is defined per mission. Exact question text and planning priority are
read from 00_project/workstream_charters.md so they cannot drift.

Outputs (deterministic):
  01_gemini_research/00_architecture/mission_packages/GEM-NN_<slug>_package_Pv1.md
  01_gemini_research/00_architecture/mission_packages/PACKAGE_INDEX.md

Usage: python3 -I 00_project/tools/build_mission_packages.py <repo_root>
Approved packages are immutable; any change creates a new package version.
"""
import hashlib
import os
import re
import sys

PKG_VERSION = "Pv1"
PKG_DATE = "08-Oct-2026"
OUT_DIR = "01_gemini_research/00_architecture/mission_packages"

# ---------------------------------------------------------------------------
# Per-question design attributes (question text and priority come from the charters)
# e=evidence type, g=expected geography (geo_level codes), p=period, k=kind,
# s=primary-source target, f=acceptable secondary fallback, d=critical definitions, r=analytical risk
# Period codes: H=2016-2026 historical; C=current status (as-of date); N=2027-2030; S=2030-2035
# ---------------------------------------------------------------------------
Q = {
    # WS-01 Macro, political economy & country risk
    "WS-01 Q1": dict(e="National accounts; export statistics by product", g="NATIONAL_AGGREGATE", p="H", k="QUANTITATIVE", s="National statistics office; central bank annual reports; IMF Article IV statistical annexes", f="World Bank WDI; UN Comtrade (mirror data labelled as such)", d="Export concentration share (numerator/denominator stated); nominal vs real GDP", r="Mirror trade data differ from national data; single-year figures presented as structure"),
    "WS-01 Q2": dict(e="Fiscal balance, public debt, contingent liabilities, subsidy outlays", g="NATIONAL_AGGREGATE", p="H; N", k="QUANTITATIVE", s="Ministry of finance budget documents; IMF programme/Article IV documents; debt sustainability analyses", f="World Bank public expenditure reviews", d="Gross vs net debt; explicit vs contingent liabilities; budgeted vs executed subsidy", r="Treating budgeted amounts as executed; inferring guarantee capacity without a source"),
    "WS-01 Q3": dict(e="Documented government actions on concessions/contracts; official statements; arbitration records", g="NATIONAL_AGGREGATE", p="H; C", k="QUALITATIVE", s="Official gazette; government communiqués; published contract reviews; arbitration registers", f="DFI country diagnostics; reputable press (Tier 5, corroboration required)", d="Renegotiation vs termination vs review; announced vs implemented action", r="Commentary presented as documented event; causal attribution without evidence"),
    "WS-01 Q4": dict(e="Published country-risk ratings and classifications with dates", g="NATIONAL_AGGREGATE", p="H; C", k="MIXED", s="Rating-agency publications; OECD country-risk classifications; DFI/MIGA country notes", f="Reputable financial press reporting ratings (verify against issuer)", d="Rating scale and agency; sovereign vs transfer/convertibility risk", r="Stale ratings presented as current; mixing agency scales"),
    "WS-01 Q5": dict(e="National development and energy strategy texts; stated targets", g="NATIONAL_AGGREGATE", p="C; N; S", k="MIXED", s="Planning ministry strategy documents; energy policy letters; official gazette", f="DFI strategy summaries (label as summary)", d="Target vs plan vs commitment (protocol §6.2)", r="Targets reported as plans or committed projects"),
    # WS-02 Electricity institutions, law & regulation
    "WS-02 Q1": dict(e="Legal instruments: title, number, date, amendment history", g="NATIONAL_AGGREGATE", p="H; C", k="QUALITATIVE", s="Official gazette; ministry legal repositories; regulator website", f="DFI legal diagnostics; law-firm guides (interpretive only)", d="Law vs decree vs order; in force vs repealed; amendment date", r="Citing a superseded text as current"),
    "WS-02 Q2": dict(e="Statutory mandates; evidence of operation (reports, decisions, budgets)", g="NATIONAL_AGGREGATE", p="C", k="QUALITATIVE", s="Founding legal texts; institutions' own publications; official gazette", f="DFI institutional assessments", d="Legal mandate vs operational reality", r="Assuming a body operates because a law created it"),
    "WS-02 Q3": dict(e="Licensing/concession/procurement provisions; award notices; signed agreements", g="NATIONAL_AGGREGATE", p="H; C", k="MIXED", s="Legal texts; procurement authority notices; regulator decisions", f="DFI project documents describing procurement", d="Licence vs concession vs PPA; competitive vs direct award", r="Counting announced or MoU deals as awards"),
    "WS-02 Q4": dict(e="Legal provisions (article-level) on self-generation, private sale, third-party access", g="NATIONAL_AGGREGATE", p="C", k="QUALITATIVE", s="Electricity law and implementing decrees; regulator decisions", f="Law-firm/DFI legal analyses (interpretation labelled)", d="Self-generation vs private bilateral sale vs wheeling/third-party access", r="Inferring legality from practice or from mining-sector precedents"),
    "WS-02 Q5": dict(e="Tariff-setting procedure; published tariff decisions with dates", g="NATIONAL_AGGREGATE", p="H; C", k="MIXED", s="Regulator/ministry tariff decisions; official gazette", f="DFI tariff studies", d="Tariff-setting authority vs approving authority; tariff schedule vs cost of supply", r="Reporting a proposed tariff as approved; stale schedules"),
    "WS-02 Q6": dict(e="Grid code / connection rules texts", g="NATIONAL_AGGREGATE", p="C", k="QUALITATIVE", s="Grid code; utility connection requirements; regulator decisions", f="WAPP regional operating rules (label as regional)", d="National grid code vs regional operation manual", r="Assuming regional rules apply nationally"),
    # WS-03 Fuel supply, logistics & thermal/gas
    "WS-03 Q1": dict(e="Fuel consumption for public and captive generation by fuel type and year", g="NATIONAL_AGGREGATE; PLANT_SITE; MINING_SITE", p="H", k="QUANTITATIVE", s="Petroleum agency/customs import statistics; utility fuel reports; IEA/UN energy balances", f="DFI sector diagnostics", d="Fuel for power vs total fuel imports; litres vs tonnes (density stated if converted)", r="Equating total petroleum imports with power-sector fuel"),
    "WS-03 Q2": dict(e="Port reception, storage capacity, distribution assets and operational status", g="PORT; INDUSTRIAL_SITE; NATIONAL_AGGREGATE", p="H; C", k="MIXED", s="Port authority reports; petroleum agency/ministry documents; DFI infrastructure diagnostics", f="Operator disclosures; Tier 5 press for status (corroborate)", d="Nameplate storage vs operational storage; redundancy", r="Reporting nameplate capacity as available after an incident"),
    "WS-03 Q3": dict(e="Documented disruption events with dates, duration, effect on generation", g="NATIONAL_AGGREGATE; PORT", p="H", k="MIXED", s="Official statements; utility/system-operator reports; DFI/IMF reports", f="Press (Tier 5; corroborate dates and effects)", d="Event vs effect on generation (separately evidenced)", r="Accepting the disruption event cited in the Gate 1 challenge without primary evidence"),
    "WS-03 Q4": dict(e="Fuel price-setting rules; tax and subsidy structures", g="NATIONAL_AGGREGATE", p="H; C", k="MIXED", s="Pricing decrees/orders; finance-ministry documents; IMF fuel-subsidy analyses", f="DFI diagnostics", d="Ex-depot vs retail vs delivered price; explicit vs implicit subsidy", r="Retail pump prices used as power-plant fuel cost"),
    "WS-03 Q5": dict(e="Delivered fuel cost components at named representative locations", g="PLANT_SITE; MINING_SITE; PORT", p="H; C", k="QUANTITATIVE", s="Company disclosures (own facts); ESIAs; DFI project documents with cost build-ups", f="Industry reports (method stated; corroboration required)", d="Delivered (landed) cost = product + logistics + taxes + margins; currency, date, fuel grade", r="Applying generic markup percentages; mixing currencies/dates"),
    "WS-03 Q6": dict(e="Gas/LNG import proposals with lifecycle-stage evidence", g="PORT; NATIONAL_AGGREGATE", p="C; N; S", k="QUALITATIVE", s="Government/ministry documents; DFI project pipelines; sponsor filings", f="Press (lead only until corroborated)", d="Lifecycle stage per methodology §6", r="Feasibility studies or MoUs reported as committed projects"),
    # WS-04 Macro-financial, FX & repatriation
    "WS-04 Q1": dict(e="Exchange-rate regime description; official rate series", g="NATIONAL_AGGREGATE", p="H", k="MIXED", s="Central bank publications; IMF AREAER and Article IV", f="IMF IFS / World Bank WDI series", d="De jure vs de facto regime; official vs parallel rate", r="Using parallel-market anecdotes as official data"),
    "WS-04 Q2": dict(e="FX regulations on export earnings, foreign-currency contracts, debt service, dividends", g="NATIONAL_AGGREGATE", p="H; C", k="QUALITATIVE", s="Central bank regulations/instructions; official gazette", f="IMF AREAER; law-firm guides (interpretation labelled)", d="Surrender vs repatriation requirement; current vs capital account", r="Assuming FX restrictions or their absence without legal text"),
    "WS-04 Q3": dict(e="Documented evidence of FX availability constraints (reports, statements, data)", g="NATIONAL_AGGREGATE", p="H; C", k="MIXED", s="IMF staff reports; central bank reports", f="DFI/rating-agency analyses", d="Documented constraint vs perceived risk", r="Generalising from other countries' FX conditions"),
    "WS-04 Q4": dict(e="Currency denomination/indexation clauses of existing PPAs/concessions", g="PLANT_SITE; NATIONAL_AGGREGATE", p="H; C", k="QUALITATIVE", s="Published contracts; DFI project documents; regulator decisions", f="Sponsor disclosures (own facts)", d="Denomination vs indexation vs payment currency", r="Inferring contract currency from sponsor nationality"),
    "WS-04 Q5": dict(e="Transaction-level mechanisms (escrow, offshore accounts, guarantees, insurance) and whether required by law or lenders", g="PLANT_SITE; NATIONAL_AGGREGATE", p="H; C", k="QUALITATIVE", s="DFI/guarantee-agency project documents; published agreements", f="Sponsor disclosures; law-firm commentary (labelled)", d="Regulatory requirement vs lender requirement vs market practice", r="Assuming offshore escrow is required (D-026)"),
    # WS-05 Generation fleet
    "WS-05 Q1": dict(e="Plant-level installed capacity with AC/DC basis and commissioning evidence", g="PLANT_SITE", p="C", k="QUANTITATIVE", s="Utility/system-operator reports; regulator/ministry statistics", f="DFI documents; IEA/IRENA statistics (definition check)", d="Installed capacity (methodology §5); MW-AC vs MW-DC", r="Counting non-commissioned or decommissioned units"),
    "WS-05 Q2": dict(e="Available/dependable capacity; hydro dependable capacity by month/season", g="PLANT_SITE", p="H; C", k="QUANTITATIVE", s="System-operator reports; utility planning studies; DFI hydro studies", f="WAPP master-plan plant data (label vintage)", d="Available vs dependable vs seasonal dependable; season definitions per source", r="Using annual averages or nameplate as dependable capacity"),
    "WS-05 Q3": dict(e="Annual and monthly gross/net generation by plant", g="PLANT_SITE; NATIONAL_AGGREGATE", p="H", k="QUANTITATIVE", s="Utility/system-operator annual reports", f="IEA/UN statistics (national totals only)", d="Gross vs net generation; calendar vs fiscal year", r="Mixing gross and net; filling gaps with estimates without labelling"),
    "WS-05 Q4": dict(e="Documented operating rules for interdependent hydro plants; dispatch-priority authority", g="PLANT_SITE; RIVER_BASIN", p="C", k="QUALITATIVE", s="Operating agreements; system-operator procedures; basin-organisation rules", f="DFI hydro studies", d="Cascade coupling vs independent operation; storage vs run-of-river", r="Assuming cascade configuration from geography (lead GL-12)"),
    "WS-05 Q5": dict(e="Rental/emergency power contracts: capacity, tenor, charges, fuel responsibility", g="PLANT_SITE; NATIONAL_AGGREGATE", p="H; C", k="MIXED", s="Published contracts; audit reports; utility financial statements notes", f="DFI/IMF reports; press (lead)", d="Capacity charge vs energy charge; rental vs owned capacity", r="Treating rental capacity as owned or permanent"),
    "WS-05 Q6": dict(e="Thermal unit heat rates, fuel types, ambient derating", g="PLANT_SITE", p="H; C", k="QUANTITATIVE", s="Utility technical reports; DFI supervision reports; OEM documentation for named units", f="Generic OEM specifications (label as generic, not plant-specific)", d="Heat rate basis (LHV/HHV, gross/net); fuel grade", r="Applying generic OEM heat rates as measured plant values"),
    # WS-06 Transmission
    "WS-06 Q1": dict(e="Network topology; line/substation status (constructed vs energised)", g="TRANSMISSION_CORRIDOR; SUBSTATION_NODE", p="C", k="MIXED", s="Utility network maps/single-line diagrams; master plans; DFI transmission documents", f="WAPP master plans (regional lines)", d="Constructed vs energised (methodology §5)", r="Reporting construction completion as energisation"),
    "WS-06 Q2": dict(e="Substation transformer ratings (MVA), loading and documented constraints", g="SUBSTATION_NODE", p="H; C", k="QUANTITATIVE", s="Grid studies; utility planning documents; DFI appraisal documents", f="Consultancy studies (date and method stated)", d="Transformer rating vs loading (%, date); N-1 only where assessed", r="Inferring constraints from demand growth without a study"),
    "WS-06 Q3": dict(e="Documented voltage/reactive/stability problems; installed or planned mitigation", g="TRANSMISSION_CORRIDOR; SUBSTATION_NODE", p="H; C", k="MIXED", s="Grid studies; system-operator incident reports; DFI documents", f="WAPP/ICC operational reports", d="Voltage stability vs frequency stability; reactive compensation types", r="Generalising regional stability issues to the national grid"),
    "WS-06 Q4": dict(e="Dispatch centre monitoring/control capability (SCADA/EMS) evidence", g="NATIONAL_AGGREGATE", p="C", k="QUALITATIVE", s="Utility/system-operator documents; DFI project documents financing control systems", f="WAPP ICC assessments", d="SCADA visibility vs control; EMS functions", r="Assuming a financed system is commissioned"),
    "WS-06 Q5": dict(e="Planned reinforcement projects with lifecycle-stage evidence", g="TRANSMISSION_CORRIDOR; SUBSTATION_NODE", p="N; S", k="MIXED", s="Transmission master plans; DFI project pipelines; procurement notices", f="Sponsor/ministry announcements (stage ≤ Announced unless evidenced)", d="Lifecycle stage per methodology §6", r="Master-plan listing reported as committed project"),
    # WS-07 Distribution & access
    "WS-07 Q1": dict(e="Access rates by geography and tier with definitions", g="NATIONAL_AGGREGATE; REGIONAL; CITY", p="H; C", k="QUANTITATIVE", s="National household surveys/census; MTF surveys; utility connection data", f="World Bank/IEA access databases (definition stated)", d="Grid connection vs household access; MTF tiers; urban/rural", r="Mixing connection counts with household access rates"),
    "WS-07 Q2": dict(e="Customer numbers by class, time series", g="NATIONAL_AGGREGATE; REGIONAL", p="H", k="QUANTITATIVE", s="Utility annual reports/statistics", f="DFI project documents", d="Customer vs connection vs meter; customer classes as defined by utility", r="Counting meters as customers"),
    "WS-07 Q3": dict(e="Loss values partitioned (T / D technical / non-technical) with measurement method", g="NATIONAL_AGGREGATE", p="H", k="QUANTITATIVE", s="Utility reports; loss audits; regulator reports", f="DFI documents (method stated)", d="Loss partitions (methodology §5); % of what base", r="Applying generic regional loss ranges (GL-24)"),
    "WS-07 Q4": dict(e="Metering/loss-reduction programmes and documented results", g="NATIONAL_AGGREGATE; CITY", p="H; C", k="MIXED", s="Utility/DFI programme reports; completion reports", f="Press (lead)", d="Output (meters installed) vs outcome (loss reduction)", r="Reporting programme targets as achieved results"),
    "WS-07 Q5": dict(e="Demand-side/efficiency measures documented", g="NATIONAL_AGGREGATE", p="H; C; N", k="QUALITATIVE", s="Ministry/utility programmes; DFI project documents", f="Donor programme summaries", d="Measure vs programme vs result", r="Counting announced programmes as implemented"),
    # WS-08 Reliability & operations
    "WS-08 Q1": dict(e="Reliability indicators (SAIDI, SAIFI, hours of supply) by region/season", g="NATIONAL_AGGREGATE; REGIONAL; CITY", p="H", k="QUANTITATIVE", s="Utility/regulator reliability statistics", f="World Bank enterprise surveys (firm-reported; label)", d="Indicator definitions; planned vs unplanned outages", r="Mixing utility-reported and survey-reported indicators"),
    "WS-08 Q2": dict(e="Load-shedding and unserved-energy evidence and drivers", g="NATIONAL_AGGREGATE; REGIONAL", p="H; C", k="MIXED", s="System-operator reports; utility statements; DFI documents", f="Press (lead; corroborate)", d="Load shedding vs forced outage; unserved energy estimation method", r="Attributing causes without documentation"),
    "WS-08 Q3": dict(e="Reserve, frequency-control and under-frequency load-shedding practice", g="NATIONAL_AGGREGATE", p="C", k="QUALITATIVE", s="Grid code; system-operator procedures; WAPP operational documents", f="DFI/consultancy studies", d="Primary/secondary reserve; UFLS", r="Assuming WAPP standards are implemented nationally"),
    "WS-08 Q4": dict(e="Customer backup generation prevalence/capacity; implications for suppressed demand", g="NATIONAL_AGGREGATE; CITY", p="H; C", k="MIXED", s="Enterprise surveys; national surveys; utility/DFI studies", f="Industry estimates (method stated)", d="Backup vs captive generation; suppressed demand estimation method", r="Converting backup-generator counts into demand without method"),
    "WS-08 Q5": dict(e="Independent indicators (e.g. night-time lights) corroborating official reliability data", g="NATIONAL_AGGREGATE; CITY", p="H", k="MIXED", s="Peer-reviewed studies; official remote-sensing products (dataset/version stated)", f="Grey literature using satellite data (method stated)", d="Radiance vs electrification vs reliability; cloud-cover limitations", r="Treating satellite proxies as direct measurements"),
    # WS-09 Utility economics
    "WS-09 Q1": dict(e="Financial statements (audited/unaudited) by year", g="NATIONAL_AGGREGATE", p="H", k="QUANTITATIVE", s="Utility financial statements; supreme audit institution reports", f="IMF/World Bank analyses of utility finances", d="Audited vs unaudited; revenue billed vs collected; consolidated vs standalone", r="Characterising financial condition without stated indicators (D-026)"),
    "WS-09 Q2": dict(e="Tariff schedules by class; cost-of-supply studies; subsidy transfers", g="NATIONAL_AGGREGATE", p="H; C", k="QUANTITATIVE", s="Tariff decisions; cost-of-service studies; budget documents", f="DFI tariff analyses", d="Tariff vs cost of supply (never equated); subsidy explicit vs implicit", r="Comparing tariffs and costs of different years/currencies"),
    "WS-09 Q3": dict(e="Collection rates by class; receivables/arrears time series", g="NATIONAL_AGGREGATE", p="H", k="QUANTITATIVE", s="Utility financial statements/reports; audit reports", f="DFI/IMF documents", d="Collection rate definition (cash collected ÷ billed, period)", r="Using a single programme-period figure as a trend"),
    "WS-09 Q4": dict(e="Documented payment record to IPPs, fuel suppliers, regional counterparties", g="NATIONAL_AGGREGATE", p="H; C", k="MIXED", s="Audit reports; IMF documents; regional counterparties' reports; financial statements notes", f="Press (lead)", d="Arrears vs disputed amounts; overdue period", r="Inferring arrears from general financial stress"),
    "WS-09 Q5": dict(e="Credit enhancement required in actual utility-offtake transactions and stated rationale", g="PLANT_SITE; NATIONAL_AGGREGATE", p="H; C", k="QUALITATIVE", s="DFI/guarantee-agency project documents", f="Sponsor disclosures", d="Guarantee vs insurance vs liquidity support", r="Assuming a financing structure is generally required (D-039)"),
    # WS-10 Demand
    "WS-10 Q1": dict(e="Served energy consumption and peak demand by class/region", g="NATIONAL_AGGREGATE; REGIONAL", p="H", k="QUANTITATIVE", s="Utility/system-operator statistics", f="IEA/UN energy statistics (national totals)", d="Served vs unconstrained; peak vs average; billed vs metered", r="Treating served peak as demand"),
    "WS-10 Q2": dict(e="Load profiles: daily, seasonal, annual", g="NATIONAL_AGGREGATE; SUBSTATION_NODE", p="H", k="QUANTITATIVE", s="System-operator load data; utility planning studies", f="Master-plan studies (vintage stated)", d="Hourly/daily profile; season definitions", r="Using a single typical day as representative"),
    "WS-10 Q3": dict(e="Suppressed and captive demand estimates with methods", g="NATIONAL_AGGREGATE", p="H; C", k="QUANTITATIVE", s="Utility/DFI studies; master plans", f="Academic/consultancy estimates (method stated)", d="Suppressed vs captive vs unserved; estimation method", r="Presenting estimates as measurements"),
    "WS-10 Q4": dict(e="Demand drivers; existing forecasts with methods/assumptions", g="NATIONAL_AGGREGATE", p="N; S", k="MIXED", s="Official master plans; WAPP master plans; DFI studies", f="Academic studies", d="Forecast vs scenario vs target", r="Adopting a forecast or linear trend without review (D-031)"),
    "WS-10 Q5": dict(e="Comparison of official forecasts with each other and outturn", g="NATIONAL_AGGREGATE", p="H; N", k="QUANTITATIVE", s="Successive master plans/forecasts; outturn statistics", f="DFI reviews", d="Forecast vintage; base year", r="Comparing forecasts with different definitions"),
    # WS-11 Bauxite & alumina
    "WS-11 Q1": dict(e="Inventory of bauxite operations and alumina refineries: operator, location, lifecycle stage", g="MINING_SITE; INDUSTRIAL_SITE", p="C; N", k="MIXED", s="Mining cadastre; EITI reports; company statutory filings", f="Company presentations (own facts); press (lead)", d="Extraction vs processing vs refining; lifecycle stage", r="Treating a refinery obligation or announcement as an operating/committed refinery"),
    "WS-11 Q2": dict(e="Site electrical and thermal demand; supply source", g="MINING_SITE; INDUSTRIAL_SITE", p="H; C", k="QUANTITATIVE", s="ESIAs; company filings; DFI documents", f="Company presentations (own facts)", d="Electrical vs thermal (steam) demand; peak vs average vs annual energy", r="Deriving electricity consumption from production capacity"),
    "WS-11 Q3": dict(e="Captive generation capacity, technology, fuel, cost", g="MINING_SITE; INDUSTRIAL_SITE", p="H; C", k="QUANTITATIVE", s="ESIAs; company filings; permits", f="OEM/contractor press releases (own facts, corroborate)", d="Installed captive capacity; fuel type; cost basis and currency", r="Assuming captive technology or fuel"),
    "WS-11 Q4": dict(e="Project-specific refinery energy requirements (electrical, steam)", g="INDUSTRIAL_SITE", p="N; S", k="QUANTITATIVE", s="Refinery project ESIAs/feasibility disclosures", f="Technical literature on refinery energy intensity (label generic, never site value)", d="Design vs operating requirement; electrical vs thermal", r="Using a generic refinery load (D-026; GL-10)"),
    "WS-11 Q5": dict(e="Operator/parent decarbonisation targets and energy-procurement policies", g="MINING_SITE; NATIONAL_AGGREGATE", p="C; S", k="QUALITATIVE", s="Parent-company sustainability reports; statutory filings", f="ESG databases (label)", d="Group-level target vs site-level plan", r="Treating a group target as a site commitment or PPA appetite"),
    # WS-12 Simandou
    "WS-12 Q1": dict(e="Components, ownership structure, lifecycle stage per component", g="MINING_SITE; PORT; TRANSMISSION_CORRIDOR", p="C; N", k="MIXED", s="Official agreements; ESIAs; company statutory filings", f="Investor presentations (own facts); press (lead)", d="Component-level lifecycle stage and progress condition", r="One status applied to all components"),
    "WS-12 Q2": dict(e="Documented power demand and supply arrangements for mines, rail, port", g="MINING_SITE; PORT; TRANSMISSION_CORRIDOR", p="C; N; S", k="QUANTITATIVE", s="ESIAs; company filings; permits", f="Contractor/OEM announcements (corroborate)", d="Peak vs annual energy; captive vs grid vs hybrid", r="Projected demand reported as current or committed"),
    "WS-12 Q3": dict(e="Commitments to supply/share power or infrastructure with grid/communities", g="MINING_SITE; LOCALITY; NATIONAL_AGGREGATE", p="C; N", k="QUALITATIVE", s="Agreements/conventions; ESIA commitments registers", f="Company sustainability reports (own commitments)", d="Commitment vs intention vs obligation", r="Statements of intent reported as binding obligations"),
    "WS-12 Q4": dict(e="Documented effects on regional demand, transmission needs, supply chains", g="REGIONAL; TRANSMISSION_CORRIDOR", p="N; S", k="MIXED", s="Government/DFI studies; ESIAs", f="Consultancy/academic studies (method stated)", d="Projected vs actual effect", r="Speculative impacts presented as findings"),
    # WS-13 Gold, diamonds & other minerals
    "WS-13 Q1": dict(e="Inventory of producing/advancing gold, diamond, other mineral operations", g="MINING_SITE", p="C", k="MIXED", s="Mining cadastre; EITI reports; company filings", f="Industry databases (label)", d="Exploration vs development vs production", r="Exploration licences reported as producing mines"),
    "WS-13 Q2": dict(e="Site power demand, supply source and cost", g="MINING_SITE", p="H; C", k="QUANTITATIVE", s="ESIAs; company filings", f="Company presentations (own facts)", d="Peak vs annual energy; captive vs grid", r="Deriving demand from ore throughput without a source"),
    "WS-13 Q3": dict(e="Evidence that other minerals are strategically relevant for energy demand", g="MINING_SITE; NATIONAL_AGGREGATE", p="C; N; S", k="QUALITATIVE", s="Mining cadastre; EITI; government mining strategy", f="Geological survey publications", d="Deposit vs project vs operation", r="Inferring future demand from geology alone"),
    "WS-13 Q4": dict(e="Evidence on artisanal mining scale and energy use", g="LOCALITY; MINING_SITE", p="H; C", k="MIXED", s="Government/EITI reports; DFI/academic studies", f="NGO reports (corroborate)", d="Artisanal vs small-scale vs industrial", r="Extrapolating national figures from case studies"),
    # WS-14 Non-mining industrial, ports & commercial
    "WS-14 Q1": dict(e="Largest non-mining consumers: demand and supply source", g="INDUSTRIAL_SITE; CITY", p="H; C", k="QUANTITATIVE", s="Utility large-customer data; industrial registries", f="Enterprise surveys; company disclosures", d="Contracted vs actual demand; grid vs captive", r="Using installed equipment as consumption"),
    "WS-14 Q2": dict(e="Port and logistics hub electricity demand and supply", g="PORT", p="H; C; N", k="QUANTITATIVE", s="Port authority reports; port operator disclosures; ESIAs", f="DFI port project documents", d="Port demand vs port-area industrial demand", r="Mixing planned port expansions with current demand"),
    "WS-14 Q3": dict(e="Captive and backup generation use in non-mining industry and commerce", g="NATIONAL_AGGREGATE; CITY", p="H; C", k="MIXED", s="Enterprise surveys; telecom regulator data; utility studies", f="Industry estimates (method stated)", d="Captive (primary) vs backup supply", r="Equating telecom tower counts with energy demand without method"),
    "WS-14 Q4": dict(e="Planned industrial/special-economic-zone developments with lifecycle evidence", g="INDUSTRIAL_SITE; LOCALITY", p="N; S", k="MIXED", s="Government investment agency documents; official gazette", f="Press (lead)", d="Lifecycle stage per methodology §6", r="Announced zones reported as committed load"),
    # WS-15 Mining legal regime
    "WS-15 Q1": dict(e="Mining-code provisions (article-level) on energy, local processing, infrastructure sharing", g="NATIONAL_AGGREGATE", p="C", k="QUALITATIVE", s="Mining code and amendments in the official gazette", f="EITI/DFI legal reviews", d="Code provision vs implementing regulation", r="Citing an article number from the Gate 1 challenge without the text (GL-22)"),
    "WS-15 Q2": dict(e="Refining/local-processing obligations: instrument, deadline, enforcement record", g="NATIONAL_AGGREGATE; MINING_SITE", p="H; C; N", k="QUALITATIVE", s="Published conventions; official gazette; government enforcement acts", f="EITI contract disclosures; press (lead)", d="Obligation vs incentive vs stated intention; deadline vs extension", r="Assuming obligations exist or are enforced (GL-06)"),
    "WS-15 Q3": dict(e="Documented cases of infrastructure sharing/third-party access", g="MINING_SITE; PORT; TRANSMISSION_CORRIDOR", p="H; C", k="QUALITATIVE", s="Access agreements; regulator/ministry decisions", f="Company disclosures (own facts)", d="Legal provision vs applied precedent", r="Treating a provision as evidence of practice"),
    "WS-15 Q4": dict(e="Convention clauses on captive rights, grid obligations, fuel tax treatment", g="MINING_SITE", p="C", k="QUALITATIVE", s="Published mining conventions", f="EITI summaries", d="Captive right vs obligation to buy from grid", r="Generalising from one convention to all"),
    # WS-16 WAPP
    "WS-16 Q1": dict(e="Interconnector status per step: constructed, energised, synchronised, operational, commercially active", g="INTERCONNECTION; TRANSMISSION_CORRIDOR", p="C", k="MIXED", s="WAPP Secretariat/ICC reports; interconnector-operator reports; regulator decisions", f="DFI completion/status reports", d="Five distinct steps (D-069)", r="Collapsing physical completion into commercial operation"),
    "WS-16 Q2": dict(e="Metered cross-border trade (MWh) by direction, period, contract", g="INTERCONNECTION; NATIONAL_AGGREGATE", p="H", k="QUANTITATIVE", s="WAPP/ICC trade statistics; regional regulator reports; utility statistics", f="IEA/UN trade statistics (national totals)", d="Contracted vs metered vs settled energy; capacity vs energy", r="Reporting interconnection capacity as traded energy"),
    "WS-16 Q3": dict(e="Wheeling/transmission charges, settlement arrangements, documented arrears", g="INTERCONNECTION", p="H; C", k="MIXED", s="Regional regulator decisions; interconnector-operator reports; audit reports", f="Press (lead)", d="Wheeling charge vs transmission service charge; arrears vs disputed amounts", r="Inferring arrears without documentation"),
    "WS-16 Q4": dict(e="Technical conditions for synchronous operation and separation protection", g="INTERCONNECTION; NATIONAL_AGGREGATE", p="C", k="QUALITATIVE", s="WAPP operation manual; ICC reports; system-operator documents", f="Consultancy studies", d="Synchronous vs asynchronous/radial operation; UFLS/islanding schemes", r="Assuming synchronisation from energisation"),
    "WS-16 Q5": dict(e="Role assigned to Guinea in successive WAPP master plans; changes", g="MULTI_COUNTRY_REGION; NATIONAL_AGGREGATE", p="H; N; S", k="MIXED", s="WAPP master plans (each edition, dated)", f="DFI summaries of master plans", d="Master-plan priority project vs committed project", r="Master-plan inclusion reported as commitment"),
    "WS-16 Q6": dict(e="Benchmark metrics B1–B13 for Guinea and the seven benchmark countries", g="NEIGHBOURING_COUNTRY; NATIONAL_AGGREGATE", p="H; C", k="QUANTITATIVE", s="National utility/regulator statistics of each country; WAPP statistics", f="IEA/IRENA/World Bank databases (definition check)", d="Identical definitions across countries (research_architecture §M)", r="Comparing metrics with different definitions or years; drifting into a generic regional study"),
    # WS-17 Basins, hydrology, climate
    "WS-17 Q1": dict(e="Basin organisations/agreements with jurisdiction over rivers with Guinea hydro; obligations", g="RIVER_BASIN; NATIONAL_AGGREGATE", p="C", k="QUALITATIVE", s="Treaties and conventions; basin-organisation statutes and reports", f="DFI basin studies", d="Membership vs jurisdiction over specific rivers/projects vs operating obligations", r="Assuming each named organisation is relevant (D-037)"),
    "WS-17 Q2": dict(e="Inventory of streamflow, reservoir and gauge data: station, period, quality", g="RIVER_BASIN; PLANT_SITE", p="H", k="MIXED", s="National hydrological service; basin organisations; dam operators", f="Global runoff databases (label; record station IDs)", d="Observed vs modelled flows; record length; gaps", r="Treating modelled or reanalysis flows as observed"),
    "WS-17 Q3": dict(e="Seasonal and inter-annual flow patterns at existing/candidate sites", g="PLANT_SITE; RIVER_BASIN", p="H", k="QUANTITATIVE", s="Hydrological yearbooks; feasibility studies; dam operating reports", f="Peer-reviewed hydrology (method stated)", d="Mean vs dry-year flows; season definitions per source", r="Using long-term means to represent dry years"),
    "WS-17 Q4": dict(e="Climate projections relevant to hydrological variability", g="RIVER_BASIN; NATIONAL_AGGREGATE", p="S", k="MIXED", s="National climate communications/adaptation plans; peer-reviewed studies (model, scenario stated)", f="Global climate portals (dataset/version stated)", d="Projection vs scenario vs forecast; emissions scenario and model", r="Presenting a single model run as a forecast"),
    "WS-17 Q5": dict(e="Documented wet-season spill/curtailment events and causes", g="PLANT_SITE", p="H", k="MIXED", s="Dam/system-operator reports; DFI supervision reports", f="Press (lead)", d="Spill vs curtailment vs planned release", r="Inferring spill from capacity vs demand (GL-25)"),
    # WS-18 Solar
    "WS-18 Q1": dict(e="Solar resource (GHI/GTI) spatial and seasonal profiles", g="NATIONAL_AGGREGATE; REGIONAL", p="H", k="QUANTITATIVE", s="Ground measurement records; national meteorological data", f="Global Solar Atlas / reanalysis (dataset and version stated)", d="GHI vs GTI vs DNI; long-term average period", r="Treating satellite averages as site measurements"),
    "WS-18 Q2": dict(e="Evidence on yield-reducing factors (cloud, aerosols, soiling, temperature)", g="REGIONAL; PLANT_SITE", p="H", k="MIXED", s="Measurement campaigns; operating-plant performance reports", f="Aerosol/reanalysis datasets; peer-reviewed studies", d="Performance ratio; soiling loss definition", r="Applying loss factors from other regions without basis"),
    "WS-18 Q3": dict(e="Inventory of ground-measured solar data", g="PLANT_SITE; LOCALITY", p="H", k="QUALITATIVE", s="Meteorological service; ESMAP measurement programme records; project developers' disclosed data", f="Research station publications", d="Station vs satellite-derived data; measurement period", r="Assuming measurements exist because programmes were announced"),
    "WS-18 Q4": dict(e="Technical potential near load/network, method and constraints applied", g="REGIONAL; SUBSTATION_NODE", p="C; S", k="QUANTITATIVE", s="Official/DFI resource assessments", f="Peer-reviewed potential studies (method stated)", d="Theoretical vs technical vs economic potential; constraint set used", r="Reporting theoretical potential as developable"),
    # WS-19 Wind
    "WS-19 Q1": dict(e="Wind resource at hub height incl. coastal/elevated areas", g="NATIONAL_AGGREGATE; REGIONAL", p="H", k="QUANTITATIVE", s="Measurement campaigns; national meteorological data", f="Global Wind Atlas / reanalysis (dataset, height, version stated)", d="Mean wind speed vs power density; hub height", r="Pre-judging wind attractiveness (D-026)"),
    "WS-19 Q2": dict(e="Measured wind data and comparison with modelled datasets", g="LOCALITY; PLANT_SITE", p="H", k="MIXED", s="Mast/LiDAR campaign reports; meteorological service", f="Peer-reviewed validation studies", d="Measurement height; record length; correlation method", r="Treating modelled data as validated"),
    "WS-19 Q3": dict(e="Seasonal wind profile relative to hydro and solar profiles", g="REGIONAL", p="H", k="QUANTITATIVE", s="Measured series; reanalysis (stated)", f="Peer-reviewed complementarity studies", d="Monthly profiles on a common basis", r="Asserting complementarity without matched data"),
    "WS-19 Q4": dict(e="Technical potential near load/network, method and constraints applied", g="REGIONAL; SUBSTATION_NODE", p="C; S", k="QUANTITATIVE", s="Official/DFI resource assessments", f="Peer-reviewed potential studies (method stated)", d="Theoretical vs technical vs economic potential", r="Excluding wind on generic regional assumptions"),
    # WS-20 Hydro development
    "WS-20 Q1": dict(e="Studied hydro sites: study level, date, results", g="PLANT_SITE; RIVER_BASIN", p="H; C", k="MIXED", s="Hydro master plans; feasibility studies; basin-organisation project documents", f="DFI summaries", d="Inventory vs pre-feasibility vs feasibility vs detailed design", r="Treating inventory sites as projects"),
    "WS-20 Q2": dict(e="Candidate seasonal dependable output and firm energy", g="PLANT_SITE", p="N; S", k="QUANTITATIVE", s="Feasibility studies (hydrology basis stated)", f="Master-plan estimates (vintage stated)", d="Installed vs seasonal dependable vs firm energy (D-037)", r="Reporting installed capacity alone"),
    "WS-20 Q3": dict(e="Rehabilitation/uprating opportunities at existing plants", g="PLANT_SITE", p="C; N", k="MIXED", s="Utility/DFI rehabilitation studies", f="OEM/consultancy reports (corroborate)", d="Rehabilitation vs uprating vs life extension", r="Assuming degradation without evidence"),
    "WS-20 Q4": dict(e="Transboundary, environmental and resettlement constraints per site", g="PLANT_SITE; RIVER_BASIN", p="C", k="QUALITATIVE", s="ESIAs; basin-organisation rules; protected-area registries", f="NGO/academic studies (corroborate)", d="Legal exclusion vs regulatory constraint vs risk flag", r="Applying universal exclusion thresholds (D-038)"),
    # WS-21 BESS, hybrids & stability
    "WS-21 Q1": dict(e="System needs (firming, reserves, frequency response, congestion) documented in grid/operations evidence", g="NATIONAL_AGGREGATE; SUBSTATION_NODE", p="C; N", k="MIXED", s="Grid studies; system-operator reports; DFI studies", f="WAPP studies", d="Need vs solution; service definitions", r="Assuming storage is needed without a documented system need"),
    "WS-21 Q2": dict(e="Existing/planned storage or hybrid projects with lifecycle evidence", g="PLANT_SITE; MINING_SITE", p="C; N", k="MIXED", s="Project documents; procurement notices; company filings", f="Press (lead)", d="MW vs MWh; lifecycle stage", r="Reporting MW without MWh, or announcements as commitments"),
    "WS-21 Q3": dict(e="Use cases where storage/hybrids compete with alternatives", g="NATIONAL_AGGREGATE; PLANT_SITE", p="N; S", k="MIXED", s="System studies comparing options", f="IEA/IRENA/NREL technology data (labelled generic)", d="Use case; alternative technologies", r="Promoting a technology before comparison (D-027)"),
    "WS-21 Q4": dict(e="Grid-code/technical requirements applicable to storage and hybrid plants", g="NATIONAL_AGGREGATE", p="C", k="QUALITATIVE", s="Grid code; connection rules", f="Regional rules (labelled)", d="Grid-forming vs grid-following; connection requirements", r="Assuming requirements from other jurisdictions"),
    # WS-22 Decentralised energy
    "WS-22 Q1": dict(e="Institutions, laws and regulations governing mini-grids/off-grid", g="NATIONAL_AGGREGATE", p="C", k="QUALITATIVE", s="Legal texts; agency founding texts; regulator decisions", f="DFI off-grid diagnostics", d="Mini-grid licence vs concession vs registration", r="Assuming an agency operates as named in leads (GL-16)"),
    "WS-22 Q2": dict(e="Mini-grid tariff-setting rules and subsidy mechanisms", g="NATIONAL_AGGREGATE", p="C", k="MIXED", s="Regulatory decisions; programme operating manuals", f="DFI programme documents", d="Cost-reflective vs uniform tariff; capital vs results-based subsidy", r="Programme design reported as operating practice"),
    "WS-22 Q3": dict(e="Deployment record: mini-grids, SHS; who, where, results", g="LOCALITY; REGIONAL", p="H", k="QUANTITATIVE", s="Agency/programme reports; GOGLA-type sales data (label)", f="Developer disclosures (own facts)", d="Installed vs operational vs connected customers", r="Counting planned sites as deployed"),
    "WS-22 Q4": dict(e="Documented anchor-load and productive-use models and results", g="LOCALITY", p="H; C", k="QUALITATIVE", s="Programme evaluations; DFI completion reports", f="Developer case studies (own facts)", d="Anchor load; productive use", r="Generalising from pilots"),
    "WS-22 Q5": dict(e="Active donor/DFI programmes and eligibility rules", g="NATIONAL_AGGREGATE", p="C; N", k="QUALITATIVE", s="Programme documents and portals", f="Programme summaries (label)", d="Programme status (active/closed/pipeline)", r="Closed programmes reported as active"),
    # WS-23 Pipeline
    "WS-23 Q1": dict(e="Project list with evidenced lifecycle stage and progress condition", g="PLANT_SITE; TRANSMISSION_CORRIDOR", p="C; N; S", k="MIXED", s="Official project lists; DFI databases; procurement records", f="Company disclosures (corroborated); press (lead)", d="Methodology §6 stages/conditions", r="Silence read as stalled/cancelled; announcements as commitments"),
    "WS-23 Q2": dict(e="Evidence of duplicate/re-announced projects", g="PLANT_SITE", p="H; C", k="QUALITATIVE", s="Successive official lists; project documents with coordinates", f="Press histories (lead)", d="De-duplication by location, capacity, sponsor", r="Double-counting renamed projects"),
    "WS-23 Q3": dict(e="Capacity by stage, technology and year (aggregated only from evidenced project records)", g="NATIONAL_AGGREGATE", p="C; N; S", k="QUANTITATIVE", s="Derived from project-level evidence", f="Official pipeline summaries (definition stated)", d="Stage-specific totals; MW-AC/DC", r="Summing capacities across inconsistent stages/definitions"),
    "WS-23 Q4": dict(e="Patterns of delay/stall/cancellation and documented causes", g="NATIONAL_AGGREGATE", p="H", k="QUALITATIVE", s="Project documents; DFI status reports", f="Press (lead)", d="Delayed vs stalled vs cancelled (methodology §6.2)", r="Causal narratives without evidence"),
    # WS-24 International finance
    "WS-24 Q1": dict(e="Financing institutions, instruments and terms for Guinea energy projects since 2016", g="NATIONAL_AGGREGATE; PLANT_SITE", p="H", k="MIXED", s="DFI project databases; ECA disclosures; signed agreements", f="Research databases (label)", d="Commitment vs disbursement; loan vs grant vs guarantee", r="Approval reported as signed financing"),
    "WS-24 Q2": dict(e="Guarantee/insurance instruments available, eligibility, use", g="NATIONAL_AGGREGATE", p="H; C", k="QUALITATIVE", s="Guarantee-agency project lists and policies", f="DFI summaries", d="PRG vs PCG vs PRI; eligibility", r="Inferring availability from general mandate (D-039)"),
    "WS-24 Q3": dict(e="Active credit lines/bilateral programmes and conditions (e.g. sourcing)", g="NATIONAL_AGGREGATE", p="H; C", k="MIXED", s="Lender disclosures (e.g. EXIM LOC lists); signed agreements", f="Official press releases (own facts)", d="Line approved vs signed vs disbursing; tied conditions", r="Announced lines reported as active"),
    "WS-24 Q4": dict(e="Project-preparation and TA facilities available", g="NATIONAL_AGGREGATE", p="C", k="QUALITATIVE", s="Facility portals and documents", f="Summaries (label)", d="Facility eligibility; status", r="Closed facilities reported as open"),
    "WS-24 Q5": dict(e="Financing structures in completed transactions", g="PLANT_SITE", p="H", k="QUALITATIVE", s="DFI project documents; financial-close announcements by parties", f="Trade press (lead)", d="Structure elements actually used", r="Generalising one transaction into a requirement"),
    # WS-25 International ecosystem
    "WS-25 Q1": dict(e="Entities with evidenced Guinea activity and role", g="NATIONAL_AGGREGATE; PLANT_SITE", p="H; C", k="QUALITATIVE", s="Procurement awards; contracts; DFI documents", f="Company disclosures (own facts)", d="Five presence classes (WS-25)", r="Global presence treated as Guinea presence"),
    "WS-25 Q2": dict(e="Origin-country instruments/strategies relevant to Guinea", g="NATIONAL_AGGREGATE", p="C", k="QUALITATIVE", s="Government/agency documents of origin countries", f="Official summaries", d="Instrument vs strategy vs announcement", r="Strategy statements reported as Guinea commitments"),
    "WS-25 Q3": dict(e="Entities with regional presence only, by benchmark country", g="NEIGHBOURING_COUNTRY", p="C", k="QUALITATIVE", s="Procurement/contract records in benchmark countries", f="Company disclosures", d="Regional presence vs Guinea presence", r="Drifting into a generic regional company survey"),
    "WS-25 Q4": dict(e="Competitive landscape per technology/service segment (evidence-based)", g="NATIONAL_AGGREGATE", p="C", k="QUALITATIVE", s="Derived from evidenced entity records", f="Industry reports (label)", d="Segment definitions", r="Market-share claims without data"),
    # WS-26 Land, environment, social
    "WS-26 Q1": dict(e="Land tenure regimes and acquisition procedures", g="NATIONAL_AGGREGATE", p="C", k="QUALITATIVE", s="Land code and implementing texts; official gazette", f="DFI/academic land-governance studies", d="Statutory vs customary tenure; acquisition vs lease", r="Assuming procedures from other jurisdictions"),
    "WS-26 Q2": dict(e="Expropriation/compensation/resettlement frameworks and precedents", g="NATIONAL_AGGREGATE; LOCALITY", p="H; C", k="QUALITATIVE", s="Legal texts; RAPs disclosed by projects; DFI safeguard documents", f="NGO reports (corroborate)", d="Legal framework vs DFI standard (IFC PS5); compensation basis", r="Treating one project's compensation rates as national standard"),
    "WS-26 Q3": dict(e="ESIA process, competent authority, practical timelines", g="NATIONAL_AGGREGATE", p="C", k="MIXED", s="Environmental code and ESIA regulations; authority publications", f="DFI project timelines (examples labelled)", d="Statutory vs observed timelines", r="Statutory timelines reported as actual"),
    "WS-26 Q4": dict(e="Protected areas, critical habitats, sensitive zones and legal status", g="NATIONAL_AGGREGATE; LOCALITY", p="C", k="MIXED", s="Official protected-area gazettes; WDPA (licence terms noted)", f="IUCN/KBA/IBAT datasets (licence terms)", d="Legal protection vs conservation designation vs habitat data", r="Treating a conservation dataset as a legal exclusion"),
    "WS-26 Q5": dict(e="Documented flood and other physical climate hazards", g="REGIONAL; LOCALITY", p="H; S", k="MIXED", s="National hazard maps; disaster-management reports", f="Global hazard datasets (version stated)", d="Hazard vs exposure vs risk", r="Global coarse data presented as site-level hazard"),
    "WS-26 Q6": dict(e="Documented community conflict around energy/mining projects and causes", g="LOCALITY; MINING_SITE", p="H; C", k="QUALITATIVE", s="Official/judicial records; ESIA grievance reports; DFI accountability-mechanism cases", f="NGO/press reports (corroborate)", d="Grievance vs protest vs litigation", r="Attributing causes without evidence"),
}

PERIOD_LABEL = {"H": "2016–2026 historical", "C": "current status (as-of date)", "N": "2027–2030 near-term", "S": "2030–2035 strategic"}

# ---------------------------------------------------------------------------
# Mission-specific content
# ---------------------------------------------------------------------------
M = {}


def mission(mid, slug, questions, **kw):
    M[mid] = dict(id=mid, slug=slug, questions=questions, **kw)


mission("GEM-01", "fuel-logistics-thermal",
        ["WS-03 Q1", "WS-03 Q2", "WS-03 Q3", "WS-03 Q4", "WS-03 Q5", "WS-03 Q6", "WS-05 Q5", "WS-05 Q6"],
        geo="National supply chain from import points to representative coastal and inland consumption locations (power plants, mining sites). Geography at PORT / PLANT_SITE / MINING_SITE level wherever the source allows.",
        temporal="Historical volumes and prices 2016–2026; current status of storage infrastructure (as-of date); gas/LNG proposals classified by lifecycle stage for 2027–2035.",
        strategy=["Official petroleum-sector and customs import statistics (volumes by product, by year).",
                  "Port-authority and petroleum-agency publications on reception and storage infrastructure and its status.",
                  "Fuel price-setting instruments (decrees/orders) and finance-ministry/IMF analyses of fuel taxation and subsidies.",
                  "Utility technical/financial reports for plant fuel use, heat rates and rental-power contracts.",
                  "ESIAs and company filings of mining/industrial operators for delivered fuel costs (own facts).",
                  "DFI sector diagnostics and supervision reports as Tier 3 cross-checks."],
        boundaries=("IN: fuels for public and captive power generation; import, storage and distribution infrastructure; pricing; delivered cost; thermal fleet performance; rental power; gas/LNG proposals.",
                    "OUT: transport-sector fuel demand except where it determines logistics costs; global oil-market analysis; recommendations on fuel choice."),
        quant=[("Fuel volumes for power generation", "volume (litres, m³ or tonnes), fuel grade, year, consumer type (public/captive), geography"),
               ("Storage capacity", "nameplate vs operational capacity (m³), facility, as-of date"),
               ("Fuel prices / delivered cost", "value, currency, nominal, date, location, fuel grade, cost components (product, freight, handling, taxes, margins)"),
               ("Thermal plant performance", "heat rate (basis LHV/HHV, gross/net), fuel type, derating factor, plant, period"),
               ("Rental power", "contracted MW, tenor, capacity charge and energy charge (currency, nominal, date)")],
        terms=[("Delivered (landed) fuel cost", "Total cost at the point of use = product + logistics + taxes + margins, with each component and its date and currency stated."),
               ("Ex-depot vs retail price", "Price at storage terminal vs regulated pump price; neither is a delivered cost to a power plant."),
               ("Heat rate", "Fuel energy per kWh generated; state LHV/HHV and gross/net basis."),
               ("Rental power", "Contracted generating capacity owned by a third party; never counted as utility-owned capacity.")],
        cross=["Import volumes vs utility-reported fuel consumption (same year, same fuel).",
               "Price instruments vs reported delivered costs (same date and currency).",
               "Storage capacity reported by different authorities (nameplate vs operational)."],
        contradictions=["Litres vs tonnes without density", "Calendar vs fiscal year", "Nameplate vs operational storage after an incident"],
        traps=["Total petroleum imports ≠ fuel used for power generation.",
               "Retail or pump price ≠ delivered fuel cost at a power plant or mine.",
               "Delivered cost markups must never be applied as generic percentages (GL-23 is a lead, not evidence).",
               "A reported disruption event (GL-02) must be evidenced in primary sources, and its effect on generation separately evidenced.",
               "Nameplate storage capacity ≠ operational capacity after an incident.",
               "Rental/emergency capacity ≠ owned or permanent capacity.",
               "Generic OEM heat rates ≠ measured plant heat rates.",
               "An LNG/FSRU study or MoU ≠ a committed gas-import project.",
               "Absence of recent news about a depot or plant ≠ closure or stalling."],
        artifacts=[],
        limitations=["Plant-level fuel and cost data may be commercially confidential.", "Delivered-cost evidence may exist only for a few locations."],
        followups=["Whether a targeted mission on delivered-cost evidence at specific consumption locations is warranted.", "Whether rental-power contract terms are available in audit or IMF documents."],
        candidates=["Société Nationale des Pétroles (SONAP) — name, mandate and current status unverified (GL-16)",
                    "French search terms: « importations de produits pétroliers », « structure des prix des produits pétroliers », « fioul lourd », « dépôt pétrolier », « centrale thermique »"])

mission("GEM-02", "river-basins-hydrology",
        ["WS-17 Q1", "WS-17 Q2", "WS-17 Q3", "WS-17 Q4", "WS-17 Q5", "WS-05 Q2", "WS-05 Q4"],
        geo="River basins with existing or candidate Guinea hydropower (RIVER_BASIN), individual plants and gauges (PLANT_SITE). Other basin states only where an agreement, shared asset or obligation affects Guinea hydro.",
        temporal="Hydrological records as far back as available (record length stated) with focus on 2016–2026 operations; climate projections for 2030–2035 (model and scenario stated).",
        strategy=["Treaty and convention texts and basin-organisation statutes (jurisdiction, obligations, operating rules).",
                  "National hydrological service yearbooks and gauge inventories.",
                  "Dam-operator and system-operator reports for monthly generation and dispatch rules.",
                  "Feasibility studies and DFI hydro studies for seasonal and firm output.",
                  "National climate communications/adaptation plans and peer-reviewed hydro-climate studies."],
        boundaries=("IN: basin governance affecting Guinea hydro; hydrological data; seasonal output and dependable capacity; operating rules; documented spill; climate projections.",
                    "OUT: general water-resources policy, irrigation and navigation except where they constrain hydro operation; basin states' internal power systems."),
        quant=[("Streamflow", "m³/s, station, period (monthly/annual), observed vs modelled, record length"),
               ("Hydro output", "monthly generation (GWh, gross/net), plant, year"),
               ("Seasonal dependable capacity", "MW per month/season, plant, season definition per source, hydrological basis"),
               ("Reservoir data", "storage volume, operating levels, plant, as-of date"),
               ("Spill events", "volume or energy, plant, period, documented cause")],
        terms=[("Seasonal dependable capacity", "Dependable capacity per month or season (methodology §5); always with nameplate."),
               ("Basin relevance", "Classify each organisation as relevant / partly relevant / not relevant to Guinea hydro, with evidence."),
               ("Spill vs curtailment", "Water released without generation vs generation reduced for system reasons; only where documented.")],
        cross=["Monthly generation vs streamflow records for the same plant and year.",
               "Basin-organisation documents vs national documents on obligations.",
               "Feasibility-study firm energy vs observed dry-season output."],
        contradictions=["Season definitions differing between sources", "Mean-year vs dry-year values", "Modelled vs observed flows"],
        traps=["Membership of a basin organisation ≠ jurisdiction over a specific Guinea river or plant (D-037).",
               "Installed capacity ≠ dependable output; an annual average ≠ seasonal dependable capacity.",
               "A cascade relationship between named plants (GL-12) must be evidenced in operating documents, not inferred from geography.",
               "Modelled or reanalysis flows ≠ observed gauge records.",
               "Long-term mean flow ≠ dry-year flow.",
               "Spill must not be inferred from capacity exceeding demand (GL-25).",
               "A climate projection (one model/scenario) ≠ a forecast.",
               "Wet/dry season month ranges must come from sources; GL-03 is internally inconsistent and is not evidence."],
        artifacts=[("Hydrological dataset inventory", "Markdown table listing datasets/stations (name, custodian, station ID, period, access terms, URL); no data downloaded or copied")],
        limitations=["Gauge records may have gaps or restricted access.", "Basin documents may be in French and not digitised."],
        followups=["Whether specific gauge datasets justify a data-acquisition request outside Gemini.", "Whether dispatch rules require direct engagement with the system operator."],
        candidates=["OMVG, OMVS, ABN — named by the sponsor/Gemini; relevance to be investigated, not assumed",
                    "French search terms: « annuaire hydrologique », « débits mensuels », « règlement d'exploitation du barrage », « productible garanti »"])

mission("GEM-03", "mining-industrial-energy",
        ["WS-11 Q1", "WS-11 Q2", "WS-11 Q3", "WS-11 Q4", "WS-11 Q5", "WS-12 Q1", "WS-12 Q2", "WS-12 Q3",
         "WS-13 Q1", "WS-13 Q2", "WS-13 Q3", "WS-13 Q4", "WS-14 Q1", "WS-14 Q2", "WS-14 Q3"],
        geo="Site level (MINING_SITE, INDUSTRIAL_SITE, PORT) for every operation; national aggregates only when built up from sites or sourced as such.",
        temporal="Current operations and supply arrangements (as-of date); historical production and energy data 2016–2026; expansions and refineries classified by lifecycle stage for 2027–2035.",
        strategy=["Mining cadastre and EITI reports to build the inventory of operations (not a pre-set list).",
                  "ESIAs and environmental permits for site power demand, captive capacity and fuel.",
                  "Company statutory filings and annual reports (own facts only).",
                  "Parent-company sustainability reports for decarbonisation targets.",
                  "DFI/ECA project documents where an operation was financed."],
        boundaries=("IN: bauxite extraction, alumina refining (separately), Simandou components (shared with GEM-12), gold, diamonds, other minerals evidenced as relevant, major non-mining industrial and port loads.",
                    "OUT: commodity-market forecasts; company valuation; any assessment of willingness to sign PPAs (Phase A objectivity)."),
        quant=[("Site electrical demand", "peak MW and/or annual GWh, site, year, basis (design vs operating)"),
               ("Site thermal demand", "steam t/h or thermal MW, site, basis"),
               ("Captive capacity", "installed MW (AC/DC for PV), technology, fuel, site, as-of date"),
               ("Fuel use and cost", "volume, fuel grade, delivered cost (currency, nominal, date), site"),
               ("Production", "output (t or Mtpa), commodity, site, year — never used to derive energy without a sourced intensity")],
        terms=[("Extraction vs processing vs refining", "Mining/haulage vs beneficiation vs chemical/metallurgical transformation; energy recorded separately for each."),
               ("Captive generation", "On-site or contracted generation for own use; capacity, fuel and technology stated."),
               ("Lifecycle stage", "Methodology §6 stages applied to each site and expansion.")],
        cross=["Cadastre/EITI inventory vs company filings (operator, status).",
               "ESIA design demand vs company-reported operating demand.",
               "Captive capacity in permits vs company disclosures."],
        contradictions=["Design vs operating demand", "Group-level vs site-level figures", "Different production units (wet vs dry tonnes)"],
        traps=["Bauxite extraction ≠ alumina refining; their energy demands must never be merged.",
               "Nearby transmission ≠ grid supply to a site.",
               "Production capacity ≠ electricity consumption.",
               "Captive generation technology and fuel must be verified per site.",
               "Mine expansion ≠ committed electricity demand.",
               "A refining obligation or announcement ≠ an operating or committed refinery (GL-06).",
               "No generic refinery load may be used (GL-10 is internally inconsistent; D-026).",
               "Group decarbonisation targets ≠ site-level commitments or PPA appetite.",
               "Company names, ownership and assets given in the Gate 1 challenge (GL-19) are leads, not facts."],
        artifacts=[("Site candidate list", "Markdown table of candidate sites (name, operator as stated, commodity, source ID) supporting the inventory; each row cites a source or is marked NO SOURCE — LEAD ONLY")],
        limitations=["Site energy data may be confidential or available only in ESIAs.", "Artisanal mining data may be sparse."],
        followups=["Whether specific refinery projects warrant targeted missions.", "Whether ESIAs are accessible from the environmental authority."],
        candidates=["Mining cadastre authority (name to verify; GL-16 suggests « Centre de Promotion et de Développement Minier (CPDM) » — unverified)",
                    "EITI Guinea (ITIE Guinée) reports",
                    "French search terms: « étude d'impact environnemental et social », « centrale captive », « consommation électrique du site »"])

mission("GEM-04", "mining-legal-private-supply",
        ["WS-15 Q1", "WS-15 Q2", "WS-15 Q3", "WS-15 Q4", "WS-02 Q4"],
        geo="National legal framework (NATIONAL_AGGREGATE); site level (MINING_SITE) for convention-specific clauses and precedents.",
        temporal="Current legal texts (latest amendment, as-of date); historical enforcement and precedents 2016–2026; stated deadlines classified as obligations, not events.",
        strategy=["Official gazette texts of the mining code and amendments.",
                  "Published mining conventions (government or EITI contract disclosures).",
                  "Electricity law and decrees for self-generation, private sale and third-party access.",
                  "Government enforcement acts, arbitration records, regulator decisions.",
                  "DFI legal reviews (Tier 3) and EITI reports (Tier 1) for interpretation, labelled as such."],
        boundaries=("IN: mining-law energy, local-processing and infrastructure-sharing provisions; convention clauses; enforcement record; electricity-law private-supply pathways.",
                    "OUT: general mining fiscal regime except energy-related clauses; legal advice or opinions."),
        quant=[("Deadlines and thresholds in legal instruments", "value as written, unit, instrument, article, date of instrument"),
               ("Enforcement events", "count/date of documented enforcement acts, instrument reference")],
        terms=[("Obligation vs incentive vs intention", "Binding legal requirement vs optional benefit vs stated aim."),
               ("Self-generation vs private sale vs third-party access", "Generation for own use vs sale to another party vs use of another party's network."),
               ("Text vs application", "What the instrument says vs evidence of how it has been applied.")],
        cross=["Gazette text vs secondary summaries of the same article.",
               "Convention clauses vs government enforcement communications."],
        contradictions=["Superseded vs current text", "Article numbering differing between versions"],
        traps=["An article number cited in the Gate 1 challenge (GL-22) must be located in the current text before use.",
               "A legal provision ≠ evidence that it has been applied.",
               "A refining obligation in one convention ≠ an obligation for all operators.",
               "A stated deadline ≠ a deadline met or enforced; an extension may exist.",
               "Mining-law infrastructure provisions ≠ electricity-law authorisation to sell power.",
               "Interpretations by law firms or Gemini are not law; label them and cite the text.",
               "Silence on enforcement ≠ non-enforcement."],
        artifacts=[("Legal instrument index", "Markdown table: instrument title (original language), number, date, article, URL/reference, access status; no full-text copies")],
        limitations=["Some conventions may not be public.", "Official gazette digitisation may be incomplete."],
        followups=["Whether specific conventions must be requested from authorities.", "Whether professional legal review is needed before reliance (verify with a qualified professional before acting)."],
        candidates=["Mining code (« Code minier ») and amendments; « conventions minières »; « Journal Officiel de la République de Guinée »; « Code de l'électricité » — titles/currency to verify (GL leads)"])

mission("GEM-05", "utility-operations-finance-network",
        ["WS-09 Q1", "WS-09 Q2", "WS-09 Q3", "WS-09 Q4", "WS-09 Q5",
         "WS-06 Q1", "WS-06 Q2", "WS-06 Q3", "WS-06 Q4", "WS-06 Q5",
         "WS-07 Q2", "WS-07 Q3", "WS-07 Q4", "WS-07 Q5",
         "WS-08 Q1", "WS-08 Q2", "WS-08 Q3", "WS-08 Q5"],
        completion=["WS-06 Q5", "WS-07 Q2", "WS-07 Q4", "WS-07 Q5", "WS-08 Q5"],
        geo="National utility and grid (NATIONAL_AGGREGATE); transmission corridors and substations (TRANSMISSION_CORRIDOR, SUBSTATION_NODE); regional/city breakdowns where sources provide them.",
        temporal="Financial and operational series 2016–2026; current network status (as-of date); reinforcement projects by lifecycle stage for 2027–2035.",
        strategy=["Utility financial statements (audited/unaudited stated) and annual reports.",
                  "Supreme audit institution reports on the utility.",
                  "Tariff decisions and cost-of-service studies.",
                  "World Bank/IMF/AfDB project and country documents on the power sector.",
                  "Grid studies, transmission master plans and system-operator reports.",
                  "DFI transmission/distribution project appraisal and completion documents."],
        boundaries=("IN: utility finances, tariffs, collection, payment record, credit-enhancement precedents; transmission topology and constraints; distribution customers, losses, metering, demand-side measures; reliability and operations.",
                    "OUT: generation-fleet analysis (GEM-14/GEM-01/GEM-02); access-rate surveys (GEM-08 primary); any conclusion on creditworthiness beyond reported indicators."),
        quant=[("Financial statement items", "value, currency, nominal, fiscal year, audited/unaudited, statement line definition"),
               ("Tariffs", "value by customer class and component, currency, nominal, effective date, instrument"),
               ("Collection and arrears", "rate (definition: cash ÷ billed, period) or amount, counterparty class, date"),
               ("Network assets", "line km by voltage and status (constructed/energised), transformer MVA, loading %, as-of date"),
               ("Losses", "% by partition (base stated), year, measurement method"),
               ("Reliability", "SAIDI/SAIFI/hours of supply with definition, region, period")],
        terms=[("Collection rate", "Cash collected ÷ amount billed for a stated period and customer class."),
               ("Constructed vs energised", "Methodology §5; a line counts as energised only with evidence."),
               ("Loss partitions", "Transmission technical / distribution technical / non-technical, base and method stated."),
               ("Tariff vs cost of supply", "Never equated (protocol §5.2).")],
        cross=["Utility statements vs audit reports vs IMF/World Bank figures (same year, same definition).",
               "Network status in master plans vs DFI completion reports.",
               "Utility-reported reliability vs enterprise-survey indicators (labelled)."],
        contradictions=["Audited vs unaudited figures", "Billed vs collected revenue", "Constructed vs energised line lengths"],
        traps=["Financial stress indicators ≠ insolvency; never characterise the utility without cited indicators (D-026).",
               "Billed revenue ≠ collected revenue.",
               "Programme loss-reduction targets ≠ achieved results.",
               "Generic regional loss ranges (GL-24) ≠ Guinea data.",
               "A financed SCADA/EMS project ≠ a commissioned system.",
               "A master-plan reinforcement ≠ a committed project.",
               "Constructed line ≠ energised line.",
               "One transaction's credit enhancement ≠ a general requirement (D-039).",
               "Satellite night-light changes ≠ measured reliability."],
        artifacts=[],
        limitations=["Audited statements may be delayed or unpublished.", "Network data may be restricted for security reasons."],
        followups=["Whether audit reports for specific years can be obtained.", "Whether grid studies require direct request to the utility or DFIs."],
        candidates=["Électricité de Guinée (EDG) — named by the sponsor; condition to be evidenced, not presumed",
                    "Supreme audit institution (« Cour des Comptes » per GL-16 — unverified)",
                    "French search terms: « états financiers », « taux de recouvrement », « pertes techniques et non techniques », « grille tarifaire »"])

mission("GEM-06", "wapp-interconnection-trade",
        ["WS-16 Q1", "WS-16 Q2", "WS-16 Q3", "WS-16 Q4", "WS-16 Q5", "WS-16 Q6"],
        geo="Guinea's interconnectors and border substations (INTERCONNECTION, TRANSMISSION_CORRIDOR); benchmark countries (NEIGHBOURING_COUNTRY) only for benchmark metrics B1–B13 or direct effects on Guinea (protocol §7.2).",
        temporal="Current status per interconnector step (as-of date); metered trade 2016–2026; master-plan roles across editions (each dated) to 2035.",
        strategy=["WAPP Secretariat and Information and Coordination Centre (ICC) reports and statistics.",
                  "Regional regulator decisions (tariffs, market rules, disputes).",
                  "Interconnector-operator annual reports.",
                  "DFI interconnection project appraisal/status/completion documents.",
                  "National utility statistics of Guinea and counterparties for metered flows."],
        boundaries=("IN: interconnector physical and commercial status; trade volumes; wheeling and settlement; synchronisation; master-plan role; benchmark metrics.",
                    "OUT: generic regional market studies; benchmark countries' internal policies unless they affect Guinea."),
        quant=[("Interconnector status", "each of the five steps (YES/NO/UNVERIFIED) with evidence and date"),
               ("Trade", "MWh by direction, period, contract; contracted vs metered vs settled"),
               ("Transfer capacity", "MW with basis (thermal/contractual/stability), as-of date"),
               ("Charges", "wheeling/transmission charges, currency, nominal, effective date, instrument"),
               ("Benchmark metrics", "B1–B13 with identical definitions; country, year, source")],
        terms=[("Constructed / energised / synchronised / operational / commercially active", "Five distinct steps (protocol §8.4; D-069)."),
               ("Contracted vs metered vs settled energy", "Contract quantity vs measured flow vs financially settled quantity."),
               ("Transfer capacity vs traded energy", "MW capability vs MWh actually traded.")],
        cross=["WAPP/ICC data vs national utility data for the same flows.",
               "DFI completion reports vs operator reports on energisation dates.",
               "Benchmark metrics vs international databases (definition check)."],
        contradictions=["Commissioning vs commercial-operation dates", "Contracted vs metered volumes", "Different master-plan editions"],
        traps=["Physical line completion ≠ energised.",
               "Energised ≠ synchronised.",
               "Synchronised ≠ operational.",
               "Operational ≠ commercially active.",
               "Interconnection capacity ≠ actual traded or imported power.",
               "Master-plan inclusion ≠ committed project.",
               "Arrears must be documented, not inferred from financial stress.",
               "Benchmark data with different definitions or years must not be compared silently.",
               "Interconnector and substation names from the Gate 1 challenge (GL-31) are leads."],
        artifacts=[],
        limitations=["Trade and settlement data may be confidential.", "Status updates may lag in public reports."],
        followups=["Whether settlement data can be obtained from regional bodies.", "Whether benchmark gaps require country-specific searches."],
        candidates=["WAPP Secretariat / ICC; ECOWAS Regional Electricity Regulatory Authority (ERERA); interconnector operators (names to verify, GL-31)"])

mission("GEM-07", "international-finance-ecosystem",
        ["WS-24 Q1", "WS-24 Q2", "WS-24 Q3", "WS-24 Q4", "WS-24 Q5", "WS-25 Q1", "WS-25 Q2", "WS-25 Q3", "WS-25 Q4", "WS-04 Q5"],
        geo="Transactions and entities with Guinea energy activity (NATIONAL_AGGREGATE, PLANT_SITE); benchmark countries only for WS-25 regional-presence classification (NEIGHBOURING_COUNTRY).",
        temporal="Financings and transactions 2016–2026; instrument and facility status as of the search date (active/closed/pipeline).",
        strategy=["DFI project databases (World Bank, IFC, AfDB, EIB, IsDB and bilateral DFIs) filtered to Guinea energy.",
                  "Guarantee and insurance agency project lists (e.g. MIGA) and policies.",
                  "ECA/EXIM disclosures and line-of-credit lists; signed agreements.",
                  "Procurement award notices and contracts for entity presence.",
                  "Research databases (e.g. on Chinese lending) labelled as Tier 4."],
        boundaries=("IN: financing institutions, instruments, eligibility, transaction precedents; entity register by origin with evidenced Guinea presence; FX treatment observed in transactions.",
                    "OUT: proposing financing structures; ranking entities as partners; Alendei fit."),
        quant=[("Financing amounts", "commitment vs disbursement, currency, nominal, date, instrument, project"),
               ("Credit-line terms", "amount, currency, status (approved/signed/disbursing), conditions, date"),
               ("Guarantee/insurance cover", "amount, currency, risk covered, project, date")],
        terms=[("Commitment vs disbursement vs approval", "Board approval ≠ signed agreement ≠ disbursement."),
               ("Presence classes", "Five WS-25 classes; Guinea-specific evidence required."),
               ("Origin sub-registers", "India, China, Europe, Middle East, USA, Japan/Korea, Africa (regional), other.")],
        cross=["Lender database entries vs signed-agreement announcements by both parties.",
               "Company presence claims vs procurement/contract records."],
        contradictions=["Approved vs signed amounts", "Currency of record", "Project naming across databases"],
        traps=["Global presence ≠ Guinea presence.",
               "Board approval ≠ signed financing ≠ disbursement.",
               "An announced credit line ≠ an active credit line.",
               "An institution's general mandate ≠ availability of an instrument for Guinea (D-039).",
               "One transaction's structure ≠ a market requirement; offshore escrow is not presumed (D-026).",
               "A framework agreement (e.g. GL-18) ≠ specific project financing.",
               "Entity lists in the Gate 1 challenge (GL-18 – GL-21) are leads only."],
        artifacts=[("Entity candidate list", "Markdown table of candidate entities (name, origin, role claimed, source ID, presence class proposed); every row sourced or marked NO SOURCE — LEAD ONLY")],
        limitations=["Some bilateral financing is not publicly disclosed.", "Databases use inconsistent project names."],
        followups=["Whether specific transactions need document requests.", "Whether origin-specific deep dives are warranted."],
        candidates=["World Bank Projects & Operations; IFC project disclosures; AfDB project portal; MIGA projects; EIB projects; IsDB; IATI registry; EXIM Bank of India LOC lists; research databases on Chinese lending to Africa"])

mission("GEM-08", "decentralised-energy",
        ["WS-22 Q1", "WS-22 Q2", "WS-22 Q3", "WS-22 Q4", "WS-22 Q5", "WS-07 Q1"],
        geo="National framework (NATIONAL_AGGREGATE); deployment at LOCALITY/REGIONAL level; access rates by region, urban/rural and tier.",
        temporal="Framework as of search date; deployment 2016–2026; programme status (active/closed/pipeline) and planned rollouts to 2030.",
        strategy=["Legal texts and founding texts of the rural electrification institution(s).",
                  "Regulatory decisions on mini-grid licensing and tariffs.",
                  "Donor/DFI programme documents, portals and evaluations.",
                  "National household surveys and MTF surveys for access by tier.",
                  "Developer disclosures (own facts) and industry sales data (labelled)."],
        boundaries=("IN: mini-grid and off-grid framework, tariffs, subsidies, deployment, anchor loads, programmes, access statistics by tier.",
                    "OUT: grid distribution operations (GEM-05); technology recommendations."),
        quant=[("Deployment", "number of mini-grids/SHS, capacity (kW/kWp with AC/DC), connected customers, locality, as-of date; installed vs operational"),
               ("Tariffs/subsidies", "value, currency, nominal, effective date, instrument/programme"),
               ("Access rates", "% by definition (connection vs household; MTF tier), geography, survey year")],
        terms=[("Mini-grid vs SHS", "Distribution network serving multiple customers vs individual system."),
               ("Installed vs operational", "Built vs currently functioning."),
               ("MTF tiers", "World Bank Multi-Tier Framework definitions.")],
        cross=["Programme-reported deployment vs agency records.",
               "Survey-based access vs utility connection data."],
        contradictions=["Installed vs operational counts", "Access definitions differing by survey"],
        traps=["A programme announcement ≠ deployment.",
               "Installed mini-grids ≠ operational mini-grids.",
               "Pilot results ≠ scalable model.",
               "Agency names from the Gate 1 challenge (GL-16) must be verified (existence, current name, mandate).",
               "A closed programme ≠ an active programme.",
               "Connection counts ≠ household access rates.",
               "Programme names in the Gate 1 challenge (GL-17) are leads."],
        artifacts=[],
        limitations=["Deployment data may be fragmented across programmes.", "Survey years may be dated."],
        followups=["Whether programme databases can be obtained from implementing agencies."],
        candidates=["Rural electrification agency (GL-16 suggests « Agence Guinéenne d'Électrification Rurale (AGER) » — unverified)",
                    "French search terms: « mini-réseaux », « électrification rurale », « kits solaires »"])

mission("GEM-09", "macro-political-fx",
        ["WS-01 Q1", "WS-01 Q2", "WS-01 Q3", "WS-01 Q4", "WS-01 Q5", "WS-04 Q1", "WS-04 Q2", "WS-04 Q3", "WS-04 Q4", "WS-04 Q5"],
        geo="National level (NATIONAL_AGGREGATE); project level (PLANT_SITE) only for transaction currency clauses.",
        temporal="Macro and FX series 2016–2026; current regulations (as-of date); strategy targets to 2035 classified as targets.",
        strategy=["Central bank regulations, instructions and statistical publications.",
                  "IMF Article IV and programme documents; IMF AREAER.",
                  "National statistics and budget documents.",
                  "Rating-agency and OECD country-risk publications.",
                  "DFI project documents for transaction-level currency treatment."],
        boundaries=("IN: macro structure, fiscal space, political-economy events affecting concessions, country risk, monetary/FX regime, FX and repatriation rules, transaction currency treatment.",
                    "OUT: macro forecasting; investment advice; financing-structure proposals."),
        quant=[("Macro indicators", "value, unit, currency, nominal/real (base year), year, source vintage"),
               ("Exchange rates", "rate (quote per base currency), rate type (period average/end-period), source class, date — recorded as FX_RATE evidence (D-070)"),
               ("Fiscal/debt indicators", "value, % of GDP (definition), year, gross/net")],
        terms=[("De jure vs de facto regime", "Officially declared vs observed exchange-rate arrangement."),
               ("Surrender vs repatriation requirement", "Obligation to sell FX to authorities vs obligation to bring earnings onshore."),
               ("Target vs plan vs commitment", "Protocol §6.2.")],
        cross=["Central bank data vs IMF IFS (same series and date).",
               "Legal FX texts vs IMF AREAER descriptions."],
        contradictions=["Data vintages/revisions", "Official vs parallel rates"],
        traps=["FX scarcity, surrender rules or escrow requirements must not be presumed (D-026; GL-09).",
               "Parallel-market anecdotes ≠ official rates.",
               "Strategy targets ≠ plans or commitments.",
               "Stale ratings ≠ current ratings.",
               "Political commentary ≠ documented event.",
               "Contract currency must not be inferred from sponsor nationality.",
               "Effects of political transitions on concessions (GL-30) require documented acts."],
        artifacts=[],
        limitations=["Regulations may be amended frequently; record instrument dates.", "Some FX instructions may be unpublished."],
        followups=["Whether professional legal/financial review is needed for FX rules (verify with a qualified professional before acting)."],
        candidates=["Central bank (GL-16 suggests « Banque Centrale de la République de Guinée (BCRG) » — unverified)",
                    "French search terms: « réglementation des changes », « rapatriement des recettes d'exportation », « instruction BCRG »"])

mission("GEM-10", "electricity-law-regulation",
        ["WS-02 Q1", "WS-02 Q2", "WS-02 Q3", "WS-02 Q4", "WS-02 Q5", "WS-02 Q6", "WS-09 Q2"],
        geo="National legal and institutional framework (NATIONAL_AGGREGATE).",
        temporal="Instruments in force as of search date with amendment history; IPP/PPP awards 2016–2026; announced reforms classified by stage.",
        strategy=["Official gazette and ministry legal repositories.",
                  "Regulator website and published decisions.",
                  "Procurement authority award notices.",
                  "Founding texts and reports of sector institutions.",
                  "DFI legal and regulatory diagnostics (Tier 3), law-firm guides (interpretive)."],
        boundaries=("IN: electricity legislation, institutions and mandates, licensing/concession/procurement routes, private-supply pathways, tariff process, grid code, mini-grid regulation (cross-reference GEM-08).",
                    "OUT: mining law (GEM-04); legal opinions."),
        quant=[("Tariff schedules", "value by class and component, currency, nominal, effective date, instrument"),
               ("Awards", "count/date of awards by route, instrument reference")],
        terms=[("Law vs decree vs order", "Hierarchy of instruments; cite number and date."),
               ("Licence vs concession vs PPA", "Authorisation vs long-term right vs offtake contract."),
               ("Mandate vs operation", "Legal establishment vs evidence of functioning.")],
        cross=["Gazette texts vs regulator summaries.",
               "Procurement notices vs DFI project documents."],
        contradictions=["Superseded vs current instrument", "Different institutional names over time"],
        traps=["A body created by law ≠ an operating body.",
               "A draft or proposed law ≠ a law in force.",
               "A proposed tariff ≠ an approved tariff.",
               "Regional grid rules ≠ national grid code.",
               "Practice ≠ legality; legality must be evidenced in texts.",
               "Institution names and the regulator's history from the Gate 1 challenge (GL-16) are leads.",
               "An MoU or announced IPP ≠ an award."],
        artifacts=[("Legal instrument index", "Markdown table: instrument title (original language), number, date, article(s), URL/reference, in-force status; no full-text copies")],
        limitations=["Gazette digitisation may be incomplete.", "Institutional websites may be outdated."],
        followups=["Whether professional legal review is required before reliance (verify with a qualified professional before acting)."],
        candidates=["Energy ministry (GL-16 suggests « Ministère de l'Énergie, de l'Hydraulique et des Hydrocarbures » — unverified)",
                    "Electricity regulator (name and status to verify; GL-16)", "Public procurement authority (name to verify; GL-16)",
                    "French search terms: « Code de l'électricité », « décret d'application », « autorité de régulation », « contrat d'achat d'électricité »"])

mission("GEM-11", "demand-baseline-loads",
        ["WS-10 Q1", "WS-10 Q2", "WS-10 Q3", "WS-10 Q4", "WS-10 Q5", "WS-14 Q1", "WS-14 Q2", "WS-14 Q3", "WS-14 Q4", "WS-08 Q4"],
        geo="National, regional and city levels for demand; INDUSTRIAL_SITE / PORT for large non-mining loads.",
        temporal="Served demand 2016–2026; existing forecasts (vintage stated) for 2027–2035 recorded as third-party projections.",
        strategy=["Utility/system-operator sales, peak and load-profile data.",
                  "National statistics (census, urbanisation, household surveys).",
                  "Official and WAPP master plans and their forecast chapters.",
                  "Enterprise surveys and telecom-regulator data for captive/backup use.",
                  "Investment-agency documents for industrial zones."],
        boundaries=("IN: served/suppressed/captive demand, load profiles, drivers, existing forecasts, non-mining industrial, port, telecom and commercial loads.",
                    "OUT: producing a new forecast (Gate 6 scenario model); mining loads (GEM-03)."),
        quant=[("Consumption", "GWh by class/region, billed vs metered, year"),
               ("Peak demand", "MW, served vs unconstrained, year, date/time if available"),
               ("Load profiles", "hourly/daily/seasonal shape, period, source"),
               ("Forecasts", "values with vintage, base year, method, scenario name — recorded as PROJECTION"),
               ("Large loads", "MW/GWh per site, contracted vs actual, year")],
        terms=[("Served vs suppressed vs unconstrained demand", "Methodology §5."),
               ("Forecast vs scenario vs target", "Protocol §6.2."),
               ("Captive vs backup", "Primary own supply vs standby supply.")],
        cross=["Utility sales vs system-operator energy dispatched (losses considered).",
               "Successive master-plan forecasts vs outturn."],
        contradictions=["Billed vs metered", "Forecast vintages", "Peak definitions (hourly vs instantaneous)"],
        traps=["Served peak ≠ demand.",
               "A forecast ≠ a commitment; linear trends must not be adopted (D-031).",
               "Generic growth rates (GL-26) are leads, not evidence.",
               "Backup-generator counts ≠ demand without a stated method.",
               "Announced industrial zones ≠ committed load.",
               "Port expansion plans ≠ current port demand.",
               "A typical day ≠ the full load profile."],
        artifacts=[],
        limitations=["Load data may be unpublished.", "Suppressed demand can only be estimated."],
        followups=["Whether hourly load data can be requested from the system operator."],
        candidates=["National statistics institute (name to verify)", "French search terms: « pointe de charge », « courbe de charge », « ventes d'électricité par catégorie »"])

mission("GEM-12", "simandou-corridor",
        ["WS-12 Q1", "WS-12 Q2", "WS-12 Q3", "WS-12 Q4"],
        geo="Each Simandou component separately: mine sites (MINING_SITE), rail corridor (TRANSMISSION_CORRIDOR/LOCALITY as applicable), port (PORT); affected regions (REGIONAL) for effects.",
        temporal="Current lifecycle stage and progress condition per component (as-of date); history 2016–2026; projected demand 2027–2035 recorded as projections.",
        strategy=["Official agreements and conventions (as published).",
                  "ESIAs and permits for each component.",
                  "Statutory filings of owners/sponsors.",
                  "DFI/ECA documents if any financing is disclosed.",
                  "Investor presentations (Tier 5, own facts) and press (never alone)."],
        boundaries=("IN: components, ownership, lifecycle stage per component, power demand and supply arrangements, grid/community commitments, infrastructure-sharing, effects on transmission and supply chains.",
                    "OUT: iron-ore market analysis; company valuation."),
        quant=[("Component power demand", "peak MW / annual GWh per component, design vs operating, year"),
               ("Supply arrangements", "captive/grid/hybrid capacity MW (AC/DC), technology, fuel, component"),
               ("Production", "actual vs projected output (t), component, year — projections labelled")],
        terms=[("Component-level status", "Each mine, rail and port component has its own lifecycle stage and progress condition."),
               ("Commitment vs intention", "Binding obligation vs stated aim.")],
        cross=["Agreements vs company filings on ownership and scope.",
               "ESIA demand vs company-reported supply plans."],
        contradictions=["Component vs project-level status", "Design vs operating demand"],
        traps=["Announced Simandou infrastructure ≠ committed infrastructure.",
               "Infrastructure completion ≠ operational status.",
               "Projected mine production ≠ actual production.",
               "Project financing ≠ commercial operation.",
               "One component's status ≠ another component's status.",
               "Corridor length, ownership splits and operator names in the Gate 1 challenge (GL-07) are leads.",
               "Statements of intent on community power ≠ binding commitments."],
        artifacts=[],
        limitations=["Commercial confidentiality; evolving project status."],
        followups=["Whether ESIA documents per component are accessible."],
        candidates=["Simandou (sponsor-named); « Compagnie du Transguinéen » (GL-07 — unverified)"])

mission("GEM-13", "resource-assessment",
        ["WS-18 Q1", "WS-18 Q2", "WS-18 Q3", "WS-18 Q4", "WS-19 Q1", "WS-19 Q2", "WS-19 Q3", "WS-19 Q4",
         "WS-20 Q1", "WS-20 Q2", "WS-20 Q3", "WS-20 Q4", "WS-21 Q1", "WS-21 Q2", "WS-21 Q3", "WS-21 Q4", "WS-17 Q4"],
        geo="National and regional resource distribution; candidate sites (PLANT_SITE) and nodes (SUBSTATION_NODE) where evidenced; basins (RIVER_BASIN) for hydro.",
        temporal="Long-term resource records (period stated); existing/planned projects by lifecycle stage; climate effects 2030–2035.",
        strategy=["Ground measurement records and meteorological-service data.",
                  "Official/DFI resource assessments and hydro master plans.",
                  "Global datasets (Global Solar Atlas, Global Wind Atlas, ERA5/ERA5-Land, CAMS) with version and licence.",
                  "Grid studies for system needs relevant to storage.",
                  "Peer-reviewed studies (method stated)."],
        boundaries=("IN: solar, wind, hydro-site and storage evidence on an equal footing; climate effects on resources; site-constraint data sources (cross-reference GEM-15).",
                    "OUT: ranking technologies; LCOE comparisons; GIS processing (Gate 6)."),
        quant=[("Solar resource", "GHI/GTI (kWh/m²/day or /year), period, dataset/version or station"),
               ("Wind resource", "mean speed (m/s) and/or power density at stated height, period, dataset/version or mast"),
               ("Hydro candidates", "installed MW, seasonal dependable MW, firm energy GWh, study level and date"),
               ("Storage projects/needs", "MW and MWh separately, use case, stage"),
               ("Technical potential", "MW or GWh with potential type (theoretical/technical/economic) and constraint set")],
        terms=[("Theoretical vs technical vs economic potential", "Resource only vs after technical constraints vs after cost criteria."),
               ("Seasonal dependable output", "Methodology §5; mandatory for hydro."),
               ("MW vs MWh (storage)", "Power vs energy capacity, always both.")],
        cross=["Satellite/reanalysis vs ground measurements where available.",
               "Feasibility-study output vs master-plan figures for the same site."],
        contradictions=["Dataset versions", "Measurement heights", "Different potential definitions"],
        traps=["Theoretical resource ≠ technical potential.",
               "Technical potential ≠ economically developable potential.",
               "Resource quality ≠ project viability.",
               "Installed potential ≠ dependable output.",
               "Proximity to the grid ≠ available grid capacity.",
               "Wind must not be pre-judged unattractive (D-026; GL-27 is a lead).",
               "No universal exclusion threshold (slope or other) may be applied (D-038).",
               "Storage MW without MWh is incomplete.",
               "No technology may be ranked or promoted (D-027)."],
        artifacts=[("Dataset reference sheet", "Markdown table: dataset name, custodian, version, resolution, period, licence/redistribution terms, URL; no data downloaded or copied")],
        limitations=["Ground measurements may be scarce.", "Global datasets have resolution and validation limits."],
        followups=["Whether measurement campaigns exist that justify data requests."],
        candidates=["Global Solar Atlas; Global Wind Atlas; ERA5/ERA5-Land; Copernicus CAMS; NASA POWER; IRENA resource publications"])

mission("GEM-14", "project-pipeline",
        ["WS-23 Q1", "WS-23 Q2", "WS-23 Q3", "WS-23 Q4", "WS-05 Q1", "WS-05 Q3"],
        geo="Project and site level (PLANT_SITE, TRANSMISSION_CORRIDOR, SUBSTATION_NODE); aggregates only from project records.",
        temporal="Operational fleet as of search date; pipeline stages and conditions as of search date with last-evidence dates; history of delays/cancellations 2016–2026; target CODs 2027–2035 recorded as targets.",
        strategy=["Official project lists and master plans (each dated).",
                  "DFI project databases and procurement records.",
                  "Utility/system-operator reports for operational plants and generation.",
                  "Company filings (corroborated for later stages).",
                  "Wave 1–2 mission outputs as context only (leads, not evidence)."],
        boundaries=("IN: all generation, storage and transmission projects (operational to proposed, plus delayed/stalled/cancelled), de-duplication, sponsors/EPCs/OEMs/financiers/offtakers.",
                    "OUT: project economics; recommending projects."),
        quant=[("Project capacity", "MW (AC/DC for PV), MWh for storage, installed vs other bases, as-of date"),
               ("Generation (operational plants)", "GWh gross/net, plant, year"),
               ("Dates", "target COD vs actual COD with sources")],
        terms=[("Lifecycle stage / progress condition", "Methodology §6; two dimensions recorded separately."),
               ("De-duplication", "Same location, capacity and sponsor ⇒ same project; name history kept.")],
        cross=["Official lists vs DFI databases vs company filings for stage evidence.",
               "Successive lists for renamed/re-announced projects."],
        contradictions=["Stage disagreements between sources", "Capacity changes across announcements"],
        traps=["Silence ≠ stalled, delayed or cancelled; record UNVERIFIED and a gap.",
               "An MoU, LOI or framework agreement ≠ above Announced.",
               "DFI board approval ≠ financially committed without signed financing.",
               "Sponsor progress claims need corroboration for Financially committed or later.",
               "A renamed project ≠ a new project.",
               "Physical completion of a line ≠ energised or commercially active.",
               "A target COD ≠ a scheduled or achieved COD.",
               "Pipeline totals must not mix stages or capacity bases."],
        artifacts=[("Project candidate list", "Markdown table: project name(s), technology, location as stated, capacity as stated, proposed stage/condition, evidence source IDs; each row sourced or marked NO SOURCE — LEAD ONLY")],
        limitations=["Status evidence may lag; last-evidence dates are essential."],
        followups=["Which projects need targeted status verification."],
        candidates=[])

mission("GEM-15", "land-environment-social",
        ["WS-26 Q1", "WS-26 Q2", "WS-26 Q3", "WS-26 Q4", "WS-26 Q5", "WS-26 Q6"],
        geo="National legal framework (NATIONAL_AGGREGATE); protected areas, hazards and precedents at LOCALITY/REGIONAL level.",
        temporal="Instruments in force as of search date; precedents and conflicts 2016–2026; climate hazard projections to 2035 (scenario stated).",
        strategy=["Land, environmental and ESIA legal texts in the official gazette.",
                  "Environmental authority publications and ESIA registries.",
                  "Project RAPs and DFI safeguard documents.",
                  "Official protected-area gazettes; WDPA/IUCN/KBA datasets (licence terms noted).",
                  "Judicial/official records and DFI accountability-mechanism cases for conflicts."],
        boundaries=("IN: tenure, expropriation, compensation, resettlement, ESIA process, protected areas and habitats, physical climate hazards, documented community conflict, constraint-data sources.",
                    "OUT: setting numeric exclusion thresholds; site suitability assessment (Gate 6/7)."),
        quant=[("Protected-area extents", "area (km²/ha), legal status, instrument/date, dataset/version"),
               ("ESIA timelines", "statutory vs observed durations (days/months), instrument or project example"),
               ("Compensation rates", "value, currency, nominal, date, project/instrument (never generalised)")],
        terms=[("Legal exclusion vs regulatory constraint vs risk flag", "research_architecture §L.2 classes."),
               ("Statutory vs customary tenure", "State-recognised title vs community-recognised rights."),
               ("Hazard vs exposure vs risk", "Physical event vs assets in harm's way vs combined likelihood/impact.")],
        cross=["Gazette protected-area status vs global datasets.",
               "RAP compensation vs legal framework."],
        contradictions=["Dataset vs legal boundaries", "Statutory vs observed timelines"],
        traps=["A conservation dataset designation ≠ a legal exclusion.",
               "One project's compensation rates ≠ a national standard.",
               "Statutory ESIA timelines ≠ actual timelines.",
               "Global coarse hazard data ≠ site-level hazard.",
               "No universal buffer or threshold may be set (D-038).",
               "Species, sites and regions named in the Gate 1 challenge (GL-28) are leads.",
               "A grievance ≠ a conflict causally linked to a project without evidence."],
        artifacts=[("Legal instrument index", "Markdown table: instrument title (original language), number, date, article(s), URL/reference, in-force status; no full-text copies"),
                   ("Dataset reference sheet", "Markdown table: dataset name, custodian, version, licence/redistribution terms, URL; no data downloaded or copied")],
        limitations=["Customary tenure is poorly documented in formal sources.", "Some global biodiversity datasets restrict redistribution."],
        followups=["Whether professional legal review is needed (verify with a qualified professional before acting)."],
        candidates=["Land code (« Code foncier et domanial » per GL leads — title/currency to verify)", "Environmental assessment authority (GL-16 suggests « BGACE » — unverified)",
                    "WDPA/Protected Planet; IUCN Red List; Key Biodiversity Areas; IBAT (licence terms apply)"])

TITLES = {}
BRIEF_WS = {}

# ---------------------------------------------------------------------------
# Common text blocks
# ---------------------------------------------------------------------------
HIERARCHY = """Authoritative six-tier hierarchy (D-082; methodology §1):

| Tier | Class | Use |
|---|---|---|
| 1 | Guinea government / primary institutional: laws, decrees, official gazette, ministry, regulator, utility and system-operator publications | May stand alone |
| 2 | WAPP / ECOWAS / regional institutional: WAPP Secretariat/ICC, ECOWAS and regional regulator, interconnector operators, river-basin organisations | May stand alone |
| 3 | World Bank / IFC / AfDB / EIB / IMF / UN / other DFIs: appraisal, status and completion documents, databases | May stand alone |
| 4 | Data institutions, science and engineering: IRENA, IEA, Global Energy Monitor, Ember, NREL, Global Solar Atlas, Global Wind Atlas, NASA, NOAA, Copernicus, scientific literature, engineering studies | May stand alone with a definition check (single source is indicative) |
| 5 | Corporate and project disclosures: OEM/EPC/IPP/mining-company disclosures, investor presentations, project-finance disclosures, tenders, corporate statutory filings | Only for the issuer's own disclosed facts (ownership, production, capacity, financials, project commitments, contracts, project status); never for unrelated government, grid, regulatory or national-system facts |
| 6 | AI-generated or otherwise unsourced material: Gemini or any AI output, unsourced web content, aggregators, blogs, social media | **LEAD ONLY — never evidence** |

Tier 6 is never part of the evidence hierarchy.

**Media and trade press** are secondary reporting and discovery sources, **not an evidence tier**. Use them to identify leads, trace the underlying primary source, provide context, or corroborate chronology or public reporting. They must not independently establish a material quantitative or legal claim where a suitable primary or authoritative source is reasonably available. Repeated reports that derive from the same underlying source are **one** source."""

SOURCE_RULES = """1. Search **primary sources first** (Tier 1, then Tier 2, then Tier 3).
2. **Trace** every secondary source back to its underlying primary source whenever possible; cite the primary source if found, and record the secondary as the pointer.
3. **Record source metadata** for every source in the Source Roster (contract section 6).
4. **Distinguish source discovery from evidence extraction**: mark each quantitative row `VALUE_READ_IN_SOURCE` (you located the value in the document, with page/table/section) or `SOURCE_IDENTIFIED_NOT_READ` (you know of the source but did not read the value in it).
5. **Never treat your own synthesis as evidence.** Inferences must be labelled "Inference" and carry no claim of fact.
6. **Never treat another AI output** (including earlier Gemini outputs and the Gate 1 architecture challenge) as an independent corroborating source.
7. **Never upgrade confidence** because several sources repeat the same underlying source (same press release, wire story, dataset or primary document).
8. Prefer **French-language official sources** where they are the original; record the original-language title.
9. Never fabricate citations. If you cannot cite a source, write **NO SOURCE — LEAD ONLY**."""

TEMPORAL = """Classify every claim with one temporal class (protocol §6.2):

| Class | Meaning | Horizon |
|---|---|---|
| HISTORICAL | Observed outturn for a past period | 2016–2026 |
| CURRENT_STATUS | State as of a stated date | as-of date |
| COMMITTED_UNDER_CONSTRUCTION | Financially committed / under construction | 2027–2030 near-term |
| PLANNED | Active development / announced / proposed | 2027–2030 and 2030–2035 |
| TARGET_ASPIRATION | Policy target or corporate ambition | 2030–2035 strategic |
| PROJECTION | Forecast, scenario or estimate by a third party (method stated) | 2027–2035 |

Rules: a **target is never a plan**; a **plan is never a commitment**; a **forecast/scenario/estimate is never a fact**; **silence never means delay, stalling or cancellation**. Record four dates separately where applicable: period described, source publication date, access date, status as-of date."""

GEO = """Use the most specific defensible geographic level, coded from: NATIONAL_AGGREGATE · REGIONAL · PREFECTURE · LOCALITY · CITY · MINING_SITE · INDUSTRIAL_SITE · PORT · PLANT_SITE · TRANSMISSION_CORRIDOR · SUBSTATION_NODE · INTERCONNECTION · RIVER_BASIN · NEIGHBOURING_COUNTRY · MULTI_COUNTRY_REGION · OTHER. Never present a national figure as a site figure, or sum values from different levels. Neighbouring-country information is in scope **only** if it is a benchmark metric (B1–B13) or materially affects Guinea's energy system, market, infrastructure, supply, demand or investment environment; state which test applies. Do not produce a generic West Africa study."""

STATUS = """For any project, plant, line, site or programme, report **lifecycle stage** (Proposed · Announced · Active development · Financially committed · Under construction · Operational · Cancelled) and **progress condition** (On track · Delayed · Stalled · Unverified) separately, each with the specific evidence and its date. MoUs/LOIs/framework agreements never exceed Announced. DFI board approval alone is not Financially committed. Stalled requires positive evidence; lack of recent news = Unverified."""

CONTRACT = """Return **all 17 sections**, in this order. A prose-only report is **NON-CONFORMING**; a non-conforming output remains a research lead and cannot enter authoritative evidence.

1. **Mission metadata** — mission ID, package version, execution date, model/tool context (if known), workstreams covered.
2. **Executive findings** — a short list; each finding carries claim IDs; no unsourced statements.
3. **Research questions addressed** — every question ID with status ANSWERED / PARTLY_ANSWERED / NOT_ANSWERED.
4. **Findings by question** — per question ID: findings with claim IDs and source IDs; what remains unknown.
5. **Quantitative evidence table** — one row per value, with columns: `claim_id | question_id | metric | definition | value (or low–high) | unit | currency | nominal/real (base year) | AC/DC basis | capacity/energy basis | geography name | geo_level | period | temporal class | source_id | page/table/section | evidence_role (VALUE_READ_IN_SOURCE / SOURCE_IDENTIFIED_NOT_READ) | self-assessed confidence + reason`. Use "n/a" only where a field genuinely does not apply.
6. **Source roster** — `source_id (GEM-NN-S##) | exact title (original language) | publisher | document type | publication date | URL or persistent reference | language | access date | proposed tier (1–6) | access limitation (open/registration/paywalled/unavailable/restricted)`.
7. **Primary-source verification** — per material claim: was the primary source consulted (Y/N); if not, why, and which secondary source was used.
8. **Cross-source corroboration** — per material value: independent sources found; agree / disagree; whether sources share an origin.
9. **Contradictions** — conflicting values side by side with sources and candidate causes; **do not resolve**.
10. **Data gaps** — questions/values with no source found; sources tried (search path).
11. **Unverified leads** — claims marked NO SOURCE — LEAD ONLY.
12. **Important definitions** — definitions used by each source for key metrics, especially where they differ from the package definitions.
13. **Geographic coverage** — levels and areas covered and not covered.
14. **Historical/current/future classification** — temporal class per claim.
15. **Confidence assessment** — self-assessment per finding with reasons (advisory only; the project assigns confidence).
16. **Research limitations** — access, language, coverage, time.
17. **Recommended follow-up questions** — unresolved questions that may justify a targeted mission.

**Claim IDs:** every material claim carries `GEM-NN-C###` (NN = this mission's number; ### sequential from 001) **and** either a source reference (`GEM-NN-S##`) **or** the words **NO SOURCE — LEAD ONLY**. Tables must appear inside the findings document."""

STOPPING = """The mission is sufficiently researched only when **all** hold (protocol §16); "all questions answered" alone is not sufficient:

1. Every CRITICAL question is answered or documented as a data gap after the search path.
2. Every HIGH question is addressed (answered, partly answered with gap logged, or logged as gap).
3. Every material quantitative value has a source with page/table/section.
4. Primary sources have been sought for every material claim (record the search).
5. Major contradictions are reported with candidate causes.
6. Important data gaps are documented with sources tried.
7. The geographic levels required by the questions are covered or logged as gaps.
8. The relevant horizons (2016–2026; 2027–2030; 2030–2035) are covered or logged as gaps.
9. Material findings rest on Tier 1–4 sources, or their weaker basis is stated.
10. Diminishing returns are assessed and stated with reasoning.

MEDIUM and LOW questions may remain open only if explicitly listed in section 10 (Data gaps)."""

SEARCH_PATH = "cited URL/reference → publisher's site or repository → official gazette/archive → DFI and international document portals → web archives → search by title or document number → French-language search"

HANDOFF = """After execution (operator and Claude Code; protocol §13–§15):

1. The operator deposits the raw Gemini output **unchanged** in `01_gemini_research/{folder}/` as `YYYY-MM-DD_{mid}_{slug}_gemini_v<N>.md` (and any permitted supporting artifact as `…_gemini_v<N>_<artifact>.md`). A re-run is a new version; earlier versions are kept.
2. Claude Code computes the SHA-256 fingerprint of each artifact.
3. Claude Code creates the `.meta.md` sidecar with the execution metadata (section 25).
4. Claude Code checks conformance with the 17-section contract; non-conforming output is kept unchanged and remains a lead.
5. Leads are entered in the lead register (`LEAD-`, RAW_LEAD) and sources in the source register (`SRC-`, CANDIDATE_SOURCE).
6. Claude Code independently retrieves sources and verifies claims (a citation alone never verifies).
7. Contradictions and data gaps are registered (`CON-`, `GAP-`).
8. Register records are created with `acceptance_status = PROPOSED` only, and only after the register validator passes (D-075).
9. Claude Code prepares the Mission Reconciliation Report (`{mid}_close_report.md`).
10. The ChatGPT reviewer / project owner challenges the result (recorded verbatim as independent review inputs).
11. Acceptance occurs only through the approved gate process (discovery acceptance at Gate 2D; evidence acceptance at Gates 3–4).

**The raw Gemini artifact is never edited.**"""

METADATA = """Record for every execution (in the `.meta.md` sidecar; operator supplies items marked †):

| Field | Value |
|---|---|
| Mission ID | {mid} |
| Mission / package version | {mid}-{ver} |
| Execution date and time † | |
| Gemini model / tool context † (or "not available") | |
| Operator † (role or initials; no personal data) | |
| Prompt/package file and its SHA-256 | `{pkgfile}` (SHA-256 in PACKAGE_INDEX.md) |
| Raw artifact filename(s) | |
| Raw artifact SHA-256 (after capture) | |
| Source access dates | as recorded in the Source Roster |
| Repository commit / gate at execution | |
| Review / acceptance status | NOT REVIEWED → reconciliation → challenge → decision ID |"""

COMMON_TRAPS = [
    "Any statement in the Gate 1 architecture challenge or an earlier Gemini output is a hypothesis, not a fact.",
    "Candidate institution or document names listed in this package are unverified search terms, not confirmed facts.",
    "A citation you have not read ≠ a verified source (mark SOURCE_IDENTIFIED_NOT_READ).",
    "Several articles repeating one press release = one source.",
]


def parse_charters(root):
    ch = open(os.path.join(root, "00_project/workstream_charters.md"), encoding="utf-8").read()
    parts = re.split(r"\n## (WS-\d\d) — (.+)\n", ch)[1:]
    qs, ws_titles = {}, {}
    for i in range(0, len(parts), 3):
        w, title, body = parts[i], parts[i + 1].strip(), parts[i + 2]
        ws_titles[w] = title
        q = body.split("**Principal questions:**")[1].split("**Required datasets:**")[0]
        for n, (pri, text) in enumerate(re.findall(r"^\s+\d+\. \*\*\[(\w+)\]\*\* (.*)$", q, re.M), 1):
            qs[f"{w} Q{n}"] = (pri, text.strip())
    return qs, ws_titles


def parse_briefs(root):
    mb = open(os.path.join(root, "00_project/gemini_mission_briefs.md"), encoding="utf-8").read()
    rows = re.findall(r"^\| (GEM-\d\d) \| ([^|]+) \| ([^|]+) \| ([^|]+) \| ([^|]+) \| (\d) \| `([^`]+)` \|$", mb, re.M)
    out = {}
    for mid, title, area, prim, sec, wave, folder in rows:
        obj = re.search(rf"### {mid} — .*?\n.*?\*\*Objective:\*\* (.*?)\n", mb, re.S).group(1).strip()
        out[mid] = dict(title=title.strip(), area=area.strip(), primary=prim.strip(), secondary=sec.strip(),
                        wave=wave, folder=folder.strip().rstrip("/").split("/")[-1], objective=obj)
    return out


def render(m, b, qs, ws_titles):
    mid, n = m["id"], m["id"][4:]
    pkgfile = f"{OUT_DIR}/{mid}_{m['slug']}_package_{PKG_VERSION}.md"
    L = []
    A = L.append
    A(f"# Mission Package {mid}-{PKG_VERSION} — {b['title']}")
    A("")
    A(f"**Package version:** {PKG_VERSION} (DRAFT, pending Gate 2C approval) · **Prepared:** {PKG_DATE} · **Gate:** 2C · **Generated by:** `00_project/tools/build_mission_packages.py`")
    A("")
    A("> **Status: NOT AUTHORISED FOR EXECUTION.** Execution requires separate Gate 2D authorisation and an approved, passing register validator (D-075). Once approved this package is immutable; changes create a new version.")
    A(">")
    A("> **Operator instructions:** submit everything between `PROMPT START` and `PROMPT END` to Gemini verbatim. Sections 24–25 (after `PROMPT END`) are operator/Claude instructions and are not sent.")
    A("")
    A("---")
    A("")
    A("<!-- PROMPT START -->")
    A("")
    A("**Role and non-negotiable rules for Gemini.** You are an independent discovery researcher for the Guinea Energy Intelligence 2026 project. Your output is treated as an **unverified research lead (Tier 6)**; every claim will be independently verified. Do not fabricate citations. Do not make recommendations, rank technologies, or assess any company's fit, including Alendei. Remain strictly technology-neutral. Do not characterise any entity (e.g. \"distressed\", \"creditworthy\") without citing the indicators that support it. Treat earlier Gemini outputs, including the Gate 1 architecture challenge, as hypotheses. Do not research beyond this mission's boundaries.")
    A("")
    A("## 1. Mission ID")
    A("")
    A(f"{mid} (package {mid}-{PKG_VERSION}; deposit folder `01_gemini_research/{b['folder']}/`; wave {b['wave']})")
    A("")
    A("## 2. Mission title")
    A("")
    A(b["title"])
    A("")
    A("## 3. Purpose")
    A("")
    A(f"{b['objective']} Coverage area: {b['area']}.")
    A("")
    A("## 4. Workstreams covered")
    A("")
    A(f"- **Primary:** {b['primary']}")
    A(f"- **Secondary:** {b['secondary']}")
    qws = {q[:5] for q in m["questions"]}
    allws = sorted(qws | set(re.findall(r"WS-\d\d", b["primary"] + " " + b["secondary"])))
    for w in allws:
        role = "questions in this package" if w in qws else "context only (no questions assigned in the Gate 1 brief; report relevant findings encountered within the boundaries)"
        A(f"- {w} — {ws_titles[w]} — {role}")
    A("")
    A("## 5. Research questions")
    A("")
    A("Question text is reproduced exactly from the approved workstream charters.")
    if m.get("completion"):
        A("")
        A("*Coverage completion (D-079, pending approval):* " + ", ".join(m["completion"]) + " are charter questions of workstreams for which this mission is primary (D-051) and were not referenced by any Gate 1 brief; they are included so that every Phase A question is covered. The Gate 1 brief is not changed.")
    A("")
    for i, ref in enumerate(m["questions"], 1):
        pri, text = qs[ref]
        a = Q[ref]
        A(f"### {mid}-Q{i:02d} — [{pri}] {ref}")
        A("")
        A(f"**Question:** {text}")
        A("")
        A(f"- **Priority:** {pri}")
        A(f"- **Required evidence type:** {a['e']}")
        A(f"- **Expected geography:** {a['g']}")
        A(f"- **Expected period:** " + "; ".join(PERIOD_LABEL[p.strip()] for p in a['p'].split(';')))
        A(f"- **Quantitative / qualitative:** {a['k']}")
        A(f"- **Primary-source target:** {a['s']}")
        A(f"- **Acceptable secondary fallback:** {a['f']}")
        A(f"- **Critical definitions:** {a['d']}")
        A(f"- **Known analytical risk:** {a['r']}")
        A("")
    A("## 6. Question priority")
    A("")
    A("Planning priority only (methodology §12): it guides effort, is not evidence confidence and is not a finding.")
    A("")
    A("| Question ID | Charter ref | Priority |")
    A("|---|---|---|")
    for i, ref in enumerate(m["questions"], 1):
        A(f"| {mid}-Q{i:02d} | {ref} | {qs[ref][0]} |")
    A("")
    A("## 7. Geographic scope")
    A("")
    A(m["geo"])
    A("")
    A(GEO)
    A("")
    A("## 8. Historical / current / future scope")
    A("")
    A(m["temporal"])
    A("")
    A(TEMPORAL)
    A("")
    A(STATUS)
    A("")
    A("## 9. Required source hierarchy")
    A("")
    A(HIERARCHY)
    A("")
    A("**Mandatory source rules:**")
    A("")
    A(SOURCE_RULES)
    A("")
    A("## 10. Primary-source search strategy")
    A("")
    A("Search in this order:")
    A("")
    for i, s in enumerate(m["strategy"], 1):
        A(f"{i}. {s}")
    A("")
    if m["candidates"]:
        A("**Candidate search terms — UNVERIFIED LEADS**")
        A("")
        A("The names below are search aids only (D-081). Every term is UNVERIFIED and must not be treated as a verified Guinea fact. Do **not** infer an institution's jurisdiction, mandate, operating status, project involvement or legal authority from a search term alone. Establish existence, current name, mandate and content from primary sources, and do not assume any document exists or contains a particular fact.")
        A("")
        for c in m["candidates"]:
            A(f"- {c} — UNVERIFIED")
        A("")
    A("## 11. Secondary-source treatment")
    A("")
    A("Secondary sources (Tier 4–5) may support a value only when the primary source has been sought (search recorded), the value is reported at the confidence it merits, its definition, period and geography are explicit, and its limitation is stated. Tier 5 corporate and project disclosures, including statutory filings, are authoritative only for the issuer's own disclosed facts, never for unrelated government, grid, regulatory or national-system facts. Media and trade press are discovery and context sources and never establish a material claim on their own. Tier 6 is never evidence. The question-level fallbacks in section 5 are the only acceptable fallbacks for this mission.")
    A("")
    A("## 12. Search boundaries")
    A("")
    A(f"- {m['boundaries'][0]}")
    A(f"- {m['boundaries'][1]}")
    A("- Do not browse for or report information outside these boundaries, even if encountered.")
    A("")
    A("## 13. Required quantitative evidence")
    A("")
    A("Usable quantitative evidence is a value **read in a source**, with all applicable metadata: value · unit · currency · nominal/real (base year) · year/date · geography (name + geo_level) · definition · AC/DC basis · installed/available/dependable/dispatched/delivered/consumed basis · source ID · page/table/section · evidence role · self-assessed confidence. Do not report bare \"statistics\". Values sought in this mission:")
    A("")
    A("| Value type | Required metadata (in addition to the general fields) |")
    A("|---|---|")
    for vt, md in m["quant"]:
        A(f"| {vt} | {md} |")
    A("")
    A("Unit rules: MWp is DC (record as MW-DC with original label); AC/DC unstated → state \"basis unstated\"; MWh/GWh/TWh are exact conversions; tariffs are never costs; currency values in original currency with year (conversions only if the source converts, stating the rate); ranges reported as low–high with the source's range definition; percentages with numerator and denominator.")
    A("")
    A("## 14. Required terminology / definitions")
    A("")
    A("| Term | Definition for this mission |")
    A("|---|---|")
    for t, d in m["terms"]:
        A(f"| {t} | {d} |")
    A("")
    A("Core distinctions apply throughout: installed / available / dependable / dispatched capacity; generated / delivered / consumed energy; peak / average / suppressed demand (methodology §5).")
    A("")
    A("## 15. Required cross-checks")
    A("")
    for c in m["cross"]:
        A(f"- {c}")
    A("- Sources that share an origin are **not** independent; report the shared origin.")
    A("")
    A("## 16. Contradiction handling")
    A("")
    A("Report conflicting values side by side with their sources (contract section 9). **Do not resolve, average or choose between them.** For each, note candidate causes from: definition · period · geography · scope · unit · AC/DC basis · capacity/energy basis · methodology · source precision · superseded edition · duplication. No numerical tolerance applies (D-072). Contradiction patterns likely in this mission: " + "; ".join(m["contradictions"]) + ".")
    A("")
    A("## 17. Data-gap handling")
    A("")
    A(f"When no adequate source is found, record the question ID, what is missing and the sources tried along the search path ({SEARCH_PATH}), plus any access limitation (paywalled, unavailable, restricted). Never fill a gap with an estimate, an analogy from another country or a weaker source presented as primary.")
    A("")
    A("## 18. HYPOTHESIS TRAPS / PROHIBITED ASSUMPTIONS")
    A("")
    A("These are methodological traps, not factual claims. Do not convert any of the following plausible assumptions into findings:")
    A("")
    for t in m["traps"]:
        A(f"- {t}")
    for t in COMMON_TRAPS:
        A(f"- {t}")
    A("")
    A("## 19. Required Gemini output structure")
    A("")
    A(CONTRACT.replace("GEM-NN", mid))
    A("")
    A("## 20. Supporting-artifact rules")
    A("")
    A("Only the artifacts listed here are permitted; no other files (no PDFs, spreadsheets, images, data downloads or copies of third-party documents).")
    A("")
    arts = [("Overflow evidence table", "Markdown continuation of contract section 5 if the table exceeds output limits; same columns")] + m["artifacts"]
    A("| Artifact | Type | Purpose | Provenance | Copyright / access | Immutable raw capture |")
    A("|---|---|---|---|---|---|")
    for name, purpose in arts:
        A(f"| {name} | Markdown (.md) | {purpose} | Produced by Gemini in the same execution; listed in contract section 1 | Short factual extracts and references only; no reproduction of third-party text; access limitations stated | Yes — deposited unchanged with SHA-256 |")
    A("")
    A("## 21. Mission stopping criteria")
    A("")
    A(STOPPING)
    A("")
    crit = [f"{mid}-Q{i:02d}" for i, r in enumerate(m["questions"], 1) if qs[r][0] == "CRITICAL"]
    high = [f"{mid}-Q{i:02d}" for i, r in enumerate(m["questions"], 1) if qs[r][0] == "HIGH"]
    A(f"**Mission-specific:** CRITICAL questions — {', '.join(crit) if crit else 'none'}; HIGH questions — {', '.join(high) if high else 'none'}. Every value type in section 13 must be either sourced or logged as a gap.")
    A("")
    A("## 22. Research limitations")
    A("")
    A("Report the limitations you encountered (contract section 16). Limitations anticipated for this mission:")
    A("")
    for x in m["limitations"]:
        A(f"- {x}")
    A("")
    A("## 23. Follow-up questions")
    A("")
    A("Report unresolved questions in contract section 17. Consider in particular:")
    A("")
    for x in m["followups"]:
        A(f"- {x}")
    A("")
    A("<!-- PROMPT END -->")
    A("")
    A("---")
    A("")
    A("## 24. Gemini → Claude handoff requirements")
    A("")
    A(HANDOFF.format(folder=b["folder"], mid=mid, slug=m["slug"]))
    A("")
    A("## 25. Execution metadata requirements")
    A("")
    A(METADATA.format(mid=mid, ver=PKG_VERSION, pkgfile=pkgfile))
    A("")
    return pkgfile, "\n".join(L).rstrip("\n") + "\n"


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    qs, ws_titles = parse_charters(root)
    briefs = parse_briefs(root)
    assert sorted(M) == sorted(briefs) == [f"GEM-{i:02d}" for i in range(1, 16)], "mission set mismatch"
    for m in M.values():
        for ref in m["questions"]:
            assert ref in qs and ref in Q, f"unknown question {ref}"
    os.makedirs(os.path.join(root, OUT_DIR), exist_ok=True)
    index = []
    for mid in sorted(M):
        path, text = render(M[mid], briefs[mid], qs, ws_titles)
        with open(os.path.join(root, path), "w", encoding="utf-8") as fh:
            fh.write(text)
        index.append((mid, briefs[mid]["title"], os.path.basename(path), len(M[mid]["questions"]),
                      hashlib.sha256(text.encode("utf-8")).hexdigest()))
        print("wrote", path)
    L = ["# Mission Package Index", "",
         f"**Package set:** {PKG_VERSION} (DRAFT, pending Gate 2C approval) · **Prepared:** {PKG_DATE} · **Generated by:** `00_project/tools/build_mission_packages.py`", "",
         "Executable mission packages for GEM-01 – GEM-15. **Not authorised for execution** until Gate 2D (and the D-075 register validator). After approval each package is immutable; integrity is checked against the SHA-256 below. Changes require a new version and a decision-log entry.", "",
         "| Mission | Title | Package file | Questions | SHA-256 |", "|---|---|---|---|---|"]
    for mid, title, fn, nq, h in index:
        L.append(f"| {mid} | {title} | `{fn}` | {nq} | `{h}` |")
    with open(os.path.join(root, OUT_DIR, "PACKAGE_INDEX.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(L) + "\n")
    print("wrote", f"{OUT_DIR}/PACKAGE_INDEX.md")


if __name__ == "__main__":
    main()
