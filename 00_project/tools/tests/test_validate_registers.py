#!/usr/bin/env python3
"""Deterministic tests for validate_registers.py (Gate 2C, D-083).

Fixtures are SYNTHETIC and built in a temporary directory; they contain no
Guinea facts and never touch the production registers.
Run:  python3 -I 00_project/tools/tests/test_validate_registers.py
"""
import copy
import datetime
import hashlib
import importlib.util
import os
import shutil
import sys
import tempfile
import unittest
import zipfile
from xml.sax.saxutils import escape

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(TOOLS))
spec = importlib.util.spec_from_file_location("validate_registers", os.path.join(TOOLS, "validate_registers.py"))
VAL = importlib.util.module_from_spec(spec)
spec.loader.exec_module(VAL)
S = VAL.S
D0 = datetime.date(2026, 1, 15)
D1 = datetime.date(2026, 2, 15)


# ---------------------------------------------------------------------------
# Minimal XLSX fixture writer (header + data rows; strings, numbers, dates)
# ---------------------------------------------------------------------------
def _col(n):
    s = ""
    while n:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


def _cell(ref, v, shared, strings):
    if v is None or v == "":
        return ""
    if isinstance(v, datetime.date):
        return f'<c r="{ref}" s="1"><v>{(v - datetime.date(1899, 12, 30)).days}</v></c>'
    if isinstance(v, (int, float)) and not isinstance(v, bool):
        return f'<c r="{ref}"><v>{v}</v></c>'
    if shared:
        if v not in strings:
            strings.append(v)
        return f'<c r="{ref}" t="s"><v>{strings.index(v)}</v></c>'
    return f'<c r="{ref}" t="inlineStr"><is><t>{escape(str(v))}</t></is></c>'


