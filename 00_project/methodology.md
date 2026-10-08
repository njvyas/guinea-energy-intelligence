# Methodology

**Version:** 1.0 (DRAFT — pending Gate 1 approval) · **Last updated:** 08-Oct-2026 · **Gate:** 1

This is the normative reference for evidence rules, metric definitions and status definitions. The research organisation (workstreams, sequencing, registers, protocols, scenarios, screening and GIS) is defined in `research_architecture.md` and `workstream_charters.md`. How missions are executed, verified, reconciled and accepted is defined in `research_execution_protocol.md` (Gate 2A), which applies these definitions without amending them.

## 1. Evidence hierarchy

The **authoritative six-tier hierarchy** (D-082, confirmed by the owner at Gate 2C) is as follows. **Tier 6 is never part of the evidence hierarchy.**

| Tier | Class | Examples | Can stand alone as evidence? |
|---|---|---|---|
| 1 | Guinea government / primary institutional | Laws, decrees, official gazette, ministry, regulator, utility and system-operator publications, Guinea public-institution statistics, government-published agreements and award notices | Yes |
| 2 | WAPP / ECOWAS / regional institutional | WAPP Secretariat/ICC documents, ECOWAS and regional regulator decisions, regional interconnector operators, river-basin organisations | Yes |
| 3 | World Bank / IFC / AfDB / EIB / IMF / UN / other DFIs | Appraisal, status and completion documents; country diagnostics; DFI databases | Yes |
| 4 | Data institutions, science and engineering | IRENA, IEA, Global Energy Monitor, Ember, NREL, Global Solar Atlas, Global Wind Atlas, NASA, NOAA, Copernicus, peer-reviewed literature, engineering studies | Yes, with a definition check (single-source value is INDICATIVE) |
| 5 | Corporate and project disclosures | OEM / EPC / IPP / mining-company disclosures, investor presentations, project-finance disclosures, tenders, corporate statutory filings | Only for the issuer's own disclosed facts (D-086); otherwise corroboration required |
| 6 | AI-generated or otherwise unsourced material | Gemini or any AI output, unsourced web content, aggregators | **Never — LEAD ONLY** |

**Gate 1 tier labels.** Labels in documents written before D-082, including the "Source priorities" lines of `workstream_charters.md`, map as follows. The order of preference stated in each charter is unchanged.

