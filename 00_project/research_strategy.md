# Research Strategy

**Version:** 1.0 (DRAFT — pending Gate 1 approval) · **Last updated:** 08-Oct-2026 · **Gate:** 1

## 1. Strategic intent

Produce an objective, evidence-led picture of Guinea's power system first; apply the Alendei commercial lens only afterwards. The sequence is deliberate: an opportunity analysis built on an unverified baseline is not decision-grade for C-suite, investor or government audiences.

## 2. Two-phase structure

| Phase | Gates | Question answered | Alendei lens |
|---|---|---|---|
| A — Independent system analysis (WS-01 – WS-26) | 1–6 | What is the actual state, trajectory and constraint set of Guinea's power system? | **Excluded** |
| B1 — Country opportunity analysis (WS-27) | 7 (part 1) | What opportunities are technically, commercially and strategically attractive for Guinea? | **Excluded** — Alendei-neutral; ratings frozen at end of B1 |
| B2 — Alendei participation (WS-28) | 7 (part 2) | Where can Alendei participate, and how should each opportunity be classified (Tier 1–4) for Alendei? | Applied — cannot alter B1 ratings |
| — Review and reconciliation | 8–9 | Do findings and opportunities survive adversarial review and final reconciliation? | — |
| C — Production and QA | 10–11 | Are the deliverables accurate, traceable and fit for a senior audience? | — |

Phase A outputs must be readable and defensible on their own, without reference to Alendei interests.

## 3. Research principles

1. Evidence before conclusions.
2. Primary sources are preferred.
3. Gemini-generated research is a research lead, not evidence.
4. Claude must independently verify material claims.
5. No unsupported material number may enter a final deliverable.
6. Every material statistic must carry the full metadata set defined in `methodology.md` §3.
7. Confidence categories: VERIFIED, CORROBORATED, ESTIMATED, INDICATIVE, DATA GAP.
8. Never silently reconcile contradictory statistics.
9. Distinguish capacity, energy and demand metrics precisely (`methodology.md` §5).
10. Distinguish project status precisely (`methodology.md` §6).
11. Do not assume solar is the answer.
12. Technology selection must follow evidence.
13. Do not assume global OEM/EPC presence means Guinea presence.
14. Do not claim Alendei capabilities, licences, partnerships or financing commitments unless verified.
15. The first major portion of the study remains objective and evidence-led.
16. Alendei strategic opportunity analysis comes after the independent Guinea energy-system analysis.
17. Every final opportunity must have an evidence chain.
18. "Do not pursue now" is a valid and mandatory opportunity classification.
19. **Technology neutrality (D-027):** solar, wind, hydro, BESS, thermal, hybrids, grid reinforcement, demand-side measures, mini-grids and other justified solutions are assessed on evidence; none is promoted or de-emphasised in advance.
20. **Gemini findings are hypotheses (D-026):** no Gemini factual claim is assumed true because Gemini stated it, including claims made in the Gate 1 architecture challenge (logged as leads GL-01 – GL-33 in `gate1_gemini_reconciliation.md`).
21. **Specific non-assumptions (D-026):** utility financial condition, offshore escrow/FX structures, basin-organisation relevance, universal GIS thresholds, generic alumina loads, wind de-prioritisation, screening weights and a preferred mining-B2B model are all investigated, not assumed (`research_architecture.md` §A.2).
22. **Country before Alendei (D-028):** Alendei strategic fit must not distort the country opportunity ranking.
23. **No linear-only forecasting (D-031):** demand and supply outlooks use the scenario architecture (`research_architecture.md` §J).

## 4. Research approach per workstream

Each of the 28 workstreams has a charter (`workstream_charters.md`) defining objective, scope, principal questions, datasets, source priorities, dependencies, expected outputs, validation requirements and downstream consumers. Phase A workstreams (WS-01 – WS-26) follow the same cycle:

1. **Question set** — Principal questions in the charter (Gate 1), each tagged with a qualitative planning priority (CRITICAL / HIGH / MEDIUM / LOW; `methodology.md` §12). Priority guides research effort only — it is not evidence confidence or a finding, and is reassessed at Gate 4.
2. **Discovery** — Gemini missions GEM-01 – GEM-15 (`gemini_mission_briefs.md`; organised by mission, each spanning several workstreams; approved as architecture, executed only after Gate 2 authorisation) and Claude independent discovery covering every workstream (Gate 2).
3. **Lead and source capture** — Claims enter the lead register; sources enter the source register; local copies only where the copyright basis is recorded (`methodology.md` §4.2).
4. **Verification** — Each material claim is checked against the original source and assigned tier, evidence state, confidence and quality dimensions (`methodology.md` §2–§3).
5. **Registration** — Verified data enter the master data / project / entity registers; conflicts enter the contradiction register (`research_architecture.md` §H); gaps enter the data-gap register.
6. **Analysis** — Workstream analysis in `04_analysis/wsNN_<slug>/`; integration in `04_analysis/00_integrated_models/` and `05_gis/`.

