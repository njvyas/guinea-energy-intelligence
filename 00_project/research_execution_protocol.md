# Research Execution Protocol

**Version:** 1.0 (APPROVED at Gate 2A, D-057; Gate 2A decisions incorporated) · **Last updated:** 08-Oct-2026 · **Gate:** 2A

**Approved baseline:** Research Architecture v1.0. Commit `a255d4f`, tag `gate-01-research-architecture`.

This protocol defines how research missions are executed, captured, verified, reconciled, challenged and accepted. It **operationalises** the approved Gate 1 architecture and does not amend it.

**Order of precedence:**

1. `methodology.md` (evidence, metric and status definitions);
2. `research_architecture.md` (registers, handoff, contradiction, scenario, screening and GIS architecture);
3. `workstream_charters.md` and `gemini_mission_briefs.md`;
4. this protocol.

Where this protocol needs something Gate 1 does not settle, the gap is recorded as a **Gate 2A pending decision** (§21) rather than by changing the Gate 1 text. This document contains **no Guinea findings**.

---

## 0. Gate 2 structure and the Gate 2A boundary

Gate 2 (Discovery research) is carried out as four sequential sub-gates, each needing its own explicit approval (D-055):

| Sub-gate | Purpose | Produces | Does NOT |
|---|---|---|---|
| **2A — Research Execution Protocol** | Define how research is executed, captured, verified, reconciled, challenged and accepted | This protocol and pointer updates in governance documents | Create registers, run research, validate Guinea facts, start missions |
| **2B — Register templates** | Create empty XLSX register templates from the approved schemas (`research_architecture.md` §G; `methodology.md` §3, §4.2, §6.3), applying the 2A decisions (§21) | Empty templates, with no rows of data | Populate data, run research |
| **2C — Mission packages** | Compile and validate an executable package for each mission: instructions, brief, output contract, prompt version | Archived mission packages in `01_gemini_research/00_architecture/` | Run missions |
| **2D — Research execution authorisation** | Authorise the running of missions and Claude's independent discovery, wave by wave; accept discovery outputs | Raw artifacts, lead and source registrations, Mission Reconciliation Reports | Accept evidence into analysis (that happens at Gates 3–4) |

**Gate 2A boundary:** Gate 2A produces this protocol only. It creates no registers, runs no research, validates no Guinea facts and starts no Gemini mission.

---

## 1. Mission lifecycle

| # | Stage | Actor | Input | Output | Gate | Exit condition |
|---|---|---|---|---|---|---|
| 1 | **Mission definition** | Claude Code (draft); User + ChatGPT (approve) | Charter questions, mission brief | Mission package: prompt version `GEM-NN-Pv<N>` | 2C | Package validated and approved |
| 2 | **Gemini execution** | Operator runs Gemini | Approved package | Gemini output that meets the contract (§12) | 2D | Output returned |
| 3 | **Raw artifact capture** | Operator deposits; Claude fingerprints | Gemini output | Immutable artifact, `.meta.md` sidecar, SHA-256 (§13) | 2D | Fingerprint recorded; contract conformance checked |
| 4 | **Source registration** | Claude Code | The artifact's source roster | Source register rows (`SRC-`), state CANDIDATE_SOURCE | 2D | Every cited source registered or flagged CITATION NOT FOUND |
| 5 | **Evidence extraction** | Claude Code | The artifact's findings and tables | Lead register rows (`LEAD-`), state RAW_LEAD | 2D | Every material claim extracted, with its claim ID |
| 6 | **Primary-source verification** | Claude Code | Retrieved sources | Lead outcome; candidate MDR, project and entity records (EXTRACTED or VERIFIED) | 2D → 3 | Each material lead has an outcome (§3.3) |
| 7 | **Cross-source corroboration** | Claude Code | Independent sources | CORROBORATED, or the confidence is held at its existing level | 3 | Corroboration attempted for each material value lacking a Tier 1–2 source |
| 8 | **Contradiction identification** | Claude Code | All values for the same metric, entity, geography and period | Contradiction register rows (`CON-`) | 3 → 4 | Every difference diagnosed under the D-072 comparability tests; every contradiction logged (§10) |
| 9 | **Data register integration** | Claude Code | Validated items | Register records with `acceptance_status = PROPOSED` (D-062) | 3 | Records complete; provenance traceable |
| 10 | **Analytical use (provisional)** | Claude Code | PROPOSED records | "Proposed analytical implications" in the reconciliation report **only** | 2D–4 | Nothing in `04_analysis/` uses records that have not been accepted |
| 11 | **Claude reconciliation** | Claude Code | Stages 3–10 | Mission Reconciliation Report (§14.1) | 2D (discovery); 3–4 (evidence) | Report complete |
| 12 | **ChatGPT / owner challenge** | User + ChatGPT | Reconciliation report | Challenge log and Claude's responses (§14.2) | 2D; 3–4 | Every challenge answered |
| 13 | **Mission acceptance** | User + ChatGPT | Report and challenge log | Acceptance recorded in the decision log; records move to `ACCEPTED` | 2D (discovery); 3–4 (evidence) | Acceptance criteria met (§15); explicit approval given |

**Mapping to Gate 1.** Stages 3–8 and 11 correspond to the handoff steps in `research_architecture.md` §F, steps [1]–[7]. Stage 10 corresponds to step [8], which may consume **accepted** register entries only. Under the Gate 1 gate sequence:

- Gate 2 covers discovery (stages 1–6 for leads and sources).
- Gate 3 covers evidence consolidation (stages 6–9).
- Gate 4 covers the contradiction and data-gap audit (stage 8).
- Gates 5–6 cover analytical use.

Mission acceptance therefore happens at **two levels** (D-062): discovery acceptance at Gate 2D, and evidence acceptance at Gates 3–4.

---

## 2. Roles

| Role | Responsibility | Never |
|---|---|---|
| Operator (project owner or delegate) | Runs approved packages in Gemini; deposits outputs unchanged; records execution metadata | Edits Gemini output; runs unapproved packages |
| Gemini | Produces leads that meet the output contract | Is treated as a source of evidence |
| Claude Code | Fingerprints, extracts, registers, verifies, corroborates, diagnoses contradictions, writes reconciliation reports, maintains registers | Edits raw artifacts; promotes unverified claims; accepts its own work |
| ChatGPT / project owner | Challenges independently; approves gates and acceptance | Is bypassed |

---

## 3. Evidence-state lifecycle

### 3.1 States

States A–I are the nine evidence states approved at Gate 1 (`methodology.md` §2.2; D-032). State J is the Gate 1 lead-register outcome `UNSUPPORTED` (`research_architecture.md` §F). It is a final lead outcome, **not** a tenth evidence state (D-058).

