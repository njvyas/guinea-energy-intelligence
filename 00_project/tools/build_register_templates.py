#!/usr/bin/env python3
"""Build the empty authoritative register templates (Gate 2B).

Single source of the register schema (D-073). Generates:
  * 11 XLSX register templates, one per logical register (Entity/Site has two
    physical sheets; D-076) (header rows, data validation, dictionary,
    controlled vocabularies - NO DATA ROWS), at the paths defined in
    research_architecture.md section G.2;
  * 00_project/register_schema.md (human-readable data dictionary).

Standard library only (zipfile + XML); output is deterministic.
Usage:  python3 -I 00_project/tools/build_register_templates.py <repo_root>
Schema changes require a decision-log entry and a re-run of this script.
"""
import os
import sys
import zipfile
from xml.sax.saxutils import escape

SCHEMA_VERSION = "1.1"
SCHEMA_DATE = "08-Oct-2026"
SCHEMA_DECISION = "D-066"
MAX_ROW = 10000
SEP = "; "

# ---------------------------------------------------------------------------
# Controlled vocabularies: name -> list of (code, definition)
# ---------------------------------------------------------------------------
WS_TITLES = [
    "Macroeconomic, Political Economy & Country Risk Context",
    "Electricity Sector Institutions, Law & Regulation",
    "Fuel Supply, Logistics, Landed Fuel Economics & Thermal/Gas Options",
    "Macro-Financial Framework, Currency, FX Convertibility & Repatriation",
    "Existing Generation Fleet, Operating Performance & Seasonal Dependable Capacity",
    "Transmission Network, Substations, System Stability & Reinforcement Options",
    "Distribution, Access, Losses, Metering & Demand-Side Measures",
    "Reliability, Outages & System Operations",
    "Utility Economics, Tariffs, Counterparty Condition & Bankability",
    "Electricity Demand Baseline, Load Profiles & Forecast Inputs",
    "Bauxite Extraction & Alumina Refining Energy",
    "Iron Ore / Simandou Megaproject & Infrastructure Corridor",
    "Gold, Diamonds & Other Strategically Relevant Minerals",
    "Non-Mining Industrial, Ports & Logistics, and Commercial Demand",
    "Mining Legal Regime, Energy-Related Obligations & Infrastructure Access",
    "WAPP, Regional Market & Cross-Border Interconnection",
    "Transboundary River Basins, Hydrology & Climate Variability",
    "Solar Resource & Technical Potential",
    "Wind Resource & Technical Potential",
    "Hydro Development Potential (New, Rehabilitation, Small Hydro)",
    "BESS, Hybridisation & Grid-Stability Applications",
    "Decentralised Energy, Mini-Grids & Productive Use",
    "Generation & Transmission Project Pipeline",
    "International Finance, DFI & Risk-Mitigation Instruments",
    "International Commercial Ecosystem (by Origin) & OEM/EPC/IPP Register",
    "Land Tenure, Resettlement, Environmental & Biodiversity Constraints",
    "Commercial Opportunity Portfolio & Structuring",
    "Alendei Strategic Participation & Ecosystem Role",
]

