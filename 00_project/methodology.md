# Methodology

**Version:** 0.1 · **Last updated:** 08-Oct-2026 · **Gate:** 0

## 1. Evidence hierarchy

| Tier | Class | Examples | Can stand alone as evidence? |
|---|---|---|---|
| 1 | Primary official | Laws, decrees, ministry / regulator / utility / system-operator reports, WAPP / ECOWAS official documents, signed agreements, statutory filings | Yes |
| 2 | Multilateral / DFI | World Bank, IFC, AfDB, EIB, IsDB, IMF, UN — appraisal and completion reports, diagnostics, databases | Yes |
| 3 | Data institutions / peer-reviewed | IEA, IRENA, academic literature | Yes, with definition check |
| 4 | Industry / corporate | Press releases, investor presentations, company disclosures | Only for that company's own facts; otherwise requires corroboration |
| 5 | Media / commentary | Trade press, news | No — corroboration required |
| 6 | Leads only | Gemini / AI output, unsourced web content | **Never** |

## 2. Confidence categories

| Category | Definition |
|---|---|
| **VERIFIED** | Confirmed directly in a Tier 1 or Tier 2 source, with metric definition and date clear. |
| **CORROBORATED** | Supported by two or more independent sources (at least one Tier 1–3) that agree within a stated tolerance, but no single definitive primary source located. |
| **ESTIMATED** | Derived by Claude or a cited source through a documented calculation or method from verified/corroborated inputs. Method recorded. |
| **INDICATIVE** | Single Tier 3–5 source, or source with unclear definition/date. Usable for context only; not for headline figures without a caveat. |
| **DATA GAP** | No adequate source located. Recorded in the data-gap register. |

Final deliverables: headline and decision-critical figures must be VERIFIED or CORROBORATED. ESTIMATED figures must show method. INDICATIVE figures must be visibly caveated. DATA GAP is stated as such.

## 3. Required metadata for every material statistic

| Field | Description |
|---|---|
| `data_id` | Unique ID (e.g. `GEN-0001`) |
| `workstream` | One of the 20 workstreams |
| `metric` | Metric name |
| `metric_definition` | Precise definition (see §5) |
| `value` | Numeric value |
| `unit` | Unit (MW, MW-DC, MW-AC, GWh, %, USD, INR, etc.) |
| `geography` | Country / region / site |
| `period` | Date or year the value refers to |
| `source_id` | Link to source register |
| `source_publication_date` | Where available |
| `source_url_or_reference` | URL, document reference, page/table |
| `confidence` | VERIFIED / CORROBORATED / ESTIMATED / INDICATIVE / DATA GAP |
| `cross_check` | Other sources consulted and their values |
| `contradiction_id` | If applicable |
| `verified_by` / `verified_date` | Agent and date |
| `notes` | Caveats |
| `status` | ACTIVE / SUPERSEDED (with `superseded_by`) |

## 4. Registers

| Register | Location | Purpose |
|---|---|---|
| Source register | `03_evidence/source_register/` | Every source, with the fields in §4.2. |
| Master data register | `03_evidence/master_data_register/` | Every material data point with §3 metadata. |
| Contradiction register | `03_evidence/contradictions/` | Conflicting values: data IDs, sources, values, likely cause (definition, date, scope, error), resolution status, governing value and reasoning. |
| Data-gap register | `03_evidence/data_gaps/` | Unanswered questions: workstream, question, materiality, sources tried, proposed next step, status. |
| Opportunity register | `06_opportunities/` | Opportunities with evidence chain and classification (§11; Gate 7). |

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
- Sponsor claims of progress (Tier 4) need corroboration before they can qualify a project for **Financially committed** or a later stage.
- When sources disagree about status, the disagreement is recorded in the contradiction register.

## 7. Contradiction handling

1. Record both (or all) values with full metadata.
2. Diagnose the likely cause: definition difference, period difference, scope difference, unit difference, transcription error, genuine disagreement.
3. Apply the hierarchy: higher tier → more recent → more specific → better-defined.
4. Record the governing value **and** the reasoning; retain the non-governing values.
5. Unresolved material contradictions are disclosed in deliverables.

## 8. Analytical models (to be specified at Gate 5)

Model specifications (supply-demand balance, reliability, demand projection, resource assessment, opportunity screening) will be defined at Gate 5. All assumptions will be listed, sourced and labelled. Financial metrics (tariff, IRR, NPV, DSCR) are **not** in scope until Gate 7 and only if evidence supports them.

## 9. Language

Many Guinea primary sources are expected to be in French (inference; to be confirmed). Original-language titles and quotes are retained; translations are marked as such.

## 10. Date and number format

Dates: DD-MMM-YYYY. INR figures in Indian formatting (lakhs, crores). Other currencies in their conventional format with ISO code.

## 11. Opportunity classification (applied from Gate 7)

| Classification | Meaning |
|---|---|
| **Tier 1 — Pursue immediately** | The evidence supports near-term action. |
| **Tier 2 — Develop** | The evidence supports further development work before a pursue decision. |
| **Tier 3 — Monitor** | Not actionable now; track for changes in conditions. |
| **Tier 4 — Do not pursue now** | The evidence does not support pursuit at present. This classification is valid and mandatory where warranted. |

Every classified opportunity carries an evidence chain to register entries. The detailed qualification criteria for each tier are defined at Gate 7.

*Note: opportunity Tiers 1–4 are separate from evidence Tiers 1–6 (§1). Always use the full label (e.g. "Tier 2 — Develop") to avoid confusion.*