| | State | Code | Definition | Where it may exist | Usable in analysis? |
|---|---|---|---|---|---|
| A | Research lead | `RAW_LEAD` | A claim from Gemini, a discovery note or another unverified origin | Lead register only | **No** |
| B | Candidate source | `CANDIDATE_SOURCE` | A source identified (cited or found) but not yet retrieved and checked | Source register only | **No** |
| C | Extracted evidence | `EXTRACTED` | A value read from a retrieved source that does not yet meet the VERIFIED or CORROBORATED rule. Confidence is INDICATIVE | MDR / project / entity registers | Context only, caveated, once accepted |
| D | Verified evidence | `VERIFIED` | Confirmed directly in a Tier 1, 2 or 3 source (D-082), with clear definition, date and geography | Registers | Yes, once accepted |
| E | Corroborated evidence | `CORROBORATED` | Two or more **independent** sources (at least one Tier 1–4) agree: the values are identical, or differ only by demonstrable reporting precision under D-072 (§11.3) | Registers | Yes, once accepted |
| F | Estimate | `ESTIMATE` | Derived by a documented method from accepted inputs. Confidence is ESTIMATED | Registers and the assumption register | Yes, labelled, once accepted |
| G | Analytical inference | `INFERENCE` | A judgement drawn from evidence | Analysis documents only, labelled "Inference" | As inference only. Never as data |
| H | Unresolved contradiction | `CONTRADICTED_UNRESOLVED` | Subject to an OPEN or RANGE-CARRIED contradiction | Registers, with a `contradiction_id` | RANGE-CARRIED: as a range only. OPEN: not in headlines |
| I | Data gap | `DATA_GAP` | Sought through the defined search path (§17) but not found | Data-gap register | Stated as a gap |
| J | Unsupported claim | lead outcome `UNSUPPORTED` | The lead's cited source does not exist or cannot be located, does not contain the claim, or contradicts it | Lead register only (terminal outcome) | **No.** Recorded permanently, never deleted |

### 3.2 Allowed transitions

| From | To | Condition (all must hold) | Recorded by |
|---|---|---|---|
| — | RAW_LEAD | A material claim is extracted from a deposited artifact or discovery note, with its claim ID and the source as cited | Lead register row |
| — | CANDIDATE_SOURCE | A source is cited or identified | Source register row |
| CANDIDATE_SOURCE | (retrieved) | The document is located and opened. The access date is recorded. The archive decision is made (§18) | Source register update |
| RAW_LEAD | EXTRACTED | Claude locates the claim in a **retrieved** source. The exact page, table or section is recorded, and the value, unit, period, geography and definition are captured. The source is Tier 4–5, or Tier 1–3 with an unclear definition, date or geography | New MDR, project or entity record; lead outcome PARTLY VERIFIED or VERIFIED |
| RAW_LEAD or EXTRACTED | VERIFIED | The value is found **exactly** (or within a stated rounding) in a Tier 1–3 source, and the metric definition, period and geography match the claim | Record updated |
| EXTRACTED | CORROBORATED | Two or more independent sources agree (identical, or differing only by demonstrable reporting precision after the D-072 comparability tests), and at least one of them is Tier 1–4. The independence test in §11.3 is passed | Record updated, with `cross_check` populated |
| Accepted inputs | ESTIMATE | The method is documented, the inputs are accepted DAT IDs, the assumptions are recorded in the assumption register, and the result is labelled ESTIMATED | New DAT record and ASM entries |
| Any registered value | CONTRADICTED_UNRESOLVED | A difference not explained by the D-072 tests is logged with outcome OPEN or RANGE-CARRIED | CON row; `contradiction_id` set |
| CONTRADICTED_UNRESOLVED | VERIFIED / CORROBORATED / EXTRACTED | The contradiction is resolved as RESOLVED-* with reasoning recorded (§10) | CON row closed; record updated |
| RAW_LEAD | UNSUPPORTED (outcome) | The cited source cannot be found after the search path in §17, does not contain the claim, or contradicts it | Lead outcome, with reason |
| RAW_LEAD | DATA_GAP | The claim cannot be verified **and** the underlying question remains material | GAP row; lead outcome NOT VERIFIABLE |
| Any state | (supersession) | A newer, better or corrected value is accepted | The old record is marked SUPERSEDED with `superseded_by`. **It is never deleted** |

### 3.3 Prohibited transitions

- RAW_LEAD can never move directly to VERIFIED or CORROBORATED without retrieval of the source by Claude.
- A citation alone never makes a claim verified (§4.1).
- Several Tier 5–6 sources can never create CORROBORATED (§11.3).
- ESTIMATE can never be upgraded to VERIFIED, however good its inputs are.
- INFERENCE can never be stored as a data point.
- UNSUPPORTED can never re-enter as data. A new lead with an independent source must be created instead.
- A record with `acceptance_status ≠ ACCEPTED` can never be used in `04_analysis/`, `05_gis/` or any deliverable.

**Lead outcomes** (Gate 1 set): VERIFIED · PARTLY VERIFIED · CONTRADICTED · UNSUPPORTED · NOT YET CHECKED. This protocol adds **NOT VERIFIABLE**, used when a lead is closed into a data gap (D-058).

---

## 4. Source discipline

### 4.1 A citation alone does NOT make a claim verified

A claim is verified only when Claude has:

1. retrieved the cited document, or an authoritative copy of it;
2. located the exact passage, table or figure;
3. confirmed that the value, unit, period, geography and metric definition match the claim;
4. recorded the page, table or section and the access date.

If any one of these steps fails, the claim stays a lead, or becomes PARTLY VERIFIED, CONTRADICTED or UNSUPPORTED.

### 4.2 Required fields for every material claim

These fields implement `methodology.md` §3 and §4.2 and D-033.

| Field | Required | Notes |
|---|---|---|
| Source ID (`SRC-`) | Always | |
| Source title (original language) | Always | Translations marked as such |
| Publisher / institution | Always | |
| Document type | Always | §4.4 categories |
| Publication date | Where available | "Undated" recorded explicitly |
| Access date | Always | DD-MMM-YYYY |
| URL or persistent reference | Always | DOI, document number or archive reference where there is no URL |
| Page / section / table | Where the document has them | Mandatory for VERIFIED |
| Geography | Always | §7 level code |
| Period or year covered | Always | Separate from the publication date (§6.1) |
| Metric / value / unit | For quantitative claims | §5 |
| Definition | Always | `methodology.md` §5 and §8 terms |
| Source tier | Always | 1–6 |
| Discloser independence | Always | `methodology.md` §1 |
| Evidence state | Always | §3 |
| Confidence | Always | §11 |
| Cross-check status | Always | NOT ATTEMPTED / AGREES / DISAGREES / NO INDEPENDENT SOURCE |
| Contradiction status | Always | NONE / OPEN / RESOLVED-* / RANGE-CARRIED |

### 4.3 Preferring primary sources

1. **Search order:** Guinea government / primary institutional (Tier 1) → WAPP / ECOWAS / regional institutional (Tier 2) → DFIs, IMF and UN (Tier 3) → data institutions, science and engineering (Tier 4) → corporate and project disclosures (Tier 5). Media and trade press are secondary reporting and discovery sources, used to find leads and trace primary sources (D-086).
2. **Trace upward.** When a secondary source cites a primary one, the primary source is sought and verified directly. The secondary source is recorded as the pointer.
3. **Prefer French-language official sources** where they are the original.
4. **Do not substitute down.** When a primary source exists but cannot be accessed, that fact is recorded (§17). A lower-tier source may then be used only under §4.4, at the confidence it merits, and with the access limitation stated.

### 4.4 Treatment by source type

Tiers follow the authoritative hierarchy (D-082; `methodology.md` §1).