V = {
    "v_acceptance_status": [
        ("PROPOSED", "Record proposed for gate acceptance; not usable in analysis or deliverables."),
        ("ACCEPTED", "Explicitly accepted at a gate (decision ID recorded); usable subject to record_status ACTIVE."),
        ("REJECTED", "Explicitly rejected at a gate; retained for audit, never used."),
    ],
    "v_record_status": [
        ("ACTIVE", "Current record."),
        ("SUPERSEDED", "Replaced by the record in superseded_by; retained, never deleted."),
    ],
    "v_actor": [
        ("CLAUDE_CODE", "Claude Code (maintainer)."),
        ("OPERATOR", "Project operator."),
        ("PROJECT_OWNER", "Project owner (User)."),
        ("CHATGPT", "ChatGPT reviewer."),
    ],
    "v_gate": [(g, f"Gate {g[1:]}") for g in ["G2D", "G3", "G4", "G5", "G6", "G7", "G8", "G9", "G10", "G11"]],
    "v_workstream": [(f"WS-{i:02d}", WS_TITLES[i - 1]) for i in range(1, 29)],
    "v_workstream_phase_a": [(f"WS-{i:02d}", WS_TITLES[i - 1]) for i in range(1, 27)],
    "v_evidence_state_register": [
        ("EXTRACTED", "Value read from a retrieved source; not yet VERIFIED/CORROBORATED (confidence INDICATIVE)."),
        ("VERIFIED", "Confirmed in a Tier 1-3 source (D-082) with clear definition, date and geography."),
        ("CORROBORATED", "Two or more independent sources (at least one Tier 1-4) agree - identical, or differing only by demonstrable reporting precision (D-072)."),
        ("ESTIMATE", "Derived by documented method from accepted inputs (confidence ESTIMATED)."),
        ("CONTRADICTED_UNRESOLVED", "Subject to an OPEN or RANGE-CARRIED contradiction."),
    ],
    "v_evidence_state_lead": [("RAW_LEAD", "Unverified claim; lead register only.")],
    "v_evidence_state_gap": [("DATA_GAP", "Sought along the standard search path but not found.")],
    "v_confidence": [
        ("VERIFIED", "Evidence state VERIFIED."),
        ("CORROBORATED", "Evidence state CORROBORATED."),
        ("ESTIMATED", "Evidence state ESTIMATE."),
        ("INDICATIVE", "Evidence state EXTRACTED: single Tier 4-5 source or unclear definition/date."),
        ("DATA GAP", "No adequate source."),
    ],
    "v_quality": [("HIGH", "High."), ("MEDIUM", "Medium."), ("LOW", "Low - may lower confidence by one level."), ("UNKNOWN", "Not assessable.")],
    "v_discloser": [
        ("INDEPENDENT_AUDITED", "E.g. supreme audit institution, DFI completion report, EITI reconciliation."),
        ("OFFICIAL_SELF_REPORTED", "E.g. utility or ministry statistics."),
        ("SELF_REPORTED_PROMOTIONAL", "E.g. press releases, investor presentations, speeches."),
    ],
    "v_cross_check": [
        ("NOT_ATTEMPTED", "No cross-check attempted yet."),
        ("AGREES", "Independent source(s) agree: identical, or differing only by demonstrable reporting precision after the D-072 comparability tests."),
        ("DISAGREES", "Independent source(s) disagree - contradiction logged."),
        ("NO_INDEPENDENT_SOURCE", "No independent source located."),
    ],
    "v_contradiction_status": [
        ("NONE", "No contradiction."),
        ("OPEN", "Contradiction under investigation."),
        ("RESOLVED-DEFINITIONAL", "Values measure different things; both retained."),
        ("RESOLVED-HIERARCHY", "Evidence hierarchy determines governing value."),
        ("RESOLVED-ERROR", "Error identified and corrected."),
        ("RANGE-CARRIED", "Unreconcilable comparable sources; low/high envelope carried."),
    ],
    "v_contradiction_outcome": [
        ("RESOLVED-DEFINITIONAL", "Values measure different things; both retained as separate metrics."),
        ("RESOLVED-HIERARCHY", "Higher tier, then more recent, more specific, better defined governs."),
        ("RESOLVED-ERROR", "Transcription or calculation error identified."),
        ("RANGE-CARRIED", "Low/high envelope carried into analysis with sensitivity flag."),
        ("OPEN", "Investigation incomplete; not usable in deliverable headlines."),
    ],
    "v_cause_code": [
        ("DEFINITION", "Different metrics (e.g. installed vs dependable; MW-AC vs MW-DC)."),
        ("PERIOD", "Different period or season."),
        ("SCOPE_GEOGRAPHY", "Different geographic or asset scope."),
        ("UNIT_CURRENCY", "Different unit, currency or price basis."),
        ("STATUS_INTERPRETATION", "E.g. constructed vs energised; MoU vs commitment."),
        ("DUPLICATION", "Same project under different names."),
        ("TRANSCRIPTION", "Copying or calculation error."),
        ("METHODOLOGY", "Different measurement or estimation methods for the same nominal metric (D-068)."),
        ("SUPERSEDED", "Later edition or revision of the same source or series (D-068)."),
        ("REPORTING_PRECISION", "Difference demonstrably attributable to reporting precision; permitted only when precision_attribution = ATTRIBUTABLE (D-072)."),
        ("GENUINE", "Real disagreement between credible sources."),
    ],
    "v_materiality": [
        ("MATERIAL", "Could change a conclusion, ranking or decision."),
        ("MODERATE", "Affects analysis detail but not conclusions."),
        ("MINOR", "No material effect."),
    ],
    "v_metric_class": [
        ("CAPACITY", "Power capacity."), ("ENERGY", "Energy volumes."), ("DEMAND", "Peak, average, suppressed demand."),
        ("NETWORK", "Line, transformer, transfer metrics."), ("ACCESS", "Electricity access."), ("LOSSES", "Network losses."),
        ("RELIABILITY", "Outage and supply-hour indicators."), ("TARIFF", "Regulated or contracted prices charged."),
        ("COST", "Cost of supply, generation cost, capex, opex."), ("FINANCIAL", "Financial-statement items."),
        ("FUEL", "Fuel volumes and delivered prices."), ("RESOURCE", "Solar/wind resource metrics."),
        ("HYDROLOGY", "Flows, reservoir levels."), ("PRODUCTION", "Mineral or industrial output."),
        ("MACRO", "Macroeconomic and fiscal indicators."), ("FX_RATE", "Exchange rates (D-070)."),
        ("PRICE_INDEX", "Deflators and price indices."), ("LAND_ENVIRONMENT", "Areas, distances, counts for land/environment."),
        ("CONTRACT_TERM", "Quantitative contract terms (tenor, volumes)."),
        ("LEGAL_INSTITUTIONAL", "Atomic legal/institutional facts held as structured categorical values within the D-074 boundary."),
        ("OTHER", "Other - explain in metric_definition."),
    ],
    "v_value_kind": [
        ("NUMERIC", "Numeric value with unit."),
        ("CATEGORICAL", "Atomic, defined, traceable structured fact in value_text with categorical_type (D-074). Never narrative, opinion, interpretation, causal explanation or commercial judgement."),
    ],
    "v_energy_class": [
        ("INSTALLED", "Nameplate rating of commissioned plant."), ("AVAILABLE", "Not on planned/forced outage."),
        ("DEPENDABLE", "Reliably available at system peak."),
        ("SEASONAL_DEPENDABLE", "Dependable capacity per month/season (mandatory for hydro)."),
        ("DISPATCHED", "Actually generating at a given time."), ("GENERATED_GROSS", "Gross generation at terminals."),
        ("GENERATED_NET", "Net generation."), ("GENERATED_UNSTATED", "Generation, gross/net not stated - flagged."),
        ("DELIVERED", "After transmission losses."), ("CONSUMED_BILLED", "Billed end-use energy."),
        ("CONSUMED_METERED", "Metered end-use energy."), ("PEAK_SERVED", "Maximum served demand."),
        ("PEAK_UNCONSTRAINED", "Estimated unconstrained peak."), ("AVERAGE_DEMAND", "Energy / hours."),
        ("SUPPRESSED_UNSERVED", "Demand not served (method stated)."), ("CAPTIVE_SELF_SUPPLIED", "Met by on-site/private generation."),
        ("CLASS_UNSTATED", "Source does not state the class - use restricted."), ("NOT_APPLICABLE", "Not a capacity/energy/demand metric."),
    ],
    "v_acdc": [
        ("AC", "MW-AC."), ("DC", "MW-DC (incl. MWp as reported)."),
        ("BASIS_UNSTATED", "AC/DC basis not stated - flagged, confidence downgraded."), ("NOT_APPLICABLE", "Not relevant."),
    ],
    "v_value_qualifier": [
        ("EXACT", "Value as reported."), ("APPROXIMATE", "Source states approximate."), ("ROUNDED", "Source rounding noted."),
        ("SOURCE_RANGE", "Range reported by the source (value_low/value_high)."),
        ("CONTRADICTION_RANGE", "Range carried from a RANGE-CARRIED contradiction."),
        ("UPPER_BOUND", "At most."), ("LOWER_BOUND", "At least."),
    ],
    "v_unit": [(u, d) for u, d in [
        ("kW", "kilowatt"), ("MW", "megawatt (non-PV or basis in ac_dc_basis)"), ("GW", "gigawatt"),
        ("MW_AC", "megawatt AC"), ("MW_DC", "megawatt DC (MWp recorded here; original label in unit_note)"),
        ("kWh", "kilowatt-hour"), ("MWh", "megawatt-hour"), ("GWh", "gigawatt-hour"), ("TWh", "terawatt-hour"),
        ("MVA", "megavolt-ampere"), ("MVAr", "megavolt-ampere reactive"), ("kV", "kilovolt"), ("Hz", "hertz"),
        ("km", "kilometre"), ("km2", "square kilometre"), ("ha", "hectare"),
        ("PERCENT", "percent (state numerator/denominator in definition)"), ("PERCENTAGE_POINT", "percentage points"),
        ("CURRENCY", "amount in currency field"), ("CURRENCY_PER_KWH", "currency per kWh"), ("CURRENCY_PER_MWH", "currency per MWh"),
        ("CURRENCY_PER_KW", "currency per kW"), ("CURRENCY_PER_KW_YEAR", "currency per kW-year"),
        ("CURRENCY_PER_LITRE", "currency per litre"), ("CURRENCY_PER_TONNE", "currency per tonne"),
        ("CURRENCY_PER_M3", "currency per cubic metre"),
        ("FX_RATE", "units of quote currency per one unit of base currency"),
        ("LITRE", "litre"), ("M3", "cubic metre"), ("TONNE", "tonne"), ("TONNE_PER_YEAR", "tonnes per year"),
        ("MTPA", "million tonnes per annum"), ("TONNE_PER_HOUR", "tonnes per hour (e.g. steam)"),
        ("M3_PER_S", "cubic metres per second"), ("KWH_PER_M2_PER_DAY", "irradiation per day"),
        ("KWH_PER_M2_PER_YEAR", "irradiation per year"), ("M_PER_S", "metres per second"), ("HOURS", "hours"),
        ("HOURS_PER_YEAR", "hours per year"), ("DAYS", "days"), ("YEARS", "years"), ("COUNT", "count"),
        ("PERSONS", "persons"), ("KWH_PER_CAPITA", "kWh per person"), ("RATIO", "dimensionless ratio"),
        ("INDEX", "index (base stated)"), ("OTHER", "other - state in unit_note"),
    ]],
    "v_price_basis": [("NOMINAL", "As reported, value of the stated year."), ("REAL", "Constant prices (base year + deflator required; ESTIMATE)."), ("NOT_APPLICABLE", "Not a monetary value.")],
    "v_conversion_type": [
        ("NONE", "Value as reported."), ("UNIT_IDENTITY", "Exact unit identity (e.g. MWh to GWh); same record."),
        ("FX", "Currency conversion - separate ESTIMATE record citing the FX_RATE record (D-070)."),
        ("DEFLATOR", "Real-terms conversion - ESTIMATE (base year per P-024)."),
        ("DC_AC_RATIO", "AC/DC conversion with documented ratio - ESTIMATE."),
        ("OTHER_DERIVATION", "Any other derived calculation - ESTIMATE."),
    ],
    "v_fx_rate_type": [
        ("PERIOD_AVERAGE", "Average over the value's period - default for flows (D-070)."),
        ("END_OF_PERIOD", "Rate at period end - default for stocks/balances (D-070)."),
        ("TRANSACTION_STATED", "Rate stated in the source transaction document."),
        ("OFFICIAL_FIXING_DATE", "Official rate on a specific date (e.g. a tariff decision date)."),
        ("NOT_APPLICABLE", "No FX involved."),
    ],
    "v_fx_source_class": [
        ("CENTRAL_BANK_OFFICIAL", "Official rate published by the issuing central bank (preference 1)."),
        ("IMF_IFS", "IMF International Financial Statistics (preference 2)."),
        ("WORLD_BANK_WDI", "World Bank World Development Indicators (preference 3)."),
        ("TRANSACTION_DOCUMENT", "Rate stated in the transaction's own document (for TRANSACTION_STATED)."),
        ("OTHER_DOCUMENTED", "Other documented source - justify in notes (preference 4)."),
    ],
    "v_geo_level": [
        ("NATIONAL_AGGREGATE", "Guinea national level."), ("REGIONAL", "Administrative region."),
        ("PREFECTURE", "Prefecture."), ("LOCALITY", "Sub-prefecture / commune / locality."),
        ("CITY", "City or urban area."), ("MINING_SITE", "Mining site."), ("INDUSTRIAL_SITE", "Industrial site."),
        ("PORT", "Port."), ("PLANT_SITE", "Generation (or storage) site."),
        ("TRANSMISSION_CORRIDOR", "Transmission line or corridor."), ("SUBSTATION_NODE", "Substation."),
        ("INTERCONNECTION", "Cross-border interconnection point or line."), ("RIVER_BASIN", "River basin / catchment."),
        ("NEIGHBOURING_COUNTRY", "Benchmark or neighbouring country (protocol section 7.2 test required)."),
        ("MULTI_COUNTRY_REGION", "Regional aggregate (e.g. power-pool-wide)."), ("OTHER", "Other - explain in notes."),
    ],
    "v_period_type": [
        ("CALENDAR_YEAR", "Calendar year."), ("FISCAL_YEAR", "Fiscal year (define in notes)."), ("QUARTER", "Quarter."),
        ("MONTH", "Month."), ("SEASON", "Season (definition per source in season_label)."), ("DATE", "Single date."),
        ("MULTI_YEAR_PERIOD", "Multi-year period."), ("POINT_IN_TIME", "Status at a point in time."),
    ],
    "v_temporal_class": [
        ("HISTORICAL", "Observed outturn, 2016-2026."), ("CURRENT_STATUS", "State as of a stated date."),
        ("COMMITTED_UNDER_CONSTRUCTION", "Financially committed / under construction future additions."),
        ("PLANNED", "Active development / announced / proposed."), ("TARGET_ASPIRATION", "Policy target or corporate ambition."),
        ("PROJECTION", "Forecast (third party or project ESTIMATE)."),
    ],
    "v_subject_type": [
        ("PROJECT", "subject_id = PRJ-"), ("SITE", "subject_id = SITE-"), ("ENTITY", "subject_id = ENT-"),
        ("NATIONAL_SYSTEM", "National power system (no subject_id)."), ("GEOGRAPHY", "A geographic unit (no subject_id)."),
        ("BASIN", "A river basin (no subject_id)."), ("OTHER", "Other - explain."),
    ],
    "v_revalidation": [
        ("TARIFF", "Revalidate before use at Gates 5-7; mandatory at Gate 9; on any newer schedule."),
        ("LAW_REGULATION", "Check amendments at Gate 3; mandatory at Gate 9."),
        ("INSTITUTIONAL_MANDATE", "At Gate 3; Gate 9; on reported restructuring."),
        ("FX_RULE", "At Gate 3; mandatory at Gate 9."),
        ("PROJECT_STATUS", "At each gate of use (5, 6, 7); mandatory at Gate 9; on new evidence."),
        ("OWNERSHIP", "At Gate 3; Gate 9."), ("EXCHANGE_RATE", "On conversion; Gate 9 for deliverable figures."),
        ("HISTORICAL_OUTTURN", "Only when a revised source edition is known/likely."),
        ("PHYSICAL_RESOURCE", "On new dataset version or longer series."), ("OTHER", "Category-specific trigger in notes."),
    ],
    "v_document_type": [(c, c.replace("_", " ").title()) for c in [
        "LAW_DECREE", "REGULATOR_DECISION", "OFFICIAL_GAZETTE", "MINISTRY_REPORT", "UTILITY_REPORT",
        "SYSTEM_OPERATOR_REPORT", "AUDIT_REPORT", "EITI_REPORT", "SIGNED_AGREEMENT", "STATUTORY_FILING",
        "DFI_PROJECT_DOCUMENT", "IMF_REPORT", "OFFICIAL_DATABASE", "PEER_REVIEWED_PAPER", "GREY_LITERATURE",
        "CONSULTANCY_REPORT", "ESIA", "CORPORATE_ANNUAL_REPORT", "INVESTOR_PRESENTATION", "PRESS_RELEASE",
        "NEWS_ARTICLE", "TRADE_PRESS", "DATASET", "GIS_DATASET", "ENGINEERING_STANDARD", "AGGREGATOR_WEB",
        "AI_OUTPUT", "OWNER_SUPPLIED_DOCUMENT", "OTHER"]],
    "v_date_precision": [("DAY", "Full date known."), ("MONTH", "Month and year known."), ("YEAR", "Year only."), ("UNDATED", "No date.")],
    "v_access_status": [("OPEN", "Openly accessible."), ("REGISTRATION", "Free registration required."), ("PAYWALLED", "Paid access."), ("UNAVAILABLE", "Offline/broken."), ("RESTRICTED", "Restricted distribution.")],
    "v_retrieval_status": [
        ("CANDIDATE_SOURCE", "Identified, not yet retrieved."), ("RETRIEVED", "Document opened and checked."),
        ("CITATION_NOT_FOUND", "Cited source cannot be found after the search path."),
        ("UNAVAILABLE", "Exists but cannot be retrieved."), ("PAYWALLED", "Exists; paid access not obtained."),
    ],
    "v_reliability_flag": [("NONE", "No concern."), ("UNDER_REVIEW", "Reliability being reassessed."), ("UNRELIABLE", "Found unreliable - dependent records flagged.")],
    "v_copyright_basis": [
        ("PUBLIC_DOMAIN", "Public domain."), ("GOVERNMENT_REDISTRIBUTABLE", "Official publication, publicly redistributable."),
        ("OPEN_LICENCE", "Open licence permitting redistribution."), ("LICENSED_FOR_REDISTRIBUTION", "Licensed for redistribution."),
        ("COPYRIGHTED", "Copyrighted - reference only."), ("UNCLEAR", "Unclear - do not commit."),
    ],
    "v_local_copy": [
        ("STORED", "Archived in 02_sources/ (basis recorded)."),
        ("NOT_STORED_REFERENCE_ONLY", "Metadata/reference only (default)."),
        ("STORED_LOCALLY_NOT_COMMITTED", "Working copy outside the repository."),
    ],
    "v_origin": [
        ("GEMINI_MISSION", "Gemini discovery mission output."), ("GEMINI_ARCHITECTURE_CHALLENGE", "Gate 1 challenge (GL-01 - GL-33)."),
        ("CLAUDE_DISCOVERY", "Claude independent discovery."), ("OWNER_SUPPLIED", "Supplied by the project owner (incl. Alendei capability evidence)."),
        ("OWNER_CHALLENGE", "Project-owner challenge (independent review input, D-064)."),
        ("CHATGPT_CHALLENGE", "ChatGPT challenge (independent review input, D-064)."), ("OTHER", "Other - explain."),
    ],
    "v_claim_type": [(c, c.replace("_", " ").title()) for c in ["QUANTITATIVE", "QUALITATIVE", "STATUS", "LEGAL_REGULATORY", "ENTITY_PRESENCE", "DEFINITION", "OTHER"]],
    "v_lead_outcome": [
        ("NOT_YET_CHECKED", "Not yet verified (Gate 1: NOT YET CHECKED)."),
        ("VERIFIED", "Claim verified; resulting record(s) listed."),
        ("PARTLY_VERIFIED", "Partly supported (Gate 1: PARTLY VERIFIED); record created as EXTRACTED."),
        ("CONTRADICTED", "Source contradicts the claim."),
        ("UNSUPPORTED", "Cited source missing or does not contain the claim - final outcome (D-058)."),
        ("NOT_VERIFIABLE", "No source given and none found; closed into a data gap (D-058)."),
    ],
    "v_outcome_reason": [(c, c.replace("_", " ").title()) for c in [
        "CITATION_NOT_FOUND", "NOT_IN_SOURCE", "SOURCE_CONTRADICTS", "PARTIAL_MATCH", "NO_SOURCE_GIVEN",
        "ACCESS_PAYWALLED", "ACCESS_UNAVAILABLE", "MALFORMED_ARTIFACT", "NOT_APPLICABLE"]],
    "v_self_confidence": [("HIGH", "High."), ("MEDIUM", "Medium."), ("LOW", "Low."), ("NOT_STATED", "Not stated.")],
    "v_priority": [
        ("CRITICAL", "Planning priority - critical path (methodology section 12); not confidence."),
        ("HIGH", "Planning priority - high."), ("MEDIUM", "Planning priority - medium."), ("LOW", "Planning priority - low."),
    ],
    "v_gap_status": [("OPEN", "Open."), ("PARTLY_FILLED", "Partly filled."), ("FILLED", "Filled - see filled_by_data_ids."), ("CLOSED_UNRESOLVABLE", "Closed: unresolvable after diminishing returns.")],
    "v_lifecycle": [
        ("PROPOSED", "In a plan/study/pipeline list (methodology section 6.1)."), ("ANNOUNCED", "Public declaration; MoU/LOI at most."),
        ("ACTIVE_DEVELOPMENT", "Documented development work."), ("FINANCIALLY_COMMITTED", "Binding financial commitment."),
        ("UNDER_CONSTRUCTION", "NTP and site works evidenced."), ("OPERATIONAL", "Commissioned/energised/COD."),
        ("CANCELLED", "Officially terminated - final."),
    ],
    "v_lifecycle_evidence": [
        ("PLAN_LISTING", "Supports PROPOSED."), ("PUBLIC_ANNOUNCEMENT", "Supports ANNOUNCED."),
        ("MOU_LOI_FRAMEWORK", "Supports ANNOUNCED at most."), ("DEVELOPMENT_WORK", "Supports ACTIVE_DEVELOPMENT."),
        ("FINANCIAL_CLOSE", "Supports FINANCIALLY_COMMITTED."), ("SIGNED_FINANCING_AGREEMENT", "Supports FINANCIALLY_COMMITTED (board approval alone does not)."),
        ("BINDING_EPC_WITH_FUNDING", "Supports FINANCIALLY_COMMITTED."), ("BUDGET_WITH_SIGNED_CONTRACT", "Supports FINANCIALLY_COMMITTED."),
        ("NTP_AND_SITE_WORKS", "Supports UNDER_CONSTRUCTION."), ("COMMISSIONING_ENERGISATION_COD", "Supports OPERATIONAL."),
        ("OFFICIAL_TERMINATION", "Supports CANCELLED."),
    ],
    "v_progress": [
        ("ON_TRACK", "No evidence of slippage."), ("DELAYED", "Missed published milestone or official revised schedule."),
        ("STALLED", "Positive evidence progress stopped/blocked - never inferred from silence."), ("UNVERIFIED", "Insufficient evidence."),
    ],
    "v_ic_step": [("YES", "Step evidenced (evidence source required)."), ("NO", "Evidence the step has not occurred."), ("UNVERIFIED", "No evidence either way."), ("NOT_APPLICABLE", "Not an interconnector/line.")],
    "v_component_type": [(c, c.replace("_", " ").title()) for c in [
        "GENERATION", "STORAGE", "HYBRID_PLANT", "TRANSMISSION_LINE", "SUBSTATION", "INTERCONNECTOR", "DISTRIBUTION",
        "MINI_GRID", "OFF_GRID_PROGRAMME", "FUEL_INFRASTRUCTURE", "MINING_INFRASTRUCTURE", "PORT", "RAIL", "OTHER"]],
    "v_technology": [(c, c.replace("_", " ").title()) for c in [
        "SOLAR_PV", "WIND_ONSHORE", "WIND_OFFSHORE", "HYDRO_RESERVOIR", "HYDRO_RUN_OF_RIVER", "HYDRO_SMALL", "HYDRO_UNSTATED",
        "THERMAL_HFO", "THERMAL_LFO_DIESEL", "THERMAL_GAS", "THERMAL_DUAL_FUEL", "THERMAL_UNSTATED", "BIOMASS",
        "BESS", "OTHER_STORAGE", "HYBRID", "TRANSMISSION_AC", "SUBSTATION", "DISTRIBUTION_NETWORK", "MINI_GRID",
        "SOLAR_HOME_SYSTEMS", "DEMAND_SIDE_MEASURE", "OTHER", "UNSTATED"]],
    "v_offtaker_type": [(c, c.replace("_", " ").title()) for c in ["UTILITY", "MINING", "PRIVATE_INDUSTRIAL", "COMMERCIAL", "REGIONAL_EXPORT", "MINI_GRID_CUSTOMERS", "CAPTIVE_OWN_USE", "OTHER", "UNSTATED"]],
    "v_yes_no": [("YES", "Yes."), ("NO", "No.")],
    "v_yes_no_unclear": [("YES", "Yes."), ("NO", "No."), ("UNCLEAR", "Unclear.")],
    "v_coord_precision": [("EXACT", "Surveyed/official coordinates."), ("APPROXIMATE", "Approximate."), ("CENTROID", "Area centroid."), ("UNKNOWN", "Unknown.")],
    "v_entity_type": [(c, c.replace("_", " ").title()) for c in [
        "GOVERNMENT_MINISTRY", "REGULATOR", "UTILITY", "SYSTEM_OPERATOR", "GOVERNMENT_AGENCY", "STATE_COMPANY",
        "BASIN_ORGANISATION", "REGIONAL_BODY", "DFI_MULTILATERAL", "DFI_BILATERAL", "ECA_EXIM", "GUARANTEE_INSURER",
        "COMMERCIAL_BANK", "FUND", "DEVELOPER", "IPP", "EPC", "OEM", "MINING_COMPANY", "INDUSTRIAL_COMPANY",
        "PORT_RAIL_OPERATOR", "CONSULTANCY", "NGO", "OTHER"]],
    "v_entity_role": [(c, c.replace("_", " ").title()) for c in [
        "SPONSOR", "OWNER", "DEVELOPER", "EPC", "OEM", "FINANCIER", "GUARANTOR", "INSURER", "OFFTAKER", "OPERATOR",
        "REGULATOR", "POLICY_MAKER", "ADVISER", "OTHER"]],
    "v_origin_subregister": [(c, c.replace("_", " ").title()) for c in ["INDIA", "CHINA", "EUROPE", "MIDDLE_EAST", "USA", "JAPAN_KOREA", "AFRICA_REGIONAL", "GUINEA_DOMESTIC", "OTHER"]],
    "v_presence_class": [
        ("CONFIRMED_OPERATIONAL_PRESENCE", "Guinea-specific evidence of operational presence."),
        ("CONFIRMED_PROJECT_SUPPLIED_OR_EXECUTED", "Guinea project supplied/executed (evidenced)."),
        ("CONFIRMED_PIPELINE", "Guinea pipeline (evidenced)."),
        ("REGIONAL_PRESENCE_ONLY", "Regional presence only."),
        ("POTENTIAL_FUTURE_SUPPLIER_PARTNER", "Potential future supplier/partner."),
        ("NOT_ASSESSED", "Not yet assessed."),
    ],
    "v_institutional_status": [("OPERATIONAL", "Operational."), ("RESTRUCTURED", "Restructured."), ("DEFUNCT", "Defunct."), ("UNVERIFIED", "Unverified."), ("NOT_APPLICABLE", "Not a public body.")],
    "v_site_segment": [(c, c.replace("_", " ").title()) for c in [
        "BAUXITE_EXTRACTION", "ALUMINA_REFINING", "IRON_ORE", "GOLD", "DIAMONDS", "OTHER_MINERAL",
        "NON_MINING_INDUSTRIAL", "PORT_LOGISTICS", "LARGE_COMMERCIAL", "URBAN_LOAD_CENTRE", "TELECOM", "OTHER"]],
    "v_site_activity": [(c, c.replace("_", " ").title()) for c in ["EXTRACTION", "PROCESSING", "REFINING", "RAIL_HAULAGE", "PORT_HANDLING", "MANUFACTURING", "SERVICES", "OTHER"]],
    "v_power_supply_mode": [(c, c.replace("_", " ").title()) for c in ["CAPTIVE", "GRID", "HYBRID", "CROSS_BORDER", "NONE", "UNSTATED"]],
    "v_fuel_type": [(c, c.replace("_", " ").title()) for c in ["HFO", "LFO", "DIESEL", "NATURAL_GAS", "LNG", "LPG", "COAL", "BIOMASS", "NONE", "OTHER", "UNSTATED"]],
    "v_asm_value_type": [
        ("DAT_REFERENCE", "Value is an MDR record - basis_data_ids required, value blank (no duplication)."),
        ("DERIVED_CALCULATION", "Computed from MDR records - method + basis_data_ids."),
        ("ANALYST_JUDGEMENT", "Judgement - method and sensitivity range required."),
        ("ENGINEERING_STANDARD", "From a cited standard - standard_source_ids required."),
        ("POLICY_TARGET", "Policy target used as a scenario input."),
        ("SCENARIO_PARAMETER", "Scenario-defining parameter."),
    ],
    "v_model_component": [(c, c.replace("_", " ").title()) for c in [
        "BASELINE", "D1_MINING_EXPANSION", "D2_PROCESSING_REFINING", "D3_INDUSTRIAL_EXPANSION", "D4_URBAN_COMMERCIAL",
        "D5_ELECTRIFICATION", "D6_INFRASTRUCTURE", "S1_HYDRO_SEASONALITY_CLIMATE", "S2_COMMITTED_ADDITIONS",
        "S3_WAPP_TRADE", "S4_DISTRIBUTED_CAPTIVE", "SCREENING", "GIS_THRESHOLD", "FX_CONVERSION", "OTHER"]],
    "v_gis_family": [(c, c.replace("_", " ").title()) for c in [
        "BASE_ADMIN", "SETTLEMENTS_DEMAND", "GENERATION", "TRANSMISSION_SUBSTATIONS", "REGIONAL_INTERCONNECTION",
        "MINING_INDUSTRIAL", "LOGISTICS", "HYDROLOGY", "RESOURCE_SOLAR", "RESOURCE_WIND", "RESOURCE_HYDRO",
        "STORAGE", "CONSTRAINT", "OPPORTUNITY"]],
    "v_gis_folder": [(c, f"05_gis/{c}/") for c in [
        "base_maps", "cities", "generation", "transmission", "substations", "wapp", "mining", "industrial",
        "logistics", "hydrology", "solar", "wind", "hydro", "bess", "constraints", "opportunities"]],
    "v_gis_format": [(c, c) for c in ["GPKG", "GEOJSON", "SHP", "GEOTIFF", "OTHER"]],
    "v_geometry": [(c, c.title()) for c in ["POINT", "LINE", "POLYGON", "RASTER", "MIXED"]],
    "v_constraint_class": [
        ("LEGAL_EXCLUSION", "Development legally prohibited - legal basis required."),
        ("REGULATORY_TECHNICAL_CONSTRAINT", "Possible subject to conditions."),
        ("RISK_FLAG", "Increases cost/risk/time."), ("NOT_A_CONSTRAINT", "Not a constraint layer."),
    ],
    "v_linked_id_type": [("PRJ", "Features carry PRJ IDs."), ("SITE", "Features carry SITE IDs."), ("OPP", "Features carry OPP IDs."), ("NONE", "No register link.")],
    "v_solution_type": [(c, c.replace("_", " ").title()) for c in ["GENERATION", "STORAGE", "HYBRID", "NETWORK", "DEMAND_SIDE", "DECENTRALISED", "REGIONAL_TRADE", "FUEL_INFRASTRUCTURE", "OTHER"]],
    "v_commercial_model": [(c, c.replace("_", " ").title()) for c in ["UTILITY_PPA", "PRIVATE_B2B_PPA", "CAPTIVE_SELF_SUPPLY", "BOO", "BOOT", "CONCESSION", "PPP", "MINI_GRID_CONCESSION", "PUBLIC_PROCUREMENT", "OTHER"]],
    "v_fatal_flaw": [("PASS", "No fatal flaw on this test."), ("FAIL", "Fatal flaw."), ("UNRESOLVED", "Evidence insufficient - held, not rejected."), ("NOT_ASSESSED", "Not yet assessed.")],
    "v_attractiveness": [
        ("HIGHLY_ATTRACTIVE", "Provisional label (P-011, confirm by Gate 7)."), ("ATTRACTIVE", "Provisional label (P-011)."),
        ("CONDITIONALLY_ATTRACTIVE", "Provisional label (P-011)."), ("NOT_CURRENTLY_ATTRACTIVE", "Provisional label (P-011)."),
    ],
    "v_alendei_role": [(c, c.replace("_", " ").title() + " (D-011 hypothesis role - not an asserted capability)") for c in [
        "OPPORTUNITY_IDENTIFICATION", "PROJECT_DEVELOPMENT", "TECHNICAL_SOLUTION_ARCHITECTURE", "RENEWABLE_INTEGRATION",
        "BESS_INTEGRATION", "INDUSTRIAL_CAPTIVE_SOLUTIONS", "IPP_BOOT_BOO_STRUCTURES", "COMMERCIAL_STRUCTURING",
        "PARTNER_COORDINATION", "OEM_EPC_INTEGRATION", "FINANCING_COORDINATION", "GOVERNMENT_INTERFACE", "INDUSTRIAL_INTERFACE"]],
    "v_gap_level": [("NONE_IDENTIFIED", "No gap identified on user-supplied evidence."), ("GAP_CLOSABLE", "Gap closable (how stated)."), ("GAP_MATERIAL", "Material gap."), ("NOT_ASSESSED", "Not yet assessed.")],
    "v_alendei_tier": [
        ("TIER_1_PURSUE_IMMEDIATELY", "Tier 1 - Pursue immediately."), ("TIER_2_DEVELOP", "Tier 2 - Develop."),
        ("TIER_3_MONITOR", "Tier 3 - Monitor."), ("TIER_4_DO_NOT_PURSUE_NOW", "Tier 4 - Do not pursue now (mandatory where warranted)."),
    ],
    "v_categorical_type": [
        ("BOOLEAN", "value_text is YES or NO (e.g. whether a regulatory requirement or licence requirement exists)."),
        ("ENTITY_REFERENCE", "value_text is an ENT- ID (e.g. the institution responsible for a defined function)."),
        ("CATEGORY_CODE", "value_text is one code from a list stated in metric_definition (e.g. a technology or status classification)."),
    ],
    "v_difference_test": [
        ("DEFINITION", "Same metric definition?"), ("PERIOD", "Same date/period?"), ("GEOGRAPHY", "Same geography?"),
        ("SCOPE", "Same asset/customer/system scope?"), ("UNIT", "Same unit and currency/price basis?"),
        ("AC_DC_BASIS", "Same AC/DC basis?"), ("ENERGY_BASIS", "Same installed/available/dependable/dispatched/delivered/consumed basis?"),
        ("METHODOLOGY", "Same measurement/estimation method?"), ("SOURCE_PRECISION", "Is the difference demonstrably attributable to reporting precision?"),
    ],
    "v_precision_attribution": [
        ("ATTRIBUTABLE", "All three D-072 conditions met: comparable definitions; comparable period/geography/scope; difference demonstrably due to reporting precision."),
        ("NOT_ATTRIBUTABLE", "Difference not shown to be reporting precision - contradiction preserved or range carried."),
        ("NOT_APPLICABLE", "Categorical/status difference."),
    ],
}

