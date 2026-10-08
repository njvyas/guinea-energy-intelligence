# Register Schema v1.1 — Data Dictionary

**Version:** 1.1 (DRAFT, pending Gate 2B approval) · **Last updated:** 08-Oct-2026 · **Gate:** 2B · **Decision:** D-066

> **Generated file.** Produced by `00_project/tools/build_register_templates.py`, together with the 11 XLSX templates (one per logical register; Entity/Site has two physical sheets, D-076), from a single schema definition (D-073). Do not edit by hand: change the generator, log a decision, and re-run it. The XLSX workbooks are the authoritative human-facing registers. They contain **no data**.

## 1. Conventions

- **Requirement codes:**
  - **R** required;
  - **C** conditional (the condition is in the description or the validation rule);
  - **O** optional;
  - **D** derived. Derived fields are populated only by tooling and are never hand-edited (VR-16).
- **Header colours** in the workbooks: dark blue R · mid blue C · light blue O · grey D.
- **Multi-value fields** use `; ` as the separator. **Dates** are stored as dates and displayed DD-MMM-YYYY.
- **Single store:** every material quantitative value is stored once, in the Master Data Register. Other registers reference `DAT-` IDs; the only other numeric attributes are coordinates and WS-27 ordinal scores (VR-17). Assumption values are held in the Assumption Register only when they are not evidence values; an evidenced value is referenced by `DAT-` ID (VR-27).
- **Acceptance vs verification:** `acceptance_status` (PROPOSED / ACCEPTED / REJECTED) records gate approval. `evidence_state` and `confidence` record verification. The vocabularies do not overlap (D-062, VR-04).
- **Supersession:** supersession is recorded in `record_status` (ACTIVE / SUPERSEDED), which is the `status` field of methodology §3. A superseded record keeps its acceptance history (D-071).
- **Fields common to every register:** `acceptance_status`, `acceptance_decision_id`, `acceptance_gate`, `record_status`, `superseded_by`, `created_by`, `created_date`, `last_modified_by`, `last_modified_date`, `notes`.
- **Workbook sheets:** README, the data sheet(s) (header row only), DICTIONARY, VOCAB (lists used for in-cell validation), VOCAB_DEFINITIONS. The contradiction register also has a DIFFERENCE_TESTS guidance sheet.
- **Register count:** 11 logical registers; Entity/Site is implemented as two physical tables/sheets where required by the schema (ORGANISATIONS, SITES; D-076).

## 2. ID conventions

| Register | ID pattern | Notes |
|---|---|---|
| DAT | `DAT-WSNN-NNNNN` | WS part = owning Phase A workstream (WS-01 – WS-26) |
| SRC | `SRC-NNNN` |  |
| LEAD | `LEAD-NNNNN` |  |
| CON | `CON-NNNN` |  |
| GAP | `GAP-NNNN` |  |
| PRJ | `PRJ-NNNN` |  |
| ENT | `ENT-NNNN` | Organisations |
| SITE | `SITE-NNNN` | Mining / industrial sites (same workbook as ENT) |
| ASM | `ASM-NNNN` |  |
| GIS | `GIS-NNNN` |  |
| OPP | `OPP-NNNN` | WS-27 |
| ALP | `ALP-NNNN` | WS-28 |
| D | `D-NNN` | Decision-log reference |
| Gemini claim | `GEM-NN-C###` | In mission artifacts and the lead register |
| Gemini mission-local source | `GEM-NN-S##` | Mapped to `SRC-` in `mission_local_ids` |
| Gate 1 architecture lead | `GL-NN` | GL-01 – GL-33 |

IDs are unique, never reused, and never deleted (VR-01, VR-03).

## 3. Relationship model

```
                 SRC (sources) ◄──────────── cited by every evidence record
                   ▲
LEAD (leads) ──verified──► DAT  MASTER DATA REGISTER (single store of quantities)
   │                          ▲  ▲  ▲  ▲
   └─unverifiable─► GAP       │  │  │  └── CON (≥2 DAT; governing / range DAT)
                              │  │  └───── ASM (basis_data_ids; never written back)
   PRJ (projects) ──*_data_ids─┘  │
   ENT / SITE ──────*_data_ids────┘
   PRJ ──entity roles──► ENT ;  SITE ──operator/owner──► ENT ;  PRJ ◄──► SITE
   GIS (layers) ──source_ids──► SRC ; features carry PRJ / SITE / OPP IDs
   OPP (WS-27) ──evidence chain──► DAT (+PRJ/SITE/ENT/GIS/ASM)   [frozen at Gate 7 part 1]
   ALP (WS-28) ──opp_id (read-only)──► OPP ; capability evidence ──► SRC (OWNER_SUPPLIED)
```

| Register | Workbook | Purpose | Maintained by / authority | Relationship to MDR |
|---|---|---|---|---|
| Master Data Register | `03_evidence/master_data_register/master_data_register.xlsx` | Single store of every material statistic with full provenance (methodology section 3). | Claude Code; approved at Gates 3, 4, 9 | Is the hub |
| Source Register | `03_evidence/source_register/source_register.xlsx` | Bibliographic, access and copyright record of every source (methodology section 4.2). | Claude Code | Every MDR record cites a SRC- ID |
| Lead Register | `03_evidence/lead_register/lead_register.xlsx` | Verification queue for unverified claims (Gemini, discovery notes, challenges, GL-01 - GL-33). Leads are never evidence. | Claude Code; acceptance = discovery acceptance at Gate 2D | A verified lead points to the record it produced; leads are never used as data |
| Contradiction Register | `03_evidence/contradictions/contradiction_register.xlsx` | Conflicting values and their resolution (research_architecture section H; protocol section 10). | Claude Code; material items reviewed by owner at Gate 4 | References two or more DAT- IDs; MDR records carry contradiction_id |
| Data-Gap Register | `03_evidence/data_gaps/data_gap_register.xlsx` | Questions sought but not answered; materiality; next steps; Gate 4 priority reassessment. | Claude Code; reviewed at Gate 4 | Records the absence of an MDR value |
| Project Register | `03_evidence/project_register/project_register.xlsx` | Identity, technology, location and evidenced status of every generation, storage, transmission and infrastructure project. | Claude Code (WS-23 owner) | Status and descriptive attributes only; quantities are DAT- references |
| Entity / Site Register | `03_evidence/entity_register/entity_register.xlsx` | Organisations (type, origin, Guinea-presence class) and mining/industrial sites. | Claude Code (WS-25; WS-11 - WS-14 owners) | Demand, captive MW, fuel cost are DAT- references |
| Assumption Register | `03_evidence/assumption_register/assumption_register.xlsx` | Modelling assumptions with basis and sensitivity; never written back to the MDR as data. | Claude Code; approved at Gates 6-7 | Cites DAT- basis or documented method |
| GIS Layer Catalogue | `05_gis/gis_layer_catalogue.xlsx` | Provenance of every GIS layer: source, date, licence, CRS, processing, constraint class. | Claude Code | Cites SRC- IDs; features carry PRJ-/SITE-/OPP- IDs |
| Opportunity Register (WS-27) | `06_opportunities/candidate_opportunities/opportunity_register.xlsx` | WS-27 country opportunities (Alendei-neutral): evidence chain, fatal-flaw screen, scores, frozen attractiveness rating. Contains no Alendei fields. | Claude Code; User + ChatGPT approve freeze at Gate 7 part 1 | Evidence chain cites DAT-/PRJ-/ENT-/ASM- IDs |
| Alendei Participation Register (WS-28) | `06_opportunities/alendei_role/alendei_participation_register.xlsx` | WS-28 Alendei roles, capability gaps, partners, Tier 1-4 classification for frozen WS-27 opportunities. | Claude Code; capability evidence supplied only by the user; User + ChatGPT approve | References OPP- IDs read-only; holds no Guinea statistics |

## 4. Register schemas

### 4.1 Master Data Register

`03_evidence/master_data_register/master_data_register.xlsx` · Single store of every material statistic with full provenance (methodology section 3).

**Sheet `MDR`** (74 fields)

| # | Field | Type | Req | Vocabulary / reference | Description |
|---|---|---|---|---|---|
| 1 | `data_id` | ID | R | DAT-WSNN-NNNNN | Unique ID DAT-WSNN-NNNNN; WS part must equal `workstream` (VR-01). |
| 2 | `workstream` | ENUM | R | v_workstream_phase_a | Owning Phase A workstream (WS-01 - WS-26). |
| 3 | `lead_id` | ID_LIST | O | LEAD | Originating lead(s). |
| 4 | `subject_type` | ENUM | R | v_subject_type | What the value describes. |
| 5 | `subject_id` | ID_REF | C | PRJ\|SITE\|ENT | Required when subject_type is PROJECT, SITE or ENTITY. |
| 6 | `metric` | TEXT | R |  | Metric name. |
| 7 | `metric_class` | ENUM | R | v_metric_class | Metric class. |
| 8 | `metric_definition` | LONGTEXT | R |  | Precise definition per methodology section 5 / protocol section 8. |
| 9 | `energy_class` | ENUM | R | v_energy_class | Capacity/energy/demand class; NOT_APPLICABLE for other metrics (VR-13). |
| 10 | `ac_dc_basis` | ENUM | R | v_acdc | Required basis for PV capacity (VR-13). |
| 11 | `value_kind` | ENUM | R | v_value_kind | NUMERIC or CATEGORICAL (D-074 boundary). |
| 12 | `value` | NUMBER | C |  | Numeric value as reported (VR-11). |
| 13 | `value_low` | NUMBER | C |  | Low bound for ranges (VR-11). |
| 14 | `value_high` | NUMBER | C |  | High bound for ranges (VR-11). |
| 15 | `value_text` | SHORTTEXT | C |  | Structured categorical value (max 100 characters) when value_kind = CATEGORICAL; format per categorical_type (D-074, VR-11a). |
| 16 | `categorical_type` | ENUM | C | v_categorical_type | Required when value_kind = CATEGORICAL (D-074). |
| 17 | `value_qualifier` | ENUM | R | v_value_qualifier | Exact, approximate, range, bound. |
| 18 | `unit` | ENUM | C | v_unit | Required for NUMERIC (VR-12). |
| 19 | `unit_note` | TEXT | O |  | Original unit label as reported (e.g. MWp). |
| 20 | `currency` | ISO4217 | C |  | ISO 4217 code; required for currency-based units (VR-12). |
| 21 | `price_basis` | ENUM | C | v_price_basis | Required when currency is set (VR-12). |
| 22 | `price_base_year` | YEAR | C |  | Required when price_basis = REAL (P-024 governs the base year). |
| 23 | `conversion_type` | ENUM | R | v_conversion_type | NONE unless derived (VR-14). |
| 24 | `input_data_ids` | ID_LIST | C | DAT | Inputs for ESTIMATE / derived records (VR-06, VR-14). |
| 25 | `assumption_ids` | ID_LIST | C | ASM | Assumptions used by an ESTIMATE. |
| 26 | `estimate_method` | LONGTEXT | C |  | Required for ESTIMATE (VR-06). |
| 27 | `fx_rate_type` | ENUM | C | v_fx_rate_type | Required for FX_RATE records and FX conversions (VR-14, D-070). |
| 28 | `fx_source_class` | ENUM | C | v_fx_source_class | Required for FX_RATE records (VR-14, D-070). |
| 29 | `fx_base_currency` | ISO4217 | C |  | FX_RATE records: base currency (one unit of). |
| 30 | `fx_quote_currency` | ISO4217 | C |  | FX_RATE records: quote currency. |
| 31 | `geography_name` | TEXT | R |  | Name of the geographic unit/site as given in the source. |
| 32 | `geo_level` | ENUM | R | v_geo_level | Geographic level (D-067). |
| 33 | `country_iso3` | ISO3 | R |  | ISO 3166-1 alpha-3 code of the country the value relates to. |
| 34 | `period_type` | ENUM | R | v_period_type | Period the value describes. |
| 35 | `period_start` | DATE | R |  | Start (or single date) of the period described - not the publication date. |
| 36 | `period_end` | DATE | C |  | End of period where applicable. |
| 37 | `season_label` | TEXT | C |  | Season definition as per source; required for SEASONAL_DEPENDABLE (VR-15). |
| 38 | `temporal_class` | ENUM | R | v_temporal_class | Protocol section 6.2. |
| 39 | `source_id` | ID_REF | C | SRC-NNNN | Required unless evidence_state = ESTIMATE (VR-06). |
| 40 | `source_title` | DERIVED | D | SRC | Lookup from source register (methodology section 3). |
| 41 | `publisher` | DERIVED | D | SRC | Lookup from source register. |
| 42 | `source_publication_date` | DERIVED | D | SRC | Lookup from source register. |
| 43 | `source_url_or_reference` | DERIVED | D | SRC | Lookup from source register. |
| 44 | `source_tier` | DERIVED | D | SRC | Lookup from source register (tier assigned there). |
| 45 | `discloser_independence` | DERIVED | D | SRC | Lookup from source register. |
| 46 | `page_table_section` | TEXT | C |  | Exact location in source; required for VERIFIED (VR-07). |
| 47 | `access_date` | DATE | C |  | Date the value was read; required with source_id. |
| 48 | `evidence_state` | ENUM | R | v_evidence_state_register | Verification state (methodology section 2.2). |
| 49 | `confidence` | ENUM | R | v_confidence | Confidence per evidence state; may be lower, never higher (VR-08). |
| 50 | `quality_source_quality` | ENUM | R | v_quality | Quality dimension: source quality (methodology section 2.1; may only lower confidence). |
| 51 | `quality_recency` | ENUM | R | v_quality | Quality dimension: recency (methodology section 2.1; may only lower confidence). |
| 52 | `quality_cross_source_agreement` | ENUM | R | v_quality | Quality dimension: cross source agreement (methodology section 2.1; may only lower confidence). |
| 53 | `quality_methodological_quality` | ENUM | R | v_quality | Quality dimension: methodological quality (methodology section 2.1; may only lower confidence). |
| 54 | `quality_completeness` | ENUM | R | v_quality | Quality dimension: completeness (methodology section 2.1; may only lower confidence). |
| 55 | `quality_definition_consistency` | ENUM | R | v_quality | Quality dimension: definition consistency (methodology section 2.1; may only lower confidence). |
| 56 | `cross_check_status` | ENUM | R | v_cross_check |  |
| 57 | `cross_check_source_ids` | ID_LIST | C | SRC | Independent sources; required for CORROBORATED (VR-09). |
| 58 | `cross_check_data_ids` | ID_LIST | O | DAT | Related MDR records compared. |
| 59 | `contradiction_status` | ENUM | R | v_contradiction_status |  |
| 60 | `contradiction_id` | ID_REF | C | CON-NNNN | Required when contradiction_status is not NONE. |
| 61 | `revalidation_category` | ENUM | R | v_revalidation | Event-based revalidation trigger (protocol section 6.4; no time expiry). |
| 62 | `last_revalidated_date` | DATE | O |  |  |
| 63 | `verified_by` | ENUM | C | v_actor | Required for VERIFIED/CORROBORATED. |
| 64 | `verified_date` | DATE | C |  | Required for VERIFIED/CORROBORATED. |
| 65 | `acceptance_status` | ENUM | R | v_acceptance_status | Gate approval status (D-062). Distinct from evidence_state/confidence; vocabularies do not overlap. |
| 66 | `acceptance_decision_id` | ID_REF | C | D-NNN | Decision-log ID; required when ACCEPTED or REJECTED (VR-02). |
| 67 | `acceptance_gate` | ENUM | C | v_gate | Gate of acceptance/rejection; required when ACCEPTED or REJECTED (VR-02). |
| 68 | `record_status` | ENUM | R | v_record_status | Methodology section 3 `status`: ACTIVE or SUPERSEDED. Records are never deleted (VR-03, D-071). |
| 69 | `superseded_by` | ID_REF | C | DAT-WSNN-NNNNN | Replacing record ID; required when SUPERSEDED (VR-03). |
| 70 | `created_by` | ENUM | R | v_actor | Who created the record. |
| 71 | `created_date` | DATE | R |  | DD-MMM-YYYY. |
| 72 | `last_modified_by` | ENUM | O | v_actor |  |
| 73 | `last_modified_date` | DATE | O |  | DD-MMM-YYYY. |
| 74 | `notes` | LONGTEXT | O |  | Caveats; never a substitute for a structured field. |