| Source type | Tier | Can it stand alone? | Conditions |
|---|---|---|---|
| Guinea laws, decrees, official gazette, regulator decisions | 1 | Yes | Check that it is the latest amendment (§6.4) |
| Guinea ministry, utility and system-operator reports and statistics | 1 | Yes | Discloser = OFFICIAL_SELF_REPORTED; methodology noted |
| Guinea supreme audit institution; EITI reconciliation reports | 1 | Yes | INDEPENDENT_AUDITED |
| Government-published agreements and award notices | 1 | Yes | |
| WAPP / ECOWAS / regional regulator / interconnector-operator / basin-organisation documents | 2 | Yes | |
| DFI project documents (appraisal, status, completion), IMF staff reports, UN agency reports, DFI databases | 3 | Yes | Distinguish appraisal-stage projections from completion-stage outturns |
| Data institutions (IRENA, IEA, Global Energy Monitor, Ember, NREL), resource atlases, NASA/NOAA/Copernicus datasets, peer-reviewed research, engineering studies | 4 | Yes, with a definition check (single source = INDICATIVE) | Record the dataset version or vintage. Imputed or estimated cells are labelled ESTIMATED |
| OEM / EPC / IPP / mining-company disclosures, investor presentations, project-finance disclosures, tenders, corporate statutory filings | 5 | Only for the issuer's **own disclosed** facts (ownership, production, capacity, financials, project commitments, contracts, project status) — never for unrelated government, grid, regulatory or national-system facts (D-086; VR-31) | SELF_REPORTED_PROMOTIONAL or OFFICIAL_SELF_REPORTED; forward-looking statements classified as targets (§6.2); announcements ≠ commitment (§9) |
| News and trade press | Secondary reporting — not an evidence tier (D-086); recorded as tier 5, document type NEWS_ARTICLE / TRADE_PRESS | **No.** It may identify leads, point to primary sources, give context and corroborate chronology or public reporting; it must not independently establish a material quantitative or legal claim where a suitable primary/authoritative source is reasonably available (VR-30) | Several reports from one underlying source count as **one** source |
| Wikipedia, aggregators, blogs, social media | 6 (lead) | **Never** | May point to sources only |
| Gemini or any AI output | 6 (lead) | **Never** | Always enters as RAW_LEAD |

### 4.5 When a secondary source can be accepted

A Tier 4–5 source may support a material register value only when **all** of the following hold:

- (a) the primary source has been sought along the §17 path, and the search is recorded;
- (b) the value is labelled at the confidence it merits: INDICATIVE alone, or CORROBORATED only under §11.3;
- (c) the definition, period and geography are explicit, or the gap is recorded;
- (d) the limitation is visible wherever the value is used.

Tier 5 sources are authoritative only for the issuer's own facts. Even then, progress claims need corroboration before a project can be staged at Financially committed or later (`methodology.md` §6.4).

---

## 5. Quantitative data rules

### 5.1 Mandatory attributes for every material quantitative value

These apply where relevant: value · unit · currency · nominal or real basis (with base year) · year or date · geography (§7) · metric definition · AC/DC basis · capacity or energy class (installed / available / dependable / dispatched / delivered / consumed) · source (`SRC-` and location) · evidence state · confidence.

**No number may enter the Master Data Register without traceable provenance:** a `SRC-` ID with page, table or section, or, for an ESTIMATE, the input DAT IDs plus the method and assumptions.

### 5.2 Unit and basis rules

| Topic | Rule |
|---|---|
| **MW vs MWp** | MWp (peak, at standard test conditions) is a DC rating for PV and is recorded as **MW-DC**, with the source's original label kept. It is never treated as MW-AC. |
| **MW-AC vs MW-DC** | Both are recorded where available (`methodology.md` §5). Where a source does not state the basis, the value is recorded as **basis unstated**, flagged, and confidence is downgraded under definition consistency. Converting between them requires a documented DC/AC ratio, which makes the result an ESTIMATE. |
| **MWh vs GWh vs TWh** | Exact unit identities. They may be normalised within a record. The original unit is kept in the notes. |
| **Annual vs dependable generation** | Annual (actual) generation, expected average generation and firm or dependable energy are distinct metrics in separate records. Hydro dependable output is stated by season or month (D-037). |
| **Installed vs available vs dependable vs dispatched** | Distinct metrics (`methodology.md` §5). They are never substituted for each other. When a source uses "capacity" without qualification, the value is recorded as **class unstated** and its use is restricted until the class is resolved. |
| **Tariff vs cost** | A tariff (the regulated or contracted price charged) is never equated with a cost (cost of supply, generation cost, LCOE). Customer class, tariff component (energy, capacity, fixed) and taxes are stated. |
| **Nominal vs real currency** | Values are recorded as reported, in nominal terms, with their year. Real-terms values require a deflator source and base year (P-024), recorded in the assumption register. Real values are ESTIMATES. |
| **Exchange-rate conversion** | The original currency value is the record of truth. A converted value is a separate **ESTIMATE** record that cites the original value and an **FX_RATE** record. The FX_RATE record is a Master Data Register record with its own provenance, rate type and source class (D-070). **Source preference:** official central-bank rate → IMF IFS → World Bank WDI → other documented source; a transaction document's own rate is used where the source transaction states one. **Rate type:** period average for flows, end of period for stocks. **Cross rates:** a direct published rate, or otherwise via USD with both rates recorded. |
| **Estimates** | They carry a method, input DAT IDs, assumptions (ASM) and a sensitivity range where material. They are never presented as verified. |
| **Ranges** | A range reported by a source is stored as low/high with the source's own range definition. A midpoint is computed only as an analytical ESTIMATE, labelled as such. Ranges arising from contradictions follow §10.4. |
| **Percentages** | The numerator, denominator and base year are stated. Percentage-point changes are never reported as percent changes. Shares are recorded with the total they are a share of. Rates (e.g. losses, access) state their definition (`methodology.md` §5). |
| **Derived calculations** | Any value computed from others (sums, ratios, per-capita figures, conversions other than exact identities) is a new **ESTIMATE** record citing its inputs. A sum of records with mixed confidence takes the **lowest** input confidence, capped at ESTIMATED. |
| **Rounding and precision** | The source's precision is preserved. No precision is added. Values reported as "about" or "approximately" are recorded with that qualifier. |
| **Aggregates vs components** | When a national total disagrees with the sum of its parts, both are kept and the difference is logged as a contradiction (definition or scope). |

---

## 6. Temporal rules

### 6.1 Four dates, never merged

| Date | Meaning |
|---|---|
| `period` | The time the value describes (year, month, season or point in time) |
| `source_publication_date` | When the source was published |
| `access_date` | When Claude retrieved it |
| `status_as_of` (projects and entities) | The date to which a status claim applies. It is recorded in the project register as `last_evidence_date` and `status_assessed_date` (`methodology.md` §6.3) |

### 6.2 Temporal classification of every claim

| Class | Meaning | Study horizon |
|---|---|---|
| HISTORICAL | An observed outturn for a past period | 2016–2026 |
| CURRENT STATUS | The state as of a stated date | As of `status_as_of` |
| COMMITTED / UNDER CONSTRUCTION | Future additions with Financially committed or Under construction evidence | 2027–2030 near-term |
| PLANNED | Active development, Announced or Proposed | 2027–2030 and 2030–2035 |
| TARGET / ASPIRATION | A policy target or corporate ambition with no project-level commitment | 2030–2035 strategic |
| PROJECTION | A forecast from a third party (method recorded) or from this project (ESTIMATE) | 2027–2035 |