# ---------------------------------------------------------------------------
# Field specs: (name, type, requirement, constraint, description)
# requirement: R required | C conditional (see VR rule) | O optional | D derived (never hand-edited)
# ---------------------------------------------------------------------------
ID_PATTERNS = {
    "DAT": ("DAT-WSNN-NNNNN", 'AND(LEFT({c},6)="DAT-WS",LEN({c})=14,MID({c},9,1)="-",ISNUMBER(--MID({c},7,2)),ISNUMBER(--MID({c},10,5)))'),
    "SRC": ("SRC-NNNN", 'AND(LEFT({c},4)="SRC-",LEN({c})=8,ISNUMBER(--MID({c},5,4)))'),
    "LEAD": ("LEAD-NNNNN", 'AND(LEFT({c},5)="LEAD-",LEN({c})=10,ISNUMBER(--MID({c},6,5)))'),
    "CON": ("CON-NNNN", 'AND(LEFT({c},4)="CON-",LEN({c})=8,ISNUMBER(--MID({c},5,4)))'),
    "GAP": ("GAP-NNNN", 'AND(LEFT({c},4)="GAP-",LEN({c})=8,ISNUMBER(--MID({c},5,4)))'),
    "PRJ": ("PRJ-NNNN", 'AND(LEFT({c},4)="PRJ-",LEN({c})=8,ISNUMBER(--MID({c},5,4)))'),
    "ENT": ("ENT-NNNN", 'AND(LEFT({c},4)="ENT-",LEN({c})=8,ISNUMBER(--MID({c},5,4)))'),
    "SITE": ("SITE-NNNN", 'AND(LEFT({c},5)="SITE-",LEN({c})=9,ISNUMBER(--MID({c},6,4)))'),
    "ASM": ("ASM-NNNN", 'AND(LEFT({c},4)="ASM-",LEN({c})=8,ISNUMBER(--MID({c},5,4)))'),
    "GIS": ("GIS-NNNN", 'AND(LEFT({c},4)="GIS-",LEN({c})=8,ISNUMBER(--MID({c},5,4)))'),
    "OPP": ("OPP-NNNN", 'AND(LEFT({c},4)="OPP-",LEN({c})=8,ISNUMBER(--MID({c},5,4)))'),
    "ALP": ("ALP-NNNN", 'AND(LEFT({c},4)="ALP-",LEN({c})=8,ISNUMBER(--MID({c},5,4)))'),
    "D": ("D-NNN", 'AND(LEFT({c},2)="D-",LEN({c})=5,ISNUMBER(--MID({c},3,3)))'),
}


def F(name, typ, req, con="", desc=""):
    return (name, typ, req, con, desc)


def common(supersede_target):
    return [
        F("acceptance_status", "ENUM", "R", "v_acceptance_status", "Gate approval status (D-062). Distinct from evidence_state/confidence; vocabularies do not overlap."),
        F("acceptance_decision_id", "ID_REF", "C", "D", "Decision-log ID; required when ACCEPTED or REJECTED (VR-02)."),
        F("acceptance_gate", "ENUM", "C", "v_gate", "Gate of acceptance/rejection; required when ACCEPTED or REJECTED (VR-02)."),
        F("record_status", "ENUM", "R", "v_record_status", "Methodology section 3 `status`: ACTIVE or SUPERSEDED. Records are never deleted (VR-03, D-071)."),
        F("superseded_by", "ID_REF", "C", supersede_target, "Replacing record ID; required when SUPERSEDED (VR-03)."),
        F("created_by", "ENUM", "R", "v_actor", "Who created the record."),
        F("created_date", "DATE", "R", "", "DD-MMM-YYYY."),
        F("last_modified_by", "ENUM", "O", "v_actor", ""),
        F("last_modified_date", "DATE", "O", "", "DD-MMM-YYYY."),
        F("notes", "LONGTEXT", "O", "", "Caveats; never a substitute for a structured field."),
    ]


QUALITY = [F(f"quality_{q}", "ENUM", "R", "v_quality", f"Quality dimension: {q.replace('_', ' ')} (methodology section 2.1; may only lower confidence).")
           for q in ["source_quality", "recency", "cross_source_agreement", "methodological_quality", "completeness", "definition_consistency"]]

GEO = [
    F("geography_name", "TEXT", "R", "", "Name of the geographic unit/site as given in the source."),
    F("geo_level", "ENUM", "R", "v_geo_level", "Geographic level (D-067)."),
    F("country_iso3", "ISO3", "R", "", "ISO 3166-1 alpha-3 code of the country the value relates to."),
]

COORDS = [
    F("latitude", "NUMBER", "O", "LAT", "Decimal degrees, -90 to 90."),
    F("longitude", "NUMBER", "O", "LON", "Decimal degrees, -180 to 180."),
    F("crs", "TEXT", "C", "", "Required with coordinates; storage CRS EPSG:4326 (research_architecture section L.3)."),
    F("coordinate_precision", "ENUM", "C", "v_coord_precision", "Required with coordinates."),
    F("coordinate_source_id", "ID_REF", "C", "SRC", "Source of coordinates; required with coordinates."),
]

STATUS = [
    F("lifecycle_stage", "ENUM", "R", "v_lifecycle", "Methodology section 6.1; highest stage with qualifying evidence."),
    F("lifecycle_evidence_type", "ENUM", "R", "v_lifecycle_evidence", "Type of evidence supporting the stage; must be consistent with the stage (VR-19)."),
    F("lifecycle_evidence_source_ids", "ID_LIST", "R", "SRC", "Sources evidencing the stage."),
    F("progress_condition", "ENUM", "R", "v_progress", "Methodology section 6.2. STALLED requires positive evidence; silence = UNVERIFIED (VR-19)."),
    F("progress_evidence_source_ids", "ID_LIST", "C", "SRC", "Required for DELAYED and STALLED."),
    F("status_summary", "LONGTEXT", "R", "", "Methodology section 6.3 status_evidence: the specific evidence for stage and condition."),
    F("last_evidence_date", "DATE", "R", "", "Date of most recent evidence of activity."),
    F("status_assessed_date", "DATE", "R", "", "Date status last assessed (status as of)."),
    F("status_confidence", "ENUM", "R", "v_confidence", "Confidence in the status assessment."),
]

REGISTERS = []


def register(key, title, path, sheets, purpose, maintainer, mdr_rel, extra_sheets=None):
    REGISTERS.append(dict(key=key, title=title, path=path, sheets=sheets, purpose=purpose,
                          maintainer=maintainer, mdr_rel=mdr_rel, extra=extra_sheets or []))