### 4.2 Source Register

`03_evidence/source_register/source_register.xlsx` · Bibliographic, access and copyright record of every source (methodology section 4.2).

**Sheet `SOURCES`** (41 fields)

| # | Field | Type | Req | Vocabulary / reference | Description |
|---|---|---|---|---|---|
| 1 | `source_id` | ID | R | SRC-NNNN | Unique ID SRC-NNNN. |
| 2 | `title_original` | TEXT | R |  | Exact title, original language. |
| 3 | `title_translation` | TEXT | O |  | Translation, marked as such. |
| 4 | `publisher` | TEXT | R |  | Issuing organisation. |
| 5 | `author` | TEXT | O |  |  |
| 6 | `document_type` | ENUM | R | v_document_type | Protocol section 4.4 categories. |
| 7 | `language` | TEXT | R |  | ISO 639-1 code (e.g. fr, en). |
| 8 | `publication_date` | DATE | C |  | Required unless publication_date_precision = UNDATED. |
| 9 | `publication_date_precision` | ENUM | R | v_date_precision |  |
| 10 | `edition_version` | TEXT | O |  | Edition, revision or dataset version. |
| 11 | `url` | TEXT | C |  | URL; url or persistent_reference required (VR-20a). |
| 12 | `persistent_reference` | TEXT | C |  | DOI, document number, archive reference. |
| 13 | `access_date` | DATE | R |  | Date first accessed. |
| 14 | `access_status` | ENUM | R | v_access_status |  |
| 15 | `retrieval_status` | ENUM | R | v_retrieval_status | CANDIDATE_SOURCE until retrieved (evidence state of a source). |
| 16 | `source_tier` | TIER | R |  | 1-6 per the authoritative hierarchy (D-082; methodology section 1), assigned by Claude (not adopted from Gemini). Tier 6 is never evidence. Media/trade press: tier 5 with document_type NEWS_ARTICLE/TRADE_PRESS - secondary reporting, not an evidence tier (D-086, VR-30). |
| 17 | `discloser_independence` | ENUM | R | v_discloser |  |
| 18 | `origin` | ENUM | R | v_origin | How the source entered the project. |
| 19 | `origin_ref` | TEXT | C |  | Mission ID + artifact version, discovery note or decision ID. |
| 20 | `mission_local_ids` | TEXT | O |  | Gemini mission-local IDs mapped to this source (GEM-NN-S##; '; '-separated). |
| 21 | `supersedes_source_id` | ID_REF | O | SRC-NNNN | Earlier edition this source supersedes. |
| 22 | `reliability_flag` | ENUM | R | v_reliability_flag | Protocol section 17. |
| 23 | `reliability_note` | LONGTEXT | C |  | Required when UNDER_REVIEW or UNRELIABLE. |
| 24 | `relevant_pages_sections` | LONGTEXT | O |  | Pages/sections/tables relied on (methodology section 4.2). |
| 25 | `evidence_extracted_summary` | LONGTEXT | O |  | Summary of what was taken (methodology section 4.2). |
| 26 | `evidence_data_ids` | DERIVED | D | DAT | Lookup: MDR records citing this source. |
| 27 | `access_copyright_note` | LONGTEXT | R |  | Licence/copyright status and redistribution restrictions. |
| 28 | `copyright_basis` | ENUM | R | v_copyright_basis |  |
| 29 | `local_copy_status` | ENUM | R | v_local_copy | Default NOT_STORED_REFERENCE_ONLY (VR-21). |
| 30 | `local_path` | TEXT | C |  | Required when STORED. |
| 31 | `search_path_log` | LONGTEXT | C |  | Required when CITATION_NOT_FOUND or UNAVAILABLE (protocol section 17). |
| 32 | `acceptance_status` | ENUM | R | v_acceptance_status | Gate approval status (D-062). Distinct from evidence_state/confidence; vocabularies do not overlap. |
| 33 | `acceptance_decision_id` | ID_REF | C | D-NNN | Decision-log ID; required when ACCEPTED or REJECTED (VR-02). |
| 34 | `acceptance_gate` | ENUM | C | v_gate | Gate of acceptance/rejection; required when ACCEPTED or REJECTED (VR-02). |
| 35 | `record_status` | ENUM | R | v_record_status | Methodology section 3 `status`: ACTIVE or SUPERSEDED. Records are never deleted (VR-03, D-071). |
| 36 | `superseded_by` | ID_REF | C | SRC-NNNN | Replacing record ID; required when SUPERSEDED (VR-03). |
| 37 | `created_by` | ENUM | R | v_actor | Who created the record. |
| 38 | `created_date` | DATE | R |  | DD-MMM-YYYY. |
| 39 | `last_modified_by` | ENUM | O | v_actor |  |
| 40 | `last_modified_date` | DATE | O |  | DD-MMM-YYYY. |
| 41 | `notes` | LONGTEXT | O |  | Caveats; never a substitute for a structured field. |

### 4.3 Lead Register

`03_evidence/lead_register/lead_register.xlsx` · Verification queue for unverified claims (Gemini, discovery notes, challenges, GL-01 - GL-33). Leads are never evidence.

**Sheet `LEADS`** (36 fields)

| # | Field | Type | Req | Vocabulary / reference | Description |
|---|---|---|---|---|---|
| 1 | `lead_id` | ID | R | LEAD-NNNNN | Unique ID LEAD-NNNNN. |
| 2 | `origin` | ENUM | R | v_origin | Gemini mission, architecture challenge, Claude discovery, owner/ChatGPT challenge. |
| 3 | `origin_ref` | TEXT | R |  | Mission ID + artifact version / discovery note / decision ID. |
| 4 | `claim_id` | TEXT | C |  | GEM-NN-C### for missions; GL-NN for architecture leads. |
| 5 | `artifact_file` | TEXT | C |  | Deposited artifact path (Gemini origins). |
| 6 | `artifact_sha256` | TEXT | C |  | 64-hex fingerprint of the artifact. |
| 7 | `claim_text` | LONGTEXT | R |  | Claim verbatim. Never edited. |
| 8 | `claim_type` | ENUM | R | v_claim_type |  |
| 9 | `workstream_primary` | ENUM | R | v_workstream |  |
| 10 | `workstreams_other` | TEXT | O |  | Other WS IDs ('; '-separated). |
| 11 | `research_question` | TEXT | O |  | Charter question, e.g. WS-05 Q2. |
| 12 | `question_priority` | DERIVED | D | charter | Lookup of charter planning priority (not confidence). |
| 13 | `temporal_class` | ENUM | O | v_temporal_class |  |
| 14 | `geo_level` | ENUM | O | v_geo_level |  |
| 15 | `cited_source_as_stated` | LONGTEXT | C |  | Citation exactly as given by the origin. |
| 16 | `cited_source_id` | ID_REF | C | SRC-NNNN | Registered source for the citation. |
| 17 | `origin_self_confidence` | ENUM | O | v_self_confidence | Origin's self-assessed confidence - advisory only. |
| 18 | `evidence_state` | ENUM | R | v_evidence_state_lead | Always RAW_LEAD (VR-18). |
| 19 | `lead_outcome` | ENUM | R | v_lead_outcome | Verification outcome (D-058). |
| 20 | `outcome_reason` | ENUM | C | v_outcome_reason | Required for UNSUPPORTED, CONTRADICTED, NOT_VERIFIABLE, PARTLY_VERIFIED. |
| 21 | `search_path_log` | LONGTEXT | C |  | Required for UNSUPPORTED / NOT_VERIFIABLE (protocol section 17). |
| 22 | `resulting_record_ids` | ID_LIST | C | DAT\|PRJ\|ENT\|SITE | Required for VERIFIED / PARTLY_VERIFIED. |
| 23 | `contradiction_id` | ID_REF | C | CON-NNNN | For CONTRADICTED where a CON row exists. |
| 24 | `gap_id` | ID_REF | C | GAP-NNNN | For NOT_VERIFIABLE. |
| 25 | `checked_by` | ENUM | C | v_actor | Required once outcome is not NOT_YET_CHECKED. |
| 26 | `checked_date` | DATE | C |  |  |
| 27 | `acceptance_status` | ENUM | R | v_acceptance_status | Gate approval status (D-062). Distinct from evidence_state/confidence; vocabularies do not overlap. |
| 28 | `acceptance_decision_id` | ID_REF | C | D-NNN | Decision-log ID; required when ACCEPTED or REJECTED (VR-02). |
| 29 | `acceptance_gate` | ENUM | C | v_gate | Gate of acceptance/rejection; required when ACCEPTED or REJECTED (VR-02). |
| 30 | `record_status` | ENUM | R | v_record_status | Methodology section 3 `status`: ACTIVE or SUPERSEDED. Records are never deleted (VR-03, D-071). |
| 31 | `superseded_by` | ID_REF | C | LEAD-NNNNN | Replacing record ID; required when SUPERSEDED (VR-03). |
| 32 | `created_by` | ENUM | R | v_actor | Who created the record. |
| 33 | `created_date` | DATE | R |  | DD-MMM-YYYY. |
| 34 | `last_modified_by` | ENUM | O | v_actor |  |
| 35 | `last_modified_date` | DATE | O |  | DD-MMM-YYYY. |
| 36 | `notes` | LONGTEXT | O |  | Caveats; never a substitute for a structured field. |

### 4.4 Contradiction Register

`03_evidence/contradictions/contradiction_register.xlsx` · Conflicting values and their resolution (research_architecture section H; protocol section 10).

**Sheet `CONTRADICTIONS`** (35 fields)

| # | Field | Type | Req | Vocabulary / reference | Description |
|---|---|---|---|---|---|
| 1 | `con_id` | ID | R | CON-NNNN | Unique ID CON-NNNN. |
| 2 | `workstream` | ENUM | R | v_workstream_phase_a |  |
| 3 | `metric` | TEXT | R |  | Metric in conflict. |
| 4 | `metric_class` | ENUM | R | v_metric_class |  |
| 5 | `subject_type` | ENUM | R | v_subject_type |  |
| 6 | `subject_id` | ID_REF | C | PRJ\|SITE\|ENT |  |
| 7 | `geography_name` | TEXT | R |  |  |
| 8 | `geo_level` | ENUM | R | v_geo_level |  |
| 9 | `period_description` | TEXT | R |  | Period(s) of the conflicting values. |
| 10 | `data_ids` | ID_LIST | R | DAT | Two or more conflicting MDR records (VR-26). Values are not copied here. |
| 11 | `diagnostic_tests_completed` | MULTI_ENUM | R | v_difference_test | D-072 comparability tests completed ('; '-separated); see DIFFERENCE_TESTS sheet. |
| 12 | `precision_attribution` | ENUM | R | v_precision_attribution | D-072 three-condition test result. |
| 13 | `precision_justification` | LONGTEXT | C |  | Required when ATTRIBUTABLE: evidence that the difference is due to reporting precision. |
| 14 | `cause_code` | ENUM | R | v_cause_code | Primary cause (D-068). |
| 15 | `cause_code_secondary` | ENUM | O | v_cause_code |  |
| 16 | `cause_notes` | LONGTEXT | R |  | Diagnosis. |
| 17 | `outcome` | ENUM | R | v_contradiction_outcome | Gate 1 outcome set (research_architecture section H). |
| 18 | `governing_data_id` | ID_REF | C | DAT-WSNN-NNNNN | Required for RESOLVED-HIERARCHY / RESOLVED-ERROR. |
| 19 | `range_data_id` | ID_REF | C | DAT-WSNN-NNNNN | MDR record holding the carried range; required for RANGE-CARRIED. |
| 20 | `reasoning` | LONGTEXT | R |  | Why the outcome was chosen. Never silent. |
| 21 | `materiality` | ENUM | R | v_materiality |  |
| 22 | `escalated` | ENUM | R | v_yes_no | MATERIAL + OPEN/RANGE-CARRIED must be YES. |
| 23 | `escalation_gate` | ENUM | C | v_gate | Required when escalated = YES. |
| 24 | `resolved_by` | ENUM | C | v_actor | Required for RESOLVED-*. |
| 25 | `resolved_date` | DATE | C |  | Required for RESOLVED-*. |
| 26 | `acceptance_status` | ENUM | R | v_acceptance_status | Gate approval status (D-062). Distinct from evidence_state/confidence; vocabularies do not overlap. |
| 27 | `acceptance_decision_id` | ID_REF | C | D-NNN | Decision-log ID; required when ACCEPTED or REJECTED (VR-02). |
| 28 | `acceptance_gate` | ENUM | C | v_gate | Gate of acceptance/rejection; required when ACCEPTED or REJECTED (VR-02). |
| 29 | `record_status` | ENUM | R | v_record_status | Methodology section 3 `status`: ACTIVE or SUPERSEDED. Records are never deleted (VR-03, D-071). |
| 30 | `superseded_by` | ID_REF | C | CON-NNNN | Replacing record ID; required when SUPERSEDED (VR-03). |
| 31 | `created_by` | ENUM | R | v_actor | Who created the record. |
| 32 | `created_date` | DATE | R |  | DD-MMM-YYYY. |
| 33 | `last_modified_by` | ENUM | O | v_actor |  |
| 34 | `last_modified_date` | DATE | O |  | DD-MMM-YYYY. |
| 35 | `notes` | LONGTEXT | O |  | Caveats; never a substitute for a structured field. |

**Sheet `DIFFERENCE_TESTS`.** This is a guidance sheet, not data. Columns: `step`, `test`, `question / rule`, `outcome guidance`. It has 11 rows: the D-072 principle (no universal numerical tolerance), the nine comparability tests, and the categorical/status rule. It contains no tolerance values.

### 4.5 Data-Gap Register

`03_evidence/data_gaps/data_gap_register.xlsx` · Questions sought but not answered; materiality; next steps; Gate 4 priority reassessment.

**Sheet `DATA_GAPS`** (34 fields)

| # | Field | Type | Req | Vocabulary / reference | Description |
|---|---|---|---|---|---|
| 1 | `gap_id` | ID | R | GAP-NNNN | Unique ID GAP-NNNN. |
| 2 | `workstream` | ENUM | R | v_workstream_phase_a |  |
| 3 | `research_question` | TEXT | R |  | Charter question, e.g. WS-09 Q4, or NEW. |
| 4 | `question_priority_original` | DERIVED | D | charter | Charter planning priority at Gate 1. |
| 5 | `question_priority_current` | ENUM | R | v_priority | Current planning priority; changes only at Gate 4 (methodology section 12). |
| 6 | `priority_change_reason` | LONGTEXT | C |  | Required when current differs from original. |
| 7 | `priority_change_decision_id` | ID_REF | C | D-NNN | Required when current differs from original (VR-25). |
| 8 | `gap_description` | LONGTEXT | R |  | What is missing. |
| 9 | `metric_class` | ENUM | O | v_metric_class |  |
| 10 | `subject_type` | ENUM | O | v_subject_type |  |
| 11 | `subject_id` | ID_REF | O | PRJ\|SITE\|ENT |  |
| 12 | `geography_name` | TEXT | O |  |  |
| 13 | `geo_level` | ENUM | O | v_geo_level |  |
| 14 | `period_description` | TEXT | O |  |  |
| 15 | `materiality` | ENUM | R | v_materiality | Evidence-based materiality (distinct from planning priority). |
| 16 | `sources_tried_ids` | ID_LIST | O | SRC |  |
| 17 | `search_path_log` | LONGTEXT | R |  | Standard search path followed (protocol section 17). |
| 18 | `access_limitations` | LONGTEXT | O |  |  |
| 19 | `lead_ids` | ID_LIST | O | LEAD |  |
| 20 | `next_step` | LONGTEXT | R |  |  |
| 21 | `proposed_mission` | TEXT | O |  | GEM-NN or NEW (new missions need a decision-log entry). |
| 22 | `gap_status` | ENUM | R | v_gap_status |  |
| 23 | `filled_by_data_ids` | ID_LIST | C | DAT | Required for FILLED / PARTLY_FILLED. |
| 24 | `evidence_state` | ENUM | R | v_evidence_state_gap | Always DATA_GAP. |
| 25 | `acceptance_status` | ENUM | R | v_acceptance_status | Gate approval status (D-062). Distinct from evidence_state/confidence; vocabularies do not overlap. |
| 26 | `acceptance_decision_id` | ID_REF | C | D-NNN | Decision-log ID; required when ACCEPTED or REJECTED (VR-02). |
| 27 | `acceptance_gate` | ENUM | C | v_gate | Gate of acceptance/rejection; required when ACCEPTED or REJECTED (VR-02). |
| 28 | `record_status` | ENUM | R | v_record_status | Methodology section 3 `status`: ACTIVE or SUPERSEDED. Records are never deleted (VR-03, D-071). |
| 29 | `superseded_by` | ID_REF | C | GAP-NNNN | Replacing record ID; required when SUPERSEDED (VR-03). |
| 30 | `created_by` | ENUM | R | v_actor | Who created the record. |
| 31 | `created_date` | DATE | R |  | DD-MMM-YYYY. |
| 32 | `last_modified_by` | ENUM | O | v_actor |  |
| 33 | `last_modified_date` | DATE | O |  | DD-MMM-YYYY. |
| 34 | `notes` | LONGTEXT | O |  | Caveats; never a substitute for a structured field. |

### 4.6 Project Register

`03_evidence/project_register/project_register.xlsx` · Identity, technology, location and evidenced status of every generation, storage, transmission and infrastructure project.

**Sheet `PROJECTS`** (78 fields)

| # | Field | Type | Req | Vocabulary / reference | Description |
|---|---|---|---|---|---|
| 1 | `project_id` | ID | R | PRJ-NNNN | Unique ID PRJ-NNNN. |
| 2 | `project_name` | TEXT | R |  | Standardised name. |
| 3 | `alternative_names` | TEXT | O |  | Name history / aliases ('; '-separated) for de-duplication. |
| 4 | `parent_project_id` | ID_REF | O | PRJ-NNNN | Parent for multi-component projects (each component has its own status). |
| 5 | `component_type` | ENUM | R | v_component_type |  |
| 6 | `technology` | ENUM | R | v_technology | Technology-neutral list. |
| 7 | `hybrid_components` | MULTI_ENUM | C | v_technology | Required when technology = HYBRID ('; '-separated). |
| 8 | `workstream_primary` | ENUM | R | v_workstream_phase_a |  |
| 9 | `workstreams_other` | TEXT | O |  |  |
| 10 | `geography_name` | TEXT | R |  | Name of the geographic unit/site as given in the source. |
| 11 | `geo_level` | ENUM | R | v_geo_level | Geographic level (D-067). |
| 12 | `country_iso3` | ISO3 | R |  | ISO 3166-1 alpha-3 code of the country the value relates to. |
| 13 | `latitude` | NUMBER | O | LAT | Decimal degrees, -90 to 90. |
| 14 | `longitude` | NUMBER | O | LON | Decimal degrees, -180 to 180. |
| 15 | `crs` | TEXT | C |  | Required with coordinates; storage CRS EPSG:4326 (research_architecture section L.3). |
| 16 | `coordinate_precision` | ENUM | C | v_coord_precision | Required with coordinates. |
| 17 | `coordinate_source_id` | ID_REF | C | SRC-NNNN | Source of coordinates; required with coordinates. |
| 18 | `basin_river` | TEXT | O |  | Hydro: river/basin as stated in source. |
| 19 | `lifecycle_stage` | ENUM | R | v_lifecycle | Methodology section 6.1; highest stage with qualifying evidence. |
| 20 | `lifecycle_evidence_type` | ENUM | R | v_lifecycle_evidence | Type of evidence supporting the stage; must be consistent with the stage (VR-19). |
| 21 | `lifecycle_evidence_source_ids` | ID_LIST | R | SRC | Sources evidencing the stage. |
| 22 | `progress_condition` | ENUM | R | v_progress | Methodology section 6.2. STALLED requires positive evidence; silence = UNVERIFIED (VR-19). |
| 23 | `progress_evidence_source_ids` | ID_LIST | C | SRC | Required for DELAYED and STALLED. |
| 24 | `status_summary` | LONGTEXT | R |  | Methodology section 6.3 status_evidence: the specific evidence for stage and condition. |
| 25 | `last_evidence_date` | DATE | R |  | Date of most recent evidence of activity. |
| 26 | `status_assessed_date` | DATE | R |  | Date status last assessed (status as of). |
| 27 | `status_confidence` | ENUM | R | v_confidence | Confidence in the status assessment. |
| 28 | `cod_target_date` | DATE | O |  | Published target COD. |
| 29 | `cod_target_source_id` | ID_REF | C | SRC-NNNN | Required with cod_target_date. |
| 30 | `cod_actual_date` | DATE | O |  | Actual COD. |
| 31 | `cod_actual_source_id` | ID_REF | C | SRC-NNNN | Required with cod_actual_date. |
| 32 | `ic_constructed` | ENUM | C | v_ic_step | Interconnector/line step 'constructed' (D-069). Required for INTERCONNECTOR. |
| 33 | `ic_constructed_evidence_source_ids` | ID_LIST | C | SRC | Required when ic_constructed = YES. |
| 34 | `ic_constructed_date` | DATE | O |  | Date the step was evidenced/occurred. |
| 35 | `ic_energised` | ENUM | C | v_ic_step | Interconnector/line step 'energised' (D-069). Required for INTERCONNECTOR. |
| 36 | `ic_energised_evidence_source_ids` | ID_LIST | C | SRC | Required when ic_energised = YES. |
| 37 | `ic_energised_date` | DATE | O |  | Date the step was evidenced/occurred. |
| 38 | `ic_synchronised` | ENUM | C | v_ic_step | Interconnector/line step 'synchronised' (D-069). Required for INTERCONNECTOR. |
| 39 | `ic_synchronised_evidence_source_ids` | ID_LIST | C | SRC | Required when ic_synchronised = YES. |
| 40 | `ic_synchronised_date` | DATE | O |  | Date the step was evidenced/occurred. |
| 41 | `ic_operational` | ENUM | C | v_ic_step | Interconnector/line step 'operational' (D-069). Required for INTERCONNECTOR. |
| 42 | `ic_operational_evidence_source_ids` | ID_LIST | C | SRC | Required when ic_operational = YES. |
| 43 | `ic_operational_date` | DATE | O |  | Date the step was evidenced/occurred. |
| 44 | `ic_commercially_active` | ENUM | C | v_ic_step | Interconnector/line step 'commercially active' (D-069). Required for INTERCONNECTOR. |
| 45 | `ic_commercially_active_evidence_source_ids` | ID_LIST | C | SRC | Required when ic_commercially_active = YES. |
| 46 | `ic_commercially_active_date` | DATE | O |  | Date the step was evidenced/occurred. |
| 47 | `capacity_data_ids` | ID_LIST | O | DAT | Capacity values (all classes) - MDR references only (VR-17). |
| 48 | `energy_data_ids` | ID_LIST | O | DAT | Energy values - MDR references. |
| 49 | `seasonal_output_data_ids` | ID_LIST | O | DAT | Seasonal dependable output (hydro mandatory) - MDR references. |
| 50 | `cost_data_ids` | ID_LIST | O | DAT | Cost/financing values - MDR references. |
| 51 | `contract_term_data_ids` | ID_LIST | O | DAT | Quantitative contract terms - MDR references. |
| 52 | `other_data_ids` | ID_LIST | O | DAT |  |
| 53 | `sponsor_entity_ids` | ID_LIST | O | ENT |  |
| 54 | `owner_entity_ids` | ID_LIST | O | ENT |  |
| 55 | `developer_entity_ids` | ID_LIST | O | ENT |  |
| 56 | `epc_entity_ids` | ID_LIST | O | ENT |  |
| 57 | `oem_entity_ids` | ID_LIST | O | ENT |  |
| 58 | `financier_entity_ids` | ID_LIST | O | ENT |  |
| 59 | `offtaker_entity_ids` | ID_LIST | O | ENT |  |
| 60 | `operator_entity_ids` | ID_LIST | O | ENT |  |
| 61 | `offtaker_type` | ENUM | O | v_offtaker_type |  |
| 62 | `ppa_publicly_documented` | ENUM | O | v_yes_no_unclear |  |
| 63 | `ppa_source_ids` | ID_LIST | C | SRC | Required when ppa_publicly_documented = YES. |
| 64 | `evacuation_project_ids` | ID_LIST | O | PRJ | Evacuation line/substation projects. |
| 65 | `related_site_ids` | ID_LIST | O | SITE |  |
| 66 | `duplicate_of_project_id` | ID_REF | O | PRJ-NNNN | If a re-announcement of another project. |
| 67 | `dedup_basis` | LONGTEXT | C |  | Location/capacity/sponsor basis; required with duplicate_of_project_id. |
| 68 | `lead_ids` | ID_LIST | O | LEAD |  |
| 69 | `acceptance_status` | ENUM | R | v_acceptance_status | Gate approval status (D-062). Distinct from evidence_state/confidence; vocabularies do not overlap. |
| 70 | `acceptance_decision_id` | ID_REF | C | D-NNN | Decision-log ID; required when ACCEPTED or REJECTED (VR-02). |
| 71 | `acceptance_gate` | ENUM | C | v_gate | Gate of acceptance/rejection; required when ACCEPTED or REJECTED (VR-02). |
| 72 | `record_status` | ENUM | R | v_record_status | Methodology section 3 `status`: ACTIVE or SUPERSEDED. Records are never deleted (VR-03, D-071). |
| 73 | `superseded_by` | ID_REF | C | PRJ-NNNN | Replacing record ID; required when SUPERSEDED (VR-03). |
| 74 | `created_by` | ENUM | R | v_actor | Who created the record. |
| 75 | `created_date` | DATE | R |  | DD-MMM-YYYY. |
| 76 | `last_modified_by` | ENUM | O | v_actor |  |
| 77 | `last_modified_date` | DATE | O |  | DD-MMM-YYYY. |
| 78 | `notes` | LONGTEXT | O |  | Caveats; never a substitute for a structured field. |

### 4.7 Entity / Site Register

`03_evidence/entity_register/entity_register.xlsx` · Organisations (type, origin, Guinea-presence class) and mining/industrial sites.

**Sheet `ORGANISATIONS`** (29 fields)

| # | Field | Type | Req | Vocabulary / reference | Description |
|---|---|---|---|---|---|
| 1 | `entity_id` | ID | R | ENT-NNNN | Unique ID ENT-NNNN. |
| 2 | `legal_name` | TEXT | R |  |  |
| 3 | `short_name` | TEXT | O |  |  |
| 4 | `alternative_names` | TEXT | O |  |  |
| 5 | `entity_type` | ENUM | R | v_entity_type |  |
| 6 | `entity_roles` | MULTI_ENUM | R | v_entity_role | '; '-separated roles. |
| 7 | `origin_subregister` | ENUM | R | v_origin_subregister | WS-25 origin sub-register. |
| 8 | `origin_country_iso3` | ISO3 | O |  |  |
| 9 | `parent_entity_id` | ID_REF | O | ENT-NNNN |  |
| 10 | `guinea_presence_class` | ENUM | R | v_presence_class | Five WS-25 classes + NOT_ASSESSED; global presence never implies Guinea presence (VR-22). |
| 11 | `presence_evidence_source_ids` | ID_LIST | C | SRC | Guinea-specific evidence; required for CONFIRMED_* and REGIONAL_PRESENCE_ONLY. |
| 12 | `presence_assessed_date` | DATE | C |  | Required when class is not NOT_ASSESSED. |
| 13 | `regional_presence_countries` | TEXT | O |  | ISO3 codes ('; '-separated). |
| 14 | `institutional_status` | ENUM | C | v_institutional_status | Required for public bodies. |
| 15 | `mandate_summary` | LONGTEXT | O |  | Public bodies: mandate as evidenced. |
| 16 | `mandate_source_ids` | ID_LIST | C | SRC | Required with mandate_summary. |
| 17 | `related_project_ids` | DERIVED | D | PRJ | Lookup from project register entity fields. |
| 18 | `workstreams` | TEXT | O |  |  |
| 19 | `lead_ids` | ID_LIST | O | LEAD |  |
| 20 | `acceptance_status` | ENUM | R | v_acceptance_status | Gate approval status (D-062). Distinct from evidence_state/confidence; vocabularies do not overlap. |
| 21 | `acceptance_decision_id` | ID_REF | C | D-NNN | Decision-log ID; required when ACCEPTED or REJECTED (VR-02). |
| 22 | `acceptance_gate` | ENUM | C | v_gate | Gate of acceptance/rejection; required when ACCEPTED or REJECTED (VR-02). |
| 23 | `record_status` | ENUM | R | v_record_status | Methodology section 3 `status`: ACTIVE or SUPERSEDED. Records are never deleted (VR-03, D-071). |
| 24 | `superseded_by` | ID_REF | C | ENT-NNNN | Replacing record ID; required when SUPERSEDED (VR-03). |
| 25 | `created_by` | ENUM | R | v_actor | Who created the record. |
| 26 | `created_date` | DATE | R |  | DD-MMM-YYYY. |
| 27 | `last_modified_by` | ENUM | O | v_actor |  |
| 28 | `last_modified_date` | DATE | O |  | DD-MMM-YYYY. |
| 29 | `notes` | LONGTEXT | O |  | Caveats; never a substitute for a structured field. |

**Sheet `SITES`** (53 fields)

| # | Field | Type | Req | Vocabulary / reference | Description |
|---|---|---|---|---|---|
| 1 | `site_id` | ID | R | SITE-NNNN | Unique ID SITE-NNNN. |
| 2 | `site_name` | TEXT | R |  |  |
| 3 | `alternative_names` | TEXT | O |  |  |
| 4 | `operator_entity_id` | ID_REF | C | ENT-NNNN |  |
| 5 | `owner_entity_ids` | ID_LIST | O | ENT |  |
| 6 | `segment` | ENUM | R | v_site_segment | D-036 segmentation; extraction and refining kept separate. |
| 7 | `activity_types` | MULTI_ENUM | R | v_site_activity | '; '-separated. |
| 8 | `commodity` | TEXT | O |  |  |
| 9 | `workstream_primary` | ENUM | R | v_workstream_phase_a |  |
| 10 | `geography_name` | TEXT | R |  | Name of the geographic unit/site as given in the source. |
| 11 | `geo_level` | ENUM | R | v_geo_level | Geographic level (D-067). |
| 12 | `country_iso3` | ISO3 | R |  | ISO 3166-1 alpha-3 code of the country the value relates to. |
| 13 | `latitude` | NUMBER | O | LAT | Decimal degrees, -90 to 90. |
| 14 | `longitude` | NUMBER | O | LON | Decimal degrees, -180 to 180. |
| 15 | `crs` | TEXT | C |  | Required with coordinates; storage CRS EPSG:4326 (research_architecture section L.3). |
| 16 | `coordinate_precision` | ENUM | C | v_coord_precision | Required with coordinates. |
| 17 | `coordinate_source_id` | ID_REF | C | SRC-NNNN | Source of coordinates; required with coordinates. |
| 18 | `lifecycle_stage` | ENUM | R | v_lifecycle | Methodology section 6.1; highest stage with qualifying evidence. |
| 19 | `lifecycle_evidence_type` | ENUM | R | v_lifecycle_evidence | Type of evidence supporting the stage; must be consistent with the stage (VR-19). |
| 20 | `lifecycle_evidence_source_ids` | ID_LIST | R | SRC | Sources evidencing the stage. |
| 21 | `progress_condition` | ENUM | R | v_progress | Methodology section 6.2. STALLED requires positive evidence; silence = UNVERIFIED (VR-19). |
| 22 | `progress_evidence_source_ids` | ID_LIST | C | SRC | Required for DELAYED and STALLED. |
| 23 | `status_summary` | LONGTEXT | R |  | Methodology section 6.3 status_evidence: the specific evidence for stage and condition. |
| 24 | `last_evidence_date` | DATE | R |  | Date of most recent evidence of activity. |
| 25 | `status_assessed_date` | DATE | R |  | Date status last assessed (status as of). |
| 26 | `status_confidence` | ENUM | R | v_confidence | Confidence in the status assessment. |
| 27 | `power_supply_modes` | MULTI_ENUM | R | v_power_supply_mode |  |
| 28 | `captive_technologies` | MULTI_ENUM | O | v_technology |  |
| 29 | `fuel_types` | MULTI_ENUM | O | v_fuel_type |  |
| 30 | `grid_connection_project_ids` | ID_LIST | O | PRJ |  |
| 31 | `demand_electrical_data_ids` | ID_LIST | O | DAT | MDR references (VR-17). |
| 32 | `demand_thermal_data_ids` | ID_LIST | O | DAT | Process steam/heat - MDR references. |
| 33 | `captive_capacity_data_ids` | ID_LIST | O | DAT |  |
| 34 | `fuel_volume_data_ids` | ID_LIST | O | DAT |  |
| 35 | `fuel_cost_data_ids` | ID_LIST | O | DAT |  |
| 36 | `production_data_ids` | ID_LIST | O | DAT |  |
| 37 | `other_data_ids` | ID_LIST | O | DAT |  |
| 38 | `legal_title_reference` | TEXT | O |  | Mining/industrial title reference as evidenced. |
| 39 | `legal_title_source_ids` | ID_LIST | C | SRC | Required with legal_title_reference. |
| 40 | `decarbonisation_commitment_summary` | LONGTEXT | O |  | Operator/parent commitments as evidenced. |
| 41 | `decarbonisation_source_ids` | ID_LIST | C | SRC | Required with the summary. |
| 42 | `related_project_ids` | ID_LIST | O | PRJ |  |
| 43 | `lead_ids` | ID_LIST | O | LEAD |  |
| 44 | `acceptance_status` | ENUM | R | v_acceptance_status | Gate approval status (D-062). Distinct from evidence_state/confidence; vocabularies do not overlap. |
| 45 | `acceptance_decision_id` | ID_REF | C | D-NNN | Decision-log ID; required when ACCEPTED or REJECTED (VR-02). |
| 46 | `acceptance_gate` | ENUM | C | v_gate | Gate of acceptance/rejection; required when ACCEPTED or REJECTED (VR-02). |
| 47 | `record_status` | ENUM | R | v_record_status | Methodology section 3 `status`: ACTIVE or SUPERSEDED. Records are never deleted (VR-03, D-071). |
| 48 | `superseded_by` | ID_REF | C | SITE-NNNN | Replacing record ID; required when SUPERSEDED (VR-03). |
| 49 | `created_by` | ENUM | R | v_actor | Who created the record. |
| 50 | `created_date` | DATE | R |  | DD-MMM-YYYY. |
| 51 | `last_modified_by` | ENUM | O | v_actor |  |
| 52 | `last_modified_date` | DATE | O |  | DD-MMM-YYYY. |
| 53 | `notes` | LONGTEXT | O |  | Caveats; never a substitute for a structured field. |

### 4.8 Assumption Register

`03_evidence/assumption_register/assumption_register.xlsx` · Modelling assumptions with basis and sensitivity; never written back to the MDR as data.

**Sheet `ASSUMPTIONS`** (32 fields)

| # | Field | Type | Req | Vocabulary / reference | Description |
|---|---|---|---|---|---|
| 1 | `asm_id` | ID | R | ASM-NNNN | Unique ID ASM-NNNN. |
| 2 | `assumption_name` | TEXT | R |  |  |
| 3 | `parameter` | TEXT | R |  | Model parameter the assumption sets. |
| 4 | `description` | LONGTEXT | R |  |  |
| 5 | `workstream` | ENUM | R | v_workstream |  |
| 6 | `model_component` | ENUM | R | v_model_component | Scenario drivers D1-D6 / S1-S4 (research_architecture section J) or other use. |
| 7 | `scenario_scope` | TEXT | R |  | ALL or named scenario(s). |
| 8 | `value_type` | ENUM | R | v_asm_value_type | DAT_REFERENCE => value blank (VR-27). |
| 9 | `basis_data_ids` | ID_LIST | C | DAT | Required for DAT_REFERENCE and DERIVED_CALCULATION. |
| 10 | `value` | NUMBER | C |  | Only when value_type is not DAT_REFERENCE (no duplication of MDR values). |
| 11 | `unit` | ENUM | C | v_unit | Required with value. |
| 12 | `currency` | ISO4217 | C |  |  |
| 13 | `price_basis` | ENUM | C | v_price_basis |  |
| 14 | `price_base_year` | YEAR | C |  | P-024 governs real-terms base year. |
| 15 | `sensitivity_low` | NUMBER | C |  | Required for material judgement/scenario parameters. |
| 16 | `sensitivity_high` | NUMBER | C |  |  |
| 17 | `method_description` | LONGTEXT | R |  |  |
| 18 | `standard_source_ids` | ID_LIST | C | SRC | Required for ENGINEERING_STANDARD / POLICY_TARGET. |
| 19 | `confidence` | ENUM | R | v_confidence | Never VERIFIED for judgement-based assumptions. |
| 20 | `assumption_owner` | ENUM | R | v_actor |  |
| 21 | `approval_gate` | ENUM | C | v_gate | Gate 6/7 approval. |
| 22 | `approval_decision_id` | ID_REF | C | D-NNN |  |
| 23 | `acceptance_status` | ENUM | R | v_acceptance_status | Gate approval status (D-062). Distinct from evidence_state/confidence; vocabularies do not overlap. |
| 24 | `acceptance_decision_id` | ID_REF | C | D-NNN | Decision-log ID; required when ACCEPTED or REJECTED (VR-02). |
| 25 | `acceptance_gate` | ENUM | C | v_gate | Gate of acceptance/rejection; required when ACCEPTED or REJECTED (VR-02). |
| 26 | `record_status` | ENUM | R | v_record_status | Methodology section 3 `status`: ACTIVE or SUPERSEDED. Records are never deleted (VR-03, D-071). |
| 27 | `superseded_by` | ID_REF | C | ASM-NNNN | Replacing record ID; required when SUPERSEDED (VR-03). |
| 28 | `created_by` | ENUM | R | v_actor | Who created the record. |
| 29 | `created_date` | DATE | R |  | DD-MMM-YYYY. |
| 30 | `last_modified_by` | ENUM | O | v_actor |  |
| 31 | `last_modified_date` | DATE | O |  | DD-MMM-YYYY. |
| 32 | `notes` | LONGTEXT | O |  | Caveats; never a substitute for a structured field. |

### 4.9 GIS Layer Catalogue

`05_gis/gis_layer_catalogue.xlsx` · Provenance of every GIS layer: source, date, licence, CRS, processing, constraint class.

**Sheet `GIS_LAYERS`** (37 fields)

| # | Field | Type | Req | Vocabulary / reference | Description |
|---|---|---|---|---|---|
| 1 | `gis_id` | ID | R | GIS-NNNN | Unique ID GIS-NNNN. |
| 2 | `layer_name` | TEXT | R |  |  |
| 3 | `layer_family` | ENUM | R | v_gis_family | research_architecture section L.1. |
| 4 | `gis_folder` | ENUM | R | v_gis_folder | 05_gis/ subfolder. |
| 5 | `file_name` | TEXT | C |  | Required when committed_to_repo = YES. |
| 6 | `file_format` | ENUM | R | v_gis_format | GeoPackage master proposed (P-012). |
| 7 | `geometry_type` | ENUM | R | v_geometry |  |
| 8 | `workstreams` | TEXT | R |  |  |
| 9 | `description` | LONGTEXT | R |  |  |
| 10 | `source_ids` | ID_LIST | R | SRC |  |
| 11 | `dataset_version` | TEXT | C |  |  |
| 12 | `dataset_date` | DATE | C |  |  |
| 13 | `licence` | TEXT | R |  |  |
| 14 | `redistribution_permitted` | ENUM | R | v_yes_no_unclear |  |
| 15 | `committed_to_repo` | ENUM | R | v_yes_no | Must be NO unless redistribution_permitted = YES (VR-23). |
| 16 | `crs_storage` | TEXT | R |  | EPSG:4326. |
| 17 | `crs_analysis` | TEXT | O |  | Projected CRS chosen at Gate 6. |
| 18 | `resolution` | TEXT | C |  | Rasters. |
| 19 | `spatial_extent` | TEXT | O |  |  |
| 20 | `processing_steps` | LONGTEXT | R |  |  |
| 21 | `constraint_class` | ENUM | R | v_constraint_class | research_architecture section L.2. |
| 22 | `legal_basis_source_ids` | ID_LIST | C | SRC | Required for LEGAL_EXCLUSION. |
| 23 | `attribute_fields` | LONGTEXT | O |  | Continuous attributes retained (no pre-applied masks). |
| 24 | `threshold_applied` | TEXT | C |  | Blank until Gates 6-7; then requires threshold_assumption_ids (VR-23). No universal thresholds. |
| 25 | `threshold_assumption_ids` | ID_LIST | C | ASM |  |
| 26 | `linked_id_type` | ENUM | O | v_linked_id_type |  |
| 27 | `file_sha256` | TEXT | C |  | Fingerprint of the committed file. |
| 28 | `acceptance_status` | ENUM | R | v_acceptance_status | Gate approval status (D-062). Distinct from evidence_state/confidence; vocabularies do not overlap. |
| 29 | `acceptance_decision_id` | ID_REF | C | D-NNN | Decision-log ID; required when ACCEPTED or REJECTED (VR-02). |
| 30 | `acceptance_gate` | ENUM | C | v_gate | Gate of acceptance/rejection; required when ACCEPTED or REJECTED (VR-02). |
| 31 | `record_status` | ENUM | R | v_record_status | Methodology section 3 `status`: ACTIVE or SUPERSEDED. Records are never deleted (VR-03, D-071). |
| 32 | `superseded_by` | ID_REF | C | GIS-NNNN | Replacing record ID; required when SUPERSEDED (VR-03). |
| 33 | `created_by` | ENUM | R | v_actor | Who created the record. |
| 34 | `created_date` | DATE | R |  | DD-MMM-YYYY. |
| 35 | `last_modified_by` | ENUM | O | v_actor |  |
| 36 | `last_modified_date` | DATE | O |  | DD-MMM-YYYY. |
| 37 | `notes` | LONGTEXT | O |  | Caveats; never a substitute for a structured field. |

### 4.10 Opportunity Register (WS-27)

`06_opportunities/candidate_opportunities/opportunity_register.xlsx` · WS-27 country opportunities (Alendei-neutral): evidence chain, fatal-flaw screen, scores, frozen attractiveness rating. Contains no Alendei fields.

**Sheet `OPPORTUNITIES`** (54 fields)

| # | Field | Type | Req | Vocabulary / reference | Description |
|---|---|---|---|---|---|
| 1 | `opp_id` | ID | R | OPP-NNNN | Unique ID OPP-NNNN. |
| 2 | `opp_name` | TEXT | R |  |  |
| 3 | `description` | LONGTEXT | R |  |  |
| 4 | `solution_type` | ENUM | R | v_solution_type | All solution types (technology-neutral). |
| 5 | `technologies` | MULTI_ENUM | R | v_technology |  |
| 6 | `geography_name` | TEXT | R |  |  |
| 7 | `geo_level` | ENUM | R | v_geo_level |  |
| 8 | `related_project_ids` | ID_LIST | O | PRJ |  |
| 9 | `related_site_ids` | ID_LIST | O | SITE |  |
| 10 | `related_entity_ids` | ID_LIST | O | ENT |  |
| 11 | `evidence_chain_data_ids` | ID_LIST | R | DAT | ACCEPTED MDR records only; never LEAD- IDs (VR-18, VR-24). |
| 12 | `evidence_chain_other_ids` | ID_LIST | O | PRJ\|SITE\|ENT\|GIS |  |
| 13 | `assumption_ids` | ID_LIST | O | ASM |  |
| 14 | `ff_legal` | ENUM | R | v_fatal_flaw | Fatal-flaw test: legal prohibition. |
| 15 | `ff_offtake` | ENUM | R | v_fatal_flaw | No credible offtaker/payment pathway. |
| 16 | `ff_site_constraint` | ENUM | R | v_fatal_flaw | Legal exclusion constraint. |
| 17 | `ff_technical` | ENUM | R | v_fatal_flaw | Technical impossibility. |
| 18 | `ff_evidence` | ENUM | R | v_fatal_flaw | Evidence too weak - UNRESOLVED, not rejected. |
| 19 | `ff_notes` | LONGTEXT | C |  | Required when any test is FAIL or UNRESOLVED. |
| 20 | `d01_demand_quality` | SCORE | C |  | Dimension 01 ordinal 1-5; blank until Gate 7 anchors are approved. |
| 21 | `d02_offtaker_counterparty_quality` | SCORE | C |  | Dimension 02 ordinal 1-5; blank until Gate 7 anchors are approved. |
| 22 | `d03_technical_feasibility` | SCORE | C |  | Dimension 03 ordinal 1-5; blank until Gate 7 anchors are approved. |
| 23 | `d04_resource_quality` | SCORE | C |  | Dimension 04 ordinal 1-5; blank until Gate 7 anchors are approved. |
| 24 | `d05_grid_proximity_capacity` | SCORE | C |  | Dimension 05 ordinal 1-5; blank until Gate 7 anchors are approved. |
| 25 | `d06_land_permitting_environment` | SCORE | C |  | Dimension 06 ordinal 1-5; blank until Gate 7 anchors are approved. |
| 26 | `d07_commercial_economics` | SCORE | C |  | Dimension 07 ordinal 1-5; blank until Gate 7 anchors are approved. |
| 27 | `d08_fx_currency_exposure` | SCORE | C |  | Dimension 08 ordinal 1-5; blank until Gate 7 anchors are approved. |
| 28 | `d09_financing_availability` | SCORE | C |  | Dimension 09 ordinal 1-5; blank until Gate 7 anchors are approved. |
| 29 | `d10_implementation_complexity` | SCORE | C |  | Dimension 10 ordinal 1-5; blank until Gate 7 anchors are approved. |
| 30 | `d11_development_timeline` | SCORE | C |  | Dimension 11 ordinal 1-5; blank until Gate 7 anchors are approved. |
| 31 | `d12_strategic_importance` | SCORE | C |  | Dimension 12 ordinal 1-5; blank until Gate 7 anchors are approved. |
| 32 | `d13_scalability` | SCORE | C |  | Dimension 13 ordinal 1-5; blank until Gate 7 anchors are approved. |
| 33 | `d14_competitive_alternatives` | SCORE | C |  | Dimension 14 ordinal 1-5; blank until Gate 7 anchors are approved. |
| 34 | `d15_evidence_confidence_overlay` | ENUM | C | v_confidence | Reported alongside the score, not weighted (research_architecture section K.2). |
| 35 | `score_rationale` | LONGTEXT | C |  | Required when scores entered. |
| 36 | `weight_set_decision_id` | ID_REF | C | D-NNN | Blank: weights not frozen (D-029). Set only after Gate 7 approval. |
| 37 | `composite_score` | DERIVED | D |  | Computed only once an approved weight set exists; never hand-entered. |
| 38 | `sensitivity_notes` | LONGTEXT | C |  | Weight-sensitivity / rank robustness. |
| 39 | `commercial_model_options` | MULTI_ENUM | O | v_commercial_model | None predetermined (D-026). |
| 40 | `structuring_notes` | LONGTEXT | O |  |  |
| 41 | `attractiveness_rating` | ENUM | C | v_attractiveness | Alendei-neutral; provisional labels (P-011). |
| 42 | `rating_frozen` | ENUM | R | v_yes_no | YES only with freeze_decision_id (Gate 7 part 1). |
| 43 | `freeze_decision_id` | ID_REF | C | D-NNN |  |
| 44 | `freeze_date` | DATE | C |  |  |
| 45 | `acceptance_status` | ENUM | R | v_acceptance_status | Gate approval status (D-062). Distinct from evidence_state/confidence; vocabularies do not overlap. |
| 46 | `acceptance_decision_id` | ID_REF | C | D-NNN | Decision-log ID; required when ACCEPTED or REJECTED (VR-02). |
| 47 | `acceptance_gate` | ENUM | C | v_gate | Gate of acceptance/rejection; required when ACCEPTED or REJECTED (VR-02). |
| 48 | `record_status` | ENUM | R | v_record_status | Methodology section 3 `status`: ACTIVE or SUPERSEDED. Records are never deleted (VR-03, D-071). |
| 49 | `superseded_by` | ID_REF | C | OPP-NNNN | Replacing record ID; required when SUPERSEDED (VR-03). |
| 50 | `created_by` | ENUM | R | v_actor | Who created the record. |
| 51 | `created_date` | DATE | R |  | DD-MMM-YYYY. |
| 52 | `last_modified_by` | ENUM | O | v_actor |  |
| 53 | `last_modified_date` | DATE | O |  | DD-MMM-YYYY. |
| 54 | `notes` | LONGTEXT | O |  | Caveats; never a substitute for a structured field. |

### 4.11 Alendei Participation Register (WS-28)

`06_opportunities/alendei_role/alendei_participation_register.xlsx` · WS-28 Alendei roles, capability gaps, partners, Tier 1-4 classification for frozen WS-27 opportunities.

**Sheet `ALENDEI_PARTICIPATION`** (30 fields)

| # | Field | Type | Req | Vocabulary / reference | Description |
|---|---|---|---|---|---|
| 1 | `alp_id` | ID | R | ALP-NNNN | Unique ID ALP-NNNN. |
| 2 | `opp_id` | ID_REF | R | OPP-NNNN | Frozen WS-27 opportunity (read-only reference; VR-24). |
| 3 | `opp_attractiveness_at_freeze` | DERIVED | D | OPP | Lookup; WS-28 cannot alter it. |
| 4 | `opp_freeze_decision_id` | DERIVED | D | OPP | Lookup. |
| 5 | `candidate_roles` | MULTI_ENUM | R | v_alendei_role | D-011 hypothesis roles - not asserted capabilities. |
| 6 | `role_rationale` | LONGTEXT | R |  |  |
| 7 | `capability_evidence_source_ids` | ID_LIST | C | SRC | User-supplied evidence only (origin OWNER_SUPPLIED; VR-24). |
| 8 | `capability_gap` | ENUM | R | v_gap_level |  |
| 9 | `licence_gap` | ENUM | R | v_gap_level |  |
| 10 | `partnership_gap` | ENUM | R | v_gap_level |  |
| 11 | `financing_gap` | ENUM | R | v_gap_level |  |
| 12 | `gap_closure_notes` | LONGTEXT | C |  | Required for GAP_CLOSABLE / GAP_MATERIAL. |
| 13 | `required_partner_entity_ids` | ID_LIST | O | ENT | From the evidenced WS-25 register. |
| 14 | `financing_pathway_entity_ids` | ID_LIST | O | ENT | From WS-24/WS-25. |
| 15 | `strategic_fit_notes` | LONGTEXT | O |  | Secondary lens (research_architecture section K.3). |
| 16 | `tier_classification` | ENUM | C | v_alendei_tier | methodology section 11; Tier 4 mandatory where warranted. |
| 17 | `classification_rationale` | LONGTEXT | C |  | Required with tier_classification. |
| 18 | `tier_eligibility_check` | DERIVED | D | OPP | Tier 1/2 requires opp rating at least CONDITIONALLY_ATTRACTIVE (proposed rule, P-011). |
| 19 | `roadmap_ref` | TEXT | O |  | 06_opportunities/roadmap/ document reference. |
| 20 | `due_diligence_ref` | TEXT | O |  | 06_opportunities/due_diligence/ document reference. |
| 21 | `acceptance_status` | ENUM | R | v_acceptance_status | Gate approval status (D-062). Distinct from evidence_state/confidence; vocabularies do not overlap. |
| 22 | `acceptance_decision_id` | ID_REF | C | D-NNN | Decision-log ID; required when ACCEPTED or REJECTED (VR-02). |
| 23 | `acceptance_gate` | ENUM | C | v_gate | Gate of acceptance/rejection; required when ACCEPTED or REJECTED (VR-02). |
| 24 | `record_status` | ENUM | R | v_record_status | Methodology section 3 `status`: ACTIVE or SUPERSEDED. Records are never deleted (VR-03, D-071). |
| 25 | `superseded_by` | ID_REF | C | ALP-NNNN | Replacing record ID; required when SUPERSEDED (VR-03). |
| 26 | `created_by` | ENUM | R | v_actor | Who created the record. |
| 27 | `created_date` | DATE | R |  | DD-MMM-YYYY. |
| 28 | `last_modified_by` | ENUM | O | v_actor |  |
| 29 | `last_modified_date` | DATE | O |  | DD-MMM-YYYY. |
| 30 | `notes` | LONGTEXT | O |  | Caveats; never a substitute for a structured field. |

## 5. Controlled vocabularies

**`v_acceptance_status`**: `PROPOSED` · `ACCEPTED` · `REJECTED`

**`v_record_status`**: `ACTIVE` · `SUPERSEDED`

**`v_actor`**: `CLAUDE_CODE` · `OPERATOR` · `PROJECT_OWNER` · `CHATGPT`

**`v_gate`**: `G2D` · `G3` · `G4` · `G5` · `G6` · `G7` · `G8` · `G9` · `G10` · `G11`

**`v_workstream`**: `WS-01` · `WS-02` · `WS-03` · `WS-04` · `WS-05` · `WS-06` · `WS-07` · `WS-08` · `WS-09` · `WS-10` · `WS-11` · `WS-12` · `WS-13` · `WS-14` · `WS-15` · `WS-16` · `WS-17` · `WS-18` · `WS-19` · `WS-20` · `WS-21` · `WS-22` · `WS-23` · `WS-24` · `WS-25` · `WS-26` · `WS-27` · `WS-28`

**`v_workstream_phase_a`**: `WS-01` · `WS-02` · `WS-03` · `WS-04` · `WS-05` · `WS-06` · `WS-07` · `WS-08` · `WS-09` · `WS-10` · `WS-11` · `WS-12` · `WS-13` · `WS-14` · `WS-15` · `WS-16` · `WS-17` · `WS-18` · `WS-19` · `WS-20` · `WS-21` · `WS-22` · `WS-23` · `WS-24` · `WS-25` · `WS-26`

**`v_evidence_state_register`**: `EXTRACTED` · `VERIFIED` · `CORROBORATED` · `ESTIMATE` · `CONTRADICTED_UNRESOLVED`

**`v_evidence_state_lead`**: `RAW_LEAD`

**`v_evidence_state_gap`**: `DATA_GAP`

**`v_confidence`**: `VERIFIED` · `CORROBORATED` · `ESTIMATED` · `INDICATIVE` · `DATA GAP`

**`v_quality`**: `HIGH` · `MEDIUM` · `LOW` · `UNKNOWN`

**`v_discloser`**: `INDEPENDENT_AUDITED` · `OFFICIAL_SELF_REPORTED` · `SELF_REPORTED_PROMOTIONAL`

**`v_cross_check`**: `NOT_ATTEMPTED` · `AGREES` · `DISAGREES` · `NO_INDEPENDENT_SOURCE`

**`v_contradiction_status`**: `NONE` · `OPEN` · `RESOLVED-DEFINITIONAL` · `RESOLVED-HIERARCHY` · `RESOLVED-ERROR` · `RANGE-CARRIED`

**`v_contradiction_outcome`**: `RESOLVED-DEFINITIONAL` · `RESOLVED-HIERARCHY` · `RESOLVED-ERROR` · `RANGE-CARRIED` · `OPEN`

**`v_cause_code`**: `DEFINITION` · `PERIOD` · `SCOPE_GEOGRAPHY` · `UNIT_CURRENCY` · `STATUS_INTERPRETATION` · `DUPLICATION` · `TRANSCRIPTION` · `METHODOLOGY` · `SUPERSEDED` · `REPORTING_PRECISION` · `GENUINE`

**`v_materiality`**: `MATERIAL` · `MODERATE` · `MINOR`

**`v_metric_class`**: `CAPACITY` · `ENERGY` · `DEMAND` · `NETWORK` · `ACCESS` · `LOSSES` · `RELIABILITY` · `TARIFF` · `COST` · `FINANCIAL` · `FUEL` · `RESOURCE` · `HYDROLOGY` · `PRODUCTION` · `MACRO` · `FX_RATE` · `PRICE_INDEX` · `LAND_ENVIRONMENT` · `CONTRACT_TERM` · `LEGAL_INSTITUTIONAL` · `OTHER`

**`v_value_kind`**: `NUMERIC` · `CATEGORICAL`

**`v_energy_class`**: `INSTALLED` · `AVAILABLE` · `DEPENDABLE` · `SEASONAL_DEPENDABLE` · `DISPATCHED` · `GENERATED_GROSS` · `GENERATED_NET` · `GENERATED_UNSTATED` · `DELIVERED` · `CONSUMED_BILLED` · `CONSUMED_METERED` · `PEAK_SERVED` · `PEAK_UNCONSTRAINED` · `AVERAGE_DEMAND` · `SUPPRESSED_UNSERVED` · `CAPTIVE_SELF_SUPPLIED` · `CLASS_UNSTATED` · `NOT_APPLICABLE`

**`v_acdc`**: `AC` · `DC` · `BASIS_UNSTATED` · `NOT_APPLICABLE`

**`v_value_qualifier`**: `EXACT` · `APPROXIMATE` · `ROUNDED` · `SOURCE_RANGE` · `CONTRADICTION_RANGE` · `UPPER_BOUND` · `LOWER_BOUND`

**`v_unit`**: `kW` · `MW` · `GW` · `MW_AC` · `MW_DC` · `kWh` · `MWh` · `GWh` · `TWh` · `MVA` · `MVAr` · `kV` · `Hz` · `km` · `km2` · `ha` · `PERCENT` · `PERCENTAGE_POINT` · `CURRENCY` · `CURRENCY_PER_KWH` · `CURRENCY_PER_MWH` · `CURRENCY_PER_KW` · `CURRENCY_PER_KW_YEAR` · `CURRENCY_PER_LITRE` · `CURRENCY_PER_TONNE` · `CURRENCY_PER_M3` · `FX_RATE` · `LITRE` · `M3` · `TONNE` · `TONNE_PER_YEAR` · `MTPA` · `TONNE_PER_HOUR` · `M3_PER_S` · `KWH_PER_M2_PER_DAY` · `KWH_PER_M2_PER_YEAR` · `M_PER_S` · `HOURS` · `HOURS_PER_YEAR` · `DAYS` · `YEARS` · `COUNT` · `PERSONS` · `KWH_PER_CAPITA` · `RATIO` · `INDEX` · `OTHER`

**`v_price_basis`**: `NOMINAL` · `REAL` · `NOT_APPLICABLE`

**`v_conversion_type`**: `NONE` · `UNIT_IDENTITY` · `FX` · `DEFLATOR` · `DC_AC_RATIO` · `OTHER_DERIVATION`

**`v_fx_rate_type`**: `PERIOD_AVERAGE` · `END_OF_PERIOD` · `TRANSACTION_STATED` · `OFFICIAL_FIXING_DATE` · `NOT_APPLICABLE`

**`v_fx_source_class`**: `CENTRAL_BANK_OFFICIAL` · `IMF_IFS` · `WORLD_BANK_WDI` · `TRANSACTION_DOCUMENT` · `OTHER_DOCUMENTED`

**`v_geo_level`**: `NATIONAL_AGGREGATE` · `REGIONAL` · `PREFECTURE` · `LOCALITY` · `CITY` · `MINING_SITE` · `INDUSTRIAL_SITE` · `PORT` · `PLANT_SITE` · `TRANSMISSION_CORRIDOR` · `SUBSTATION_NODE` · `INTERCONNECTION` · `RIVER_BASIN` · `NEIGHBOURING_COUNTRY` · `MULTI_COUNTRY_REGION` · `OTHER`

**`v_period_type`**: `CALENDAR_YEAR` · `FISCAL_YEAR` · `QUARTER` · `MONTH` · `SEASON` · `DATE` · `MULTI_YEAR_PERIOD` · `POINT_IN_TIME`

**`v_temporal_class`**: `HISTORICAL` · `CURRENT_STATUS` · `COMMITTED_UNDER_CONSTRUCTION` · `PLANNED` · `TARGET_ASPIRATION` · `PROJECTION`

**`v_subject_type`**: `PROJECT` · `SITE` · `ENTITY` · `NATIONAL_SYSTEM` · `GEOGRAPHY` · `BASIN` · `OTHER`

**`v_revalidation`**: `TARIFF` · `LAW_REGULATION` · `INSTITUTIONAL_MANDATE` · `FX_RULE` · `PROJECT_STATUS` · `OWNERSHIP` · `EXCHANGE_RATE` · `HISTORICAL_OUTTURN` · `PHYSICAL_RESOURCE` · `OTHER`

**`v_document_type`**: `LAW_DECREE` · `REGULATOR_DECISION` · `OFFICIAL_GAZETTE` · `MINISTRY_REPORT` · `UTILITY_REPORT` · `SYSTEM_OPERATOR_REPORT` · `AUDIT_REPORT` · `EITI_REPORT` · `SIGNED_AGREEMENT` · `STATUTORY_FILING` · `DFI_PROJECT_DOCUMENT` · `IMF_REPORT` · `OFFICIAL_DATABASE` · `PEER_REVIEWED_PAPER` · `GREY_LITERATURE` · `CONSULTANCY_REPORT` · `ESIA` · `CORPORATE_ANNUAL_REPORT` · `INVESTOR_PRESENTATION` · `PRESS_RELEASE` · `NEWS_ARTICLE` · `TRADE_PRESS` · `DATASET` · `GIS_DATASET` · `ENGINEERING_STANDARD` · `AGGREGATOR_WEB` · `AI_OUTPUT` · `OWNER_SUPPLIED_DOCUMENT` · `OTHER`

**`v_date_precision`**: `DAY` · `MONTH` · `YEAR` · `UNDATED`

**`v_access_status`**: `OPEN` · `REGISTRATION` · `PAYWALLED` · `UNAVAILABLE` · `RESTRICTED`

**`v_retrieval_status`**: `CANDIDATE_SOURCE` · `RETRIEVED` · `CITATION_NOT_FOUND` · `UNAVAILABLE` · `PAYWALLED`

**`v_reliability_flag`**: `NONE` · `UNDER_REVIEW` · `UNRELIABLE`

**`v_copyright_basis`**: `PUBLIC_DOMAIN` · `GOVERNMENT_REDISTRIBUTABLE` · `OPEN_LICENCE` · `LICENSED_FOR_REDISTRIBUTION` · `COPYRIGHTED` · `UNCLEAR`

**`v_local_copy`**: `STORED` · `NOT_STORED_REFERENCE_ONLY` · `STORED_LOCALLY_NOT_COMMITTED`

**`v_origin`**: `GEMINI_MISSION` · `GEMINI_ARCHITECTURE_CHALLENGE` · `CLAUDE_DISCOVERY` · `OWNER_SUPPLIED` · `OWNER_CHALLENGE` · `CHATGPT_CHALLENGE` · `OTHER`

**`v_claim_type`**: `QUANTITATIVE` · `QUALITATIVE` · `STATUS` · `LEGAL_REGULATORY` · `ENTITY_PRESENCE` · `DEFINITION` · `OTHER`

**`v_lead_outcome`**: `NOT_YET_CHECKED` · `VERIFIED` · `PARTLY_VERIFIED` · `CONTRADICTED` · `UNSUPPORTED` · `NOT_VERIFIABLE`

**`v_outcome_reason`**: `CITATION_NOT_FOUND` · `NOT_IN_SOURCE` · `SOURCE_CONTRADICTS` · `PARTIAL_MATCH` · `NO_SOURCE_GIVEN` · `ACCESS_PAYWALLED` · `ACCESS_UNAVAILABLE` · `MALFORMED_ARTIFACT` · `NOT_APPLICABLE`

**`v_self_confidence`**: `HIGH` · `MEDIUM` · `LOW` · `NOT_STATED`

**`v_priority`**: `CRITICAL` · `HIGH` · `MEDIUM` · `LOW`

**`v_gap_status`**: `OPEN` · `PARTLY_FILLED` · `FILLED` · `CLOSED_UNRESOLVABLE`

**`v_lifecycle`**: `PROPOSED` · `ANNOUNCED` · `ACTIVE_DEVELOPMENT` · `FINANCIALLY_COMMITTED` · `UNDER_CONSTRUCTION` · `OPERATIONAL` · `CANCELLED`

**`v_lifecycle_evidence`**: `PLAN_LISTING` · `PUBLIC_ANNOUNCEMENT` · `MOU_LOI_FRAMEWORK` · `DEVELOPMENT_WORK` · `FINANCIAL_CLOSE` · `SIGNED_FINANCING_AGREEMENT` · `BINDING_EPC_WITH_FUNDING` · `BUDGET_WITH_SIGNED_CONTRACT` · `NTP_AND_SITE_WORKS` · `COMMISSIONING_ENERGISATION_COD` · `OFFICIAL_TERMINATION`

**`v_progress`**: `ON_TRACK` · `DELAYED` · `STALLED` · `UNVERIFIED`

**`v_ic_step`**: `YES` · `NO` · `UNVERIFIED` · `NOT_APPLICABLE`

**`v_component_type`**: `GENERATION` · `STORAGE` · `HYBRID_PLANT` · `TRANSMISSION_LINE` · `SUBSTATION` · `INTERCONNECTOR` · `DISTRIBUTION` · `MINI_GRID` · `OFF_GRID_PROGRAMME` · `FUEL_INFRASTRUCTURE` · `MINING_INFRASTRUCTURE` · `PORT` · `RAIL` · `OTHER`

**`v_technology`**: `SOLAR_PV` · `WIND_ONSHORE` · `WIND_OFFSHORE` · `HYDRO_RESERVOIR` · `HYDRO_RUN_OF_RIVER` · `HYDRO_SMALL` · `HYDRO_UNSTATED` · `THERMAL_HFO` · `THERMAL_LFO_DIESEL` · `THERMAL_GAS` · `THERMAL_DUAL_FUEL` · `THERMAL_UNSTATED` · `BIOMASS` · `BESS` · `OTHER_STORAGE` · `HYBRID` · `TRANSMISSION_AC` · `SUBSTATION` · `DISTRIBUTION_NETWORK` · `MINI_GRID` · `SOLAR_HOME_SYSTEMS` · `DEMAND_SIDE_MEASURE` · `OTHER` · `UNSTATED`

**`v_offtaker_type`**: `UTILITY` · `MINING` · `PRIVATE_INDUSTRIAL` · `COMMERCIAL` · `REGIONAL_EXPORT` · `MINI_GRID_CUSTOMERS` · `CAPTIVE_OWN_USE` · `OTHER` · `UNSTATED`

**`v_yes_no`**: `YES` · `NO`

**`v_yes_no_unclear`**: `YES` · `NO` · `UNCLEAR`

**`v_coord_precision`**: `EXACT` · `APPROXIMATE` · `CENTROID` · `UNKNOWN`

**`v_entity_type`**: `GOVERNMENT_MINISTRY` · `REGULATOR` · `UTILITY` · `SYSTEM_OPERATOR` · `GOVERNMENT_AGENCY` · `STATE_COMPANY` · `BASIN_ORGANISATION` · `REGIONAL_BODY` · `DFI_MULTILATERAL` · `DFI_BILATERAL` · `ECA_EXIM` · `GUARANTEE_INSURER` · `COMMERCIAL_BANK` · `FUND` · `DEVELOPER` · `IPP` · `EPC` · `OEM` · `MINING_COMPANY` · `INDUSTRIAL_COMPANY` · `PORT_RAIL_OPERATOR` · `CONSULTANCY` · `NGO` · `OTHER`

**`v_entity_role`**: `SPONSOR` · `OWNER` · `DEVELOPER` · `EPC` · `OEM` · `FINANCIER` · `GUARANTOR` · `INSURER` · `OFFTAKER` · `OPERATOR` · `REGULATOR` · `POLICY_MAKER` · `ADVISER` · `OTHER`

**`v_origin_subregister`**: `INDIA` · `CHINA` · `EUROPE` · `MIDDLE_EAST` · `USA` · `JAPAN_KOREA` · `AFRICA_REGIONAL` · `GUINEA_DOMESTIC` · `OTHER`

**`v_presence_class`**: `CONFIRMED_OPERATIONAL_PRESENCE` · `CONFIRMED_PROJECT_SUPPLIED_OR_EXECUTED` · `CONFIRMED_PIPELINE` · `REGIONAL_PRESENCE_ONLY` · `POTENTIAL_FUTURE_SUPPLIER_PARTNER` · `NOT_ASSESSED`

**`v_institutional_status`**: `OPERATIONAL` · `RESTRUCTURED` · `DEFUNCT` · `UNVERIFIED` · `NOT_APPLICABLE`

**`v_site_segment`**: `BAUXITE_EXTRACTION` · `ALUMINA_REFINING` · `IRON_ORE` · `GOLD` · `DIAMONDS` · `OTHER_MINERAL` · `NON_MINING_INDUSTRIAL` · `PORT_LOGISTICS` · `LARGE_COMMERCIAL` · `URBAN_LOAD_CENTRE` · `TELECOM` · `OTHER`

**`v_site_activity`**: `EXTRACTION` · `PROCESSING` · `REFINING` · `RAIL_HAULAGE` · `PORT_HANDLING` · `MANUFACTURING` · `SERVICES` · `OTHER`

**`v_power_supply_mode`**: `CAPTIVE` · `GRID` · `HYBRID` · `CROSS_BORDER` · `NONE` · `UNSTATED`

**`v_fuel_type`**: `HFO` · `LFO` · `DIESEL` · `NATURAL_GAS` · `LNG` · `LPG` · `COAL` · `BIOMASS` · `NONE` · `OTHER` · `UNSTATED`

**`v_asm_value_type`**: `DAT_REFERENCE` · `DERIVED_CALCULATION` · `ANALYST_JUDGEMENT` · `ENGINEERING_STANDARD` · `POLICY_TARGET` · `SCENARIO_PARAMETER`

**`v_model_component`**: `BASELINE` · `D1_MINING_EXPANSION` · `D2_PROCESSING_REFINING` · `D3_INDUSTRIAL_EXPANSION` · `D4_URBAN_COMMERCIAL` · `D5_ELECTRIFICATION` · `D6_INFRASTRUCTURE` · `S1_HYDRO_SEASONALITY_CLIMATE` · `S2_COMMITTED_ADDITIONS` · `S3_WAPP_TRADE` · `S4_DISTRIBUTED_CAPTIVE` · `SCREENING` · `GIS_THRESHOLD` · `FX_CONVERSION` · `OTHER`

**`v_gis_family`**: `BASE_ADMIN` · `SETTLEMENTS_DEMAND` · `GENERATION` · `TRANSMISSION_SUBSTATIONS` · `REGIONAL_INTERCONNECTION` · `MINING_INDUSTRIAL` · `LOGISTICS` · `HYDROLOGY` · `RESOURCE_SOLAR` · `RESOURCE_WIND` · `RESOURCE_HYDRO` · `STORAGE` · `CONSTRAINT` · `OPPORTUNITY`

**`v_gis_folder`**: `base_maps` · `cities` · `generation` · `transmission` · `substations` · `wapp` · `mining` · `industrial` · `logistics` · `hydrology` · `solar` · `wind` · `hydro` · `bess` · `constraints` · `opportunities`

**`v_gis_format`**: `GPKG` · `GEOJSON` · `SHP` · `GEOTIFF` · `OTHER`

**`v_geometry`**: `POINT` · `LINE` · `POLYGON` · `RASTER` · `MIXED`

**`v_constraint_class`**: `LEGAL_EXCLUSION` · `REGULATORY_TECHNICAL_CONSTRAINT` · `RISK_FLAG` · `NOT_A_CONSTRAINT`

**`v_linked_id_type`**: `PRJ` · `SITE` · `OPP` · `NONE`

**`v_solution_type`**: `GENERATION` · `STORAGE` · `HYBRID` · `NETWORK` · `DEMAND_SIDE` · `DECENTRALISED` · `REGIONAL_TRADE` · `FUEL_INFRASTRUCTURE` · `OTHER`

**`v_commercial_model`**: `UTILITY_PPA` · `PRIVATE_B2B_PPA` · `CAPTIVE_SELF_SUPPLY` · `BOO` · `BOOT` · `CONCESSION` · `PPP` · `MINI_GRID_CONCESSION` · `PUBLIC_PROCUREMENT` · `OTHER`

**`v_fatal_flaw`**: `PASS` · `FAIL` · `UNRESOLVED` · `NOT_ASSESSED`

**`v_attractiveness`**: `HIGHLY_ATTRACTIVE` · `ATTRACTIVE` · `CONDITIONALLY_ATTRACTIVE` · `NOT_CURRENTLY_ATTRACTIVE`

**`v_alendei_role`**: `OPPORTUNITY_IDENTIFICATION` · `PROJECT_DEVELOPMENT` · `TECHNICAL_SOLUTION_ARCHITECTURE` · `RENEWABLE_INTEGRATION` · `BESS_INTEGRATION` · `INDUSTRIAL_CAPTIVE_SOLUTIONS` · `IPP_BOOT_BOO_STRUCTURES` · `COMMERCIAL_STRUCTURING` · `PARTNER_COORDINATION` · `OEM_EPC_INTEGRATION` · `FINANCING_COORDINATION` · `GOVERNMENT_INTERFACE` · `INDUSTRIAL_INTERFACE`

**`v_gap_level`**: `NONE_IDENTIFIED` · `GAP_CLOSABLE` · `GAP_MATERIAL` · `NOT_ASSESSED`

**`v_alendei_tier`**: `TIER_1_PURSUE_IMMEDIATELY` · `TIER_2_DEVELOP` · `TIER_3_MONITOR` · `TIER_4_DO_NOT_PURSUE_NOW`

**`v_categorical_type`**: `BOOLEAN` · `ENTITY_REFERENCE` · `CATEGORY_CODE`

**`v_difference_test`**: `DEFINITION` · `PERIOD` · `GEOGRAPHY` · `SCOPE` · `UNIT` · `AC_DC_BASIS` · `ENERGY_BASIS` · `METHODOLOGY` · `SOURCE_PRECISION`

**`v_precision_attribution`**: `ATTRIBUTABLE` · `NOT_ATTRIBUTABLE` · `NOT_APPLICABLE`

Definitions for every code are in each workbook's VOCAB_DEFINITIONS sheet.

## 6. Validation rules

| Rule | Applies to | Rule | Enforcement |
|---|---|---|---|
| VR-01 | All | Record IDs follow the register pattern, are unique, and are never reused. MDR: WS part of data_id equals `workstream`. | In-cell (pattern) + validator |
| VR-02 | All | acceptance_status in {PROPOSED, ACCEPTED, REJECTED}. ACCEPTED/REJECTED require acceptance_decision_id (existing D-NNN) and acceptance_gate. New records start PROPOSED. | In-cell (list) + validator |
| VR-03 | All | record_status SUPERSEDED requires superseded_by referencing an existing record of the same register. Rows are never deleted; corrections are made by supersession. | Validator |
| VR-04 | All | acceptance_status and evidence_state/confidence are separate fields with non-overlapping vocabularies; acceptance never implies verification (D-062). | Structural |
| VR-05 | All | Every *_id / *_ids reference resolves to an existing record in the target register; ID lists use '; ' as separator. | Validator |
| VR-06 | MDR | source_id required unless evidence_state = ESTIMATE; ESTIMATE requires input_data_ids and estimate_method. | Validator |
| VR-07 | MDR | evidence_state VERIFIED requires page_table_section, access_date, verified_by, verified_date, and a source of tier 1-3 (D-082). | Validator |
| VR-08 | MDR | Confidence mapping: VERIFIED->VERIFIED; CORROBORATED->CORROBORATED; ESTIMATE->ESTIMATED; EXTRACTED->INDICATIVE; CONTRADICTED_UNRESOLVED requires contradiction_id. Confidence may be lower than the mapping (quality dimensions) but never higher. | Validator |
| VR-09 | MDR | CORROBORATED requires cross_check_status = AGREES (identical, or differing only by demonstrable reporting precision under D-072) and >= 2 independent sources (source_id + cross_check_source_ids) with at least one tier <= 4 (D-082); sources sharing an origin, citing each other or AI outputs are not independent. | Validator + reviewer |
| VR-10 | MDR | If the only sources are tier 5-6 (D-082), confidence is at most INDICATIVE. | Validator |
| VR-11 | MDR | NUMERIC: value, or value_low + value_high, required. SOURCE_RANGE/CONTRADICTION_RANGE require low and high; CONTRADICTION_RANGE requires contradiction_status = RANGE-CARRIED. CATEGORICAL requires value_text and blank numeric fields. | Validator |
| VR-11a | MDR | P-025 boundary (D-074): CATEGORICAL records must be atomic, defined and traceable - categorical_type required; BOOLEAN => value_text YES/NO; ENTITY_REFERENCE => an existing ENT- ID; CATEGORY_CODE => a code listed in metric_definition; value_text <= 100 characters; metric, definition, geography, effective period (period_start/end), source, evidence state, confidence and provenance required as for numbers. Narrative, opinions, interpretations, broad qualitative assessments, causal explanations and commercial judgements are prohibited in the MDR and belong in lead, analysis or reconciliation structures. | In-cell (length, list) + validator + reviewer |
| VR-12 | MDR/ASM | unit required for NUMERIC; CURRENCY* units require currency (ISO 4217) and price_basis; REAL requires price_base_year and an assumption reference for the deflator. | In-cell (pattern) + validator |
| VR-13 | MDR | metric_class CAPACITY/ENERGY/DEMAND requires energy_class other than NOT_APPLICABLE; PV capacity requires ac_dc_basis AC or DC (BASIS_UNSTATED flagged and confidence downgraded); CLASS_UNSTATED restricts use. | Validator |
| VR-14 | MDR | conversion_type FX/DEFLATOR/DC_AC_RATIO/OTHER_DERIVATION requires evidence_state = ESTIMATE and input_data_ids; FX conversions must cite an FX_RATE record; FX_RATE records require fx_rate_type, fx_source_class, fx_base_currency, fx_quote_currency (D-070). | Validator |
| VR-15 | MDR | energy_class SEASONAL_DEPENDABLE requires period_type MONTH or SEASON and season_label; hydro plant records require seasonal dependable capacity alongside nameplate (D-037). | Validator |
| VR-16 | All | DERIVED columns are populated only by tooling from the authoritative register and are never hand-edited. | Structural + validator |
| VR-17 | PRJ/ENT/SITE/OPP/ALP | No quantitative evidence columns exist outside the MDR (and non-evidence assumption values in ASM); quantities are referenced by DAT- IDs (single store). The only other numeric attributes permitted are spatial coordinates (latitude/longitude, with source) and WS-27 ordinal assessment scores (1-5), neither of which is an evidence statistic. | Structural |
| VR-18 | LEAD/OPP | Lead evidence_state is always RAW_LEAD; UNSUPPORTED/NOT_VERIFIABLE/CONTRADICTED require outcome_reason; LEAD- IDs never appear in evidence chains or as evidence anywhere. | In-cell (list) + validator |
| VR-19 | PRJ/SITE | lifecycle_evidence_type must support lifecycle_stage (MoU/LOI at most ANNOUNCED; board approval alone never FINANCIALLY_COMMITTED); stages FINANCIALLY_COMMITTED and later need corroboration if only tier-5 sources (D-082); STALLED requires positive evidence in progress_evidence_source_ids; silence = UNVERIFIED. | Validator + reviewer |
| VR-20 | PRJ | component_type INTERCONNECTOR requires all five ic_* steps; each YES requires its evidence; energised requires constructed; synchronised, operational and commercially_active each require energised; lifecycle OPERATIONAL for lines/interconnectors requires ic_energised = YES; steps are never collapsed (D-069). | Validator |
| VR-20a | SRC | url or persistent_reference required; access_date required; local_path required when local_copy_status = STORED. | Validator |
| VR-21 | SRC/GIS | STORED / committed only with copyright_basis PUBLIC_DOMAIN, GOVERNMENT_REDISTRIBUTABLE, OPEN_LICENCE or LICENSED_FOR_REDISTRIBUTION; UNCLEAR is never committed. | Validator |
| VR-22 | ENT | CONFIRMED_* presence classes require Guinea-specific presence_evidence_source_ids; global presence never implies Guinea presence. | Validator + reviewer |
| VR-23 | GIS | LEGAL_EXCLUSION requires legal_basis_source_ids; threshold_applied blank before Gate 6 and otherwise requires threshold_assumption_ids; committed_to_repo = NO unless redistribution_permitted = YES. | Validator |
| VR-24 | OPP/ALP | OPP contains no Alendei fields; scores blank until Gate 7; composite_score only with weight_set_decision_id; rating_frozen = YES requires freeze_decision_id; evidence chains cite ACCEPTED records only. ALP opp_id must reference a frozen OPP; WS-28 cannot alter OPP ratings; capability evidence must come from OWNER_SUPPLIED sources; Tier 1/2 eligibility per P-011 (provisional). | Validator + reviewer |
| VR-25 | GAP | question_priority_current differing from the charter priority requires priority_change_reason and priority_change_decision_id (Gate 4). | Validator |
| VR-26 | CON | data_ids lists >= 2 MDR records; RESOLVED-HIERARCHY/RESOLVED-ERROR require governing_data_id; RANGE-CARRIED requires range_data_id; MATERIAL + OPEN/RANGE-CARRIED requires escalated = YES. D-072: no universal numerical tolerance - any difference triggers the comparability tests; cause REPORTING_PRECISION only with precision_attribution = ATTRIBUTABLE, all nine tests in diagnostic_tests_completed and a precision_justification; otherwise the contradiction is preserved or a range carried. | Validator |
| VR-27 | ASM | value_type DAT_REFERENCE requires basis_data_ids and blank value (no duplication); other types require value, unit and method_description; assumptions are never written back into the MDR. | Validator |
| VR-28 | All | Analysis, GIS and deliverables may use only records with acceptance_status = ACCEPTED and record_status = ACTIVE. | Validator + gate review |
| VR-30 | MDR | Media/trade press (document_type NEWS_ARTICLE or TRADE_PRESS) never independently establishes a material claim (D-086): a record whose only sources are media is at most EXTRACTED/INDICATIVE; media reports derived from one underlying source count once. | Validator + reviewer |
| VR-31 | MDR | Corporate statutory filings and other Tier 5 disclosures are authoritative only for the issuer's own disclosed facts (D-086): a record whose only sources are Tier 5 must not describe NATIONAL_SYSTEM, GEOGRAPHY or BASIN subjects (government, grid, regulatory or national-system facts). | Validator + reviewer |
| VR-29 | All | Dates are stored as dates and displayed DD-MMM-YYYY; period_start is the period described, never the publication date. | In-cell (date) |

**Enforcement:**
- **In-cell:** Excel data validation covers enumerations, ID patterns, dates, numbers, tiers, scores and ISO-code format.
- **Cross-field and cross-register rules** are enforced by a register validator: a CLI or equivalent automated tool (D-075).
- **The validator must exist, be approved and pass before Gate 2D research execution or the first authoritative data entry.** It is implemented as `00_project/tools/validate_registers.py` (D-083), with deterministic tests in `00_project/tools/tests/test_validate_registers.py`.
- **Usage:** `python3 -I 00_project/tools/validate_registers.py --gate <current gate> [--hide-pass] [--format tsv] [--strict]`. The validator is read-only. Each result is PASS / FAIL / WARNING with rule, register, record, field, reason and remediation. Exit code 1 if any FAIL. It must report FAIL = 0 before Gate 2D, before any acceptance decision and before records are used in analysis.
- **Rule IDs:** VR-01 – VR-31, VR-11a and VR-20a; schema checks SCHEMA-01 (headers), SCHEMA-02 (required fields), SCHEMA-03 (vocabularies) and SCHEMA-04 (types); D-077 (no populated data before Gate 2D).
- **The validator must be able to check:** schema · IDs · controlled vocabularies · required fields · duplicate records · provenance · acceptance/evidence compatibility · cross-register references · supersession · units/currency · project status transitions · interconnector status ordering · contradiction references · opportunity evidence eligibility · Alendei participation restrictions.

## 7. Gate 2B data-model decisions

| Item | Decision |
|---|---|
| P-018 → D-067 | **Geographic level codes** (`v_geo_level`). The Gate 1 codes are retained (NATIONAL_AGGREGATE, REGIONAL, PREFECTURE, SUBSTATION_NODE, PLANT_SITE, OTHER). Added: LOCALITY, CITY, MINING_SITE, INDUSTRIAL_SITE, PORT, TRANSMISSION_CORRIDOR, INTERCONNECTION, RIVER_BASIN, NEIGHBOURING_COUNTRY, MULTI_COUNTRY_REGION |
| P-019 → D-068 | **Contradiction cause codes** (`v_cause_code`). The Gate 1 causes are retained; METHODOLOGY and SUPERSEDED are added |
| P-020 → D-069 | **Interconnector status.** Five distinct project-register steps: `ic_constructed`, `ic_energised`, `ic_synchronised`, `ic_operational`, `ic_commercially_active`. Each has its own value, evidence sources and date, and the steps are never collapsed (VR-20) |
| P-023 → D-070 | **Exchange rates.** Each rate is its own MDR record (metric_class FX_RATE), with `fx_rate_type`, `fx_source_class` and base/quote currencies. Source preference: CENTRAL_BANK_OFFICIAL → IMF_IFS → WORLD_BANK_WDI → OTHER_DOCUMENTED; TRANSACTION_DOCUMENT applies when a transaction states its own rate. Rate type: PERIOD_AVERAGE for flows, END_OF_PERIOD for stocks, TRANSACTION_STATED where a source transaction states a rate. A conversion is a separate ESTIMATE record citing the original value and the rate record. Cross rates use a direct published rate where available; otherwise they go via USD, with both rates recorded |
| D-071 (APPROVED) | `acceptance_status` = PROPOSED / ACCEPTED / REJECTED. `record_status` = ACTIVE / SUPERSEDED (the methodology §3 `status` field). A record may legitimately be ACCEPTED + SUPERSEDED: accepted as valid for its historical context, later superseded. SUPERSEDED is never an acceptance status. RETIRED/CLOSED is not added because no current register requires it: lead and gap closure are carried by `lead_outcome` and `gap_status` |
| D-072 (FINAL, as modified by owner) | **No universal numerical contradiction tolerance is assumed.** Any difference triggers the comparability tests: definition, date, geography, scope, unit, AC/DC basis, capacity/energy basis, methodology, source precision. A difference is classified as reporting precision **only** when (1) the definitions are comparable, (2) the periods, geography and scope are comparable, and (3) the difference is demonstrably attributable to reporting precision (cause REPORTING_PRECISION). Otherwise the contradiction is preserved, or a range is carried where the sources are comparable and none can reasonably be preferred. No arbitrary percentage tolerance |
| D-073 | The generator script is the single schema definition; the XLSX templates and this dictionary are generated from it |
| P-025 → D-074 (APPROVED WITH BOUNDARY) | Atomic, defined, traceable structured facts may be stored in the MDR (`value_kind` CATEGORICAL, `categorical_type`, `value_text` ≤ 100 characters), with metric, structured value, type, geography, effective period, definition, source, evidence state, confidence and provenance. Examples: whether a regulatory requirement exists; the institution responsible for a defined function; whether a specific licence is required; a categorical technology or status classification. **The MDR must not become a narrative repository** (VR-11a) |
| P-026 → D-075 (APPROVED, strengthened) | The register validator is a **prerequisite for Gate 2D research execution / first authoritative data entry**. A CLI or equivalent automated tool is acceptable; it may be designed and built at Gate 2C (capabilities in §6) |
| D-076 | **11 logical registers.** Entity/Site is implemented as two physical tables/sheets (ORGANISATIONS, SITES) where required by the schema |