Targets and projections are never recorded as plans or commitments.

### 6.3 Handling changes over time

| Situation | Rule |
|---|---|
| **Historical snapshots** | Each period's value is a separate record. An earlier year is not overwritten with a later one. |
| **Current status** | Always stated "as of" a date, citing the evidence that supports it. |
| **Project announcements** | Recorded as Announced at most. The announcement date and the announcing party are recorded. |
| **Project revisions** (capacity, date, sponsor) | A new record or field version is created. The earlier version is SUPERSEDED, not deleted. The name history is kept in `alternative_names`. |
| **Cancellations** | Require an official termination, withdrawal or revocation (`methodology.md` §6.1). |
| **Delays** | Require a missed published milestone or an official revised schedule (`methodology.md` §6.2). |
| **Superseded information** | Kept, marked SUPERSEDED, with a pointer. The newer value governs only if it passes the §10 hierarchy. |
| **Conflicting dates** | Handled as a contradiction (§10). Cause categories: period mismatch; announcement vs execution date; target vs actual date. |
| **Changing tariffs and regulations** | Each version is recorded with its effective date and instrument. The "current" version is determined at Gate 9 re-verification (§6.4). |
| **Stale information** | Information is not stale merely because of its age. Recency is a quality dimension (`methodology.md` §2.1) and is assessed against how likely the data class is to change. |

### 6.4 Revalidation by data category (D-048, with no universal time threshold)

**No universal expiry period applies.** Revalidation is triggered by events, by data category:

| Data category | Revalidation trigger |
|---|---|
| Tariffs and tariff schedules | Before any analytical use at Gates 5–7; mandatory at Gate 9; whenever any source refers to a newer schedule |
| Laws, decrees, regulations | Check for amendments before acceptance at Gate 3; mandatory at Gate 9 |
| Institutional mandates and existence of bodies | At Gate 3 acceptance; at Gate 9; whenever restructuring is reported |
| FX and repatriation rules | At Gate 3 acceptance; mandatory at Gate 9 |
| Project lifecycle stage and progress condition | At each gate where the project is used (5, 6, 7) and mandatory at Gate 9. The progress condition is reassessed whenever new evidence appears. |
| Ownership and sponsorship | At Gate 3 acceptance; at Gate 9 |
| Exchange rates used for conversion | When a conversion is created; at Gate 9 for deliverable figures |
| Historical outturns (generation, consumption, finances for closed periods) | Only when a revised edition of the source is known or likely to exist (e.g. restated accounts, revised statistics) |
| Physical resource data (e.g. irradiance, wind, hydrology series) | When a new dataset version is released or a longer series becomes available |

---

## 7. Geographic rules

### 7.1 Geographic levels

Each claim carries one `geo_level` code, from the controlled list `v_geo_level` in `register_schema.md` (D-067). The list keeps the Gate 1 codes and adds finer levels.

| Level | Code |
|---|---|
| Guinea, national | NATIONAL_AGGREGATE |
| Administrative region | REGIONAL |
| Prefecture | PREFECTURE |
| Sub-prefecture / commune / locality | LOCALITY |
| City / urban area | CITY |
| Mining site | MINING_SITE |
| Industrial site | INDUSTRIAL_SITE |
| Port | PORT |
| Generation (or storage) site | PLANT_SITE |
| Transmission corridor | TRANSMISSION_CORRIDOR |
| Substation | SUBSTATION_NODE |
| WAPP interconnection | INTERCONNECTION |
| River basin / catchment | RIVER_BASIN |
| Neighbouring or benchmark country | NEIGHBOURING_COUNTRY |
| Regional (multi-country) aggregate | MULTI_COUNTRY_REGION |
| Other (explained in notes) | OTHER |

Rules:

- Values at different levels are never summed or compared without stating the level.
- A national figure is never taken to represent a site.
- Site-level records carry coordinates where available, with the CRS stated (`research_architecture.md` §L.3).

### 7.2 Neighbouring and benchmark countries

Information about another country is collected only when it meets one of these tests:

- **(a) Benchmark metric:** it is one of the regional benchmark metrics B1–B13 (`research_architecture.md` §M) for the approved benchmark universe.
- **(b) Direct effect on Guinea:** it materially affects Guinea's energy system, market, infrastructure, supply, demand or investment environment. Examples: an interconnector counterparty, a shared basin, cross-border trade, a regional project that includes Guinea, or a competing source of supply or demand.

Each such record states which test it meets. Generic West African material that meets neither test is out of scope.

---

## 8. Energy-system terminology

This section supplements `methodology.md` §5. Where the two overlap, the methodology governs. Each term below is a separate category; **values in different categories are never mixed or substituted for one another.**

### 8.1 Generation

| Term | Definition | Not to be confused with |
|---|---|---|
| Installed | Nameplate rating of commissioned plant (AC/DC stated for PV) | Available, dependable |
| Available | Capacity not on planned or forced outage at a given time | Installed |
| Dependable | Capacity reliably available at system peak, after hydrology, fuel and derating | Available; annual average |
| Dispatched | Output actually being produced at a given time | Available |
| Generated (energy) | Gross or net (stated) energy at the plant terminals | Delivered, consumed |
| Delivered | Energy delivered to the distribution system or to customers after transmission losses | Generated |
| Consumed | Energy billed or metered at the point of end use (billed vs consumed stated) | Delivered |

### 8.2 Grid

| Term | Definition |
|---|---|
| Transmission | The high-voltage network as defined by the national utility or grid code (voltage threshold as stated in the source) |
| Distribution | The medium- and low-voltage network below the transmission threshold |
| Capacity (line / corridor) | Transfer capability stated with its basis: thermal, stability or contractual |
| Thermal limit | The maximum continuous current or power of a conductor or equipment under stated ambient conditions |
| Transformer rating (MVA) | Nameplate apparent-power rating; loading recorded separately, as a percentage of the rating, with the date |
| N-1 | The ability to withstand the loss of any single element without unacceptable loading or voltage. Stated only where a study or operator document assesses it |
| Congestion | A documented instance in which transfer was limited below demand or below dispatch need, with its location and period |
| Reactive power / voltage stability | Documented voltage-control capability, voltage excursions, or reactive compensation (installed or planned) |
| Frequency | Documented frequency performance, reserve practice and protection arrangements |
| Losses | Partitioned as transmission technical, distribution technical and non-technical, with the measurement method stated (`methodology.md` §5) |

### 8.3 Hydro

| Term | Definition |
|---|---|
| Installed capacity | Nameplate rating |
| Seasonal output | Energy or capacity by month or season |
| Dependable output | The seasonal dependable capacity (`methodology.md` §5), stated per season or month, with the season definitions taken from the source |
| Dry-season derating | The reduction from installed to dependable capacity during low-flow periods, as documented |
| Reservoir constraints | Storage volume, operating levels and release rules (including obligations under basin agreements), as documented |
| Hydrology | Inflow series and their period, gauge and quality |
| Spill / curtailment | Recorded **only where evidence documents it**, with period and cause. It is never inferred from capacity versus demand |