# 1 Master Data Register --------------------------------------------------
register("MDR", "Master Data Register", "03_evidence/master_data_register/master_data_register.xlsx", [("MDR", "DAT", [
    F("data_id", "ID", "R", "DAT", "Unique ID DAT-WSNN-NNNNN; WS part must equal `workstream` (VR-01)."),
    F("workstream", "ENUM", "R", "v_workstream_phase_a", "Owning Phase A workstream (WS-01 - WS-26)."),
    F("lead_id", "ID_LIST", "O", "LEAD", "Originating lead(s)."),
    F("subject_type", "ENUM", "R", "v_subject_type", "What the value describes."),
    F("subject_id", "ID_REF", "C", "PRJ|SITE|ENT", "Required when subject_type is PROJECT, SITE or ENTITY."),
    F("metric", "TEXT", "R", "", "Metric name."),
    F("metric_class", "ENUM", "R", "v_metric_class", "Metric class."),
    F("metric_definition", "LONGTEXT", "R", "", "Precise definition per methodology section 5 / protocol section 8."),
    F("energy_class", "ENUM", "R", "v_energy_class", "Capacity/energy/demand class; NOT_APPLICABLE for other metrics (VR-13)."),
    F("ac_dc_basis", "ENUM", "R", "v_acdc", "Required basis for PV capacity (VR-13)."),
    F("value_kind", "ENUM", "R", "v_value_kind", "NUMERIC or CATEGORICAL (D-074 boundary)."),
    F("value", "NUMBER", "C", "", "Numeric value as reported (VR-11)."),
    F("value_low", "NUMBER", "C", "", "Low bound for ranges (VR-11)."),
    F("value_high", "NUMBER", "C", "", "High bound for ranges (VR-11)."),
    F("value_text", "SHORTTEXT", "C", "", "Structured categorical value (max 100 characters) when value_kind = CATEGORICAL; format per categorical_type (D-074, VR-11a)."),
    F("categorical_type", "ENUM", "C", "v_categorical_type", "Required when value_kind = CATEGORICAL (D-074)."),
    F("value_qualifier", "ENUM", "R", "v_value_qualifier", "Exact, approximate, range, bound."),
    F("unit", "ENUM", "C", "v_unit", "Required for NUMERIC (VR-12)."),
    F("unit_note", "TEXT", "O", "", "Original unit label as reported (e.g. MWp)."),
    F("currency", "ISO4217", "C", "", "ISO 4217 code; required for currency-based units (VR-12)."),
    F("price_basis", "ENUM", "C", "v_price_basis", "Required when currency is set (VR-12)."),
    F("price_base_year", "YEAR", "C", "", "Required when price_basis = REAL (P-024 governs the base year)."),
    F("conversion_type", "ENUM", "R", "v_conversion_type", "NONE unless derived (VR-14)."),
    F("input_data_ids", "ID_LIST", "C", "DAT", "Inputs for ESTIMATE / derived records (VR-06, VR-14)."),
    F("assumption_ids", "ID_LIST", "C", "ASM", "Assumptions used by an ESTIMATE."),
    F("estimate_method", "LONGTEXT", "C", "", "Required for ESTIMATE (VR-06)."),
    F("fx_rate_type", "ENUM", "C", "v_fx_rate_type", "Required for FX_RATE records and FX conversions (VR-14, D-070)."),
    F("fx_source_class", "ENUM", "C", "v_fx_source_class", "Required for FX_RATE records (VR-14, D-070)."),
    F("fx_base_currency", "ISO4217", "C", "", "FX_RATE records: base currency (one unit of)."),
    F("fx_quote_currency", "ISO4217", "C", "", "FX_RATE records: quote currency."),
] + GEO + [
    F("period_type", "ENUM", "R", "v_period_type", "Period the value describes."),
    F("period_start", "DATE", "R", "", "Start (or single date) of the period described - not the publication date."),
    F("period_end", "DATE", "C", "", "End of period where applicable."),
    F("season_label", "TEXT", "C", "", "Season definition as per source; required for SEASONAL_DEPENDABLE (VR-15)."),
    F("temporal_class", "ENUM", "R", "v_temporal_class", "Protocol section 6.2."),
    F("source_id", "ID_REF", "C", "SRC", "Required unless evidence_state = ESTIMATE (VR-06)."),
    F("source_title", "DERIVED", "D", "SRC", "Lookup from source register (methodology section 3)."),
    F("publisher", "DERIVED", "D", "SRC", "Lookup from source register."),
    F("source_publication_date", "DERIVED", "D", "SRC", "Lookup from source register."),
    F("source_url_or_reference", "DERIVED", "D", "SRC", "Lookup from source register."),
    F("source_tier", "DERIVED", "D", "SRC", "Lookup from source register (tier assigned there)."),
    F("discloser_independence", "DERIVED", "D", "SRC", "Lookup from source register."),
    F("page_table_section", "TEXT", "C", "", "Exact location in source; required for VERIFIED (VR-07)."),
    F("access_date", "DATE", "C", "", "Date the value was read; required with source_id."),
    F("evidence_state", "ENUM", "R", "v_evidence_state_register", "Verification state (methodology section 2.2)."),
    F("confidence", "ENUM", "R", "v_confidence", "Confidence per evidence state; may be lower, never higher (VR-08)."),
] + QUALITY + [
    F("cross_check_status", "ENUM", "R", "v_cross_check", ""),
    F("cross_check_source_ids", "ID_LIST", "C", "SRC", "Independent sources; required for CORROBORATED (VR-09)."),
    F("cross_check_data_ids", "ID_LIST", "O", "DAT", "Related MDR records compared."),
    F("contradiction_status", "ENUM", "R", "v_contradiction_status", ""),
    F("contradiction_id", "ID_REF", "C", "CON", "Required when contradiction_status is not NONE."),
    F("revalidation_category", "ENUM", "R", "v_revalidation", "Event-based revalidation trigger (protocol section 6.4; no time expiry)."),
    F("last_revalidated_date", "DATE", "O", "", ""),
    F("verified_by", "ENUM", "C", "v_actor", "Required for VERIFIED/CORROBORATED."),
    F("verified_date", "DATE", "C", "", "Required for VERIFIED/CORROBORATED."),
] + common("DAT"))],
    "Single store of every material statistic with full provenance (methodology section 3).",
    "Claude Code; approved at Gates 3, 4, 9", "Is the hub")

# 2 Source register --------------------------------------------------------
register("SRC", "Source Register", "03_evidence/source_register/source_register.xlsx", [("SOURCES", "SRC", [
    F("source_id", "ID", "R", "SRC", "Unique ID SRC-NNNN."),
    F("title_original", "TEXT", "R", "", "Exact title, original language."),
    F("title_translation", "TEXT", "O", "", "Translation, marked as such."),
    F("publisher", "TEXT", "R", "", "Issuing organisation."),
    F("author", "TEXT", "O", "", ""),
    F("document_type", "ENUM", "R", "v_document_type", "Protocol section 4.4 categories."),
    F("language", "TEXT", "R", "", "ISO 639-1 code (e.g. fr, en)."),
    F("publication_date", "DATE", "C", "", "Required unless publication_date_precision = UNDATED."),
    F("publication_date_precision", "ENUM", "R", "v_date_precision", ""),
    F("edition_version", "TEXT", "O", "", "Edition, revision or dataset version."),
    F("url", "TEXT", "C", "", "URL; url or persistent_reference required (VR-20a)."),
    F("persistent_reference", "TEXT", "C", "", "DOI, document number, archive reference."),
    F("access_date", "DATE", "R", "", "Date first accessed."),
    F("access_status", "ENUM", "R", "v_access_status", ""),
    F("retrieval_status", "ENUM", "R", "v_retrieval_status", "CANDIDATE_SOURCE until retrieved (evidence state of a source)."),
    F("source_tier", "TIER", "R", "", "1-6 per the authoritative hierarchy (D-082; methodology section 1), assigned by Claude (not adopted from Gemini). Tier 6 is never evidence. Media/trade press: tier 5 with document_type NEWS_ARTICLE/TRADE_PRESS - secondary reporting, not an evidence tier (D-086, VR-30)."),
    F("discloser_independence", "ENUM", "R", "v_discloser", ""),
    F("origin", "ENUM", "R", "v_origin", "How the source entered the project."),
    F("origin_ref", "TEXT", "C", "", "Mission ID + artifact version, discovery note or decision ID."),
    F("mission_local_ids", "TEXT", "O", "", "Gemini mission-local IDs mapped to this source (GEM-NN-S##; '; '-separated)."),
    F("supersedes_source_id", "ID_REF", "O", "SRC", "Earlier edition this source supersedes."),
    F("reliability_flag", "ENUM", "R", "v_reliability_flag", "Protocol section 17."),
    F("reliability_note", "LONGTEXT", "C", "", "Required when UNDER_REVIEW or UNRELIABLE."),
    F("relevant_pages_sections", "LONGTEXT", "O", "", "Pages/sections/tables relied on (methodology section 4.2)."),
    F("evidence_extracted_summary", "LONGTEXT", "O", "", "Summary of what was taken (methodology section 4.2)."),
    F("evidence_data_ids", "DERIVED", "D", "DAT", "Lookup: MDR records citing this source."),
    F("access_copyright_note", "LONGTEXT", "R", "", "Licence/copyright status and redistribution restrictions."),
    F("copyright_basis", "ENUM", "R", "v_copyright_basis", ""),
    F("local_copy_status", "ENUM", "R", "v_local_copy", "Default NOT_STORED_REFERENCE_ONLY (VR-21)."),
    F("local_path", "TEXT", "C", "", "Required when STORED."),
    F("search_path_log", "LONGTEXT", "C", "", "Required when CITATION_NOT_FOUND or UNAVAILABLE (protocol section 17)."),
] + common("SRC"))],
    "Bibliographic, access and copyright record of every source (methodology section 4.2).",
    "Claude Code", "Every MDR record cites a SRC- ID")

# 3 Lead register ----------------------------------------------------------
register("LEAD", "Lead Register", "03_evidence/lead_register/lead_register.xlsx", [("LEADS", "LEAD", [
    F("lead_id", "ID", "R", "LEAD", "Unique ID LEAD-NNNNN."),
    F("origin", "ENUM", "R", "v_origin", "Gemini mission, architecture challenge, Claude discovery, owner/ChatGPT challenge."),
    F("origin_ref", "TEXT", "R", "", "Mission ID + artifact version / discovery note / decision ID."),
    F("claim_id", "TEXT", "C", "", "GEM-NN-C### for missions; GL-NN for architecture leads."),
    F("artifact_file", "TEXT", "C", "", "Deposited artifact path (Gemini origins)."),
    F("artifact_sha256", "TEXT", "C", "", "64-hex fingerprint of the artifact."),
    F("claim_text", "LONGTEXT", "R", "", "Claim verbatim. Never edited."),
    F("claim_type", "ENUM", "R", "v_claim_type", ""),
    F("workstream_primary", "ENUM", "R", "v_workstream", ""),
    F("workstreams_other", "TEXT", "O", "", "Other WS IDs ('; '-separated)."),
    F("research_question", "TEXT", "O", "", "Charter question, e.g. WS-05 Q2."),
    F("question_priority", "DERIVED", "D", "charter", "Lookup of charter planning priority (not confidence)."),
    F("temporal_class", "ENUM", "O", "v_temporal_class", ""),
    F("geo_level", "ENUM", "O", "v_geo_level", ""),
    F("cited_source_as_stated", "LONGTEXT", "C", "", "Citation exactly as given by the origin."),
    F("cited_source_id", "ID_REF", "C", "SRC", "Registered source for the citation."),
    F("origin_self_confidence", "ENUM", "O", "v_self_confidence", "Origin's self-assessed confidence - advisory only."),
    F("evidence_state", "ENUM", "R", "v_evidence_state_lead", "Always RAW_LEAD (VR-18)."),
    F("lead_outcome", "ENUM", "R", "v_lead_outcome", "Verification outcome (D-058)."),
    F("outcome_reason", "ENUM", "C", "v_outcome_reason", "Required for UNSUPPORTED, CONTRADICTED, NOT_VERIFIABLE, PARTLY_VERIFIED."),
    F("search_path_log", "LONGTEXT", "C", "", "Required for UNSUPPORTED / NOT_VERIFIABLE (protocol section 17)."),
    F("resulting_record_ids", "ID_LIST", "C", "DAT|PRJ|ENT|SITE", "Required for VERIFIED / PARTLY_VERIFIED."),
    F("contradiction_id", "ID_REF", "C", "CON", "For CONTRADICTED where a CON row exists."),
    F("gap_id", "ID_REF", "C", "GAP", "For NOT_VERIFIABLE."),
    F("checked_by", "ENUM", "C", "v_actor", "Required once outcome is not NOT_YET_CHECKED."),
    F("checked_date", "DATE", "C", "", ""),
] + common("LEAD"))],
    "Verification queue for unverified claims (Gemini, discovery notes, challenges, GL-01 - GL-33). Leads are never evidence.",
    "Claude Code; acceptance = discovery acceptance at Gate 2D", "A verified lead points to the record it produced; leads are never used as data")

# 4 Contradiction register --------------------------------------------------
DIFF_TEST_ROWS = [
    ("PRINCIPLE", "No universal numerical contradiction tolerance is assumed (D-072). Any difference between values for the same metric, entity, geography and period triggers the tests below. Never introduce an arbitrary percentage tolerance.", "", ""),
] + [(str(i), code, q, "If not comparable: record the cause code; values may be RESOLVED-DEFINITIONAL (different things measured).")
     for i, (code, q) in enumerate(V["v_difference_test"][:8], 1)] + [
    ("9", "SOURCE_PRECISION", "Classify as reporting precision ONLY when (1) definitions are comparable, (2) period/geography/scope are comparable, and (3) the difference is demonstrably attributable to reporting precision.", "If met: cause REPORTING_PRECISION, precision_attribution ATTRIBUTABLE, justification recorded. Otherwise: preserve the contradiction, or carry a range where sources are comparable and none can reasonably be preferred."),
    ("CATEGORICAL", "STATUS_AND_CATEGORICAL", "Any difference in a categorical or status value is a contradiction.", "precision_attribution NOT_APPLICABLE."),
]

register("CON", "Contradiction Register", "03_evidence/contradictions/contradiction_register.xlsx", [("CONTRADICTIONS", "CON", [
    F("con_id", "ID", "R", "CON", "Unique ID CON-NNNN."),
    F("workstream", "ENUM", "R", "v_workstream_phase_a", ""),
    F("metric", "TEXT", "R", "", "Metric in conflict."),
    F("metric_class", "ENUM", "R", "v_metric_class", ""),
    F("subject_type", "ENUM", "R", "v_subject_type", ""),
    F("subject_id", "ID_REF", "C", "PRJ|SITE|ENT", ""),
    F("geography_name", "TEXT", "R", "", ""),
    F("geo_level", "ENUM", "R", "v_geo_level", ""),
    F("period_description", "TEXT", "R", "", "Period(s) of the conflicting values."),
    F("data_ids", "ID_LIST", "R", "DAT", "Two or more conflicting MDR records (VR-26). Values are not copied here."),
    F("diagnostic_tests_completed", "MULTI_ENUM", "R", "v_difference_test", "D-072 comparability tests completed ('; '-separated); see DIFFERENCE_TESTS sheet."),
    F("precision_attribution", "ENUM", "R", "v_precision_attribution", "D-072 three-condition test result."),
    F("precision_justification", "LONGTEXT", "C", "", "Required when ATTRIBUTABLE: evidence that the difference is due to reporting precision."),
    F("cause_code", "ENUM", "R", "v_cause_code", "Primary cause (D-068)."),
    F("cause_code_secondary", "ENUM", "O", "v_cause_code", ""),
    F("cause_notes", "LONGTEXT", "R", "", "Diagnosis."),
    F("outcome", "ENUM", "R", "v_contradiction_outcome", "Gate 1 outcome set (research_architecture section H)."),
    F("governing_data_id", "ID_REF", "C", "DAT", "Required for RESOLVED-HIERARCHY / RESOLVED-ERROR."),
    F("range_data_id", "ID_REF", "C", "DAT", "MDR record holding the carried range; required for RANGE-CARRIED."),
    F("reasoning", "LONGTEXT", "R", "", "Why the outcome was chosen. Never silent."),
    F("materiality", "ENUM", "R", "v_materiality", ""),
    F("escalated", "ENUM", "R", "v_yes_no", "MATERIAL + OPEN/RANGE-CARRIED must be YES."),
    F("escalation_gate", "ENUM", "C", "v_gate", "Required when escalated = YES."),
    F("resolved_by", "ENUM", "C", "v_actor", "Required for RESOLVED-*."),
    F("resolved_date", "DATE", "C", "", "Required for RESOLVED-*."),
] + common("CON"))],
    "Conflicting values and their resolution (research_architecture section H; protocol section 10).",
    "Claude Code; material items reviewed by owner at Gate 4", "References two or more DAT- IDs; MDR records carry contradiction_id",
    extra_sheets=[("DIFFERENCE_TESTS", ["step", "test", "question / rule", "outcome guidance"], DIFF_TEST_ROWS)])