Sequencing and dependencies: `research_architecture.md` §D. Handoff protocol: §F.

## 5. Source-targeting strategy

Source priorities are defined per workstream in `workstream_charters.md`. Guinea-specific institutions and documents named in the Gemini challenge are treated as **candidate source targets to verify** (GL-16, GL-17), not as confirmed. Summary:

| Source class | Indicative publishers / types | Guinea-specific holdings |
|---|---|---|
| Government of Guinea | Energy, mines, finance, planning and environment ministries; regulator; national utility; rural electrification agency; petroleum agency; audit institutions; official gazette | DATA NOT YET RESEARCHED |
| Regional | WAPP, ECOWAS and regional regulator, interconnector operators, river-basin organisations (relevance to be established) | DATA NOT YET RESEARCHED |
| Multilateral / DFI | World Bank, IFC, MIGA, AfDB, EIB, IsDB, IMF, UN agencies, bilateral DFIs and ECAs | DATA NOT YET RESEARCHED |
| Data institutions | IEA, IRENA, ESMAP/global resource atlases, reanalysis datasets, academic and research bodies, EITI | DATA NOT YET RESEARCHED |
| Mining and industrial | Mining cadastre, EITI, company statutory filings, ESIAs, industrial and port authorities | DATA NOT YET RESEARCHED |
| Commercial ecosystem | OEMs, EPCs, IPPs, developers and financiers by origin (India, China, Europe, Middle East, USA, Japan/Korea, Africa) | DATA NOT YET RESEARCHED |

## 6. Benchmarking strategy

Guinea is benchmarked against Senegal, Mali, Côte d'Ivoire, Sierra Leone, Liberia, Guinea-Bissau and Ghana (minimum). Benchmark metrics will be defined at Gate 1 and must use identical metric definitions across countries; where definitions differ, the difference is recorded, not normalised silently.

## 7. Opportunity strategy (Phase B — not started)

- **WS-27 (country, Alendei-neutral):** opportunities are generated from Phase A evidence across all solution types; fatal-flaw screen; multi-criteria screening on preliminary dimensions with **no frozen weights** until Gate 7 sensitivity testing (D-029); evidence confidence reported alongside, not blended; commercial models (utility PPA, private B2B, captive, BOO/BOOT, concession, PPP, mini-grid) assessed on evidence with **none predetermined** (D-026). Attractiveness ratings are frozen before WS-28.
- **WS-28 (Alendei):** Alendei participation is assessed against the frozen WS-27 portfolio using user-supplied capability evidence only, and each opportunity receives one classification: **Tier 1 — Pursue immediately**, **Tier 2 — Develop**, **Tier 3 — Monitor**, or **Tier 4 — Do not pursue now** (`methodology.md` §11).
- Each opportunity carries an evidence chain linking it to register entries.
- Full architecture: `research_architecture.md` §K.

## 8. Risks to research quality

| Risk | Mitigation |
|---|---|
| AI-generated hallucinated statistics | Gemini output treated as Tier 6 leads; independent verification mandatory. |
| Stale data presented as current | Every data point carries a year and source publication date; staleness flagged. |
| Metric conflation (e.g. installed vs available capacity) | Mandatory metric definitions; contradiction register. |
| Status inflation (announced presented as committed) | Mandatory status taxonomy. |
| Confirmation bias toward any technology / Alendei interests | Technology-neutral charters and coverage matrix; Phase A excludes Alendei lens; adversarial review at Gate 8. |
| French-language primary sources missed | Source searches to include French-language terms and publications. |
| Policy and tariff information outdated | Flag verification date; mandatory re-verification of volatile data classes at Gate 9 (D-048). |
| Gemini premises imported into architecture or analysis | Gemini assertions logged as leads (GL-01 – GL-33); neutral wording of questions and mission titles; lead register separate from evidence registers. |
| Premature thresholds or weights (GIS, scoring) | Constraint layers stored with continuous attributes; weights tested with sensitivity at Gate 7 (D-029, D-038). |
| Alendei fit distorting country ranking | WS-27 ratings frozen before WS-28; WS-28 cannot alter them (D-028). |
| Lumpy demand misforecast by trend extrapolation | Site-level, evidence-linked scenario drivers; linear trend only as reference (D-031). |

## 9. Guinea-specific findings

DATA NOT YET RESEARCHED.