### 8.4 WAPP and interconnection

The technical status of an interconnector is recorded as five **distinct** project-register steps: `ic_constructed`, `ic_energised`, `ic_synchronised`, `ic_operational`, `ic_commercially_active`. Each has its own value, evidence sources and date. The steps are never collapsed into a single status (D-069; VR-20). Each step requires its own evidence:

| Status | Evidence required |
|---|---|
| Physically constructed | Mechanical completion of the line and substations |
| Energised | Evidence that it has been energised (`methodology.md` §6.4) |
| Synchronised | Documented synchronous operation with the connected system(s) |
| Operational | In regular service; the lifecycle stage "Operational" requires at least energisation |
| Commercially active | Contracted and metered cross-border transactions |
| Contracted / imported / exported power | MW and MWh by direction, period and contract, from metered or settlement data |

**Physical completion never implies commercial operation or trading.**

### 8.5 Mining and industrial energy

| Term | Definition |
|---|---|
| Extraction | Mining and haulage of ore (e.g. run-of-mine operations) |
| Processing | Beneficiation (crushing, washing, drying) at or near the mine |
| Refining | Chemical or metallurgical transformation (e.g. alumina refining). Its electrical and thermal (steam) demand is recorded separately |
| Captive generation | Generation owned or contracted on site for the site's own use (capacity, fuel and technology stated) |
| Grid supply | Supply from the public grid (connection voltage and contracted demand stated) |
| PPA | A contracted supply agreement (counterparty, tenor, currency and structure, where public) |
| BESS | Storage installed at a site (MW and MWh stated separately) |
| Thermal fuel supply | Fuel type (diesel, HFO or other), volume and delivered-cost evidence (WS-03) |

Extraction, processing and refining loads are never aggregated without showing their components (D-036).

---

## 9. Project-status rules

The approved two-dimensional framework is used unchanged (`methodology.md` §6; D-022, D-030):

- **Lifecycle stage:** Proposed → Announced → Active development → Financially committed → Under construction → Operational. **Cancelled** is a final stage.
- **Progress condition:** On track · Delayed · Stalled · Unverified.

### 9.1 Evidence required for each lifecycle transition

| Transition | Minimum evidence (any one, unless "and" is stated) |
|---|---|
| → Proposed | Inclusion in a plan, master plan, study or pipeline list |
| Proposed → Announced | A public declaration by a named sponsor or a government body of a specific project. An MoU, LOI or framework agreement **at most** qualifies here |
| Announced → Active development | Documented development work: feasibility or ESIA commissioned or completed; site rights; a permit or licence applied for or granted; grid studies; PPA or concession negotiation; procurement launched; DFI preparation |
| Active development → Financially committed | Financial close; or a signed financing agreement (board approval alone does not qualify); or a binding EPC contract with confirmed funding; or a budget allocation backed by a signed contract |
| Financially committed → Under construction | Notice to proceed **and** evidence of site works |
| Under construction → Operational | Commissioning, energisation or COD evidence. Partial commissioning is recorded with the portion specified. For transmission, energisation evidence is required |
| Any → Cancelled | An official termination, withdrawal, revocation or DFI cancellation |

### 9.2 Progress condition

- **Delayed:** a missed published milestone, or an official revised schedule.
- **Stalled:** **positive evidence** that progress has stopped or is blocked (`methodology.md` §6.2).
- **Silence, or a lack of recent news, never means Stalled.** The condition is then **Unverified**, and a data-gap entry is raised.
- **Unverified:** the evidence is insufficient to assess progress.

### 9.3 Rules

- Sponsor progress claims (Tier 5) need corroboration before a project can be staged at Financially committed or later.
- Each component of a multi-component project carries its own status.
- Re-announced projects are de-duplicated by location, capacity and sponsor.
- Disagreements about status between sources are logged as contradictions.

---

## 10. Contradiction protocol

This section operationalises `research_architecture.md` §H. The outcome set approved at Gate 1 is used unchanged.

### 10.1 Trigger

**No universal numerical contradiction tolerance is assumed (D-072).** No arbitrary percentage tolerance is ever introduced. When two values for the same metric, entity, geography and period differ, the following are tested first:

1. definition;
2. date or period;
3. geography;
4. scope;
5. unit;
6. AC/DC basis;
7. installed / available / dependable / dispatched / delivered / consumed basis;
8. methodology;
9. source precision.

A difference may be classified as **rounding or reporting precision only** when all three of these hold:

- (1) the underlying definitions are comparable;
- (2) the periods, geography and scope are comparable;
- (3) the difference is demonstrably attributable to reporting precision.

In that case the cause is `REPORTING_PRECISION` and the justification is recorded. Otherwise, the contradiction is preserved, or a range is carried where the sources are comparable and none can reasonably be preferred (§10.4). Any difference in a categorical value or a status is a contradiction. The tests are listed in the contradiction register's DIFFERENCE_TESTS sheet.

### 10.2 Diagnosis: cause codes

These are the Gate 1 causes, plus METHODOLOGY and SUPERSEDED (marked †, added by D-068) and REPORTING_PRECISION (marked ‡, added by D-072). The full list is `v_cause_code` in `register_schema.md`.

| Cause code | Meaning |
|---|---|
| DEFINITION | The values measure different metrics (e.g. installed vs dependable; MW-AC vs MW-DC) |
| PERIOD | Different period or season |
| SCOPE (geography) | Different geographic or asset scope |
| UNIT / CURRENCY | Different unit, currency or price basis |
| STATUS-INTERPRETATION | E.g. constructed vs energised; MoU vs commitment |
| DUPLICATION | The same project under different names |
| TRANSCRIPTION | A copying or calculation error |
| METHODOLOGY † | Different measurement or estimation methods for the same nominal metric |
| SUPERSEDED † | A later edition or revision of the same source or series |
| REPORTING_PRECISION ‡ | Difference demonstrably attributable to reporting precision. Permitted only when all three D-072 conditions are met (§10.1) |
| GENUINE | A real disagreement between credible sources |

### 10.3 Outcomes and how the owner's categories map to them

| Owner-listed category | Gate 1 outcome |
|---|---|
| Source hierarchy resolution | `RESOLVED-HIERARCHY` (higher tier → more recent → more specific → better defined) |
| Definition mismatch | `RESOLVED-DEFINITIONAL` (both retained as separate metrics) |
| Date mismatch | `RESOLVED-DEFINITIONAL` if the values describe different periods; otherwise assessed under the hierarchy |
| Geography mismatch | `RESOLVED-DEFINITIONAL` (different scope) |
| Methodology mismatch | `RESOLVED-DEFINITIONAL` if both methods are valid, with both kept and labelled; `RANGE-CARRIED` if both claim to measure the same quantity |
| Superseded information | `RESOLVED-HIERARCHY` (the later edition governs; the earlier is retained and marked SUPERSEDED) |
| Error identified | `RESOLVED-ERROR` |
| Range carried forward | `RANGE-CARRIED` |
| Unresolved contradiction | `OPEN` |

### 10.4 When a range is preserved

A low/high range is carried instead of a single value when **all** of the following apply:

- (a) the sources are of comparable tier and independence;
- (b) no definitional, period, scope, unit, error or supersession explanation resolves the difference;
- (c) the hierarchy does not clearly favour one source.