# 5 Data-gap register --------------------------------------------------------
register("GAP", "Data-Gap Register", "03_evidence/data_gaps/data_gap_register.xlsx", [("DATA_GAPS", "GAP", [
    F("gap_id", "ID", "R", "GAP", "Unique ID GAP-NNNN."),
    F("workstream", "ENUM", "R", "v_workstream_phase_a", ""),
    F("research_question", "TEXT", "R", "", "Charter question, e.g. WS-09 Q4, or NEW."),
    F("question_priority_original", "DERIVED", "D", "charter", "Charter planning priority at Gate 1."),
    F("question_priority_current", "ENUM", "R", "v_priority", "Current planning priority; changes only at Gate 4 (methodology section 12)."),
    F("priority_change_reason", "LONGTEXT", "C", "", "Required when current differs from original."),
    F("priority_change_decision_id", "ID_REF", "C", "D", "Required when current differs from original (VR-25)."),
    F("gap_description", "LONGTEXT", "R", "", "What is missing."),
    F("metric_class", "ENUM", "O", "v_metric_class", ""),
    F("subject_type", "ENUM", "O", "v_subject_type", ""),
    F("subject_id", "ID_REF", "O", "PRJ|SITE|ENT", ""),
    F("geography_name", "TEXT", "O", "", ""),
    F("geo_level", "ENUM", "O", "v_geo_level", ""),
    F("period_description", "TEXT", "O", "", ""),
    F("materiality", "ENUM", "R", "v_materiality", "Evidence-based materiality (distinct from planning priority)."),
    F("sources_tried_ids", "ID_LIST", "O", "SRC", ""),
    F("search_path_log", "LONGTEXT", "R", "", "Standard search path followed (protocol section 17)."),
    F("access_limitations", "LONGTEXT", "O", "", ""),
    F("lead_ids", "ID_LIST", "O", "LEAD", ""),
    F("next_step", "LONGTEXT", "R", "", ""),
    F("proposed_mission", "TEXT", "O", "", "GEM-NN or NEW (new missions need a decision-log entry)."),
    F("gap_status", "ENUM", "R", "v_gap_status", ""),
    F("filled_by_data_ids", "ID_LIST", "C", "DAT", "Required for FILLED / PARTLY_FILLED."),
    F("evidence_state", "ENUM", "R", "v_evidence_state_gap", "Always DATA_GAP."),
] + common("GAP"))],
    "Questions sought but not answered; materiality; next steps; Gate 4 priority reassessment.",
    "Claude Code; reviewed at Gate 4", "Records the absence of an MDR value")

# 6 Project register ---------------------------------------------------------
IC = []
for step in ["constructed", "energised", "synchronised", "operational", "commercially_active"]:
    IC += [F(f"ic_{step}", "ENUM", "C", "v_ic_step", f"Interconnector/line step '{step.replace('_', ' ')}' (D-069). Required for INTERCONNECTOR."),
           F(f"ic_{step}_evidence_source_ids", "ID_LIST", "C", "SRC", f"Required when ic_{step} = YES."),
           F(f"ic_{step}_date", "DATE", "O", "", "Date the step was evidenced/occurred.")]

register("PRJ", "Project Register", "03_evidence/project_register/project_register.xlsx", [("PROJECTS", "PRJ", [
    F("project_id", "ID", "R", "PRJ", "Unique ID PRJ-NNNN."),
    F("project_name", "TEXT", "R", "", "Standardised name."),
    F("alternative_names", "TEXT", "O", "", "Name history / aliases ('; '-separated) for de-duplication."),
    F("parent_project_id", "ID_REF", "O", "PRJ", "Parent for multi-component projects (each component has its own status)."),
    F("component_type", "ENUM", "R", "v_component_type", ""),
    F("technology", "ENUM", "R", "v_technology", "Technology-neutral list."),
    F("hybrid_components", "MULTI_ENUM", "C", "v_technology", "Required when technology = HYBRID ('; '-separated)."),
    F("workstream_primary", "ENUM", "R", "v_workstream_phase_a", ""),
    F("workstreams_other", "TEXT", "O", "", ""),
] + GEO + COORDS + [
    F("basin_river", "TEXT", "O", "", "Hydro: river/basin as stated in source."),
] + STATUS + [
    F("cod_target_date", "DATE", "O", "", "Published target COD."),
    F("cod_target_source_id", "ID_REF", "C", "SRC", "Required with cod_target_date."),
    F("cod_actual_date", "DATE", "O", "", "Actual COD."),
    F("cod_actual_source_id", "ID_REF", "C", "SRC", "Required with cod_actual_date."),
] + IC + [
    F("capacity_data_ids", "ID_LIST", "O", "DAT", "Capacity values (all classes) - MDR references only (VR-17)."),
    F("energy_data_ids", "ID_LIST", "O", "DAT", "Energy values - MDR references."),
    F("seasonal_output_data_ids", "ID_LIST", "O", "DAT", "Seasonal dependable output (hydro mandatory) - MDR references."),
    F("cost_data_ids", "ID_LIST", "O", "DAT", "Cost/financing values - MDR references."),
    F("contract_term_data_ids", "ID_LIST", "O", "DAT", "Quantitative contract terms - MDR references."),
    F("other_data_ids", "ID_LIST", "O", "DAT", ""),
    F("sponsor_entity_ids", "ID_LIST", "O", "ENT", ""),
    F("owner_entity_ids", "ID_LIST", "O", "ENT", ""),
    F("developer_entity_ids", "ID_LIST", "O", "ENT", ""),
    F("epc_entity_ids", "ID_LIST", "O", "ENT", ""),
    F("oem_entity_ids", "ID_LIST", "O", "ENT", ""),
    F("financier_entity_ids", "ID_LIST", "O", "ENT", ""),
    F("offtaker_entity_ids", "ID_LIST", "O", "ENT", ""),
    F("operator_entity_ids", "ID_LIST", "O", "ENT", ""),
    F("offtaker_type", "ENUM", "O", "v_offtaker_type", ""),
    F("ppa_publicly_documented", "ENUM", "O", "v_yes_no_unclear", ""),
    F("ppa_source_ids", "ID_LIST", "C", "SRC", "Required when ppa_publicly_documented = YES."),
    F("evacuation_project_ids", "ID_LIST", "O", "PRJ", "Evacuation line/substation projects."),
    F("related_site_ids", "ID_LIST", "O", "SITE", ""),
    F("duplicate_of_project_id", "ID_REF", "O", "PRJ", "If a re-announcement of another project."),
    F("dedup_basis", "LONGTEXT", "C", "", "Location/capacity/sponsor basis; required with duplicate_of_project_id."),
    F("lead_ids", "ID_LIST", "O", "LEAD", ""),
] + common("PRJ"))],
    "Identity, technology, location and evidenced status of every generation, storage, transmission and infrastructure project.",
    "Claude Code (WS-23 owner)", "Status and descriptive attributes only; quantities are DAT- references")

# 7 Entity / Site register ---------------------------------------------------
register("ENT", "Entity / Site Register", "03_evidence/entity_register/entity_register.xlsx", [
    ("ORGANISATIONS", "ENT", [
        F("entity_id", "ID", "R", "ENT", "Unique ID ENT-NNNN."),
        F("legal_name", "TEXT", "R", "", ""),
        F("short_name", "TEXT", "O", "", ""),
        F("alternative_names", "TEXT", "O", "", ""),
        F("entity_type", "ENUM", "R", "v_entity_type", ""),
        F("entity_roles", "MULTI_ENUM", "R", "v_entity_role", "'; '-separated roles."),
        F("origin_subregister", "ENUM", "R", "v_origin_subregister", "WS-25 origin sub-register."),
        F("origin_country_iso3", "ISO3", "O", "", ""),
        F("parent_entity_id", "ID_REF", "O", "ENT", ""),
        F("guinea_presence_class", "ENUM", "R", "v_presence_class", "Five WS-25 classes + NOT_ASSESSED; global presence never implies Guinea presence (VR-22)."),
        F("presence_evidence_source_ids", "ID_LIST", "C", "SRC", "Guinea-specific evidence; required for CONFIRMED_* and REGIONAL_PRESENCE_ONLY."),
        F("presence_assessed_date", "DATE", "C", "", "Required when class is not NOT_ASSESSED."),
        F("regional_presence_countries", "TEXT", "O", "", "ISO3 codes ('; '-separated)."),
        F("institutional_status", "ENUM", "C", "v_institutional_status", "Required for public bodies."),
        F("mandate_summary", "LONGTEXT", "O", "", "Public bodies: mandate as evidenced."),
        F("mandate_source_ids", "ID_LIST", "C", "SRC", "Required with mandate_summary."),
        F("related_project_ids", "DERIVED", "D", "PRJ", "Lookup from project register entity fields."),
        F("workstreams", "TEXT", "O", "", ""),
        F("lead_ids", "ID_LIST", "O", "LEAD", ""),
    ] + common("ENT")),
    ("SITES", "SITE", [
        F("site_id", "ID", "R", "SITE", "Unique ID SITE-NNNN."),
        F("site_name", "TEXT", "R", "", ""),
        F("alternative_names", "TEXT", "O", "", ""),
        F("operator_entity_id", "ID_REF", "C", "ENT", ""),
        F("owner_entity_ids", "ID_LIST", "O", "ENT", ""),
        F("segment", "ENUM", "R", "v_site_segment", "D-036 segmentation; extraction and refining kept separate."),
        F("activity_types", "MULTI_ENUM", "R", "v_site_activity", "'; '-separated."),
        F("commodity", "TEXT", "O", "", ""),
        F("workstream_primary", "ENUM", "R", "v_workstream_phase_a", ""),
    ] + GEO + COORDS + STATUS + [
        F("power_supply_modes", "MULTI_ENUM", "R", "v_power_supply_mode", ""),
        F("captive_technologies", "MULTI_ENUM", "O", "v_technology", ""),
        F("fuel_types", "MULTI_ENUM", "O", "v_fuel_type", ""),
        F("grid_connection_project_ids", "ID_LIST", "O", "PRJ", ""),
        F("demand_electrical_data_ids", "ID_LIST", "O", "DAT", "MDR references (VR-17)."),
        F("demand_thermal_data_ids", "ID_LIST", "O", "DAT", "Process steam/heat - MDR references."),
        F("captive_capacity_data_ids", "ID_LIST", "O", "DAT", ""),
        F("fuel_volume_data_ids", "ID_LIST", "O", "DAT", ""),
        F("fuel_cost_data_ids", "ID_LIST", "O", "DAT", ""),
        F("production_data_ids", "ID_LIST", "O", "DAT", ""),
        F("other_data_ids", "ID_LIST", "O", "DAT", ""),
        F("legal_title_reference", "TEXT", "O", "", "Mining/industrial title reference as evidenced."),
        F("legal_title_source_ids", "ID_LIST", "C", "SRC", "Required with legal_title_reference."),
        F("decarbonisation_commitment_summary", "LONGTEXT", "O", "", "Operator/parent commitments as evidenced."),
        F("decarbonisation_source_ids", "ID_LIST", "C", "SRC", "Required with the summary."),
        F("related_project_ids", "ID_LIST", "O", "PRJ", ""),
        F("lead_ids", "ID_LIST", "O", "LEAD", ""),
    ] + common("SITE")),
], "Organisations (type, origin, Guinea-presence class) and mining/industrial sites.",
    "Claude Code (WS-25; WS-11 - WS-14 owners)", "Demand, captive MW, fuel cost are DAT- references")

# 8 Assumption register -------------------------------------------------------
register("ASM", "Assumption Register", "03_evidence/assumption_register/assumption_register.xlsx", [("ASSUMPTIONS", "ASM", [
    F("asm_id", "ID", "R", "ASM", "Unique ID ASM-NNNN."),
    F("assumption_name", "TEXT", "R", "", ""),
    F("parameter", "TEXT", "R", "", "Model parameter the assumption sets."),
    F("description", "LONGTEXT", "R", "", ""),
    F("workstream", "ENUM", "R", "v_workstream", ""),
    F("model_component", "ENUM", "R", "v_model_component", "Scenario drivers D1-D6 / S1-S4 (research_architecture section J) or other use."),
    F("scenario_scope", "TEXT", "R", "", "ALL or named scenario(s)."),
    F("value_type", "ENUM", "R", "v_asm_value_type", "DAT_REFERENCE => value blank (VR-27)."),
    F("basis_data_ids", "ID_LIST", "C", "DAT", "Required for DAT_REFERENCE and DERIVED_CALCULATION."),
    F("value", "NUMBER", "C", "", "Only when value_type is not DAT_REFERENCE (no duplication of MDR values)."),
    F("unit", "ENUM", "C", "v_unit", "Required with value."),
    F("currency", "ISO4217", "C", "", ""),
    F("price_basis", "ENUM", "C", "v_price_basis", ""),
    F("price_base_year", "YEAR", "C", "", "P-024 governs real-terms base year."),
    F("sensitivity_low", "NUMBER", "C", "", "Required for material judgement/scenario parameters."),
    F("sensitivity_high", "NUMBER", "C", "", ""),
    F("method_description", "LONGTEXT", "R", "", ""),
    F("standard_source_ids", "ID_LIST", "C", "SRC", "Required for ENGINEERING_STANDARD / POLICY_TARGET."),
    F("confidence", "ENUM", "R", "v_confidence", "Never VERIFIED for judgement-based assumptions."),
    F("assumption_owner", "ENUM", "R", "v_actor", ""),
    F("approval_gate", "ENUM", "C", "v_gate", "Gate 6/7 approval."),
    F("approval_decision_id", "ID_REF", "C", "D", ""),
] + common("ASM"))],
    "Modelling assumptions with basis and sensitivity; never written back to the MDR as data.",
    "Claude Code; approved at Gates 6-7", "Cites DAT- basis or documented method")