| Gate 1 label | Authoritative tier (D-082) |
|---|---|
| T1 | T1 (Guinea government) or T2 (WAPP/ECOWAS/regional); corporate statutory filings → T5 (issuer's own facts, D-086) |
| T2 | T3 |
| T3 | T4 |
| T4 | T5 |
| T5 (media) | Secondary reporting / discovery, not an evidence tier (D-086); recorded as tier 5 with document type NEWS_ARTICLE / TRADE_PRESS |
| T6 | T6 |

**Media and trade press (P-029 resolved, D-086)** are secondary reporting and discovery sources. **They are not an evidence tier equivalent to institutional or primary sources.** They may identify leads, point researchers to the underlying primary sources, provide contextual reporting, and corroborate chronology or public reporting where appropriate. **They must not independently establish a material quantitative or legal claim where a suitable primary or authoritative source is reasonably available.** Repeated media reports that derive from the same underlying source are not independent corroboration. In the source register they carry `source_tier` 5 with `document_type` NEWS_ARTICLE or TRADE_PRESS; the document type, not the tier number, governs their limited use (validator VR-30).

**Corporate statutory filings (D-086)** are Tier 5. They are authoritative for the **issuer's own disclosed facts**, subject to the normal verification rules. Examples: company ownership, company-reported production, capacity, financial information, project commitments, contracts or project status. A corporate filing is **not** authoritative for unrelated government, grid, regulatory or national-system facts merely because it is a statutory filing (validator VR-31).

**Discloser independence** (recorded per source and data point): `INDEPENDENT_AUDITED` (e.g. supreme audit institution, DFI completion report, EITI reconciliation) · `OFFICIAL_SELF_REPORTED` (e.g. utility or ministry statistics) · `SELF_REPORTED_PROMOTIONAL` (e.g. press releases, investor presentations, speeches). Tier and independence are recorded separately.

## 2. Confidence categories

| Category | Definition |
|---|---|
| **VERIFIED** | Confirmed directly in a Tier 1, 2 or 3 source (D-082 numbering), with metric definition and date clear. |
| **CORROBORATED** | Supported by two or more independent sources (at least one Tier 1–4, D-082) that agree within a stated tolerance, but no single definitive primary source located. |
| **ESTIMATED** | Derived by Claude or a cited source through a documented calculation or method from verified/corroborated inputs. Method recorded. |
| **INDICATIVE** | Single Tier 4–5 source (D-082), or source with unclear definition/date. Usable for context only; not for headline figures without a caveat. |
| **DATA GAP** | No adequate source located. Recorded in the data-gap register. |

*"Agree within a stated tolerance" and "within tolerance" are applied under D-072: no universal numerical tolerance is assumed, and values agree when they are identical or differ only by demonstrable reporting precision after the comparability tests (`research_execution_protocol.md` §10.1).*

Final deliverables: headline and decision-critical figures must be VERIFIED or CORROBORATED. ESTIMATED figures must show method. INDICATIVE figures must be visibly caveated. DATA GAP is stated as such.

### 2.1 Quality dimensions — confidence is not a substitute for evidence (D-040)

Each data point is rated on six dimensions (`HIGH` / `MEDIUM` / `LOW` / `UNKNOWN`):

| Dimension | Question |
|---|---|
| Source quality | Tier, discloser independence, primary vs secondary. |
| Recency | How current is the value relative to the period it describes and to the likelihood of change? |
| Cross-source agreement | Do independent sources agree within tolerance? |
| Methodological quality | Is the measurement / estimation method documented and sound? |
| Completeness | Does the value cover the full scope claimed (all plants, full year, whole country)? |
| Definition consistency | Is the metric definition explicit and consistent with §5? |

Rules:
1. The confidence category is determined first by the evidence rules above (source tier, corroboration, method). Quality dimensions can **only downgrade** a category, never upgrade it.
2. An ESTIMATED value remains ESTIMATED regardless of how high its quality ratings are. **A high-confidence estimate is never presented as a verified fact.**
3. **Recency without a fixed time threshold (D-048):** data classes liable to change — tariffs, laws and regulations, institutional mandates, FX rules, project status, ownership — must be re-verified against the latest available source at Gate 9 before entering a deliverable, irrespective of age. Other data classes are flagged for re-verification where a newer edition of the source is known or likely to exist.

### 2.2 Evidence states (D-032)

Every item carries an evidence state that records where it sits in the verification pipeline (`research_architecture.md` §F):

| State | Meaning | Lives in |
|---|---|---|
| `RAW_LEAD` | Unverified claim (Gemini, Claude discovery note, other) | Lead register only |
| `CANDIDATE_SOURCE` | Source identified but not yet retrieved and checked | Source register only |
| `EXTRACTED` | Value taken from a retrieved source; not yet meeting VERIFIED/CORROBORATED rules (confidence INDICATIVE) | Master data / project / entity register |
| `VERIFIED` | Meets the VERIFIED rule | Registers |
| `CORROBORATED` | Meets the CORROBORATED rule | Registers |
| `ESTIMATE` | Derived by documented method (confidence ESTIMATED) | Registers + assumption register |
| `INFERENCE` | Analytical judgement drawn from evidence | Analysis documents only, labelled "Inference" — never stored as a data point |
| `CONTRADICTED_UNRESOLVED` | Subject to an OPEN or RANGE-CARRIED contradiction | Registers, with `contradiction_id` |
| `DATA_GAP` | Sought but not found | Data-gap register |

No material statistic enters the master data register without a traceable source (`source_id`, page/table/section).

## 3. Required metadata for every material statistic

| Field | Description |
|---|---|
| `data_id` | Unique ID, format `DAT-WSNN-NNNNN` |
| `workstream` | One of WS-01 – WS-26 (`workstream_charters.md`) |
| `metric` | Metric name |
| `metric_definition` | Precise definition (see §5) |
| `value` | Numeric value (or low/high for RANGE-CARRIED) |
| `unit` | Unit (MW, MW-DC, MW-AC, GWh, %, USD, INR, etc.) |
| `geography` | Country / region / site |
| `spatial_granularity` | `NATIONAL_AGGREGATE` / `REGIONAL` / `PREFECTURE` / `SUBSTATION_NODE` / `PLANT_SITE` / `OTHER`, extended by D-067. Implemented as `geo_level` with the controlled list `v_geo_level` in `register_schema.md` |
| `period` | Date, year, month or season the value refers to |
| `source_id` | Link to source register |
| `source_title` / `publisher` | As in the source register (denormalised for review) |
| `source_publication_date` | Where available |
| `source_url_or_reference` | URL or document reference |
| `page_table_section` | Exact location of the value in the source |
| `access_date` | DD-MMM-YYYY |
| `source_tier` | 1–6 |
| `discloser_independence` | §1 |
| `evidence_state` | §2.2 |
| `confidence` | VERIFIED / CORROBORATED / ESTIMATED / INDICATIVE / DATA GAP |
| `quality_*` | Six quality dimensions (§2.1) |
| `cross_check` | Other sources consulted and their values |
| `contradiction_status` / `contradiction_id` | NONE / OPEN / RESOLVED-* / RANGE-CARRIED (`research_architecture.md` §H) |
| `lead_id` | Originating lead, if any |
| `verified_by` / `verified_date` | Agent and date |
| `notes` | Caveats |
| `status` | ACTIVE / SUPERSEDED (with `superseded_by`) |

*Under D-074, the Master Data Register may also hold atomic, defined, traceable structured categorical facts (`value_kind` CATEGORICAL, with `categorical_type` and `value_text`), subject to the same metadata and provenance. Narrative, opinions, interpretations, broad qualitative assessments, causal explanations and commercial judgements are excluded; they belong in lead, analysis or reconciliation structures (`register_schema.md` VR-11a).*

## 4. Registers

The full register architecture (11 logical registers per D-076, locations, ID formats, contents) is defined in `research_architecture.md` §G. This section governs format and source-document handling.

### 4.1 Register format

- **Master working format: XLSX.** The human-facing master evidence, data, source and opportunity registers are maintained as XLSX workbooks. The XLSX file is the authoritative version.
- **Machine-readable derivatives: CSV / JSON**, introduced later only where useful (e.g. for the HTML platform or analytical workflows). Derivatives are generated from the XLSX master, never edited by hand, and never treated as authoritative.
- No duplicate register files are created until a concrete downstream need exists.

### 4.2 Source register fields and third-party documents

Every source is logged in the source register with, at minimum:

| Field | Description |
|---|---|
| `source_id` | Unique ID (e.g. `SRC-0001`) |
| `title` | Title in original language (translation marked as such) |
| `publisher` | Issuing organisation |
| `publication_date` | Where available |
| `url` | Direct link |
| `access_date` | Date accessed (DD-MMM-YYYY) |
| `document_type` | e.g. law/decree, regulator report, utility report, DFI appraisal, dataset, press release, article |
| `tier` | Evidence tier (§1) |
| `relevant_pages_sections` | Pages, sections, tables or figures relied on |
| `evidence_extracted` | Summary of what was taken from the source, with data IDs |
| `access_copyright_note` | Licence / copyright status and any redistribution restriction |
| `local_copy_status` | `STORED` (with path) / `NOT STORED — REFERENCE ONLY` / `STORED LOCALLY, NOT COMMITTED` |

**Copyright rule:** Copyrighted third-party PDFs and documents are **not** committed to the repository automatically. The register entry (URL, pages/sections, extracted evidence) is what makes the evidence traceable.

Documents may be stored in `02_sources/` where appropriate, namely when they are:

- licensed for redistribution;
- in the public domain;
- government or other official publications that are publicly redistributable; or
- otherwise appropriately shareable (e.g. under an open licence that permits it).

The basis for storing a document is recorded in `access_copyright_note`. When the position is unclear, the document is not committed.

## 5. Metric definitions (mandatory distinctions)

**Capacity**
| Term | Definition |
|---|---|
| Installed capacity | Nameplate rated capacity of commissioned plant. State MW-AC or MW-DC for solar. |
| Available capacity | Capacity not on planned/forced outage at a given time. |
| Dependable capacity | Capacity reliably available at system peak (accounts for hydrology, fuel, derating). |
| Seasonal dependable capacity (hydro) | Dependable capacity stated per month or season (minimum: wet and dry season, with the months defining each season stated per source). **Mandatory for every hydro plant alongside nameplate; an annual average is never used alone** (D-037). |
| Dispatched capacity | Capacity actually generating at a given time. |

**Energy**
| Term | Definition |
|---|---|
| Generation | Gross (or net — state which) energy produced at plant terminals, GWh. |
| Delivered electricity | Energy delivered to the distribution system / customers after transmission losses. |
| Consumed electricity | Energy billed or metered at end use (state billed vs consumed; note unbilled/non-technical losses). |

**Demand**
| Term | Definition |
|---|---|
| Peak demand | Maximum served (or estimated unconstrained — state which) demand over a period, MW. |
| Average demand | Energy over a period divided by hours, MW. |
| Suppressed / unserved demand | Demand not served due to supply or network constraints; method of estimation must be stated. |
| Captive / self-supplied demand | Demand met by on-site or private generation outside the public grid; recorded separately from served grid demand. |

**Network and access**
| Term | Definition |
|---|---|
| Transmission line — constructed | Physically built (mechanical completion); not necessarily energised. |
| Transmission line — energised | Energised and operating, with evidence of substation commissioning. |
| Interconnector — commercially active | Energised **and** carrying contracted, metered cross-border trade. |
| Access rate | State definition: grid connection count vs household access (multi-tier framework tier); disaggregate urban/rural and by tier where available. |
| Losses | Partition: transmission technical · distribution technical · non-technical / commercial; state the measurement method. |

Default unit convention: power in MW (solar stated as MW-DC unless the source specifies MW-AC; both recorded where available). Currency recorded in source currency; conversions to USD and INR (₹, Indian formatting — lakhs/crores) show rate and date.

## 6. Project status framework

A project's status is assigned from **evidence of progress and commitment**, not from the time elapsed. Each project record carries two separate dimensions plus supporting evidence:

1. **Lifecycle stage:** how far the project has verifiably advanced.
2. **Progress condition:** whether it is advancing as expected.

### 6.1 Lifecycle stage

A project is assigned the highest stage for which qualifying evidence exists. Claims alone do not qualify; the evidence must be documented.

| Stage | Qualifying evidence (indicative, not exhaustive) |
|---|---|
| **Proposed** | Appears in a plan, master plan, study, pipeline list or concept note. No named sponsor has publicly committed to developing the specific project. |
| **Announced** | A named sponsor, government body or credible party has publicly declared intent to develop a specific project (identifiable site, technology or scale). MoUs, LOIs and framework agreements count here at most. There is no evidence of development work beyond the announcement. |
| **Active development** | Documented development work is under way: feasibility or ESIA studies commissioned or completed; land or site rights secured; licences, permits or concessions applied for or granted; grid-connection or interconnection studies; PPA, concession or offtake negotiation; procurement launched; DFI project-preparation activity. There is no binding financial commitment. |
| **Financially committed** | A binding financial commitment is evidenced: financial close; signed financing agreements (e.g. a signed DFI loan, not only board approval); a binding EPC contract with confirmed funding; or a public budget allocation backed by a signed contract. |
| **Under construction** | Physical works are verifiably under way: notice to proceed issued **and** site works evidenced (official progress reports, contractor or DFI supervision reports, credible site documentation). |
| **Operational** | Commissioned, energised or at commercial operation date. Partial commissioning is recorded with the commissioned portion specified. |
| **Cancelled** | Officially terminated or withdrawn: government or sponsor statement, contract termination, licence or concession revocation, or DFI cancellation. This is a terminal stage. |

### 6.2 Progress condition

| Condition | Evidence basis |
|---|---|
| **On track** | No evidence of slippage against published milestones. |
| **Delayed** | The project is still progressing, but a published milestone (financial close, construction start, COD, etc.) has been missed, or an official revised schedule has been issued. |
| **Stalled** | Positive evidence that progress has stopped or is blocked, for example: an official suspension; contractor demobilisation; financing withdrawn, suspended or frozen; a DFI project suspended or restructured; a sponsor exit; a licence or concession lapsed; an unresolved dispute or arbitration; an expected milestone that would ordinarily be publicly evidenced has not appeared, with no counter-evidence of continuing activity. |
| **Unverified** | Evidence is insufficient to assess progress. |

**Absence of news alone is not evidence that a project is Stalled.** In that case the condition is **Unverified**, and a data-gap entry is raised.

### 6.3 Required status fields

| Field | Description |
|---|---|
| `lifecycle_stage` | One value from §6.1 |
| `progress_condition` | One value from §6.2 |
| `status_evidence` | The specific evidence supporting stage and condition, with source IDs |
| `last_evidence_date` | Date of the most recent evidence of project activity |
| `status_assessed_date` | Date the status was last assessed |
| `status_confidence` | Confidence category (§2) |

### 6.4 Rules

- MoUs, LOIs and framework agreements never qualify a project above **Announced**.
- DFI board approval without a signed financing agreement does not qualify as **Financially committed**.
- Sponsor claims of progress (Tier 5, D-082) need corroboration before they can qualify a project for **Financially committed** or a later stage.
- When sources disagree about status, the disagreement is recorded in the contradiction register.
- **Transmission and interconnectors:** "Operational" requires evidence of energisation (not mechanical completion). Interconnector commercial activation is recorded separately (§5).
- **Multi-component projects** (e.g. mine + rail + port; plant + evacuation line): each component carries its own stage and condition.
- **Re-announced / renamed projects** are de-duplicated by location, capacity and sponsor; name history is kept in `alternative_names`.
- These rules apply equally to generation, storage, transmission, mining/industrial and infrastructure projects tracked in the project and entity registers.

## 7. Contradiction handling

The contradiction-resolution protocol — triggers, cause diagnosis, standing normalisation rules, resolution outcomes (`RESOLVED-DEFINITIONAL`, `RESOLVED-HIERARCHY`, `RESOLVED-ERROR`, `RANGE-CARRIED`, `OPEN`), materiality and escalation — is defined in `research_architecture.md` §H. Contradictions are never silently reconciled.

## 8. Analytical models

The forecasting and scenario architecture is defined in `research_architecture.md` §J (model specification finalised at Gates 5–6). All assumptions are recorded in the assumption register with basis and sensitivity range. Financial metrics (tariff, IRR, NPV, DSCR) are **not** in scope until Gate 7 and only if evidence supports them.

## 9. Language

Many Guinea primary sources are expected to be in French (inference; to be confirmed). Original-language titles and quotes are retained; translations are marked as such.

## 10. Date and number format

Dates: DD-MMM-YYYY. INR figures in Indian formatting (lakhs, crores). Other currencies in their conventional format with ISO code.

## 11. Opportunity classification (applied from Gate 7)

Opportunity assessment is split into two sequential steps (D-028; `research_architecture.md` §K):

1. **WS-27 — Country opportunity attractiveness (Alendei-neutral).** Proposed labels (P-011): *Highly attractive / Attractive / Conditionally attractive / Not currently attractive*. Frozen before WS-28 begins.
2. **WS-28 — Alendei pursuit classification**, applied to the frozen WS-27 portfolio:

| Classification | Meaning |
|---|---|
| **Tier 1 — Pursue immediately** | The evidence supports near-term action. |
| **Tier 2 — Develop** | The evidence supports further development work before a pursue decision. |
| **Tier 3 — Monitor** | Not actionable now; track for changes in conditions. |
| **Tier 4 — Do not pursue now** | The evidence does not support pursuit at present. This classification is valid and mandatory where warranted. |

Every classified opportunity carries an evidence chain to register entries. WS-28 cannot alter a WS-27 rating. The detailed qualification criteria for each tier are defined at Gate 7.

*Note: opportunity Tiers 1–4 are separate from evidence Tiers 1–6 (§1). Always use the full label (e.g. "Tier 2 — Develop") to avoid confusion.*

## 12. Research-question priority (planning classification)

Every research question in `workstream_charters.md` carries one qualitative **architectural research priority**:

| Priority | Planning meaning |
|---|---|
| **CRITICAL** | The answer is on the analytical critical path (`research_architecture.md` §D), or could by itself materially change the power-system picture or the opportunity screen. It must be addressed in Gate 2 discovery. |
| **HIGH** | Materially shapes a workstream's analysis. It must be addressed in Gate 2 discovery. |
| **MEDIUM** | Refines the analysis. It is addressed where sources allow. |
| **LOW** | Contextual. It is addressed if found in the course of other research. |

Rules:

1. Priority is a **research-planning classification**. It is **not** an evidence-based conclusion.
2. Priority must **not** be used as, or confused with, evidence confidence (§2) or source tier (§1).
3. Priority must **not** be treated or cited as a factual finding about Guinea.
4. Priority may be revised after evidence review. **Gate 4 reassesses priorities** against the actual evidence gaps and their decision impact, and records the changes in the data-gap register and the decision log.
5. No numerical materiality scores are assigned to questions before evidence exists.
6. Data-gap materiality (Material / Moderate / Minor, applied in the data-gap and contradiction registers) is assessed separately, on evidence, from Gate 3 onwards.