**No false precision.** The project never averages conflicting values into a single number, never picks the convenient value, and never reports a midpoint without labelling it as an analytical ESTIMATE. Ranges are carried into analysis with a sensitivity flag.

### 10.5 Materiality, escalation and record

- **Materiality:** Material, Moderate or Minor. A contradiction is Material when it could change a conclusion, ranking or decision.
- **Escalation:** Material contradictions that are OPEN or RANGE-CARRIED are listed in the Mission Reconciliation Report and in the Gate 4 audit for owner review. They are disclosed in deliverables at Gate 10.
- **Record:** every resolution records who resolved it, the date and the reasoning. Contradictions are never silently reconciled.

---

## 11. Confidence model

### 11.1 Evidence state and confidence are different things

- **Evidence state** (§3) records where an item stands in the verification pipeline.
- **Confidence** records how far a value may be relied on.

Both are recorded for every item.

### 11.2 Confidence categories (D-009; `methodology.md` §2)

| Category | Assigned when |
|---|---|
| **VERIFIED** | The evidence state is VERIFIED (Tier 1–3, with clear definition, date and geography) |
| **CORROBORATED** | The evidence state is CORROBORATED (§11.3) |
| **ESTIMATED** | The evidence state is ESTIMATE |
| **INDICATIVE** | The evidence state is EXTRACTED: a single Tier 4–5 source, or a source with an unclear definition or date |
| **DATA GAP** | The evidence state is DATA_GAP |

### 11.3 Corroboration and independence

Several low-quality sources never raise confidence. CORROBORATED requires **two or more independent** sources that agree, **at least one of them Tier 1–4**. "Agree" means the values are identical or differ only by demonstrable reporting precision (D-072). Sources are **not independent** when any of the following applies:

- they share a common origin (e.g. the same press release, wire story or dataset);
- one cites the other (circular citation);
- both rely on the same underlying primary source (in which case that primary source should be verified directly instead);
- one is an AI summary of the other;
- they are Gemini outputs from different missions.

Any number of Tier 5–6 sources, however many agree, leaves the confidence at **INDICATIVE** at most.

### 11.4 Quality dimensions can only lower confidence (D-040; `methodology.md` §2.1)

The dimensions are source quality, recency, cross-source agreement, methodological quality, completeness and definition consistency. Each is rated HIGH, MEDIUM, LOW or UNKNOWN.

- A LOW rating on any dimension **may lower** the category by one level. A material value rated LOW on definition consistency or completeness **must** be lowered, or carried with an explicit caveat.
- No rating raises a category.
- A high-confidence estimate remains ESTIMATED and is never presented as a verified fact.
- Research priority (CRITICAL / HIGH / MEDIUM / LOW; `methodology.md` §12) is never used as confidence.

---

## 12. Gemini output contract

Every mission output **must** follow this structure. A prose-only report is non-conforming (§17). The contract contains every section of the Gate 1 template (`gemini_mission_briefs.md` §4) and extends it. **It is the operational execution and output contract** (D-061). The Gate 1 mission briefs remain the mission-definition layer (objective, scope, questions, guardrails, sources) and are not rewritten.

**Claim IDs:** every material finding carries an ID in the form `GEM-NN-C###`. Every table row cites the claim ID, and every claim cites at least one source or is marked **"NO SOURCE — LEAD ONLY"**.

| # | Section | Required content | Gate 1 template § |
|---|---|---|---|
| 1 | Mission metadata | Mission ID; prompt version (`GEM-NN-Pv<N>`); execution date; Gemini model or tool context (if known); workstreams covered; operator | 1 |
| 2 | Executive findings | At most a short list of key findings, each with claim IDs. No unsourced statements | 2 |
| 3 | Research questions addressed | Each charter question in the mission (WS-NN Qn), with coverage: ANSWERED / PARTLY ANSWERED / NOT ANSWERED | — |
| 4 | Findings by question | For each question: findings with claim IDs and source IDs; what remains unknown | 2 |
| 5 | Quantitative evidence table | One row per value: claim ID · metric · definition · value · unit · currency · nominal/real · AC/DC · capacity/energy class · geography (level) · period · source ID · page/table/section · Gemini's self-assessed confidence and reason | 3 |
| 6 | Source roster | Source ID (mission-local, e.g. `GEM-NN-S##`) · exact title · publisher · document type · publication date · URL or persistent reference · language · access date · tier proposed by Gemini · access limitations (paywall, unavailable) | 4 |
| 7 | Primary-source verification | For each material claim: was the primary source itself consulted (Y/N)? If not, why not, and which secondary source was used | — |
| 8 | Cross-source corroboration | For each material value: the independent sources found and whether they agree | — |
| 9 | Contradictions | The conflicting values, shown side by side with their sources. **Not resolved** | 5 |
| 10 | Data gaps | The questions or values for which no source was found, and the sources tried | 6 |
| 11 | Unverified leads | Claims Gemini could not source, marked "NO SOURCE — LEAD ONLY" | 2 / 7 |
| 12 | Important definitions | The definitions each source uses for key metrics, especially where they differ from `methodology.md` §5 | — |
| 13 | Geographic coverage | Areas and levels covered, and areas not covered (§7) | — |
| 14 | Historical / current / future classification | The temporal class of each claim (§6.2) | — |
| 15 | Confidence assessment | Gemini's self-assessment per finding, with reasons. **Advisory only**; Claude assigns project confidence | 3 |
| 16 | Research limitations | Access barriers, language, coverage and time limits | — |
| 17 | Recommended follow-up questions | Unresolved questions that might justify a targeted mission | 7 |

**Contract rules:**

- Stay technology-neutral.
- Make no recommendations and no Alendei assessment.
- Characterise entities only with cited indicators.
- Treat earlier Gemini outputs, including the Gate 1 challenge, as hypotheses.
- Apply the status framework (§9) and the terminology (§8).
- Do not fabricate citations.
- Structured tables must appear inside the findings document. Separate supporting files are allowed **only when the mission package explicitly permits them** (D-060). Each permitted supporting artifact carries its own provenance and its copyright and access metadata. Arbitrary third-party documents are never archived into the repository automatically; §18 governs.

---

## 13. Gemini → Claude handoff

### 13.1 Deposit

- The operator deposits the Gemini output **unchanged** in `01_gemini_research/GEM-NN_<slug>/`.
- The file is named under the Gate 1 convention, `YYYY-MM-DD_GEM-NN_<slug>_gemini_v<N>.md`. This is the **single authoritative naming convention** (D-059); no other naming is maintained. The file is the mission's findings artifact.
- Permitted supporting artifacts take the same stem with a suffix (`…_gemini_v<N>_<artifact>.<ext>`), only when the mission package permits them (D-060). Their sidecar records provenance and copyright and access metadata.
- A re-run is a **new version** (`v<N+1>`). Earlier versions are kept.

### 13.2 Claude's handoff steps

1. **Fingerprint.** Compute the SHA-256 and write the `.meta.md` sidecar. The sidecar records:
   - date generated, date deposited, depositor;
   - prompt version;
   - Gemini model or tool context, where known;
   - size;
   - SHA-256;
   - evidence status (Tier 6);
   - repository commit and gate at the time of deposit.