# 9 GIS layer catalogue --------------------------------------------------------
register("GIS", "GIS Layer Catalogue", "05_gis/gis_layer_catalogue.xlsx", [("GIS_LAYERS", "GIS", [
    F("gis_id", "ID", "R", "GIS", "Unique ID GIS-NNNN."),
    F("layer_name", "TEXT", "R", "", ""),
    F("layer_family", "ENUM", "R", "v_gis_family", "research_architecture section L.1."),
    F("gis_folder", "ENUM", "R", "v_gis_folder", "05_gis/ subfolder."),
    F("file_name", "TEXT", "C", "", "Required when committed_to_repo = YES."),
    F("file_format", "ENUM", "R", "v_gis_format", "GeoPackage master proposed (P-012)."),
    F("geometry_type", "ENUM", "R", "v_geometry", ""),
    F("workstreams", "TEXT", "R", "", ""),
    F("description", "LONGTEXT", "R", "", ""),
    F("source_ids", "ID_LIST", "R", "SRC", ""),
    F("dataset_version", "TEXT", "C", "", ""),
    F("dataset_date", "DATE", "C", "", ""),
    F("licence", "TEXT", "R", "", ""),
    F("redistribution_permitted", "ENUM", "R", "v_yes_no_unclear", ""),
    F("committed_to_repo", "ENUM", "R", "v_yes_no", "Must be NO unless redistribution_permitted = YES (VR-23)."),
    F("crs_storage", "TEXT", "R", "", "EPSG:4326."),
    F("crs_analysis", "TEXT", "O", "", "Projected CRS chosen at Gate 6."),
    F("resolution", "TEXT", "C", "", "Rasters."),
    F("spatial_extent", "TEXT", "O", "", ""),
    F("processing_steps", "LONGTEXT", "R", "", ""),
    F("constraint_class", "ENUM", "R", "v_constraint_class", "research_architecture section L.2."),
    F("legal_basis_source_ids", "ID_LIST", "C", "SRC", "Required for LEGAL_EXCLUSION."),
    F("attribute_fields", "LONGTEXT", "O", "", "Continuous attributes retained (no pre-applied masks)."),
    F("threshold_applied", "TEXT", "C", "", "Blank until Gates 6-7; then requires threshold_assumption_ids (VR-23). No universal thresholds."),
    F("threshold_assumption_ids", "ID_LIST", "C", "ASM", ""),
    F("linked_id_type", "ENUM", "O", "v_linked_id_type", ""),
    F("file_sha256", "TEXT", "C", "", "Fingerprint of the committed file."),
] + common("GIS"))],
    "Provenance of every GIS layer: source, date, licence, CRS, processing, constraint class.",
    "Claude Code", "Cites SRC- IDs; features carry PRJ-/SITE-/OPP- IDs")

# 10 Opportunity register --------------------------------------------------------
DIMS = ["demand_quality", "offtaker_counterparty_quality", "technical_feasibility", "resource_quality",
        "grid_proximity_capacity", "land_permitting_environment", "commercial_economics", "fx_currency_exposure",
        "financing_availability", "implementation_complexity", "development_timeline", "strategic_importance",
        "scalability", "competitive_alternatives"]
register("OPP", "Opportunity Register (WS-27)", "06_opportunities/candidate_opportunities/opportunity_register.xlsx", [("OPPORTUNITIES", "OPP", [
    F("opp_id", "ID", "R", "OPP", "Unique ID OPP-NNNN."),
    F("opp_name", "TEXT", "R", "", ""),
    F("description", "LONGTEXT", "R", "", ""),
    F("solution_type", "ENUM", "R", "v_solution_type", "All solution types (technology-neutral)."),
    F("technologies", "MULTI_ENUM", "R", "v_technology", ""),
    F("geography_name", "TEXT", "R", "", ""),
    F("geo_level", "ENUM", "R", "v_geo_level", ""),
    F("related_project_ids", "ID_LIST", "O", "PRJ", ""),
    F("related_site_ids", "ID_LIST", "O", "SITE", ""),
    F("related_entity_ids", "ID_LIST", "O", "ENT", ""),
    F("evidence_chain_data_ids", "ID_LIST", "R", "DAT", "ACCEPTED MDR records only; never LEAD- IDs (VR-18, VR-24)."),
    F("evidence_chain_other_ids", "ID_LIST", "O", "PRJ|SITE|ENT|GIS", ""),
    F("assumption_ids", "ID_LIST", "O", "ASM", ""),
    F("ff_legal", "ENUM", "R", "v_fatal_flaw", "Fatal-flaw test: legal prohibition."),
    F("ff_offtake", "ENUM", "R", "v_fatal_flaw", "No credible offtaker/payment pathway."),
    F("ff_site_constraint", "ENUM", "R", "v_fatal_flaw", "Legal exclusion constraint."),
    F("ff_technical", "ENUM", "R", "v_fatal_flaw", "Technical impossibility."),
    F("ff_evidence", "ENUM", "R", "v_fatal_flaw", "Evidence too weak - UNRESOLVED, not rejected."),
    F("ff_notes", "LONGTEXT", "C", "", "Required when any test is FAIL or UNRESOLVED."),
] + [F(f"d{i + 1:02d}_{d}", "SCORE", "C", "", f"Dimension {i + 1:02d} ordinal 1-5; blank until Gate 7 anchors are approved.") for i, d in enumerate(DIMS)] + [
    F("d15_evidence_confidence_overlay", "ENUM", "C", "v_confidence", "Reported alongside the score, not weighted (research_architecture section K.2)."),
    F("score_rationale", "LONGTEXT", "C", "", "Required when scores entered."),
    F("weight_set_decision_id", "ID_REF", "C", "D", "Blank: weights not frozen (D-029). Set only after Gate 7 approval."),
    F("composite_score", "DERIVED", "D", "", "Computed only once an approved weight set exists; never hand-entered."),
    F("sensitivity_notes", "LONGTEXT", "C", "", "Weight-sensitivity / rank robustness."),
    F("commercial_model_options", "MULTI_ENUM", "O", "v_commercial_model", "None predetermined (D-026)."),
    F("structuring_notes", "LONGTEXT", "O", "", ""),
    F("attractiveness_rating", "ENUM", "C", "v_attractiveness", "Alendei-neutral; provisional labels (P-011)."),
    F("rating_frozen", "ENUM", "R", "v_yes_no", "YES only with freeze_decision_id (Gate 7 part 1)."),
    F("freeze_decision_id", "ID_REF", "C", "D", ""),
    F("freeze_date", "DATE", "C", "", ""),
] + common("OPP"))],
    "WS-27 country opportunities (Alendei-neutral): evidence chain, fatal-flaw screen, scores, frozen attractiveness rating. Contains no Alendei fields.",
    "Claude Code; User + ChatGPT approve freeze at Gate 7 part 1", "Evidence chain cites DAT-/PRJ-/ENT-/ASM- IDs")

# 11 Alendei participation register -----------------------------------------------
register("ALP", "Alendei Participation Register (WS-28)", "06_opportunities/alendei_role/alendei_participation_register.xlsx", [("ALENDEI_PARTICIPATION", "ALP", [
    F("alp_id", "ID", "R", "ALP", "Unique ID ALP-NNNN."),
    F("opp_id", "ID_REF", "R", "OPP", "Frozen WS-27 opportunity (read-only reference; VR-24)."),
    F("opp_attractiveness_at_freeze", "DERIVED", "D", "OPP", "Lookup; WS-28 cannot alter it."),
    F("opp_freeze_decision_id", "DERIVED", "D", "OPP", "Lookup."),
    F("candidate_roles", "MULTI_ENUM", "R", "v_alendei_role", "D-011 hypothesis roles - not asserted capabilities."),
    F("role_rationale", "LONGTEXT", "R", "", ""),
    F("capability_evidence_source_ids", "ID_LIST", "C", "SRC", "User-supplied evidence only (origin OWNER_SUPPLIED; VR-24)."),
    F("capability_gap", "ENUM", "R", "v_gap_level", ""),
    F("licence_gap", "ENUM", "R", "v_gap_level", ""),
    F("partnership_gap", "ENUM", "R", "v_gap_level", ""),
    F("financing_gap", "ENUM", "R", "v_gap_level", ""),
    F("gap_closure_notes", "LONGTEXT", "C", "", "Required for GAP_CLOSABLE / GAP_MATERIAL."),
    F("required_partner_entity_ids", "ID_LIST", "O", "ENT", "From the evidenced WS-25 register."),
    F("financing_pathway_entity_ids", "ID_LIST", "O", "ENT", "From WS-24/WS-25."),
    F("strategic_fit_notes", "LONGTEXT", "O", "", "Secondary lens (research_architecture section K.3)."),
    F("tier_classification", "ENUM", "C", "v_alendei_tier", "methodology section 11; Tier 4 mandatory where warranted."),
    F("classification_rationale", "LONGTEXT", "C", "", "Required with tier_classification."),
    F("tier_eligibility_check", "DERIVED", "D", "OPP", "Tier 1/2 requires opp rating at least CONDITIONALLY_ATTRACTIVE (proposed rule, P-011)."),
    F("roadmap_ref", "TEXT", "O", "", "06_opportunities/roadmap/ document reference."),
    F("due_diligence_ref", "TEXT", "O", "", "06_opportunities/due_diligence/ document reference."),
] + common("ALP"))],
    "WS-28 Alendei roles, capability gaps, partners, Tier 1-4 classification for frozen WS-27 opportunities.",
    "Claude Code; capability evidence supplied only by the user; User + ChatGPT approve", "References OPP- IDs read-only; holds no Guinea statistics")

# ---------------------------------------------------------------------------
# Validation rules (enforced in-cell where Excel allows; others by the register
# validator, to be built before data entry at Gate 2D)
# ---------------------------------------------------------------------------
VR = [
    ("VR-01", "All", "Record IDs follow the register pattern, are unique, and are never reused. MDR: WS part of data_id equals `workstream`.", "In-cell (pattern) + validator"),
    ("VR-02", "All", "acceptance_status in {PROPOSED, ACCEPTED, REJECTED}. ACCEPTED/REJECTED require acceptance_decision_id (existing D-NNN) and acceptance_gate. New records start PROPOSED.", "In-cell (list) + validator"),
    ("VR-03", "All", "record_status SUPERSEDED requires superseded_by referencing an existing record of the same register. Rows are never deleted; corrections are made by supersession.", "Validator"),
    ("VR-04", "All", "acceptance_status and evidence_state/confidence are separate fields with non-overlapping vocabularies; acceptance never implies verification (D-062).", "Structural"),
    ("VR-05", "All", "Every *_id / *_ids reference resolves to an existing record in the target register; ID lists use '; ' as separator.", "Validator"),
    ("VR-06", "MDR", "source_id required unless evidence_state = ESTIMATE; ESTIMATE requires input_data_ids and estimate_method.", "Validator"),
    ("VR-07", "MDR", "evidence_state VERIFIED requires page_table_section, access_date, verified_by, verified_date, and a source of tier 1-3 (D-082).", "Validator"),
    ("VR-08", "MDR", "Confidence mapping: VERIFIED->VERIFIED; CORROBORATED->CORROBORATED; ESTIMATE->ESTIMATED; EXTRACTED->INDICATIVE; CONTRADICTED_UNRESOLVED requires contradiction_id. Confidence may be lower than the mapping (quality dimensions) but never higher.", "Validator"),
    ("VR-09", "MDR", "CORROBORATED requires cross_check_status = AGREES (identical, or differing only by demonstrable reporting precision under D-072) and >= 2 independent sources (source_id + cross_check_source_ids) with at least one tier <= 4 (D-082); sources sharing an origin, citing each other or AI outputs are not independent.", "Validator + reviewer"),
    ("VR-10", "MDR", "If the only sources are tier 5-6 (D-082), confidence is at most INDICATIVE.", "Validator"),
    ("VR-11", "MDR", "NUMERIC: value, or value_low + value_high, required. SOURCE_RANGE/CONTRADICTION_RANGE require low and high; CONTRADICTION_RANGE requires contradiction_status = RANGE-CARRIED. CATEGORICAL requires value_text and blank numeric fields.", "Validator"),
    ("VR-11a", "MDR", "P-025 boundary (D-074): CATEGORICAL records must be atomic, defined and traceable - categorical_type required; BOOLEAN => value_text YES/NO; ENTITY_REFERENCE => an existing ENT- ID; CATEGORY_CODE => a code listed in metric_definition; value_text <= 100 characters; metric, definition, geography, effective period (period_start/end), source, evidence state, confidence and provenance required as for numbers. Narrative, opinions, interpretations, broad qualitative assessments, causal explanations and commercial judgements are prohibited in the MDR and belong in lead, analysis or reconciliation structures.", "In-cell (length, list) + validator + reviewer"),
    ("VR-12", "MDR/ASM", "unit required for NUMERIC; CURRENCY* units require currency (ISO 4217) and price_basis; REAL requires price_base_year and an assumption reference for the deflator.", "In-cell (pattern) + validator"),
    ("VR-13", "MDR", "metric_class CAPACITY/ENERGY/DEMAND requires energy_class other than NOT_APPLICABLE; PV capacity requires ac_dc_basis AC or DC (BASIS_UNSTATED flagged and confidence downgraded); CLASS_UNSTATED restricts use.", "Validator"),
    ("VR-14", "MDR", "conversion_type FX/DEFLATOR/DC_AC_RATIO/OTHER_DERIVATION requires evidence_state = ESTIMATE and input_data_ids; FX conversions must cite an FX_RATE record; FX_RATE records require fx_rate_type, fx_source_class, fx_base_currency, fx_quote_currency (D-070).", "Validator"),
    ("VR-15", "MDR", "energy_class SEASONAL_DEPENDABLE requires period_type MONTH or SEASON and season_label; hydro plant records require seasonal dependable capacity alongside nameplate (D-037).", "Validator"),
    ("VR-16", "All", "DERIVED columns are populated only by tooling from the authoritative register and are never hand-edited.", "Structural + validator"),
    ("VR-17", "PRJ/ENT/SITE/OPP/ALP", "No quantitative evidence columns exist outside the MDR (and non-evidence assumption values in ASM); quantities are referenced by DAT- IDs (single store). The only other numeric attributes permitted are spatial coordinates (latitude/longitude, with source) and WS-27 ordinal assessment scores (1-5), neither of which is an evidence statistic.", "Structural"),
    ("VR-18", "LEAD/OPP", "Lead evidence_state is always RAW_LEAD; UNSUPPORTED/NOT_VERIFIABLE/CONTRADICTED require outcome_reason; LEAD- IDs never appear in evidence chains or as evidence anywhere.", "In-cell (list) + validator"),
    ("VR-19", "PRJ/SITE", "lifecycle_evidence_type must support lifecycle_stage (MoU/LOI at most ANNOUNCED; board approval alone never FINANCIALLY_COMMITTED); stages FINANCIALLY_COMMITTED and later need corroboration if only tier-5 sources (D-082); STALLED requires positive evidence in progress_evidence_source_ids; silence = UNVERIFIED.", "Validator + reviewer"),
    ("VR-20", "PRJ", "component_type INTERCONNECTOR requires all five ic_* steps; each YES requires its evidence; energised requires constructed; synchronised, operational and commercially_active each require energised; lifecycle OPERATIONAL for lines/interconnectors requires ic_energised = YES; steps are never collapsed (D-069).", "Validator"),
    ("VR-20a", "SRC", "url or persistent_reference required; access_date required; local_path required when local_copy_status = STORED.", "Validator"),
    ("VR-21", "SRC/GIS", "STORED / committed only with copyright_basis PUBLIC_DOMAIN, GOVERNMENT_REDISTRIBUTABLE, OPEN_LICENCE or LICENSED_FOR_REDISTRIBUTION; UNCLEAR is never committed.", "Validator"),
    ("VR-22", "ENT", "CONFIRMED_* presence classes require Guinea-specific presence_evidence_source_ids; global presence never implies Guinea presence.", "Validator + reviewer"),
    ("VR-23", "GIS", "LEGAL_EXCLUSION requires legal_basis_source_ids; threshold_applied blank before Gate 6 and otherwise requires threshold_assumption_ids; committed_to_repo = NO unless redistribution_permitted = YES.", "Validator"),
    ("VR-24", "OPP/ALP", "OPP contains no Alendei fields; scores blank until Gate 7; composite_score only with weight_set_decision_id; rating_frozen = YES requires freeze_decision_id; evidence chains cite ACCEPTED records only. ALP opp_id must reference a frozen OPP; WS-28 cannot alter OPP ratings; capability evidence must come from OWNER_SUPPLIED sources; Tier 1/2 eligibility per P-011 (provisional).", "Validator + reviewer"),
    ("VR-25", "GAP", "question_priority_current differing from the charter priority requires priority_change_reason and priority_change_decision_id (Gate 4).", "Validator"),
    ("VR-26", "CON", "data_ids lists >= 2 MDR records; RESOLVED-HIERARCHY/RESOLVED-ERROR require governing_data_id; RANGE-CARRIED requires range_data_id; MATERIAL + OPEN/RANGE-CARRIED requires escalated = YES. D-072: no universal numerical tolerance - any difference triggers the comparability tests; cause REPORTING_PRECISION only with precision_attribution = ATTRIBUTABLE, all nine tests in diagnostic_tests_completed and a precision_justification; otherwise the contradiction is preserved or a range carried.", "Validator"),
    ("VR-27", "ASM", "value_type DAT_REFERENCE requires basis_data_ids and blank value (no duplication); other types require value, unit and method_description; assumptions are never written back into the MDR.", "Validator"),
    ("VR-28", "All", "Analysis, GIS and deliverables may use only records with acceptance_status = ACCEPTED and record_status = ACTIVE.", "Validator + gate review"),
    ("VR-30", "MDR", "Media/trade press (document_type NEWS_ARTICLE or TRADE_PRESS) never independently establishes a material claim (D-086): a record whose only sources are media is at most EXTRACTED/INDICATIVE; media reports derived from one underlying source count once.", "Validator + reviewer"),
    ("VR-31", "MDR", "Corporate statutory filings and other Tier 5 disclosures are authoritative only for the issuer's own disclosed facts (D-086): a record whose only sources are Tier 5 must not describe NATIONAL_SYSTEM, GEOGRAPHY or BASIN subjects (government, grid, regulatory or national-system facts).", "Validator + reviewer"),
    ("VR-29", "All", "Dates are stored as dates and displayed DD-MMM-YYYY; period_start is the period described, never the publication date.", "In-cell (date)"),
]