def write_book(path, sheets, shared=False):
    """sheets: list of (name, header, rows[dict])."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    ns = 'xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"'
    strings, files = [], {}
    wb, rels, ct = [], [], []
    for i, (name, header, rows) in enumerate(sheets, 1):
        xml_rows = []
        for rn, row in enumerate([dict(zip(header, header))] + rows, 1):
            cells = "".join(_cell(f"{_col(ci)}{rn}", row.get(h), shared, strings) for ci, h in enumerate(header, 1))
            xml_rows.append(f'<row r="{rn}">{cells}</row>')
        files[f"xl/worksheets/sheet{i}.xml"] = f'<?xml version="1.0" encoding="UTF-8"?><worksheet {ns}><sheetData>{"".join(xml_rows)}</sheetData></worksheet>'
        wb.append(f'<sheet name="{name}" sheetId="{i}" r:id="rId{i}"/>')
        rels.append(f'<Relationship Id="rId{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet{i}.xml"/>')
        ct.append(f'<Override PartName="/xl/worksheets/sheet{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>')
    n = len(sheets)
    rels.append(f'<Relationship Id="rId{n + 1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>')
    if shared:
        rels.append(f'<Relationship Id="rId{n + 2}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/sharedStrings" Target="sharedStrings.xml"/>')
        files["xl/sharedStrings.xml"] = f'<?xml version="1.0" encoding="UTF-8"?><sst xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">' + "".join(f"<si><t>{escape(s)}</t></si>" for s in strings) + "</sst>"
        ct.append('<Override PartName="/xl/sharedStrings.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sharedStrings+xml"/>')
    files["xl/workbook.xml"] = f'<?xml version="1.0" encoding="UTF-8"?><workbook {ns}><sheets>{"".join(wb)}</sheets></workbook>'
    files["xl/_rels/workbook.xml.rels"] = '<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">' + "".join(rels) + "</Relationships>"
    files["xl/styles.xml"] = ('<?xml version="1.0" encoding="UTF-8"?><styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
                              '<numFmts count="1"><numFmt numFmtId="164" formatCode="dd\\-mmm\\-yyyy"/></numFmts>'
                              '<fonts count="1"><font/></fonts><fills count="2"><fill><patternFill patternType="none"/></fill><fill><patternFill patternType="gray125"/></fill></fills>'
                              '<borders count="1"><border/></borders><cellStyleXfs count="1"><xf/></cellStyleXfs>'
                              '<cellXfs count="2"><xf numFmtId="0"/><xf numFmtId="164" applyNumberFormat="1"/></cellXfs></styleSheet>')
    files["_rels/.rels"] = '<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>'
    files["[Content_Types].xml"] = ('<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
                                    '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/>'
                                    '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
                                    '<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>' + "".join(ct) + "</Types>")
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for k in sorted(files):
            zi = zipfile.ZipInfo(k, (1980, 1, 1, 0, 0, 0))
            z.writestr(zi, files[k])


# ---------------------------------------------------------------------------
# Synthetic baseline dataset (valid)
# ---------------------------------------------------------------------------
COMMON = dict(acceptance_status="PROPOSED", record_status="ACTIVE", created_by="CLAUDE_CODE", created_date=D0)
QUAL = {f"quality_{q}": "HIGH" for q in ["source_quality", "recency", "cross_source_agreement", "methodological_quality", "completeness", "definition_consistency"]}


def src(i, tier, pub, origin="CLAUDE_DISCOVERY"):
    return dict(source_id=i, title_original=f"Synthetic Test Source {i}", publisher=pub, document_type="MINISTRY_REPORT", language="en",
                publication_date=D0, publication_date_precision="DAY", url=f"https://example.org/{i}", access_date=D0,
                access_status="OPEN", retrieval_status="RETRIEVED", source_tier=tier, discloser_independence="OFFICIAL_SELF_REPORTED",
                origin=origin, origin_ref="TEST-FIXTURE", reliability_flag="NONE", access_copyright_note="Synthetic test record",
                copyright_basis="COPYRIGHTED", local_copy_status="NOT_STORED_REFERENCE_ONLY", **COMMON)


def dat(i, ws, **kw):
    base = dict(data_id=i, workstream=ws, subject_type="NATIONAL_SYSTEM", metric="Synthetic test metric", metric_class="OTHER",
                metric_definition="Synthetic definition for validator testing", energy_class="NOT_APPLICABLE", ac_dc_basis="NOT_APPLICABLE",
                value_kind="NUMERIC", value=10, value_qualifier="EXACT", unit="COUNT", conversion_type="NONE",
                geography_name="Test Area", geo_level="NATIONAL_AGGREGATE", country_iso3="ZZZ", period_type="CALENDAR_YEAR",
                period_start=D0, temporal_class="HISTORICAL", source_id="SRC-0001", page_table_section="p. 1", access_date=D0,
                evidence_state="VERIFIED", confidence="VERIFIED", cross_check_status="NOT_ATTEMPTED", contradiction_status="NONE",
                revalidation_category="OTHER", verified_by="CLAUDE_CODE", verified_date=D0, **QUAL, **COMMON)
    base.update(kw)
    return base


def status(**kw):
    base = dict(lifecycle_stage="OPERATIONAL", lifecycle_evidence_type="COMMISSIONING_ENERGISATION_COD", lifecycle_evidence_source_ids="SRC-0001",
                progress_condition="ON_TRACK", status_summary="Synthetic status evidence", last_evidence_date=D0, status_assessed_date=D0,
                status_confidence="VERIFIED")
    base.update(kw)
    return base


def baseline():
    acc = dict(acceptance_status="ACCEPTED", acceptance_decision_id="D-001", acceptance_gate="G3")
    return {
        "SRC": [src("SRC-0001", 1, "Test Publisher A"), src("SRC-0002", 3, "Test Publisher B"),
                src("SRC-0003", 5, "Test Publisher C"), src("SRC-0004", 5, "Test Publisher D", origin="OWNER_SUPPLIED"),
                dict(src("SRC-0005", 5, "Test Newswire E"), document_type="NEWS_ARTICLE")],
        "ENT": [dict(entity_id="ENT-0001", legal_name="Test Entity One", entity_type="DEVELOPER", entity_roles="DEVELOPER",
                     origin_subregister="OTHER", guinea_presence_class="NOT_ASSESSED", **COMMON)],
        "SITE": [dict(site_id="SITE-0001", site_name="Test Site One", segment="OTHER", activity_types="OTHER", workstream_primary="WS-14",
                      geography_name="Test Area", geo_level="INDUSTRIAL_SITE", country_iso3="ZZZ", power_supply_modes="GRID", **status(), **COMMON)],
        "PRJ": [dict(project_id="PRJ-0001", project_name="Test Hydro Plant", component_type="GENERATION", technology="HYDRO_RESERVOIR",
                     workstream_primary="WS-05", geography_name="Test Area", geo_level="PLANT_SITE", country_iso3="ZZZ", **status(), **COMMON),
                dict(project_id="PRJ-0002", project_name="Test Interconnector", component_type="INTERCONNECTOR", technology="TRANSMISSION_AC",
                     workstream_primary="WS-16", geography_name="Test Corridor", geo_level="INTERCONNECTION", country_iso3="ZZZ",
                     **status(lifecycle_stage="UNDER_CONSTRUCTION", lifecycle_evidence_type="NTP_AND_SITE_WORKS"),
                     ic_constructed="NO", ic_energised="NO", ic_synchronised="NO", ic_operational="NO", ic_commercially_active="NO", **COMMON)],
        "MDR": [dict(dat("DAT-WS05-00001", "WS-05", subject_type="PROJECT", subject_id="PRJ-0001", metric="Installed capacity",
                         metric_class="CAPACITY", energy_class="INSTALLED", unit="MW", geo_level="PLANT_SITE", period_type="POINT_IN_TIME",
                         temporal_class="CURRENT_STATUS"), **acc),
                dat("DAT-WS05-00002", "WS-05", subject_type="PROJECT", subject_id="PRJ-0001", metric="Seasonal dependable capacity",
                    metric_class="CAPACITY", energy_class="SEASONAL_DEPENDABLE", value=4, unit="MW", geo_level="PLANT_SITE",
                    period_type="SEASON", season_label="Dry season as defined in source"),
                dat("DAT-WS04-00003", "WS-04", metric="Exchange rate", metric_class="FX_RATE", unit="FX_RATE", value=2,
                    fx_rate_type="PERIOD_AVERAGE", fx_source_class="CENTRAL_BANK_OFFICIAL", fx_base_currency="XTS", fx_quote_currency="XXX")],
        "LEAD": [dict(lead_id="LEAD-00001", origin="CLAUDE_DISCOVERY", origin_ref="TEST-FIXTURE", claim_text="Synthetic claim for testing",
                      claim_type="QUANTITATIVE", workstream_primary="WS-05", evidence_state="RAW_LEAD", lead_outcome="NOT_YET_CHECKED", **COMMON)],
        "CON": [],
        "GAP": [dict(gap_id="GAP-0001", workstream="WS-05", research_question="WS-05 Q1", question_priority_original="CRITICAL",
                     question_priority_current="CRITICAL", gap_description="Synthetic gap", materiality="MINOR",
                     search_path_log="Synthetic search path", next_step="None (test)", gap_status="OPEN", evidence_state="DATA_GAP", **COMMON)],
        "ASM": [dict(asm_id="ASM-0001", assumption_name="Test assumption", parameter="test_param", description="Synthetic", workstream="WS-05",
                     model_component="BASELINE", scenario_scope="ALL", value_type="DAT_REFERENCE", basis_data_ids="DAT-WS05-00001",
                     method_description="Reference to MDR", confidence="VERIFIED", assumption_owner="CLAUDE_CODE", **COMMON)],
        "GIS": [dict(gis_id="GIS-0001", layer_name="Test layer", layer_family="BASE_ADMIN", gis_folder="base_maps", file_format="GPKG",
                     geometry_type="POLYGON", workstreams="WS-26", description="Synthetic", source_ids="SRC-0002", licence="Test licence",
                     redistribution_permitted="NO", committed_to_repo="NO", crs_storage="EPSG:4326", processing_steps="None",
                     constraint_class="NOT_A_CONSTRAINT", **COMMON)],
        "OPP": [dict(opp_id="OPP-0001", opp_name="Test opportunity", description="Synthetic", solution_type="GENERATION", technologies="HYDRO_RESERVOIR",
                     geography_name="Test Area", geo_level="REGIONAL", evidence_chain_data_ids="DAT-WS05-00001", ff_legal="PASS",
                     ff_offtake="PASS", ff_site_constraint="PASS", ff_technical="PASS", ff_evidence="PASS", attractiveness_rating="ATTRACTIVE",
                     rating_frozen="YES", freeze_decision_id="D-001", freeze_date=D0, **COMMON)],
        "ALP": [dict(alp_id="ALP-0001", opp_id="OPP-0001", candidate_roles="PROJECT_DEVELOPMENT", role_rationale="Synthetic",
                     capability_gap="NOT_ASSESSED", licence_gap="NOT_ASSESSED", partnership_gap="NOT_ASSESSED", financing_gap="NOT_ASSESSED", **COMMON)],
    }


def build_root(tmp, ds, shared=False, header_override=None):
    for doc in ("00_project/decision_log.md", "00_project/workstream_charters.md"):
        os.makedirs(os.path.join(tmp, "00_project"), exist_ok=True)
        shutil.copy(os.path.join(ROOT, doc), os.path.join(tmp, doc))
    for reg in S.REGISTERS:
        sheets = []
        for sname, idk, fields in reg["sheets"]:
            key = "SITE" if idk == "SITE" else reg["key"]
            header = [f[0] for f in fields]
            if header_override and key in header_override:
                header = header_override[key](header)
            sheets.append((sname, header, ds.get(key, [])))
        write_book(os.path.join(tmp, reg["path"]), sheets, shared=shared)


def run(ds, gate="G3", shared=False, header_override=None):
    tmp = tempfile.mkdtemp(prefix="valtest_")
    try:
        build_root(tmp, ds, shared, header_override)
        return VAL.validate(tmp, gate)
    finally:
        shutil.rmtree(tmp)


def rules(res, status="FAIL"):
    return {i[1] for i in res.items if i[0] == status}


def find(ds, key, rid):
    for r in ds[key]:
        if list(r.values())[0] == rid:
            return r
    raise KeyError(rid)


class BaselineTests(unittest.TestCase):
    def test_baseline_valid_no_fail(self):
        res = run(baseline())
        fails = [i for i in res.items if i[0] == "FAIL"]
        self.assertEqual(fails, [], fails)

    def test_baseline_no_warning(self):
        res = run(baseline())
        self.assertEqual([i for i in res.items if i[0] == "WARNING"], [])

    def test_shared_strings_reader(self):
        res = run(baseline(), shared=True)
        self.assertEqual([i for i in res.items if i[0] == "FAIL"], [])

    def test_result_fields_present(self):
        res = run(baseline())
        for it in res.items:
            self.assertEqual(len(it), 7)
            self.assertIn(it[0], ("PASS", "FAIL", "WARNING"))

    def test_production_templates_pass_at_g2c(self):
        res = VAL.validate(ROOT, "G2C")
        self.assertEqual([i for i in res.items if i[0] == "FAIL"], [])

    def test_read_only(self):
        tmp = tempfile.mkdtemp(prefix="valtest_")
        try:
            build_root(tmp, baseline())
            paths = [os.path.join(tmp, r["path"]) for r in S.REGISTERS]
            def digest(p):
                with open(p, "rb") as fh:
                    return hashlib.sha256(fh.read()).hexdigest()
            before = [digest(p) for p in paths]
            VAL.validate(tmp, "G3")
            after = [digest(p) for p in paths]
            self.assertEqual(before, after)
        finally:
            shutil.rmtree(tmp)

    def test_deterministic(self):
        self.assertEqual(run(baseline()).items, run(baseline()).items)


def mutate(fn):
    ds = baseline()
    fn(ds)
    return ds


CASES = [
    # (name, mutation, expected rule, expected status, gate)
    ("D-077 data before Gate 2D", lambda d: None, "D-077", "FAIL", "G2C"),
    ("SCHEMA-01 header changed", None, "SCHEMA-01", "FAIL", "G3"),
    ("SCHEMA-02 required empty", lambda d: find(d, "MDR", "DAT-WS05-00001").update(metric=None), "SCHEMA-02", "FAIL", "G3"),
    ("SCHEMA-03 vocabulary", lambda d: find(d, "MDR", "DAT-WS05-00001").update(confidence="SURE"), "SCHEMA-03", "FAIL", "G3"),
    ("SCHEMA-04 type", lambda d: find(d, "MDR", "DAT-WS05-00001").update(value="ten"), "SCHEMA-04", "FAIL", "G3"),
    ("VR-01 bad ID", lambda d: find(d, "LEAD", "LEAD-00001").update(lead_id="LEAD-1"), "VR-01", "FAIL", "G3"),
    ("VR-01 WS mismatch", lambda d: find(d, "MDR", "DAT-WS05-00002").update(workstream="WS-06"), "VR-01", "FAIL", "G3"),
    ("VR-01 duplicate ID", lambda d: d["SRC"].append(copy.deepcopy(d["SRC"][0])), "VR-01", "FAIL", "G3"),
    ("VR-02 accepted without decision", lambda d: find(d, "LEAD", "LEAD-00001").update(acceptance_status="ACCEPTED"), "VR-02", "FAIL", "G3"),
    ("VR-03 superseded without pointer", lambda d: find(d, "SRC", "SRC-0002").update(record_status="SUPERSEDED"), "VR-03", "FAIL", "G3"),
    ("VR-05 missing reference", lambda d: find(d, "MDR", "DAT-WS04-00003").update(source_id="SRC-0099"), "VR-05", "FAIL", "G3"),
    ("VR-05 unknown decision", lambda d: find(d, "OPP", "OPP-0001").update(freeze_decision_id="D-999"), "VR-05", "FAIL", "G3"),
    ("VR-06 no source", lambda d: find(d, "MDR", "DAT-WS04-00003").update(source_id=None), "VR-06", "FAIL", "G3"),
    ("VR-07 verified with tier 5", lambda d: find(d, "MDR", "DAT-WS04-00003").update(source_id="SRC-0003"), "VR-07", "FAIL", "G3"),
    ("VR-08 confidence above mapping", lambda d: find(d, "MDR", "DAT-WS04-00003").update(evidence_state="EXTRACTED"), "VR-08", "FAIL", "G3"),
    ("VR-09 corroborated single source", lambda d: find(d, "MDR", "DAT-WS04-00003").update(evidence_state="CORROBORATED", confidence="CORROBORATED", cross_check_status="AGREES"), "VR-09", "FAIL", "G3"),
    ("VR-10 tier-5 only", lambda d: find(d, "MDR", "DAT-WS04-00003").update(source_id="SRC-0003", evidence_state="EXTRACTED", confidence="ESTIMATED"), "VR-10", "FAIL", "G3"),
    ("VR-11 numeric without value", lambda d: find(d, "MDR", "DAT-WS04-00003").update(value=None), "VR-11", "FAIL", "G3"),
    ("VR-11a boolean value", lambda d: find(d, "MDR", "DAT-WS04-00003").update(metric_class="LEGAL_INSTITUTIONAL", value_kind="CATEGORICAL", value=None, unit=None, value_text="MAYBE", categorical_type="BOOLEAN", fx_rate_type=None, fx_source_class=None, fx_base_currency=None, fx_quote_currency=None), "VR-11a", "FAIL", "G3"),
    ("VR-11a narrative", lambda d: find(d, "MDR", "DAT-WS04-00003").update(metric_class="LEGAL_INSTITUTIONAL", value_kind="CATEGORICAL", value=None, unit=None, value_text="Likely yes because the ministry suggests it should apply", categorical_type="CATEGORY_CODE", fx_rate_type=None, fx_source_class=None, fx_base_currency=None, fx_quote_currency=None), "VR-11a", "FAIL", "G3"),
    ("VR-12 currency unit without currency", lambda d: find(d, "MDR", "DAT-WS04-00003").update(metric_class="TARIFF", unit="CURRENCY_PER_KWH", fx_rate_type=None, fx_source_class=None, fx_base_currency=None, fx_quote_currency=None), "VR-12", "FAIL", "G3"),
    ("VR-13 capacity with energy unit", lambda d: find(d, "MDR", "DAT-WS05-00001").update(unit="GWh"), "VR-13", "FAIL", "G3"),
    ("VR-13 MW_DC vs AC basis", lambda d: find(d, "MDR", "DAT-WS05-00001").update(unit="MW_DC", ac_dc_basis="AC"), "VR-13", "FAIL", "G3"),
    ("VR-13 class/metric mixing", lambda d: find(d, "MDR", "DAT-WS05-00001").update(energy_class="GENERATED_NET"), "VR-13", "FAIL", "G3"),
    ("VR-14 FX conversion without rate", lambda d: d["MDR"].append(dat("DAT-WS09-00004", "WS-09", evidence_state="ESTIMATE", confidence="ESTIMATED", conversion_type="FX", source_id=None, page_table_section=None, access_date=None, input_data_ids="DAT-WS05-00001", estimate_method="Conversion", fx_rate_type="PERIOD_AVERAGE")), "VR-14", "FAIL", "G3"),
    ("VR-14 FX rate incomplete", lambda d: find(d, "MDR", "DAT-WS04-00003").update(fx_source_class=None), "VR-14", "FAIL", "G3"),
    ("VR-15 seasonal without label", lambda d: find(d, "MDR", "DAT-WS05-00002").update(season_label=None), "VR-15", "FAIL", "G3"),
    ("VR-15 hydro without seasonal", lambda d: d["MDR"].remove(find(d, "MDR", "DAT-WS05-00002")), "VR-15", "FAIL", "G3"),
    ("VR-16 derived mismatch", lambda d: find(d, "MDR", "DAT-WS04-00003").update(source_title="Edited title"), "VR-16", "WARNING", "G3"),
    ("VR-18 unsupported without reason", lambda d: find(d, "LEAD", "LEAD-00001").update(lead_outcome="UNSUPPORTED", checked_by="CLAUDE_CODE", checked_date=D0), "VR-18", "FAIL", "G3"),
    ("VR-18 lead as evidence", lambda d: find(d, "OPP", "OPP-0001").update(evidence_chain_other_ids="LEAD-00001"), "VR-18", "FAIL", "G3"),
    ("VR-19 MoU above announced", lambda d: find(d, "PRJ", "PRJ-0001").update(lifecycle_stage="FINANCIALLY_COMMITTED", lifecycle_evidence_type="MOU_LOI_FRAMEWORK"), "VR-19", "FAIL", "G3"),
    ("VR-19 stalled without evidence", lambda d: find(d, "PRJ", "PRJ-0001").update(progress_condition="STALLED"), "VR-19", "FAIL", "G3"),
    ("VR-19 tier-5-only commitment", lambda d: find(d, "PRJ", "PRJ-0001").update(lifecycle_evidence_source_ids="SRC-0003"), "VR-19", "FAIL", "G3"),
    ("VR-20 energised without constructed", lambda d: find(d, "PRJ", "PRJ-0002").update(ic_energised="YES", ic_energised_evidence_source_ids="SRC-0001"), "VR-20", "FAIL", "G3"),
    ("VR-20 missing step", lambda d: find(d, "PRJ", "PRJ-0002").update(ic_synchronised=None), "VR-20", "FAIL", "G3"),
    ("VR-20 operational without energisation", lambda d: find(d, "PRJ", "PRJ-0002").update(lifecycle_stage="OPERATIONAL", lifecycle_evidence_type="COMMISSIONING_ENERGISATION_COD"), "VR-20", "FAIL", "G3"),
    ("VR-20a no url or reference", lambda d: find(d, "SRC", "SRC-0002").update(url=None), "VR-20a", "FAIL", "G3"),
    ("VR-21 stored copyrighted", lambda d: find(d, "SRC", "SRC-0002").update(local_copy_status="STORED", local_path="02_sources/x.pdf"), "VR-21", "FAIL", "G3"),
    ("VR-21 GIS committed without permission", lambda d: find(d, "GIS", "GIS-0001").update(committed_to_repo="YES"), "VR-21", "FAIL", "G3"),
    ("VR-22 presence without evidence", lambda d: find(d, "ENT", "ENT-0001").update(guinea_presence_class="CONFIRMED_OPERATIONAL_PRESENCE", presence_assessed_date=D0), "VR-22", "FAIL", "G3"),
    ("VR-23 threshold before Gate 6", lambda d: find(d, "GIS", "GIS-0001").update(threshold_applied="test threshold", threshold_assumption_ids="ASM-0001"), "VR-23", "FAIL", "G3"),
    ("VR-24 scores before Gate 7", lambda d: find(d, "OPP", "OPP-0001").update(d01_demand_quality=3), "VR-24", "FAIL", "G3"),
    ("VR-24 ALP on unfrozen opportunity", lambda d: find(d, "OPP", "OPP-0001").update(rating_frozen="NO"), "VR-24", "FAIL", "G3"),
    ("VR-24 capability evidence not owner-supplied", lambda d: find(d, "ALP", "ALP-0001").update(capability_evidence_source_ids="SRC-0002"), "VR-24", "FAIL", "G3"),
    ("VR-24 Tier 1 without capability evidence", lambda d: find(d, "ALP", "ALP-0001").update(tier_classification="TIER_1_PURSUE_IMMEDIATELY", classification_rationale="Synthetic"), "VR-24", "FAIL", "G3"),
    ("VR-24 rating altered by WS-28", lambda d: find(d, "ALP", "ALP-0001").update(opp_attractiveness_at_freeze="HIGHLY_ATTRACTIVE"), "VR-24", "FAIL", "G3"),
    ("VR-25 priority changed without decision", lambda d: find(d, "GAP", "GAP-0001").update(question_priority_current="LOW"), "VR-25", "FAIL", "G3"),
    ("VR-26 single data id", lambda d: d["CON"].append(dict(con_id="CON-0001", workstream="WS-05", metric="m", metric_class="CAPACITY", subject_type="NATIONAL_SYSTEM", geography_name="Test Area", geo_level="NATIONAL_AGGREGATE", period_description="2026", data_ids="DAT-WS05-00001", diagnostic_tests_completed="DEFINITION", precision_attribution="NOT_ATTRIBUTABLE", cause_code="GENUINE", cause_notes="x", outcome="OPEN", reasoning="x", materiality="MINOR", escalated="NO", **COMMON)), "VR-26", "FAIL", "G3"),
    ("VR-26 precision without tests", lambda d: d["CON"].append(dict(con_id="CON-0002", workstream="WS-05", metric="m", metric_class="CAPACITY", subject_type="NATIONAL_SYSTEM", geography_name="Test Area", geo_level="NATIONAL_AGGREGATE", period_description="2026", data_ids="DAT-WS05-00001; DAT-WS05-00002", diagnostic_tests_completed="DEFINITION", precision_attribution="NOT_ATTRIBUTABLE", cause_code="REPORTING_PRECISION", cause_notes="x", outcome="OPEN", reasoning="x", materiality="MINOR", escalated="NO", **COMMON)), "VR-26", "FAIL", "G3"),
    ("VR-27 DAT reference with copied value", lambda d: find(d, "ASM", "ASM-0001").update(value=10), "VR-27", "FAIL", "G3"),
    ("VR-28 evidence chain not accepted", lambda d: find(d, "OPP", "OPP-0001").update(evidence_chain_data_ids="DAT-WS05-00002"), "VR-28", "FAIL", "G3"),
    ("VR-30 media establishes a claim", lambda d: find(d, "MDR", "DAT-WS04-00003").update(source_id="SRC-0005", evidence_state="EXTRACTED", confidence="CORROBORATED"), "VR-30", "FAIL", "G3"),
    ("VR-30 media-only without search note", lambda d: find(d, "MDR", "DAT-WS04-00003").update(source_id="SRC-0005", evidence_state="EXTRACTED", confidence="INDICATIVE", page_table_section=None, verified_by=None, verified_date=None), "VR-30", "WARNING", "G3"),
    ("VR-31 corporate filing for national-system fact", lambda d: find(d, "MDR", "DAT-WS04-00003").update(source_id="SRC-0003", evidence_state="EXTRACTED", confidence="INDICATIVE", page_table_section=None, verified_by=None, verified_date=None), "VR-31", "FAIL", "G3"),
    ("VR-29 period end before start", lambda d: find(d, "MDR", "DAT-WS04-00003").update(period_end=datetime.date(2025, 1, 1)), "VR-29", "FAIL", "G3"),
    ("VR-29 date stored as text", lambda d: find(d, "MDR", "DAT-WS04-00003").update(verified_date="15-Jan-2026"), "VR-29", "WARNING", "G3"),
]


class MutationTests(unittest.TestCase):
    pass


def _make(name, fn, rule, status, gate):
    def t(self):
        if rule == "SCHEMA-01":
            res = run(baseline(), gate, header_override={"MDR": lambda h: h[:-1]})
        else:
            res = run(mutate(fn) if fn else baseline(), gate)
        self.assertIn(rule, rules(res, status), f"{name}: expected {status} {rule}; got FAIL={sorted(rules(res))} WARNING={sorted(rules(res, 'WARNING'))}")
        for it in res.items:
            if it[0] in ("FAIL", "WARNING"):
                self.assertTrue(it[5] and it[6], f"reason/remediation missing: {it}")
    return t


for _i, (_n, _f, _r, _s, _g) in enumerate(CASES, 1):
    setattr(MutationTests, f"test_{_i:02d}_{_r.replace('-', '_')}", _make(_n, _f, _r, _s, _g))


class RuleCoverageTest(unittest.TestCase):
    def test_every_rule_has_an_invalid_case(self):
        covered = {c[2] for c in CASES}
        expected = {f"VR-{i:02d}" for i in range(1, 32)} | {"VR-11a", "VR-20a"}
        structural = {"VR-04", "VR-17"}   # schema-level, checked against the generator schema
        self.assertEqual(sorted(expected - structural - covered), [])

    def test_structural_rules_pass_on_schema(self):
        res = run(baseline())
        self.assertIn(("PASS", "VR-04"), {(i[0], i[1]) for i in res.items})
        self.assertIn(("PASS", "VR-17"), {(i[0], i[1]) for i in res.items})


if __name__ == "__main__":
    unittest.main(verbosity=1)