2. **Conformance check.** Check the artifact against the §12 contract. A non-conforming artifact is handled under §17, and **is not edited**.
3. **Extract.** Each material claim becomes a lead register row (`LEAD-`), carrying its Gemini claim ID, the mission, the workstream(s), the source as cited, and state RAW_LEAD.
4. **Register sources.** Each roster entry becomes a source register row (`SRC-`), state CANDIDATE_SOURCE. Gemini's mission-local source IDs are mapped to `SRC-` IDs. Duplicate sources are merged under one `SRC-`, with the mapping recorded.
5. **Verify.** Retrieve each source and verify the claim under §4.1. Assign the tier and discloser independence yourself; do not adopt Gemini's tier.
6. **Cross-check.** Seek independent corroboration under §11.3.
7. **Contradictions and gaps.** Log CON and GAP rows.
8. **Update registers after validation only.** Register records are created as `acceptance_status = PROPOSED`. They become ACCEPTED only on gate approval (§14.3).
9. **Report.** Write the Mission Reconciliation Report (§14.1).

### 13.3 Recording claims that cannot be verified

| Situation | Lead outcome | Further action |
|---|---|---|
| The cited source does not exist or cannot be found after the §17 search path | UNSUPPORTED (reason: CITATION NOT FOUND) | None. The lead remains on record |
| The source exists but does not contain the claim | UNSUPPORTED (reason: NOT IN SOURCE) | None. The lead remains on record |
| The source contradicts the claim | CONTRADICTED | A CON row if the source's own value is registered |
| The claim is partly supported (e.g. value matches, definition unclear) | PARTLY VERIFIED | The record is created as EXTRACTED / INDICATIVE |
| No source was given ("NO SOURCE — LEAD ONLY") and none can be found | NOT VERIFIABLE | A GAP row if the question is material |
| The source exists but is inaccessible (paywall, offline) | NOT YET CHECKED (reason: ACCESS) | Access limitation recorded; §17 applies |

**The raw artifact is never edited** to remove, correct or annotate claims. All corrections live in the registers and the reconciliation report.

---

## 14. Reconciliation, challenge and acceptance

### 14.1 Mission Reconciliation Report

This is the Gate 1 "mission close report", `GEM-NN_close_report.md`, written by Claude in the mission folder. **It is the authoritative mission-close artifact** (D-063). It is versioned (`_v<N>`) when it is revised after a challenge. It contains:

1. **What Gemini claimed:** counts by workstream and by question, with claim IDs.
2. **Verified:** claims verified, with SRC and DAT IDs.
3. **Corroborated:** values corroborated, with their independent sources.
4. **Rejected:** UNSUPPORTED and CONTRADICTED leads, with reasons.
5. **Uncertain:** PARTLY VERIFIED, NOT YET CHECKED and INDICATIVE items.
6. **Contradictions:** CON rows, with diagnosis, outcome and materiality.
7. **Data gaps:** GAP rows, with materiality and next steps.
8. **Materiality and priority implications:** changes to research priority proposed for Gate 4 (`methodology.md` §12).
9. **Register changes:** records proposed (PROPOSED), by register.
10. **Unresolved decisions:** items for the owner.
11. **Proposed analytical implications:** labelled as **provisional inference**. Not used in analysis before acceptance.
12. **Coverage against stopping criteria** (§16).
13. **Reproducibility record** (§19).
14. **Challenge log:** the owner's and ChatGPT's challenges, recorded verbatim as **independent review inputs**, with Claude's response alongside and any resulting change (§14.2; D-064).

### 14.2 ChatGPT / owner challenge

The User and ChatGPT independently challenge:

- **material numbers:** traceability, definition and unit;
- **important conclusions and inferences;**
- **source quality:** tier, independence and recency;
- **contradictions:** diagnosis and outcome;
- **assumptions;**
- **commercial implications:** these must not appear in Phase A analysis;
- **missing evidence:** gaps and unexplored sources.

Claude answers every challenge, accepting it with a change made or declining it with reasons. A challenge Claude declines remains open until the owner closes it.

**Challenges are independent review inputs (D-064):**

- They are recorded verbatim, attributed to the reviewer, and kept separate from Claude's responses.
- Claude must never rewrite a challenge into what looks like an original research finding.
- A factual assertion made in a challenge is entered in the lead register as a `RAW_LEAD`, with origin `OWNER_CHALLENGE`. It is verified like any other lead before it can affect any register value.

### 14.3 Acceptance

No mission output becomes accepted evidence until the relevant gate is **explicitly approved**. Acceptance is recorded in the decision log, with the mission ID, the version of the reconciliation report and the scope accepted. Acceptance has two levels (D-062).

**Acceptance status is not verification status.**

- Acceptance status (`acceptance_status`: PROPOSED / ACCEPTED / REJECTED) records **gate approval** of a register record.
- Evidence state (§3) and confidence (§11) record **verification**.
- They are separate fields with non-overlapping vocabularies. An ACCEPTED record can still be INDICATIVE. A VERIFIED record is not usable until it is ACCEPTED.

| Level | Gate | What is accepted |
|---|---|---|
| Discovery acceptance | 2D | The artifact has been captured; leads and sources are registered; the report is complete; the mission's discovery coverage is adequate |
| Evidence acceptance | 3–4 | Specific register records move from PROPOSED to **ACCEPTED** and become usable in analysis |

---

## 15. Mission acceptance criteria

A mission can be accepted when **all** of the following hold:

1. The artifact is deposited, unchanged, fingerprinted, with a complete sidecar. Its conformance with the contract has been checked, and any non-conformity has been handled under §17.
2. Every material claim has been extracted to the lead register, and every cited source has been registered.
3. Every material lead has an outcome other than NOT YET CHECKED, or has been logged as a data gap with its access limitation.
4. Every material value proposed for the registers has full provenance (§4.2, §5.1).
5. Contradictions are logged and diagnosed. Material ones are escalated.
6. Data gaps are logged with materiality and next steps.
7. The stopping criteria (§16) are met, or any shortfall is explicitly accepted by the owner.
8. The Mission Reconciliation Report is complete, and every challenge has been answered.
9. No Alendei assessment, technology preference or commercial recommendation appears in the Phase A outputs.
10. The User and ChatGPT have explicitly approved the mission.

**A mission may be accepted with documented data gaps.**

---

## 16. Research stopping criteria

"Gemini has answered all questions" is **not** sufficient. A mission is sufficiently researched when:

| # | Criterion | Test |
|---|---|---|
| 1 | CRITICAL questions | Every CRITICAL question in the mission is ANSWERED, or recorded as a data gap after the §17 search path |
| 2 | HIGH questions | Every HIGH question is addressed: answered, partly answered with the gap logged, or logged as a gap |
| 3 | Material quantitative values | Every material value has a registered source with page, table or section |
| 4 | Primary sources | Primary sources have been sought for every material claim, and each search is recorded |
| 5 | Contradictions | Major contradictions have been investigated to an outcome other than unexamined |
| 6 | Data gaps | Important gaps are documented, with the sources tried |
| 7 | Geographic coverage | Every geographic level that the mission's charter questions require is addressed or logged as a gap |
| 8 | Temporal coverage | The study horizons relevant to the mission (2016–2026; 2027–2030; 2030–2035) are addressed or logged as gaps |
| 9 | Source quality | Material findings rest on Tier 1–4 evidence, or their lower confidence is explicitly recorded |
| 10 | Diminishing returns | Further searching along the §17 path is unlikely to yield higher-tier evidence, and this judgement is recorded with its reasoning |