# ---------------------------------------------------------------------------
# XLSX writer (stdlib)
# ---------------------------------------------------------------------------
NS = 'xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"'
FIXED = (1980, 1, 1, 0, 0, 0)

STYLES = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
<numFmts count="1"><numFmt numFmtId="164" formatCode="dd\\-mmm\\-yyyy"/></numFmts>
<fonts count="4">
<font><sz val="11"/><name val="Calibri"/><family val="2"/></font>
<font><b/><sz val="11"/><name val="Calibri"/><family val="2"/></font>
<font><b/><sz val="11"/><color rgb="FFFFFFFF"/><name val="Calibri"/><family val="2"/></font>
<font><b/><sz val="14"/><name val="Calibri"/><family val="2"/></font>
</fonts>
<fills count="7">
<fill><patternFill patternType="none"/></fill>
<fill><patternFill patternType="gray125"/></fill>
<fill><patternFill patternType="solid"><fgColor rgb="FF1F3864"/><bgColor indexed="64"/></patternFill></fill>
<fill><patternFill patternType="solid"><fgColor rgb="FF2E75B6"/><bgColor indexed="64"/></patternFill></fill>
<fill><patternFill patternType="solid"><fgColor rgb="FFDDEBF7"/><bgColor indexed="64"/></patternFill></fill>
<fill><patternFill patternType="solid"><fgColor rgb="FFD9D9D9"/><bgColor indexed="64"/></patternFill></fill>
<fill><patternFill patternType="solid"><fgColor rgb="FFFFF2CC"/><bgColor indexed="64"/></patternFill></fill>
</fills>
<borders count="1"><border><left/><right/><top/><bottom/><diagonal/></border></borders>
<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>
<cellXfs count="10">
<xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>
<xf numFmtId="0" fontId="2" fillId="2" borderId="0" xfId="0" applyFont="1" applyFill="1"/>
<xf numFmtId="0" fontId="2" fillId="3" borderId="0" xfId="0" applyFont="1" applyFill="1"/>
<xf numFmtId="0" fontId="1" fillId="4" borderId="0" xfId="0" applyFont="1" applyFill="1"/>
<xf numFmtId="0" fontId="1" fillId="5" borderId="0" xfId="0" applyFont="1" applyFill="1"/>
<xf numFmtId="0" fontId="3" fillId="0" borderId="0" xfId="0" applyFont="1"/>
<xf numFmtId="0" fontId="1" fillId="0" borderId="0" xfId="0" applyFont="1"/>
<xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0" applyAlignment="1"><alignment wrapText="1" vertical="top"/></xf>
<xf numFmtId="0" fontId="1" fillId="6" borderId="0" xfId="0" applyFont="1" applyFill="1" applyAlignment="1"><alignment wrapText="1" vertical="top"/></xf>
<xf numFmtId="164" fontId="0" fillId="0" borderId="0" xfId="0" applyNumberFormat="1"/>
</cellXfs>
<cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles>
</styleSheet>'''
HDR_STYLE = {"R": 1, "C": 2, "O": 3, "D": 4}


def col(n):
    s = ""
    while n:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


def cell(ref, text, style=0):
    st = f' s="{style}"' if style else ""
    return f'<c r="{ref}" t="inlineStr"{st}><is><t xml:space="preserve">{escape(str(text))}</t></is></c>'


def sheet_xml(rows, widths, freeze=False, autofilter=None, validations=(), col_styles=None):
    out = [f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<worksheet {NS}>']
    ncols = max((len(r) for r in rows), default=1)
    nrows = max(len(rows), 1)
    out.append(f'<dimension ref="A1:{col(ncols)}{nrows}"/>')
    out.append('<sheetViews><sheetView workbookViewId="0">')
    if freeze:
        out.append('<pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/><selection pane="bottomLeft" activeCell="A2" sqref="A2"/>')
    out.append('</sheetView></sheetViews><sheetFormatPr defaultRowHeight="15"/>')
    out.append("<cols>")
    for i, w in enumerate(widths, 1):
        sty = f' style="{col_styles[i]}"' if col_styles and i in col_styles else ""
        out.append(f'<col min="{i}" max="{i}" width="{w}" customWidth="1"{sty}/>')
    out.append("</cols><sheetData>")
    for r, row in enumerate(rows, 1):
        out.append(f'<row r="{r}">' + "".join(cell(f"{col(c)}{r}", v, s) for c, (v, s) in enumerate(row, 1) if v != "") + "</row>")
    out.append("</sheetData>")
    if autofilter:
        out.append(f'<autoFilter ref="{autofilter}"/>')
    if validations:
        out.append(f'<dataValidations count="{len(validations)}">' + "".join(validations) + "</dataValidations>")
    out.append('<pageMargins left="0.7" right="0.7" top="0.75" bottom="0.75" header="0.3" footer="0.3"/></worksheet>')
    return "".join(out)


def dv(kind, sqref, f1=None, f2=None, op=None, prompt="", title="", err=""):
    a = f' type="{kind}"' if kind != "custom" else ' type="custom"'
    if op:
        a += f' operator="{op}"'
    a += ' allowBlank="1" showInputMessage="1" showErrorMessage="1"'
    if title:
        a += f' promptTitle="{escape(title[:32], {chr(34): "&quot;"})}"'
    if prompt:
        a += f' prompt="{escape(prompt[:250], {chr(34): "&quot;"})}"'
    if err:
        a += f' errorTitle="Invalid value" error="{escape(err[:220], {chr(34): "&quot;"})}"'
    body = ""
    if f1 is not None:
        body += f"<formula1>{escape(f1)}</formula1>"
    if f2 is not None:
        body += f"<formula2>{escape(f2)}</formula2>"
    return f'<dataValidation{a} sqref="{sqref}">{body}</dataValidation>'


def field_validation(f, letter):
    name, typ, req, con, desc = f
    rng = f"{letter}2:{letter}{MAX_ROW}"
    c = f"{letter}2"
    p = f"[{ {'R': 'Required', 'C': 'Conditional', 'O': 'Optional', 'D': 'DERIVED - do not edit'}[req]}] {desc}"
    if typ in ("ENUM",):
        return dv("list", rng, con, prompt=p, title=name, err=f"Use a value from {con} (VOCAB sheet).")
    if typ == "ID":
        return dv("custom", rng, ID_PATTERNS[con][1].format(c=c), prompt=p, title=name, err=f"ID must match {ID_PATTERNS[con][0]}.")
    if typ == "ID_REF" and con in ID_PATTERNS:
        return dv("custom", rng, ID_PATTERNS[con][1].format(c=c), prompt=p, title=name, err=f"Reference must match {ID_PATTERNS[con][0]}.")
    if typ == "DATE":
        return dv("date", rng, "1", "73051", "between", prompt=p + " Format DD-MMM-YYYY.", title=name, err="Enter a valid date.")
    if typ == "NUMBER":
        if con == "LAT":
            return dv("decimal", rng, "-90", "90", "between", prompt=p, title=name, err="Latitude -90 to 90.")
        if con == "LON":
            return dv("decimal", rng, "-180", "180", "between", prompt=p, title=name, err="Longitude -180 to 180.")
        return dv("decimal", rng, "-1E+307", "1E+307", "between", prompt=p, title=name, err="Enter a number.")
    if typ == "TIER":
        return dv("whole", rng, "1", "6", "between", prompt=p, title=name, err="Tier 1-6.")
    if typ == "SCORE":
        return dv("whole", rng, "1", "5", "between", prompt=p, title=name, err="Score 1-5.")
    if typ == "YEAR":
        return dv("whole", rng, "1900", "2100", "between", prompt=p, title=name, err="Four-digit year.")
    if typ == "SHORTTEXT":
        return dv("textLength", rng, "0", "100", "between", prompt=p, title=name, err="Max 100 characters: atomic structured value only (D-074).")
    if typ in ("ISO4217", "ISO3"):
        return dv("custom", rng, f'AND(LEN({c})=3,EXACT({c},UPPER({c})))', prompt=p, title=name, err="Three upper-case letters (ISO code).")
    return dv("custom", rng, f'LEN({c})>=0', prompt=p, title=name) if desc else None


def vocab_names(fields):
    out = []
    for f in fields:
        if f[1] in ("ENUM", "MULTI_ENUM") and f[3] not in out:
            out.append(f[3])
    return out


def build_workbook(reg, root):
    sheets = []          # (name, xml)
    defined = []
    all_fields = [f for _, _, fl in reg["sheets"] for f in fl]
    vocabs = vocab_names(all_fields)
    # README
    rd = [[("TEMPLATE - CONTAINS NO DATA", 8)], [(reg["title"], 5)], [("", 0)],
          [("Purpose", 6), (reg["purpose"], 7)],
          [("Workbook", 6), (reg["path"], 0)],
          [("Maintained by / authority", 6), (reg["maintainer"], 7)],
          [("Relationship to Master Data Register", 6), (reg["mdr_rel"], 7)],
          [("Schema version", 6), (f"{SCHEMA_VERSION} ({SCHEMA_DATE}); decision {SCHEMA_DECISION}; generated by 00_project/tools/build_register_templates.py", 7)],
          [("Data dictionary", 6), ("DICTIONARY sheet; full schema in 00_project/register_schema.md", 7)],
          [("Register architecture", 6), ("11 logical registers; Entity/Site is implemented as two physical tables/sheets where required by the schema (D-076).", 7)],
          [("", 0)],
          [("Single-source-of-truth rules (research_architecture.md section G.1)", 6)],
          [("1", 0), ("This XLSX workbook is the authoritative register. CSV/JSON are generated derivatives only, never hand-edited.", 7)],
          [("2", 0), ("No manually maintained duplicate of this register may exist.", 7)],
          [("3", 0), ("Every material quantitative value is stored once, in the Master Data Register; other registers reference DAT- IDs.", 7)],
          [("4", 0), ("acceptance_status (gate approval) is not evidence_state/confidence (verification) (D-062).", 7)],
          [("5", 0), ("Rows are never deleted; corrections are made by supersession (record_status = SUPERSEDED).", 7)],
          [("6", 0), ("Only ACCEPTED + ACTIVE records may be used in analysis, GIS or deliverables.", 7)],
          [("7", 0), ("Multi-value fields use '; ' as separator. Dates are DD-MMM-YYYY.", 7)],
          [("8", 0), ("Header colours: dark blue = required; mid blue = conditional; light blue = optional; grey = DERIVED (never edit).", 7)],
          [("", 0)],
          [("Status", 6), ("Gate 2B empty template. No Guinea data, claims or findings. Population begins only after Gate 2D authorisation.", 7)]]
    sheets.append(("README", sheet_xml(rd, [38, 110])))
    # data sheets
    for sname, _idk, fields in reg["sheets"]:
        hdr = [[(f[0], HDR_STYLE[f[2]]) for f in fields]]
        widths = [max(14, min(40, len(f[0]) + 4)) if f[1] != "LONGTEXT" else 50 for f in fields]
        cs = {i + 1: 9 for i, f in enumerate(fields) if f[1] == "DATE"}
        vals = []
        for i, f in enumerate(fields, 1):
            v = field_validation(f, col(i))
            if v:
                vals.append(v)
        last = col(len(fields))
        sheets.append((sname, sheet_xml(hdr, widths, freeze=True, autofilter=f"A1:{last}1", validations=vals, col_styles=cs)))
        defined.append((f"_xlnm._FilterDatabase", len(sheets) - 1, f"'{sname}'!$A$1:${last}$1", True))
    # extra sheets (e.g. DIFFERENCE_TESTS)
    for xname, xhdr, xrows in reg["extra"]:
        rows = [[(h, 3) for h in xhdr]] + [[(v, 0) for v in r] for r in xrows]
        sheets.append((xname, sheet_xml(rows, [14, 26, 90, 90][:len(xhdr)], freeze=True)))
    # DICTIONARY
    drows = [[(h, 3) for h in ["sheet", "field", "type", "requirement", "vocabulary / reference / pattern", "description"]]]
    reqname = {"R": "REQUIRED", "C": "CONDITIONAL", "O": "OPTIONAL", "D": "DERIVED"}
    for sname, _idk, fields in reg["sheets"]:
        for f in fields:
            con = f[3]
            if f[1] in ("ID", "ID_REF") and con in ID_PATTERNS:
                con = ID_PATTERNS[con][0]
            drows.append([(sname, 0), (f[0], 0), (f[1], 0), (reqname[f[2]], 0), (con, 0), (f[4], 7)])
    sheets.append(("DICTIONARY", sheet_xml(drows, [22, 34, 12, 14, 30, 100], freeze=True)))
    # VOCAB (one column per vocabulary) + VOCAB_DEFINITIONS
    vidx = len(sheets)
    maxlen = max(len(V[v]) for v in vocabs)
    vrows = [[(v, 3) for v in vocabs]]
    for i in range(maxlen):
        vrows.append([(V[v][i][0] if i < len(V[v]) else "", 0) for v in vocabs])
    sheets.append(("VOCAB", sheet_xml(vrows, [max(18, len(v) + 2) for v in vocabs], freeze=True)))
    for j, v in enumerate(vocabs, 1):
        defined.append((v, None, f"VOCAB!${col(j)}$2:${col(j)}${len(V[v]) + 1}", False))
    vdrows = [[(h, 3) for h in ["vocabulary", "code", "definition"]]]
    for v in vocabs:
        for code, d in V[v]:
            vdrows.append([(v, 0), (code, 0), (d, 7)])
    sheets.append(("VOCAB_DEFINITIONS", sheet_xml(vdrows, [26, 40, 100], freeze=True)))
    _ = vidx
    return write_xlsx(os.path.join(root, reg["path"]), sheets, defined)


def write_xlsx(path, sheets, defined):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    ct = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">',
          '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>',
          '<Default Extension="xml" ContentType="application/xml"/>',
          '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>',
          '<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>']
    rels = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">']
    wb = [f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<workbook {NS}><bookViews><workbookView activeTab="0"/></bookViews><sheets>']
    files = {}
    for i, (name, xml) in enumerate(sheets, 1):
        files[f"xl/worksheets/sheet{i}.xml"] = xml
        ct.append(f'<Override PartName="/xl/worksheets/sheet{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>')
        rels.append(f'<Relationship Id="rId{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet{i}.xml"/>')
        wb.append(f'<sheet name="{escape(name)}" sheetId="{i}" r:id="rId{i}"/>')
    rels.append(f'<Relationship Id="rId{len(sheets) + 1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>')
    wb.append("</sheets><definedNames>")
    for name, local, ref, hidden in defined:
        la = f' localSheetId="{local}"' if local is not None else ""
        hd = ' hidden="1"' if hidden else ""
        wb.append(f'<definedName name="{name}"{la}{hd}>{escape(ref)}</definedName>')
    wb.append("</definedNames></workbook>")
    ct.append("</Types>")
    rels.append("</Relationships>")
    files["[Content_Types].xml"] = "".join(ct)
    files["_rels/.rels"] = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>')
    files["xl/workbook.xml"] = "".join(wb)
    files["xl/_rels/workbook.xml.rels"] = "".join(rels)
    files["xl/styles.xml"] = STYLES
    order = ["[Content_Types].xml", "_rels/.rels", "xl/workbook.xml", "xl/_rels/workbook.xml.rels", "xl/styles.xml"] + \
            [f"xl/worksheets/sheet{i}.xml" for i in range(1, len(sheets) + 1)]
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for n in order:
            zi = zipfile.ZipInfo(n, FIXED)
            zi.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(zi, files[n].encode("utf-8"))
    return path


# ---------------------------------------------------------------------------
# Markdown data dictionary
# ---------------------------------------------------------------------------
def md_escape(s):
    return str(s).replace("|", "\\|")


def build_markdown(root):
    L = [f"# Register Schema v{SCHEMA_VERSION} — Data Dictionary", "",
         f"**Version:** {SCHEMA_VERSION} (DRAFT, pending Gate 2B approval) · **Last updated:** {SCHEMA_DATE} · **Gate:** 2B · **Decision:** {SCHEMA_DECISION}", "",
         "> **Generated file.** Produced by `00_project/tools/build_register_templates.py`, together with the 11 XLSX templates (one per logical register; Entity/Site has two physical sheets, D-076), from a single schema definition (D-073). Do not edit by hand: change the generator, log a decision, and re-run it. The XLSX workbooks are the authoritative human-facing registers. They contain **no data**.", "",
         "## 1. Conventions", "",
         "- **Requirement codes:**",
         "  - **R** required;",
         "  - **C** conditional (the condition is in the description or the validation rule);",
         "  - **O** optional;",
         "  - **D** derived. Derived fields are populated only by tooling and are never hand-edited (VR-16).",
         "- **Header colours** in the workbooks: dark blue R · mid blue C · light blue O · grey D.",
         "- **Multi-value fields** use `; ` as the separator. **Dates** are stored as dates and displayed DD-MMM-YYYY.",
         "- **Single store:** every material quantitative value is stored once, in the Master Data Register. Other registers reference `DAT-` IDs; the only other numeric attributes are coordinates and WS-27 ordinal scores (VR-17). Assumption values are held in the Assumption Register only when they are not evidence values; an evidenced value is referenced by `DAT-` ID (VR-27).",
         "- **Acceptance vs verification:** `acceptance_status` (PROPOSED / ACCEPTED / REJECTED) records gate approval. `evidence_state` and `confidence` record verification. The vocabularies do not overlap (D-062, VR-04).",
         "- **Supersession:** supersession is recorded in `record_status` (ACTIVE / SUPERSEDED), which is the `status` field of methodology §3. A superseded record keeps its acceptance history (D-071).",
         "- **Fields common to every register:** `acceptance_status`, `acceptance_decision_id`, `acceptance_gate`, `record_status`, `superseded_by`, `created_by`, `created_date`, `last_modified_by`, `last_modified_date`, `notes`.",
         "- **Workbook sheets:** README, the data sheet(s) (header row only), DICTIONARY, VOCAB (lists used for in-cell validation), VOCAB_DEFINITIONS. The contradiction register also has a DIFFERENCE_TESTS guidance sheet.",
         "- **Register count:** 11 logical registers; Entity/Site is implemented as two physical tables/sheets where required by the schema (ORGANISATIONS, SITES; D-076).", "",
         "## 2. ID conventions", "",
         "| Register | ID pattern | Notes |", "|---|---|---|"]
    notes = {"DAT": "WS part = owning Phase A workstream (WS-01 – WS-26)", "SRC": "", "LEAD": "", "CON": "", "GAP": "",
             "PRJ": "", "ENT": "Organisations", "SITE": "Mining / industrial sites (same workbook as ENT)", "ASM": "",
             "GIS": "", "OPP": "WS-27", "ALP": "WS-28", "D": "Decision-log reference"}
    for k, (pat, _) in ID_PATTERNS.items():
        L.append(f"| {k} | `{pat}` | {notes.get(k, '')} |")
    L += ["| Gemini claim | `GEM-NN-C###` | In mission artifacts and the lead register |",
          "| Gemini mission-local source | `GEM-NN-S##` | Mapped to `SRC-` in `mission_local_ids` |",
          "| Gate 1 architecture lead | `GL-NN` | GL-01 – GL-33 |", "",
          "IDs are unique, never reused, and never deleted (VR-01, VR-03).", "",
          "## 3. Relationship model", "",
          "```",
          "                 SRC (sources) ◄──────────── cited by every evidence record",
          "                   ▲",
          "LEAD (leads) ──verified──► DAT  MASTER DATA REGISTER (single store of quantities)",
          "   │                          ▲  ▲  ▲  ▲",
          "   └─unverifiable─► GAP       │  │  │  └── CON (≥2 DAT; governing / range DAT)",
          "                              │  │  └───── ASM (basis_data_ids; never written back)",
          "   PRJ (projects) ──*_data_ids─┘  │",
          "   ENT / SITE ──────*_data_ids────┘",
          "   PRJ ──entity roles──► ENT ;  SITE ──operator/owner──► ENT ;  PRJ ◄──► SITE",
          "   GIS (layers) ──source_ids──► SRC ; features carry PRJ / SITE / OPP IDs",
          "   OPP (WS-27) ──evidence chain──► DAT (+PRJ/SITE/ENT/GIS/ASM)   [frozen at Gate 7 part 1]",
          "   ALP (WS-28) ──opp_id (read-only)──► OPP ; capability evidence ──► SRC (OWNER_SUPPLIED)",
          "```", "",
          "| Register | Workbook | Purpose | Maintained by / authority | Relationship to MDR |", "|---|---|---|---|---|"]
    for r in REGISTERS:
        L.append(f"| {r['title']} | `{r['path']}` | {md_escape(r['purpose'])} | {md_escape(r['maintainer'])} | {md_escape(r['mdr_rel'])} |")
    L += ["", "## 4. Register schemas", ""]
    for n, r in enumerate(REGISTERS, 1):
        L.append(f"### 4.{n} {r['title']}")
        L.append("")
        L.append(f"`{r['path']}` · {md_escape(r['purpose'])}")
        L.append("")
        for sname, _idk, fields in r["sheets"]:
            L.append(f"**Sheet `{sname}`** ({len(fields)} fields)")
            L.append("")
            L.append("| # | Field | Type | Req | Vocabulary / reference | Description |")
            L.append("|---|---|---|---|---|---|")
            for i, f in enumerate(fields, 1):
                con = f[3]
                if f[1] in ("ID", "ID_REF") and con in ID_PATTERNS:
                    con = ID_PATTERNS[con][0]
                L.append(f"| {i} | `{f[0]}` | {f[1]} | {f[2]} | {md_escape(con)} | {md_escape(f[4])} |")
            L.append("")
        for xname, xhdr, xrows in r["extra"]:
            L.append(f"**Sheet `{xname}`.** This is a guidance sheet, not data. Columns: " + ", ".join(f"`{h}`" for h in xhdr) + f". It has {len(xrows)} rows: the D-072 principle (no universal numerical tolerance), the nine comparability tests, and the categorical/status rule. It contains no tolerance values.")
            L.append("")
    L += ["## 5. Controlled vocabularies", ""]
    for v, items in V.items():
        L.append(f"**`{v}`**: " + " · ".join(f"`{c}`" for c, _ in items))
        L.append("")
    L.append("Definitions for every code are in each workbook's VOCAB_DEFINITIONS sheet.")
    L += ["", "## 6. Validation rules", "", "| Rule | Applies to | Rule | Enforcement |", "|---|---|---|---|"]
    for vid, ap, rule, enf in VR:
        L.append(f"| {vid} | {ap} | {md_escape(rule)} | {enf} |")
    L += ["", "**Enforcement:**",
          "- **In-cell:** Excel data validation covers enumerations, ID patterns, dates, numbers, tiers, scores and ISO-code format.",
          "- **Cross-field and cross-register rules** are enforced by a register validator: a CLI or equivalent automated tool (D-075).",
          "- **The validator must exist, be approved and pass before Gate 2D research execution or the first authoritative data entry.** It is implemented as `00_project/tools/validate_registers.py` (D-083), with deterministic tests in `00_project/tools/tests/test_validate_registers.py`.",
          "- **Usage:** `python3 -I 00_project/tools/validate_registers.py --gate <current gate> [--hide-pass] [--format tsv] [--strict]`. The validator is read-only. Each result is PASS / FAIL / WARNING with rule, register, record, field, reason and remediation. Exit code 1 if any FAIL. It must report FAIL = 0 before Gate 2D, before any acceptance decision and before records are used in analysis.",
          "- **Rule IDs:** VR-01 – VR-31, VR-11a and VR-20a; schema checks SCHEMA-01 (headers), SCHEMA-02 (required fields), SCHEMA-03 (vocabularies) and SCHEMA-04 (types); D-077 (no populated data before Gate 2D).",
          "- **The validator must be able to check:** schema · IDs · controlled vocabularies · required fields · duplicate records · provenance · acceptance/evidence compatibility · cross-register references · supersession · units/currency · project status transitions · interconnector status ordering · contradiction references · opportunity evidence eligibility · Alendei participation restrictions.", "",
          "## 7. Gate 2B data-model decisions", "",
          "| Item | Decision |", "|---|---|",
          "| P-018 → D-067 | **Geographic level codes** (`v_geo_level`). The Gate 1 codes are retained (NATIONAL_AGGREGATE, REGIONAL, PREFECTURE, SUBSTATION_NODE, PLANT_SITE, OTHER). Added: LOCALITY, CITY, MINING_SITE, INDUSTRIAL_SITE, PORT, TRANSMISSION_CORRIDOR, INTERCONNECTION, RIVER_BASIN, NEIGHBOURING_COUNTRY, MULTI_COUNTRY_REGION |",
          "| P-019 → D-068 | **Contradiction cause codes** (`v_cause_code`). The Gate 1 causes are retained; METHODOLOGY and SUPERSEDED are added |",
          "| P-020 → D-069 | **Interconnector status.** Five distinct project-register steps: `ic_constructed`, `ic_energised`, `ic_synchronised`, `ic_operational`, `ic_commercially_active`. Each has its own value, evidence sources and date, and the steps are never collapsed (VR-20) |",
          "| P-023 → D-070 | **Exchange rates.** Each rate is its own MDR record (metric_class FX_RATE), with `fx_rate_type`, `fx_source_class` and base/quote currencies. Source preference: CENTRAL_BANK_OFFICIAL → IMF_IFS → WORLD_BANK_WDI → OTHER_DOCUMENTED; TRANSACTION_DOCUMENT applies when a transaction states its own rate. Rate type: PERIOD_AVERAGE for flows, END_OF_PERIOD for stocks, TRANSACTION_STATED where a source transaction states a rate. A conversion is a separate ESTIMATE record citing the original value and the rate record. Cross rates use a direct published rate where available; otherwise they go via USD, with both rates recorded |",
          "| D-071 (APPROVED) | `acceptance_status` = PROPOSED / ACCEPTED / REJECTED. `record_status` = ACTIVE / SUPERSEDED (the methodology §3 `status` field). A record may legitimately be ACCEPTED + SUPERSEDED: accepted as valid for its historical context, later superseded. SUPERSEDED is never an acceptance status. RETIRED/CLOSED is not added because no current register requires it: lead and gap closure are carried by `lead_outcome` and `gap_status` |",
          "| D-072 (FINAL, as modified by owner) | **No universal numerical contradiction tolerance is assumed.** Any difference triggers the comparability tests: definition, date, geography, scope, unit, AC/DC basis, capacity/energy basis, methodology, source precision. A difference is classified as reporting precision **only** when (1) the definitions are comparable, (2) the periods, geography and scope are comparable, and (3) the difference is demonstrably attributable to reporting precision (cause REPORTING_PRECISION). Otherwise the contradiction is preserved, or a range is carried where the sources are comparable and none can reasonably be preferred. No arbitrary percentage tolerance |",
          "| D-073 | The generator script is the single schema definition; the XLSX templates and this dictionary are generated from it |",
          "| P-025 → D-074 (APPROVED WITH BOUNDARY) | Atomic, defined, traceable structured facts may be stored in the MDR (`value_kind` CATEGORICAL, `categorical_type`, `value_text` ≤ 100 characters), with metric, structured value, type, geography, effective period, definition, source, evidence state, confidence and provenance. Examples: whether a regulatory requirement exists; the institution responsible for a defined function; whether a specific licence is required; a categorical technology or status classification. **The MDR must not become a narrative repository** (VR-11a) |",
          "| P-026 → D-075 (APPROVED, strengthened) | The register validator is a **prerequisite for Gate 2D research execution / first authoritative data entry**. A CLI or equivalent automated tool is acceptable; it may be designed and built at Gate 2C (capabilities in §6) |",
          "| D-076 | **11 logical registers.** Entity/Site is implemented as two physical tables/sheets (ORGANISATIONS, SITES) where required by the schema |", ""]
    path = os.path.join(root, "00_project/register_schema.md")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L).rstrip("\n") + "\n")
    return path


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    for r in REGISTERS:
        for _s, _i, fields in r["sheets"]:
            for f in fields:
                if f[1] in ("ENUM", "MULTI_ENUM") and f[3] not in V:
                    raise SystemExit(f"Unknown vocabulary {f[3]} in {r['key']}.{f[0]}")
            names = [f[0] for f in fields]
            if len(names) != len(set(names)):
                raise SystemExit(f"Duplicate field in {r['key']}")
    for r in REGISTERS:
        print("wrote", build_workbook(r, root))
    print("wrote", build_markdown(root))


if __name__ == "__main__":
    main()