MEDIUM and LOW questions may remain open without blocking acceptance, provided they are recorded.

---

## 17. Failure and retry rules

**Standard search path** before a claim is declared UNSUPPORTED or a data gap:

1. the cited URL or reference;
2. the publisher's site or repository;
3. official gazette or archive;
4. DFI and international document portals;
5. web archives;
6. a search by title or document number;
7. a French-language search.

| Situation | Rule |
|---|---|
| **Gemini cannot access a source** | Gemini records the access limitation in contract §6 and §16. Claude attempts retrieval along the search path. |
| **Source is paywalled** | The metadata is recorded with `access = PAYWALLED`. The claim stays NOT YET CHECKED. Claude may use the abstract or a public summary only as INDICATIVE. If the claim is material, the owner may decide to obtain access. |
| **Source is unavailable** (offline, link broken) | Web archives and alternative repositories are tried. If retrieval still fails, the source is marked UNAVAILABLE and the claim stays unverified. |
| **Primary document cannot be located** | The search is recorded. A secondary source may be used only under §4.5, at INDICATIVE or (with independent corroboration) CORROBORATED. **A weaker source is never silently substituted** for missing primary evidence. |
| **Source contradicts another** | §10. |
| **Gemini produces unsupported claims** | Each one becomes an UNSUPPORTED lead. If unsupported claims are pervasive in a mission (a judgement recorded in the report), the owner may require a re-run (new version) or a targeted follow-up mission. |
| **Research is incomplete** | Measured against §16. Gaps are logged. A targeted follow-up mission (new GEM ID with a decision-log entry) or a re-run may be proposed. |
| **Output is malformed** (non-conforming to §12, e.g. prose-only, or claims without IDs or sources) | The artifact is kept unchanged, as deposited. Claude records the non-conformity in the report and may extract leads, but **no claim from a malformed artifact proceeds beyond RAW_LEAD** until it is independently sourced. A conforming re-run is requested. |
| **A source is later found to be unreliable** | The source register is updated (tier or reliability note). Every record citing it is flagged for re-assessment. Confidence is lowered as warranted. Affected analyses are listed in the next reconciliation or gate report. History is kept: records are superseded, not deleted. |

---

## 18. Copyright and source-archive rules

This section implements `methodology.md` §4.2 and D-019.

| Situation | Action |
|---|---|
| Copyrighted third-party document (default) | **Metadata and reference only.** Record the URL or persistent reference, the relevant pages, sections or tables, and the evidence extracted. Do not commit the document. `local_copy_status = NOT STORED — REFERENCE ONLY` |
| Public-domain document, or government or official publication that is publicly redistributable | May be archived in `02_sources/<publisher>/`. The basis is recorded in `access_copyright_note`. `local_copy_status = STORED` |
| Licensed for redistribution (e.g. an open licence that permits it) | May be archived. The licence is recorded |
| Status unclear | Do not commit. A local working copy outside the repository may be kept: `STORED LOCALLY, NOT COMMITTED` |
| Datasets and GIS layers | As above. The dataset's licence terms are recorded in the GIS layer catalogue. Layers that cannot be redistributed are catalogued but not committed (`research_architecture.md` §L.3) |
| Relevant extracts | Only page, table and section references and short factual extracts are recorded in the registers, never substantial reproductions |
| Access limitations | Recorded in the source register as `access` (OPEN / REGISTRATION / PAYWALLED / UNAVAILABLE / RESTRICTED) together with the access date |

---

## 19. Reproducibility

Another researcher must be able to retrace the research path. For each mission run, the **reproducibility record** (kept in the `.meta.md` sidecar and in §13 of the reconciliation report) contains:

| Element | Recorded where |
|---|---|
| Mission ID and prompt version (`GEM-NN-Pv<N>`) | Sidecar; mission package in `00_architecture/` |
| Full prompt text as issued | Archived mission package (Gate 2C) |
| Execution date and operator | Sidecar |
| Gemini model or tool context, where available | Sidecar ("not available" stated explicitly) |
| Artifact fingerprint (SHA-256) and version | Sidecar |
| Source list and access dates | Source register (`SRC-` IDs, mapped to the mission-local IDs) |
| Search paths for UNSUPPORTED and gap items | Lead register and data-gap register |
| Repository commit and gate at deposit and at acceptance | Sidecar; decision log |
| Analyst (Claude Code) and reviewers (User, ChatGPT) | Reconciliation report; decision log |
| Acceptance status and decision ID | Decision log |

---

## 20. Claude independent discovery

Claude's independent discovery covers every Phase A workstream, WS-01 to WS-26 (`gemini_mission_briefs.md` §3). It follows the same lifecycle from stage 4 onward:

- leads are recorded with origin "Claude discovery";
- the same verification, confidence, contradiction and acceptance rules apply;
- Claude's own findings receive the same owner challenge (§14.2), with no self-acceptance.

Independent discovery begins only when Gate 2D authorises it.

---

## 21. Gate 2A decisions (resolved at Gate 2A closure)

| Item | Disposition | Decision |
|---|---|---|
| P-013 | APPROVED: "unsupported claim" is a final lead outcome (`UNSUPPORTED`), and `NOT VERIFIABLE` is added. It is not a tenth evidence state | D-058 |
| P-014 | APPROVED: the Gate 1 naming convention `YYYY-MM-DD_GEM-NN_<slug>_gemini_v<N>.md` is the single authoritative convention | D-059 |
| P-015 | APPROVED: supporting artifacts only where the mission package explicitly permits them; provenance, copyright and access metadata retained; no automatic archiving of third-party documents | D-060 |
| P-016 | APPROVED: the 17-section contract (§12) is the operational execution and output contract; the Gate 1 briefs remain the mission-definition layer, unchanged | D-061 |
| P-017 | APPROVED: two-level acceptance (discovery at 2D; evidence at Gates 3–4, PROPOSED → ACCEPTED); acceptance status is distinct from verification status | D-062 |
| P-018 | APPROVED; resolved at Gate 2B: geographic level codes (§7.1) | D-065 → D-067 |
| P-019 | APPROVED; resolved at Gate 2B: METHODOLOGY and SUPERSEDED cause codes (§10.2) | D-065 → D-068 |
| P-020 | APPROVED; resolved at Gate 2B: five distinct interconnector steps, never collapsed (§8.4) | D-065 → D-069 |
| P-021 | APPROVED: the reconciliation report (`GEM-NN_close_report.md`) is the authoritative mission-close artifact | D-063 |
| P-022 | APPROVED: challenges are recorded as independent review inputs; responses sit alongside them; challenges are never rewritten into apparent research findings | D-064 |
| P-023 | DEFERRED TO GATE 2B; resolved at Gate 2B: exchange-rate source and rate type (§5.2) | D-070 |
| P-024 | DEFERRED TO GATE 5: base year and deflator for real-terms values; not frozen early | Open (Gate 5) |

P-018 to P-020 and P-023 are implemented in the register schema (`register_schema.md`; D-066 to D-070, pending Gate 2B approval).
