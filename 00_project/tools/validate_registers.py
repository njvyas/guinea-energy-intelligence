#!/usr/bin/env python3
"""Register validator (Gate 2C; D-075, D-083).

Validates the authoritative XLSX registers against the approved schema
(00_project/tools/build_register_templates.py) and validation rules VR-01 - VR-31,
VR-11a and VR-20a (00_project/register_schema.md section 6), plus the D-077
gate-transition rule.

The validator is READ-ONLY: it never modifies, corrects or re-saves a register.
Every result is PASS, FAIL or WARNING, with rule ID, register, record ID, field,
reason and remediation guidance. Exit code: 0 = no FAIL; 1 = at least one FAIL;
2 = usage/IO error. With --strict, WARNINGs also produce exit code 1.

Usage:
  python3 -I 00_project/tools/validate_registers.py [--root .] [--gate G2C]
          [--format text|tsv] [--hide-pass] [--strict]
Standard library only.
"""
import argparse
import datetime
import importlib.util
import os
import re
import sys
import zipfile
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
GATES = ["G2A", "G2B", "G2C", "G2D", "G3", "G4", "G5", "G6", "G7", "G8", "G9", "G10", "G11"]


def _load_schema():
    spec = importlib.util.spec_from_file_location("register_schema", os.path.join(HERE, "build_register_templates.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


S = _load_schema()
V = {k: [c for c, _ in v] for k, v in S.V.items()}
ID_RE = {
    "DAT": re.compile(r"^DAT-WS(\d\d)-\d{5}$"), "SRC": re.compile(r"^SRC-\d{4}$"), "LEAD": re.compile(r"^LEAD-\d{5}$"),
    "CON": re.compile(r"^CON-\d{4}$"), "GAP": re.compile(r"^GAP-\d{4}$"), "PRJ": re.compile(r"^PRJ-\d{4}$"),
    "ENT": re.compile(r"^ENT-\d{4}$"), "SITE": re.compile(r"^SITE-\d{4}$"), "ASM": re.compile(r"^ASM-\d{4}$"),
    "GIS": re.compile(r"^GIS-\d{4}$"), "OPP": re.compile(r"^OPP-\d{4}$"), "ALP": re.compile(r"^ALP-\d{4}$"),
    "D": re.compile(r"^D-\d{3}$"),
}
REG_OF_PREFIX = {"DAT": "MDR", "SRC": "SRC", "LEAD": "LEAD", "CON": "CON", "GAP": "GAP", "PRJ": "PRJ", "ENT": "ENT",
                 "SITE": "SITE", "ASM": "ASM", "GIS": "GIS", "OPP": "OPP", "ALP": "ALP"}
SEP = ";"
NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
RID = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"
GUIDE_SHEETS = {"README", "DICTIONARY", "VOCAB", "VOCAB_DEFINITIONS", "DIFFERENCE_TESTS"}
CONF_RANK = {"DATA GAP": 0, "INDICATIVE": 1, "ESTIMATED": 2, "CORROBORATED": 3, "VERIFIED": 4}
MAPPED_CONF = {"VERIFIED": "VERIFIED", "CORROBORATED": "CORROBORATED", "ESTIMATE": "ESTIMATED", "EXTRACTED": "INDICATIVE"}
CAPACITY_CLASSES = {"INSTALLED", "AVAILABLE", "DEPENDABLE", "SEASONAL_DEPENDABLE", "DISPATCHED"}
ENERGY_CLASSES = {"GENERATED_GROSS", "GENERATED_NET", "GENERATED_UNSTATED", "DELIVERED", "CONSUMED_BILLED", "CONSUMED_METERED"}
DEMAND_CLASSES = {"PEAK_SERVED", "PEAK_UNCONSTRAINED", "AVERAGE_DEMAND", "SUPPRESSED_UNSERVED", "CAPTIVE_SELF_SUPPLIED"}
POWER_UNITS = {"kW", "MW", "GW", "MW_AC", "MW_DC"}
ENERGY_UNITS = {"kWh", "MWh", "GWh", "TWh"}
STAGE_ORDER = ["PROPOSED", "ANNOUNCED", "ACTIVE_DEVELOPMENT", "FINANCIALLY_COMMITTED", "UNDER_CONSTRUCTION", "OPERATIONAL"]
EVIDENCE_SUPPORTS = {
    "PLAN_LISTING": "PROPOSED", "PUBLIC_ANNOUNCEMENT": "ANNOUNCED", "MOU_LOI_FRAMEWORK": "ANNOUNCED",
    "DEVELOPMENT_WORK": "ACTIVE_DEVELOPMENT", "FINANCIAL_CLOSE": "FINANCIALLY_COMMITTED",
    "SIGNED_FINANCING_AGREEMENT": "FINANCIALLY_COMMITTED", "BINDING_EPC_WITH_FUNDING": "FINANCIALLY_COMMITTED",
    "BUDGET_WITH_SIGNED_CONTRACT": "FINANCIALLY_COMMITTED", "NTP_AND_SITE_WORKS": "UNDER_CONSTRUCTION",
    "COMMISSIONING_ENERGISATION_COD": "OPERATIONAL", "OFFICIAL_TERMINATION": "CANCELLED",
}
IC_STEPS = ["constructed", "energised", "synchronised", "operational", "commercially_active"]
STORABLE_BASIS = {"PUBLIC_DOMAIN", "GOVERNMENT_REDISTRIBUTABLE", "OPEN_LICENCE", "LICENSED_FOR_REDISTRIBUTION"}
ELIGIBLE_RATINGS = {"HIGHLY_ATTRACTIVE", "ATTRACTIVE", "CONDITIONALLY_ATTRACTIVE"}
NINE_TESTS = set(V["v_difference_test"])


# ---------------------------------------------------------------------------
# Minimal read-only XLSX reader (inline strings, shared strings, numbers, dates, booleans)
# ---------------------------------------------------------------------------
def _col_index(ref):
    letters = re.match(r"[A-Z]+", ref).group(0)
    n = 0
    for ch in letters:
        n = n * 26 + ord(ch) - 64
    return n - 1


def _date_styles(z):
    if "xl/styles.xml" not in z.namelist():
        return set()
    st = ET.fromstring(z.read("xl/styles.xml"))
    custom = {}
    nf = st.find(NS + "numFmts")
    if nf is not None:
        for f in nf:
            code = re.sub(r'"[^"]*"|\[[^\]]*\]|\\.', "", f.get("formatCode", "")).lower()
            custom[int(f.get("numFmtId"))] = bool(re.search(r"[dy]", code))
    builtin = set(range(14, 23)) | {27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 45, 46, 47, 50, 51, 52, 53, 54, 55, 56, 57, 58}
    out = set()
    xfs = st.find(NS + "cellXfs")
    if xfs is not None:
        for i, xf in enumerate(xfs):
            fid = int(xf.get("numFmtId", "0"))
            if fid in builtin or custom.get(fid):
                out.add(i)
    return out


def read_xlsx(path):
    """Return {sheet_name: [[cell values]]}; values are str, float, bool, datetime.date or None."""
    with zipfile.ZipFile(path) as z:
        wb = ET.fromstring(z.read("xl/workbook.xml"))
        rels = {r.get("Id"): r.get("Target") for r in ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))}
        shared = []
        if "xl/sharedStrings.xml" in z.namelist():
            for si in ET.fromstring(z.read("xl/sharedStrings.xml")):
                shared.append("".join(t.text or "" for t in si.iter(NS + "t")))
        dstyles = _date_styles(z)
        out = {}
        for sh in wb.find(NS + "sheets"):
            target = rels[sh.get(RID)]
            target = target.lstrip("/")
            target = target if target.startswith("xl/") else "xl/" + target
            ws = ET.fromstring(z.read(target))
            rows = []
            for r in ws.find(NS + "sheetData"):
                rn = int(r.get("r")) - 1
                while len(rows) <= rn:
                    rows.append([])
                row = rows[rn]
                for c in r:
                    ci = _col_index(c.get("r"))
                    while len(row) <= ci:
                        row.append(None)
                    t = c.get("t")
                    v = c.find(NS + "v")
                    if t == "inlineStr":
                        val = "".join(x.text or "" for x in c.iter(NS + "t"))
                    elif t == "s":
                        val = shared[int(v.text)] if v is not None else ""
                    elif t in ("str", "e"):
                        val = v.text if v is not None else ""
                    elif t == "b":
                        val = (v is not None and v.text == "1")
                    else:
                        if v is None:
                            val = None
                        else:
                            num = float(v.text)
                            if int(c.get("s", "0")) in dstyles:
                                val = datetime.date(1899, 12, 30) + datetime.timedelta(days=int(num))
                            else:
                                val = num
                    if isinstance(val, str):
                        val = val.strip()
                        if val == "":
                            val = None
                    row[ci] = val
            out[sh.get("name")] = rows
        return out


# ---------------------------------------------------------------------------
# Results
# ---------------------------------------------------------------------------
class Results:
    def __init__(self):
        self.items = []
        self.checked = set()   # (rule, register)

    def add(self, status, rule, register, record="*", field="-", reason="", remediation=""):
        self.items.append((status, rule, register, record or "*", field or "-", reason, remediation))

    def fail(self, *a, **k):
        self.add("FAIL", *a, **k)

    def warn(self, *a, **k):
        self.add("WARNING", *a, **k)

    def ran(self, rule, register):
        self.checked.add((rule, register))

    def finalize(self):
        flagged = {(i[1], i[2]) for i in self.items if i[0] in ("FAIL", "WARNING")}
        for rule, reg in sorted(self.checked):
            if (rule, reg) not in flagged:
                self.add("PASS", rule, reg, "*", "-", "No violations found", "-")
        order = {"FAIL": 0, "WARNING": 1, "PASS": 2}
        self.items.sort(key=lambda i: (order[i[0]], _rule_key(i[1]), i[2], i[3], i[4]))

    def counts(self):
        c = {"PASS": 0, "FAIL": 0, "WARNING": 0}
        for i in self.items:
            c[i[0]] += 1
        return c


def _rule_key(r):
    m = re.match(r"([A-Z]+)-(\d+)([a-z]?)", r)
    return (m.group(1), int(m.group(2)), m.group(3)) if m else (r, 0, "")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def split_ids(v):
    if v is None:
        return []
    return [x.strip() for x in str(v).split(SEP) if x.strip()]


def blank(v):
    return v is None or (isinstance(v, str) and v.strip() == "")


def num(v):
    if isinstance(v, (int, float)) and not isinstance(v, bool):
        return float(v)
    try:
        return float(str(v))
    except (TypeError, ValueError):
        return None


def prefix_of(i):
    for p, rx in ID_RE.items():
        if rx.match(i):
            return p
    return None


def target_prefixes(con):
    if con in ("", None):
        return []
    return [p for p in con.split("|") if p in ID_RE]


def decision_ids(root):
    p = os.path.join(root, "00_project/decision_log.md")
    if not os.path.exists(p):
        return set()
    with open(p, encoding="utf-8") as fh:
        return set(re.findall(r"^\| (D-\d{3}) \|", fh.read(), re.M))


def charter_priorities(root):
    p = os.path.join(root, "00_project/workstream_charters.md")
    out = {}
    if not os.path.exists(p):
        return out
    with open(p, encoding="utf-8") as fh:
        ch = fh.read()
    parts = re.split(r"\n## (WS-\d\d) — .+\n", ch)[1:]
    for w, b in zip(parts[0::2], parts[1::2]):
        q = b.split("**Principal questions:**")[1].split("**Required datasets:**")[0]
        for n, pri in enumerate(re.findall(r"^\s+\d+\. \*\*\[(\w+)\]\*\*", q, re.M), 1):
            out[f"{w} Q{n}"] = pri
    return out


# ---------------------------------------------------------------------------
# Loading
# ---------------------------------------------------------------------------
def load_registers(root, res):
    """Return {key: {"fields": [...], "records": [(row, dict)], "reg": schema}} keyed by MDR, SRC, ..., ENT, SITE."""
    data = {}
    for reg in S.REGISTERS:
        path = os.path.join(root, reg["path"])
        for sname, idk, fields in reg["sheets"]:
            key = "SITE" if idk == "SITE" else reg["key"]
            res.ran("SCHEMA-01", key)
            entry = {"fields": fields, "records": [], "reg": reg, "sheet": sname, "path": reg["path"]}
            data[key] = entry
            if not os.path.exists(path):
                res.fail("SCHEMA-01", key, "*", "-", f"Workbook missing: {reg['path']}", "Regenerate the template with build_register_templates.py.")
                continue
            try:
                book = read_xlsx(path)
            except Exception as ex:  # noqa: BLE001
                res.fail("SCHEMA-01", key, "*", "-", f"Workbook unreadable: {ex}", "Restore the workbook from version control.")
                continue
            if sname not in book:
                res.fail("SCHEMA-01", key, "*", "-", f"Data sheet '{sname}' missing", "Restore the sheet from the template.")
                continue
            rows = book[sname]
            header = [h for h in (rows[0] if rows else [])]
            while header and header[-1] is None:
                header.pop()
            expected = [f[0] for f in fields]
            if header != expected:
                missing = [f for f in expected if f not in header]
                extra = [h for h in header if h not in expected]
                res.fail("SCHEMA-01", key, "*", "header",
                         f"Header differs from schema (missing {missing}, extra {extra}, or order changed)",
                         "Do not edit template structure; change the schema only via the generator with a decision.")
                continue
            for rn, row in enumerate(rows[1:], start=2):
                if not any(not blank(x) for x in row):
                    continue
                rec = {f: (row[i] if i < len(row) else None) for i, f in enumerate(expected)}
                entry["records"].append((rn, rec))
            for extra in sorted(set(book) - GUIDE_SHEETS - {s for s, _, _ in reg["sheets"]}):
                res.warn("SCHEMA-01", key, "*", "-", f"Unexpected sheet '{extra}' in workbook", "Remove sheets that are not part of the template.")
    return data


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------
def validate(root=".", gate="G2C"):
    res = Results()
    if gate not in GATES:
        raise ValueError(f"unknown gate {gate}")
    gi = GATES.index(gate)
    data = load_registers(root, res)
    dec = decision_ids(root)
    prios = charter_priorities(root)
    ids = {k: {} for k in data}
    for k, e in data.items():
        idf = e["fields"][0][0]
        for rn, r in e["records"]:
            if not blank(r[idf]):
                ids[k].setdefault(str(r[idf]), r)

    def rid(k, r):
        return str(r[data[k]["fields"][0][0]] or f"row?")

    # ---- D-077 gate-transition rule -------------------------------------
    total = sum(len(e["records"]) for e in data.values())
    res.ran("D-077", "ALL")
    if gi < GATES.index("G2D") and total:
        for k, e in data.items():
            for rn, r in e["records"]:
                res.fail("D-077", k, rid(k, r), "-", f"Data record (row {rn}) exists before Gate 2D research authorisation",
                         "Remove the record: no populated evidence data before authorised research execution (D-077).")

    # ---- generic schema checks per record -------------------------------
    for k, e in data.items():
        for rule in ("SCHEMA-02", "SCHEMA-03", "SCHEMA-04", "VR-01", "VR-02", "VR-03", "VR-05", "VR-16", "VR-29"):
            res.ran(rule, k)
        idf = e["fields"][0]
        seen = {}
        content = {}
        for rn, r in e["records"]:
            rec_id = rid(k, r)
            # VR-01 ID format/uniqueness
            rx = ID_RE[idf[3]]
            if blank(r[idf[0]]) or not rx.match(str(r[idf[0]])):
                res.fail("VR-01", k, rec_id, idf[0], f"ID '{r[idf[0]]}' does not match {S.ID_PATTERNS[idf[3]][0]}", "Assign a correctly formatted, never-reused ID.")
            elif str(r[idf[0]]) in seen:
                res.fail("VR-01", k, rec_id, idf[0], f"Duplicate ID (rows {seen[str(r[idf[0]])]} and {rn})", "IDs must be unique; supersede rather than reuse.")
            else:
                seen[str(r[idf[0]])] = rn
            sig = tuple((f, r[f]) for f, *_ in e["fields"][1:] if f not in ("created_date", "last_modified_date", "notes", "created_by", "last_modified_by"))
            if sig in content and any(not blank(v) for _, v in sig):
                res.warn("VR-01", k, rec_id, "-", f"Possible duplicate record: content identical to {content[sig]}", "Merge or supersede duplicates; do not keep parallel records.")
            else:
                content[sig] = rec_id
            for f in e["fields"]:
                name, typ, req, con, _desc = f
                val = r[name]
                if req == "R" and blank(val):
                    res.fail("SCHEMA-02", k, rec_id, name, "Required field is empty", "Populate the field (see DICTIONARY sheet).")
                if blank(val):
                    continue
                if typ == "ENUM" and str(val) not in V[con]:
                    res.fail("SCHEMA-03", k, rec_id, name, f"'{val}' not in {con}", f"Use a code from {con} (VOCAB sheet).")
                elif typ == "MULTI_ENUM":
                    bad = [x for x in split_ids(val) if x not in V[con]]
                    if bad:
                        res.fail("SCHEMA-03", k, rec_id, name, f"{bad} not in {con}", f"Use codes from {con}, separated by '; '.")
                elif typ == "DATE":
                    if isinstance(val, str):
                        try:
                            datetime.datetime.strptime(val, "%d-%b-%Y")
                            res.warn("VR-29", k, rec_id, name, f"Date stored as text '{val}'", "Store as an Excel date formatted DD-MMM-YYYY.")
                        except ValueError:
                            res.fail("SCHEMA-04", k, rec_id, name, f"'{val}' is not a date", "Enter a valid date (DD-MMM-YYYY).")
                    elif not isinstance(val, datetime.date):
                        res.fail("SCHEMA-04", k, rec_id, name, f"'{val}' is not a date (cell not date-formatted)", "Enter a date with the template's date format.")
                elif typ in ("NUMBER", "SCORE", "TIER", "YEAR"):
                    n = num(val)
                    if n is None:
                        res.fail("SCHEMA-04", k, rec_id, name, f"'{val}' is not numeric", "Enter a number.")
                    else:
                        lim = {"SCORE": (1, 5), "TIER": (1, 6), "YEAR": (1900, 2100)}.get(typ)
                        if con == "LAT":
                            lim = (-90, 90)
                        if con == "LON":
                            lim = (-180, 180)
                        if lim and not (lim[0] <= n <= lim[1]) or (typ in ("SCORE", "TIER", "YEAR") and n != int(n)):
                            res.fail("SCHEMA-04", k, rec_id, name, f"{val} outside allowed range {lim}", "Correct the value.")
                elif typ in ("ISO4217", "ISO3"):
                    if not re.fullmatch(r"[A-Z]{3}", str(val)):
                        res.fail("SCHEMA-04", k, rec_id, name, f"'{val}' is not a 3-letter upper-case ISO code", "Use the ISO code.")
                elif typ == "SHORTTEXT" and len(str(val)) > 100:
                    res.fail("VR-11a", k, rec_id, name, "Structured value exceeds 100 characters", "Keep categorical values atomic; move narrative to analysis or reconciliation documents.")
                elif typ in ("ID_REF", "ID_LIST") and con != "charter":
                    targets = ["DAT"] if con == "DAT" else target_prefixes(con)
                    if not targets:
                        continue
                    for i in split_ids(val) if typ == "ID_LIST" else [str(val)]:
                        p = prefix_of(i)
                        if p not in targets:
                            res.fail("VR-05", k, rec_id, name, f"'{i}' is not a valid {'/'.join(targets)} reference", "Use a correctly formatted ID of the referenced register.")
                        elif p == "D":
                            if dec and i not in dec:
                                res.fail("VR-05", k, rec_id, name, f"Decision {i} not in decision log", "Reference an existing decision-log entry.")
                        elif i not in ids.get(REG_OF_PREFIX[p], {}):
                            res.fail("VR-05", k, rec_id, name, f"Referenced record {i} does not exist", "Create the referenced record first, or correct the reference.")
                elif typ == "DERIVED" and not blank(val):
                    pass  # checked by VR-16 below
            # VR-02 acceptance
            acc = r.get("acceptance_status")
            if acc in ("ACCEPTED", "REJECTED"):
                if blank(r.get("acceptance_decision_id")):
                    res.fail("VR-02", k, rec_id, "acceptance_decision_id", f"{acc} without a decision ID", "Record the decision-log ID that accepted/rejected this record.")
                if blank(r.get("acceptance_gate")):
                    res.fail("VR-02", k, rec_id, "acceptance_gate", f"{acc} without a gate", "Record the gate of acceptance/rejection.")
            elif acc == "PROPOSED" and not blank(r.get("acceptance_decision_id")):
                res.warn("VR-02", k, rec_id, "acceptance_decision_id", "PROPOSED record carries an acceptance decision ID", "Clear the decision ID or update acceptance_status.")
            # VR-03 supersession
            if r.get("record_status") == "SUPERSEDED":
                sb = r.get("superseded_by")
                if blank(sb):
                    res.fail("VR-03", k, rec_id, "superseded_by", "SUPERSEDED without superseded_by", "Reference the replacing record.")
                elif str(sb) == rec_id:
                    res.fail("VR-03", k, rec_id, "superseded_by", "Record supersedes itself", "Reference a different, replacing record.")
                elif str(sb) not in ids[k]:
                    res.fail("VR-03", k, rec_id, "superseded_by", f"Replacing record {sb} not found in this register", "Supersession must point to a record of the same register.")
            elif r.get("record_status") == "ACTIVE" and not blank(r.get("superseded_by")):
                res.warn("VR-03", k, rec_id, "superseded_by", "ACTIVE record has superseded_by set", "Set record_status = SUPERSEDED or clear superseded_by.")
            # VR-29 period ordering
            ps, pe = r.get("period_start"), r.get("period_end")
            if isinstance(ps, datetime.date) and isinstance(pe, datetime.date) and pe < ps:
                res.fail("VR-29", k, rec_id, "period_end", "period_end before period_start", "Correct the period.")

    mdr, src = ids.get("MDR", {}), ids.get("SRC", {})

    def tier(sid):
        s = src.get(sid)
        return int(num(s["source_tier"])) if s and num(s.get("source_tier")) is not None else None

    # ---- VR-16 derived lookups -------------------------------------------
    derived_map = {"source_title": "title_original", "publisher": "publisher", "source_publication_date": "publication_date",
                   "source_url_or_reference": "url", "source_tier": "source_tier", "discloser_independence": "discloser_independence"}
    for rn, r in data.get("MDR", {}).get("records", []):
        s = src.get(str(r.get("source_id")))
        for f, sf in derived_map.items():
            if blank(r.get(f)):
                continue
            exp = s.get(sf) if s else None
            if f == "source_url_or_reference" and s and blank(exp):
                exp = s.get("persistent_reference")
            if f == "source_tier":
                ok = s is not None and num(r[f]) == num(exp)
            else:
                ok = s is not None and str(r[f]) == str(exp)
            if not ok:
                res.warn("VR-16", "MDR", rid("MDR", r), f, "Derived value differs from the source register (hand-edited or stale)", "Regenerate derived columns from the authoritative register; never hand-edit.")

    # ---- MDR rules -------------------------------------------------------
    prj, site = ids.get("PRJ", {}), ids.get("SITE", {})
    for rule in ("VR-06", "VR-07", "VR-08", "VR-09", "VR-10", "VR-11", "VR-11a", "VR-12", "VR-13", "VR-14", "VR-15", "VR-30", "VR-31"):
        res.ran(rule, "MDR")
    for rn, r in data.get("MDR", {}).get("records", []):
        i = rid("MDR", r)
        es, conf = r.get("evidence_state"), r.get("confidence")
        m = ID_RE["DAT"].match(i)
        if m and r.get("workstream") and f"WS-{m.group(1)}" != r.get("workstream"):
            res.fail("VR-01", "MDR", i, "data_id", f"WS part of ID ({m.group(1)}) differs from workstream {r.get('workstream')}", "Use the owning workstream number in the ID.")
        # VR-06
        if es == "ESTIMATE":
            if blank(r.get("input_data_ids")):
                res.fail("VR-06", "MDR", i, "input_data_ids", "ESTIMATE without input_data_ids", "List the accepted input records.")
            if blank(r.get("estimate_method")):
                res.fail("VR-06", "MDR", i, "estimate_method", "ESTIMATE without estimate_method", "Document the method.")
        elif blank(r.get("source_id")):
            res.fail("VR-06", "MDR", i, "source_id", f"{es} record without source_id", "Cite the source register entry; only ESTIMATE records may omit it.")
        if not blank(r.get("source_id")) and blank(r.get("access_date")):
            res.fail("VR-06", "MDR", i, "access_date", "source_id given without access_date", "Record the date the value was read.")
        sids = [s for s in [r.get("source_id")] + split_ids(r.get("cross_check_source_ids")) if not blank(s)]
        tiers = [tier(str(s)) for s in sids if tier(str(s)) is not None]
        # VR-07
        if es == "VERIFIED":
            for f in ("page_table_section", "access_date", "verified_by", "verified_date"):
                if blank(r.get(f)):
                    res.fail("VR-07", "MDR", i, f, f"VERIFIED requires {f}", "Record exact location, access date and verifier.")
            t = tier(str(r.get("source_id")))
            if t is None or t > 3:
                res.fail("VR-07", "MDR", i, "source_id", f"VERIFIED requires a Tier 1-3 source (found tier {t})", "Downgrade to EXTRACTED/INDICATIVE or cite a Tier 1-3 source (D-082).")
        # VR-08
        if es in MAPPED_CONF and conf in CONF_RANK:
            mapped = MAPPED_CONF[es]
            if CONF_RANK[conf] > CONF_RANK[mapped] or (es == "ESTIMATE" and conf in ("VERIFIED", "CORROBORATED")):
                res.fail("VR-08", "MDR", i, "confidence", f"Confidence {conf} exceeds the maximum for evidence state {es} ({mapped})", "Confidence may be lower than the mapping, never higher.")
            lows = [q for q in ("quality_definition_consistency", "quality_completeness") if r.get(q) == "LOW"]
            if lows and conf == mapped and blank(r.get("notes")):
                res.warn("VR-08", "MDR", i, lows[0], "LOW quality rating without downgrade or caveat", "Lower the confidence or record an explicit caveat in notes (methodology section 2.1).")
        if es == "CONTRADICTED_UNRESOLVED" and blank(r.get("contradiction_id")):
            res.fail("VR-08", "MDR", i, "contradiction_id", "CONTRADICTED_UNRESOLVED without contradiction_id", "Link the contradiction register entry.")
        if r.get("contradiction_status") not in (None, "NONE") and blank(r.get("contradiction_id")):
            res.fail("VR-08", "MDR", i, "contradiction_id", "contradiction_status set without contradiction_id", "Link the contradiction register entry.")
        # VR-09
        if es == "CORROBORATED":
            if r.get("cross_check_status") != "AGREES":
                res.fail("VR-09", "MDR", i, "cross_check_status", "CORROBORATED requires cross_check_status = AGREES", "Record agreement or downgrade.")
            distinct = sorted(set(map(str, sids)))
            pubs = {str(src[s]["publisher"]) for s in distinct if s in src}
            if len(distinct) < 2:
                res.fail("VR-09", "MDR", i, "cross_check_source_ids", "CORROBORATED requires at least two sources", "Add independent corroborating sources or downgrade.")
            elif len(pubs) < 2:
                res.fail("VR-09", "MDR", i, "cross_check_source_ids", "Corroborating sources share one publisher (not independent)", "Find an independent source; shared origins count as one.")
            if not any(t is not None and t <= 4 for t in tiers):
                res.fail("VR-09", "MDR", i, "cross_check_source_ids", "No Tier 1-4 source among corroborating sources", "At least one source must be Tier 1-4 (D-082).")
            if any(t == 6 for t in tiers):
                res.fail("VR-09", "MDR", i, "cross_check_source_ids", "A Tier 6 (AI/unsourced) source is counted as corroboration", "Tier 6 is never evidence; remove it.")
        # VR-10
        if tiers and min(tiers) >= 5 and CONF_RANK.get(conf, 0) > CONF_RANK["INDICATIVE"]:
            res.fail("VR-10", "MDR", i, "confidence", f"Only Tier 5-6 sources but confidence {conf}", "Cap confidence at INDICATIVE (D-082).")
        # VR-30 media / trade press (D-086)
        media = [x for x in map(str, sids) if src.get(x, {}).get("document_type") in ("NEWS_ARTICLE", "TRADE_PRESS")]
        if sids and len(media) == len(sids):
            if es in ("VERIFIED", "CORROBORATED") or CONF_RANK.get(conf, 0) > CONF_RANK["INDICATIVE"]:
                res.fail("VR-30", "MDR", i, "source_id", "Media/trade press used to establish a material claim", "Media are discovery/context sources only: trace and cite the underlying primary or authoritative source (D-086).")
            elif blank(r.get("notes")):
                res.warn("VR-30", "MDR", i, "notes", "Media-only record without a note on the primary-source search", "Record that the primary source was sought and why it is not cited (D-086).")
        # VR-31 corporate filings: issuer's own facts only (D-086)
        if sids and tiers and len(tiers) == len(sids) and all(t == 5 for t in tiers) and len(media) < len(sids) \
                and r.get("subject_type") in ("NATIONAL_SYSTEM", "GEOGRAPHY", "BASIN"):
            res.fail("VR-31", "MDR", i, "subject_type", f"Tier 5 corporate source used for a {r.get('subject_type')} fact", "Corporate filings are authoritative only for the issuer's own facts; cite a Tier 1-4 source for government, grid, regulatory or national-system facts.")
        # VR-11 / VR-11a
        kind = r.get("value_kind")
        nv, lo, hi = (num(r.get(x)) if not blank(r.get(x)) else None for x in ("value", "value_low", "value_high"))
        q = r.get("value_qualifier")
        if kind == "NUMERIC":
            if nv is None and (lo is None or hi is None):
                res.fail("VR-11", "MDR", i, "value", "NUMERIC record without value or low/high", "Record the value or a range.")
            if q in ("SOURCE_RANGE", "CONTRADICTION_RANGE") and (lo is None or hi is None):
                res.fail("VR-11", "MDR", i, "value_low", f"{q} requires value_low and value_high", "Record both bounds.")
            if lo is not None and hi is not None and lo > hi:
                res.fail("VR-11", "MDR", i, "value_low", "value_low greater than value_high", "Correct the bounds.")
            if q == "CONTRADICTION_RANGE" and r.get("contradiction_status") != "RANGE-CARRIED":
                res.fail("VR-11", "MDR", i, "contradiction_status", "CONTRADICTION_RANGE requires contradiction_status = RANGE-CARRIED", "Link the RANGE-CARRIED contradiction.")
            if not blank(r.get("value_text")):
                res.fail("VR-11", "MDR", i, "value_text", "NUMERIC record carries value_text", "Use value_kind CATEGORICAL or clear value_text.")
        elif kind == "CATEGORICAL":
            if blank(r.get("value_text")):
                res.fail("VR-11", "MDR", i, "value_text", "CATEGORICAL record without value_text", "Record the structured value.")
            if any(x is not None for x in (nv, lo, hi)):
                res.fail("VR-11", "MDR", i, "value", "CATEGORICAL record carries numeric values", "Clear numeric fields.")
            ct, vt = r.get("categorical_type"), r.get("value_text")
            if blank(ct):
                res.fail("VR-11a", "MDR", i, "categorical_type", "CATEGORICAL record without categorical_type", "Set BOOLEAN, ENTITY_REFERENCE or CATEGORY_CODE (D-074).")
            elif not blank(vt):
                vt = str(vt)
                if ct == "BOOLEAN" and vt not in ("YES", "NO"):
                    res.fail("VR-11a", "MDR", i, "value_text", "BOOLEAN value must be YES or NO", "Record YES or NO only.")
                if ct == "ENTITY_REFERENCE" and (not ID_RE["ENT"].match(vt) or vt not in ids.get("ENT", {})):
                    res.fail("VR-11a", "MDR", i, "value_text", "ENTITY_REFERENCE must be an existing ENT- ID", "Reference the entity register.")
                if ct == "CATEGORY_CODE" and vt not in str(r.get("metric_definition") or ""):
                    res.fail("VR-11a", "MDR", i, "value_text", "CATEGORY_CODE value not listed in metric_definition", "Define the code list in metric_definition.")
                if len(vt.split()) > 8 or re.search(r"\b(because|due to|likely|suggests|should|we|recommend)\b", vt, re.I):
                    res.fail("VR-11a", "MDR", i, "value_text", "Value looks like narrative/interpretation, not an atomic fact", "Keep the MDR atomic; move narrative, opinion or causal explanation to analysis/reconciliation (D-074).")
        # VR-12
        unit, cur = r.get("unit"), r.get("currency")
        if kind == "NUMERIC" and blank(unit):
            res.fail("VR-12", "MDR", i, "unit", "NUMERIC record without unit", "Record the unit.")
        if unit and str(unit).startswith("CURRENCY"):
            if blank(cur):
                res.fail("VR-12", "MDR", i, "currency", "Currency-based unit without currency", "Record the ISO 4217 currency.")
            if blank(r.get("price_basis")):
                res.fail("VR-12", "MDR", i, "price_basis", "Currency value without price_basis", "Record NOMINAL or REAL.")
        elif not blank(cur) and unit != "FX_RATE":
            res.warn("VR-12", "MDR", i, "currency", f"currency set for non-currency unit {unit}", "Check unit/currency.")
        if r.get("price_basis") == "REAL":
            if blank(r.get("price_base_year")):
                res.fail("VR-12", "MDR", i, "price_base_year", "REAL value without base year", "Record the base year (P-024).")
            if blank(r.get("assumption_ids")):
                res.fail("VR-12", "MDR", i, "assumption_ids", "REAL value without deflator assumption", "Reference the deflator assumption.")
        # VR-13
        mc, ec, ac = r.get("metric_class"), r.get("energy_class"), r.get("ac_dc_basis")
        if mc in ("CAPACITY", "ENERGY", "DEMAND") and ec == "NOT_APPLICABLE":
            res.fail("VR-13", "MDR", i, "energy_class", f"{mc} metric requires a capacity/energy/demand class", "Record installed/available/dependable/... basis.")
        if ec in CAPACITY_CLASSES and mc not in ("CAPACITY",):
            res.fail("VR-13", "MDR", i, "energy_class", f"Capacity class {ec} used with metric_class {mc}", "Do not mix capacity with energy/demand metrics.")
        if ec in ENERGY_CLASSES and mc not in ("ENERGY",):
            res.fail("VR-13", "MDR", i, "energy_class", f"Energy class {ec} used with metric_class {mc}", "Do not mix energy with capacity/demand metrics.")
        if ec in DEMAND_CLASSES and mc not in ("DEMAND", "ENERGY"):
            res.fail("VR-13", "MDR", i, "energy_class", f"Demand class {ec} used with metric_class {mc}", "Use metric_class DEMAND.")
        if ec in CAPACITY_CLASSES and unit and unit not in POWER_UNITS:
            res.fail("VR-13", "MDR", i, "unit", f"Capacity class with non-power unit {unit}", "Use kW/MW/GW (MW_AC/MW_DC for PV).")
        if ec in ENERGY_CLASSES and unit and unit not in ENERGY_UNITS:
            res.fail("VR-13", "MDR", i, "unit", f"Energy class with non-energy unit {unit}", "Use kWh/MWh/GWh/TWh.")
        if unit == "MW_AC" and ac != "AC" or unit == "MW_DC" and ac != "DC":
            res.fail("VR-13", "MDR", i, "ac_dc_basis", f"Unit {unit} inconsistent with ac_dc_basis {ac}", "Align unit and AC/DC basis.")
        subj = prj.get(str(r.get("subject_id"))) if r.get("subject_type") == "PROJECT" else None
        is_pv = subj is not None and ("SOLAR_PV" in [subj.get("technology")] + split_ids(subj.get("hybrid_components")))
        if mc == "CAPACITY" and is_pv and ac not in ("AC", "DC", "BASIS_UNSTATED"):
            res.fail("VR-13", "MDR", i, "ac_dc_basis", "PV capacity without AC/DC basis", "Record AC or DC (or BASIS_UNSTATED with downgrade).")
        if ac == "BASIS_UNSTATED" and conf == "VERIFIED":
            res.fail("VR-13", "MDR", i, "confidence", "AC/DC basis unstated but confidence VERIFIED", "Downgrade confidence (protocol section 5.2).")
        if ec == "CLASS_UNSTATED":
            res.warn("VR-13", "MDR", i, "energy_class", "Capacity/energy class unstated - restricted use", "Resolve the class before analytical use.")
        # VR-14
        ct = r.get("conversion_type")
        if ct in ("FX", "DEFLATOR", "DC_AC_RATIO", "OTHER_DERIVATION"):
            if es != "ESTIMATE":
                res.fail("VR-14", "MDR", i, "evidence_state", f"Conversion {ct} must be an ESTIMATE record", "Record conversions as separate ESTIMATE records.")
            if blank(r.get("input_data_ids")):
                res.fail("VR-14", "MDR", i, "input_data_ids", "Conversion without input records", "Cite the original value and the rate record.")
            if ct == "FX" and not any(mdr.get(x, {}).get("metric_class") == "FX_RATE" for x in split_ids(r.get("input_data_ids"))):
                res.fail("VR-14", "MDR", i, "input_data_ids", "FX conversion does not cite an FX_RATE record", "Reference the FX_RATE record used (D-070).")
            if ct == "FX" and blank(r.get("fx_rate_type")):
                res.fail("VR-14", "MDR", i, "fx_rate_type", "FX conversion without rate type", "Record PERIOD_AVERAGE / END_OF_PERIOD / ...")
        if mc == "FX_RATE":
            for f in ("fx_rate_type", "fx_source_class", "fx_base_currency", "fx_quote_currency"):
                if blank(r.get(f)):
                    res.fail("VR-14", "MDR", i, f, f"FX_RATE record without {f}", "Complete the FX metadata (D-070).")
            if unit != "FX_RATE":
                res.fail("VR-14", "MDR", i, "unit", "FX_RATE record must use unit FX_RATE", "Set unit = FX_RATE.")
            if not blank(r.get("fx_base_currency")) and r.get("fx_base_currency") == r.get("fx_quote_currency"):
                res.fail("VR-14", "MDR", i, "fx_quote_currency", "Base and quote currency identical", "Correct the currency pair.")
            if (r.get("fx_rate_type") == "TRANSACTION_STATED") != (r.get("fx_source_class") == "TRANSACTION_DOCUMENT"):
                res.warn("VR-14", "MDR", i, "fx_source_class", "TRANSACTION_STATED and TRANSACTION_DOCUMENT should be used together", "Check rate type/source class.")
        # VR-15
        if ec == "SEASONAL_DEPENDABLE":
            if r.get("period_type") not in ("MONTH", "SEASON"):
                res.fail("VR-15", "MDR", i, "period_type", "SEASONAL_DEPENDABLE requires period_type MONTH or SEASON", "Record the month or season.")
            if blank(r.get("season_label")):
                res.fail("VR-15", "MDR", i, "season_label", "SEASONAL_DEPENDABLE without season_label", "Record the source's season definition.")
    hydro = {p for p, x in prj.items() if str(x.get("technology", "")).startswith("HYDRO") and x.get("component_type") == "GENERATION"}
    for p in sorted(hydro):
        recs = [r for r in mdr.values() if r.get("subject_type") == "PROJECT" and str(r.get("subject_id")) == p and r.get("record_status") != "SUPERSEDED"]
        if any(r.get("energy_class") == "INSTALLED" for r in recs) and not any(r.get("energy_class") == "SEASONAL_DEPENDABLE" for r in recs):
            res.fail("VR-15", "PRJ", p, "seasonal_output_data_ids", "Hydro plant has installed capacity but no seasonal dependable capacity record", "Add seasonal dependable capacity alongside nameplate (D-037).")

    # ---- VR-04 / VR-17 structural ------------------------------------------
    res.ran("VR-04", "SCHEMA")
    acc_v = set(V["v_acceptance_status"])
    ver_v = set(V["v_evidence_state_register"]) | set(V["v_confidence"]) | set(V["v_lead_outcome"]) | set(V["v_retrieval_status"])
    if acc_v & ver_v:
        res.fail("VR-04", "SCHEMA", "*", "acceptance_status", f"Acceptance vocabulary overlaps verification vocabularies: {acc_v & ver_v}", "Keep acceptance and verification vocabularies disjoint (D-062).")
    res.ran("VR-17", "SCHEMA")
    for reg in S.REGISTERS:
        if reg["key"] in ("MDR", "ASM"):
            continue
        for _s, _i, fl in reg["sheets"]:
            for f in fl:
                if f[1] == "NUMBER" and f[0] not in ("latitude", "longitude"):
                    res.fail("VR-17", "SCHEMA", "*", f[0], f"Quantitative column outside MDR/ASM in {reg['key']}", "Store quantities in the MDR and reference DAT- IDs.")

    # ---- Lead register ------------------------------------------------------
    for rule in ("VR-18",):
        res.ran(rule, "LEAD")
    for rn, r in data.get("LEAD", {}).get("records", []):
        i = rid("LEAD", r)
        o = r.get("lead_outcome")
        if r.get("evidence_state") != "RAW_LEAD":
            res.fail("VR-18", "LEAD", i, "evidence_state", "Lead evidence_state must be RAW_LEAD", "Leads never change state; create records in other registers.")
        if o in ("UNSUPPORTED", "CONTRADICTED", "NOT_VERIFIABLE", "PARTLY_VERIFIED") and blank(r.get("outcome_reason")):
            res.fail("VR-18", "LEAD", i, "outcome_reason", f"{o} without outcome_reason", "Record the reason (protocol section 13.3).")
        if o in ("UNSUPPORTED", "NOT_VERIFIABLE") and blank(r.get("search_path_log")):
            res.fail("VR-18", "LEAD", i, "search_path_log", f"{o} without search path", "Record the standard search path followed (protocol section 17).")
        if o in ("VERIFIED", "PARTLY_VERIFIED") and blank(r.get("resulting_record_ids")):
            res.fail("VR-18", "LEAD", i, "resulting_record_ids", f"{o} without resulting records", "Link the records created from this lead.")
        if o == "NOT_VERIFIABLE" and blank(r.get("gap_id")):
            res.fail("VR-18", "LEAD", i, "gap_id", "NOT_VERIFIABLE without gap_id", "Link the data-gap entry.")
        if o != "NOT_YET_CHECKED" and (blank(r.get("checked_by")) or blank(r.get("checked_date"))):
            res.fail("VR-18", "LEAD", i, "checked_by", "Checked lead without checked_by/checked_date", "Record who checked it and when.")
    for k in ("OPP", "CON", "ASM"):
        res.ran("VR-18", k)
        for rn, r in data.get(k, {}).get("records", []):
            for f in ("evidence_chain_data_ids", "evidence_chain_other_ids", "data_ids", "basis_data_ids"):
                if any(x.startswith("LEAD-") for x in split_ids(r.get(f))):
                    res.fail("VR-18", k, rid(k, r), f, "Lead ID used as evidence", "Leads are never evidence; cite verified records.")

    # ---- Projects / sites ----------------------------------------------------
    for k in ("PRJ", "SITE"):
        res.ran("VR-19", k)
        for rn, r in data.get(k, {}).get("records", []):
            i = rid(k, r)
            st, et, pc = r.get("lifecycle_stage"), r.get("lifecycle_evidence_type"), r.get("progress_condition")
            sup = EVIDENCE_SUPPORTS.get(et)
            if st and sup:
                if st == "CANCELLED" or sup == "CANCELLED":
                    if st != sup:
                        res.fail("VR-19", k, i, "lifecycle_evidence_type", f"Evidence {et} does not support stage {st}", "CANCELLED requires OFFICIAL_TERMINATION evidence (and vice versa).")
                elif STAGE_ORDER.index(st) > STAGE_ORDER.index(sup):
                    res.fail("VR-19", k, i, "lifecycle_stage", f"Stage {st} exceeds what {et} supports ({sup})", "Lower the stage or cite qualifying evidence (MoU at most ANNOUNCED; board approval is not financial commitment).")
                elif STAGE_ORDER.index(st) < STAGE_ORDER.index(sup):
                    res.warn("VR-19", k, i, "lifecycle_stage", f"Stage {st} below what {et} supports ({sup})", "Assign the highest stage with qualifying evidence.")
            if st in ("FINANCIALLY_COMMITTED", "UNDER_CONSTRUCTION", "OPERATIONAL"):
                ts = [tier(s) for s in split_ids(r.get("lifecycle_evidence_source_ids"))]
                ts = [t for t in ts if t is not None]
                if ts and min(ts) >= 5:
                    res.fail("VR-19", k, i, "lifecycle_evidence_source_ids", "Stage relies only on Tier 5-6 sponsor claims", "Corroborate with a Tier 1-4 source (methodology section 6.4).")
            if pc in ("DELAYED", "STALLED") and blank(r.get("progress_evidence_source_ids")):
                res.fail("VR-19", k, i, "progress_evidence_source_ids", f"{pc} without positive evidence", "Cite evidence; silence means UNVERIFIED, never STALLED.")
            if any(tier(s) == 6 for s in split_ids(r.get("lifecycle_evidence_source_ids")) + split_ids(r.get("progress_evidence_source_ids"))):
                res.fail("VR-19", k, i, "lifecycle_evidence_source_ids", "Tier 6 source used as status evidence", "Tier 6 is never evidence.")
    res.ran("VR-20", "PRJ")
    for rn, r in data.get("PRJ", {}).get("records", []):
        i = rid("PRJ", r)
        ic = {s: r.get(f"ic_{s}") for s in IC_STEPS}
        if r.get("component_type") == "INTERCONNECTOR":
            for s in IC_STEPS:
                if blank(ic[s]) or ic[s] == "NOT_APPLICABLE":
                    res.fail("VR-20", "PRJ", i, f"ic_{s}", "Interconnector step missing", "Record all five steps (YES/NO/UNVERIFIED) (D-069).")
        for s in IC_STEPS:
            if ic[s] == "YES" and blank(r.get(f"ic_{s}_evidence_source_ids")):
                res.fail("VR-20", "PRJ", i, f"ic_{s}_evidence_source_ids", f"Step {s} = YES without evidence", "Cite evidence for each step.")
        if ic["energised"] == "YES" and ic["constructed"] != "YES":
            res.fail("VR-20", "PRJ", i, "ic_constructed", "Energised without constructed", "Steps are sequential.")
        for s in ("synchronised", "operational", "commercially_active"):
            if ic[s] == "YES" and ic["energised"] != "YES":
                res.fail("VR-20", "PRJ", i, f"ic_{s}", f"{s} = YES requires energised = YES", "Physical completion never implies operation or trading.")
        if ic["commercially_active"] == "YES" and ic["operational"] != "YES":
            res.warn("VR-20", "PRJ", i, "ic_operational", "Commercially active but not recorded as operational", "Check the operational step.")
        if r.get("component_type") in ("INTERCONNECTOR", "TRANSMISSION_LINE") and r.get("lifecycle_stage") == "OPERATIONAL" and ic["energised"] != "YES":
            res.fail("VR-20", "PRJ", i, "ic_energised", "OPERATIONAL line/interconnector without energisation evidence", "Record ic_energised = YES with evidence, or lower the stage.")

    # ---- Sources / GIS copyright ------------------------------------------------
    res.ran("VR-20a", "SRC")
    res.ran("VR-21", "SRC")
    for rn, r in data.get("SRC", {}).get("records", []):
        i = rid("SRC", r)
        if blank(r.get("url")) and blank(r.get("persistent_reference")):
            res.fail("VR-20a", "SRC", i, "url", "Neither url nor persistent_reference", "Record a URL or persistent reference.")
        if r.get("publication_date_precision") != "UNDATED" and blank(r.get("publication_date")):
            res.fail("VR-20a", "SRC", i, "publication_date", "Dated source without publication_date", "Record the date or set precision UNDATED.")
        if r.get("retrieval_status") in ("CITATION_NOT_FOUND", "UNAVAILABLE") and blank(r.get("search_path_log")):
            res.fail("VR-20a", "SRC", i, "search_path_log", "Unfound/unavailable source without search path", "Record the search path (protocol section 17).")
        if r.get("reliability_flag") in ("UNDER_REVIEW", "UNRELIABLE") and blank(r.get("reliability_note")):
            res.fail("VR-20a", "SRC", i, "reliability_note", "Reliability flag without note", "Explain the reliability concern.")
        if r.get("local_copy_status") == "STORED":
            if blank(r.get("local_path")):
                res.fail("VR-20a", "SRC", i, "local_path", "STORED without local_path", "Record the archive path.")
            if r.get("copyright_basis") not in STORABLE_BASIS:
                res.fail("VR-21", "SRC", i, "copyright_basis", f"Stored with copyright basis {r.get('copyright_basis')}", "Do not commit copyrighted/unclear documents; keep reference only (D-019).")
    res.ran("VR-21", "GIS")
    res.ran("VR-23", "GIS")
    for rn, r in data.get("GIS", {}).get("records", []):
        i = rid("GIS", r)
        if r.get("committed_to_repo") == "YES" and r.get("redistribution_permitted") != "YES":
            res.fail("VR-21", "GIS", i, "committed_to_repo", "Layer committed without redistribution permission", "Catalogue only; do not commit.")
        if r.get("constraint_class") == "LEGAL_EXCLUSION" and blank(r.get("legal_basis_source_ids")):
            res.fail("VR-23", "GIS", i, "legal_basis_source_ids", "LEGAL_EXCLUSION without legal basis", "Cite the legal instrument.")
        if not blank(r.get("threshold_applied")):
            if gi < GATES.index("G6"):
                res.fail("VR-23", "GIS", i, "threshold_applied", f"Threshold applied before Gate 6 (current {gate})", "No thresholds before Gates 6-7 (D-038).")
            if blank(r.get("threshold_assumption_ids")):
                res.fail("VR-23", "GIS", i, "threshold_assumption_ids", "Threshold without assumption reference", "Record the threshold basis in the assumption register.")

    # ---- Entities -----------------------------------------------------------
    res.ran("VR-22", "ENT")
    for rn, r in data.get("ENT", {}).get("records", []):
        i = rid("ENT", r)
        pcl = r.get("guinea_presence_class")
        if pcl and pcl != "NOT_ASSESSED":
            ev = split_ids(r.get("presence_evidence_source_ids"))
            if pcl != "POTENTIAL_FUTURE_SUPPLIER_PARTNER" and not ev:
                res.fail("VR-22", "ENT", i, "presence_evidence_source_ids", f"{pcl} without evidence", "Cite Guinea-specific evidence; global presence never implies Guinea presence.")
            if any(tier(s) == 6 for s in ev):
                res.fail("VR-22", "ENT", i, "presence_evidence_source_ids", "Tier 6 source used as presence evidence", "Tier 6 is never evidence.")
            if blank(r.get("presence_assessed_date")):
                res.fail("VR-22", "ENT", i, "presence_assessed_date", "Presence class without assessment date", "Record the date assessed.")

    # ---- Gaps ------------------------------------------------------------------
    res.ran("VR-25", "GAP")
    for rn, r in data.get("GAP", {}).get("records", []):
        i = rid("GAP", r)
        exp = prios.get(str(r.get("research_question")))
        orig = r.get("question_priority_original")
        if exp and not blank(orig) and orig != exp:
            res.warn("VR-16", "GAP", i, "question_priority_original", f"Derived priority {orig} differs from charter {exp}", "Regenerate derived columns.")
        base = exp or orig
        if base and r.get("question_priority_current") and r.get("question_priority_current") != base:
            for f in ("priority_change_reason", "priority_change_decision_id"):
                if blank(r.get(f)):
                    res.fail("VR-25", "GAP", i, f, "Priority changed without reason/decision", "Priority changes occur only at Gate 4 with a decision (methodology section 12).")
        if r.get("gap_status") in ("FILLED", "PARTLY_FILLED") and blank(r.get("filled_by_data_ids")):
            res.fail("VR-25", "GAP", i, "filled_by_data_ids", "Filled gap without data references", "Link the filling MDR records.")

    # ---- Contradictions ---------------------------------------------------------
    res.ran("VR-26", "CON")
    for rn, r in data.get("CON", {}).get("records", []):
        i = rid("CON", r)
        d = split_ids(r.get("data_ids"))
        if len(set(d)) < 2:
            res.fail("VR-26", "CON", i, "data_ids", "Fewer than two conflicting MDR records", "List at least two DAT- IDs.")
        o = r.get("outcome")
        if o in ("RESOLVED-HIERARCHY", "RESOLVED-ERROR") and blank(r.get("governing_data_id")):
            res.fail("VR-26", "CON", i, "governing_data_id", f"{o} without governing_data_id", "Record the governing value.")
        if o == "RANGE-CARRIED":
            rd = r.get("range_data_id")
            if blank(rd):
                res.fail("VR-26", "CON", i, "range_data_id", "RANGE-CARRIED without range_data_id", "Reference the MDR range record.")
            elif mdr.get(str(rd), {}).get("value_qualifier") != "CONTRADICTION_RANGE":
                res.fail("VR-26", "CON", i, "range_data_id", "Range record is not a CONTRADICTION_RANGE", "Record the carried range with value_qualifier CONTRADICTION_RANGE.")
        if r.get("materiality") == "MATERIAL" and o in ("OPEN", "RANGE-CARRIED"):
            if r.get("escalated") != "YES":
                res.fail("VR-26", "CON", i, "escalated", "Material unresolved contradiction not escalated", "Escalate to owner review (Gate 4).")
            elif blank(r.get("escalation_gate")):
                res.fail("VR-26", "CON", i, "escalation_gate", "Escalated without gate", "Record the escalation gate.")
        if str(o).startswith("RESOLVED") and (blank(r.get("resolved_by")) or blank(r.get("resolved_date"))):
            res.fail("VR-26", "CON", i, "resolved_by", "Resolved without resolver/date", "Record who resolved it and when.")
        if "REPORTING_PRECISION" in (r.get("cause_code"), r.get("cause_code_secondary")):
            if r.get("precision_attribution") != "ATTRIBUTABLE":
                res.fail("VR-26", "CON", i, "precision_attribution", "REPORTING_PRECISION without ATTRIBUTABLE attribution", "All three D-072 conditions must be met.")
            if set(split_ids(r.get("diagnostic_tests_completed"))) != NINE_TESTS:
                res.fail("VR-26", "CON", i, "diagnostic_tests_completed", "Not all nine comparability tests recorded", "Complete every D-072 test before attributing to precision.")
        if r.get("precision_attribution") == "ATTRIBUTABLE" and blank(r.get("precision_justification")):
            res.fail("VR-26", "CON", i, "precision_justification", "ATTRIBUTABLE without justification", "Document why the difference is reporting precision.")
        for x in d:
            if x in mdr and str(mdr[x].get("contradiction_id") or "") != i:
                res.warn("VR-26", "CON", i, "data_ids", f"{x} does not reference this contradiction", "Set contradiction_id on the MDR record.")

    # ---- Assumptions ------------------------------------------------------------
    res.ran("VR-27", "ASM")
    for rn, r in data.get("ASM", {}).get("records", []):
        i = rid("ASM", r)
        vt = r.get("value_type")
        if vt == "DAT_REFERENCE":
            if blank(r.get("basis_data_ids")):
                res.fail("VR-27", "ASM", i, "basis_data_ids", "DAT_REFERENCE without basis_data_ids", "Reference the MDR record.")
            if not blank(r.get("value")):
                res.fail("VR-27", "ASM", i, "value", "DAT_REFERENCE carries a copied value", "Do not duplicate MDR values (D-053).")
        elif vt:
            for f in ("value", "unit"):
                if blank(r.get(f)):
                    res.fail("VR-27", "ASM", i, f, f"{vt} without {f}", "Record value and unit.")
            if vt == "DERIVED_CALCULATION" and blank(r.get("basis_data_ids")):
                res.fail("VR-27", "ASM", i, "basis_data_ids", "Derived assumption without basis records", "Reference the MDR inputs.")
            if vt in ("ENGINEERING_STANDARD", "POLICY_TARGET") and blank(r.get("standard_source_ids")):
                res.fail("VR-27", "ASM", i, "standard_source_ids", f"{vt} without source", "Cite the standard/policy source.")
            if vt == "ANALYST_JUDGEMENT" and r.get("confidence") in ("VERIFIED", "CORROBORATED"):
                res.fail("VR-27", "ASM", i, "confidence", "Judgement assumption with verified/corroborated confidence", "Judgement is never verified evidence.")

    # ---- Opportunities / Alendei participation -------------------------------
    res.ran("VR-24", "OPP")
    res.ran("VR-28", "OPP")
    opp = ids.get("OPP", {})
    score_fields = [f[0] for f in data.get("OPP", {}).get("fields", []) if re.match(r"d\d\d_", f[0]) and f[1] == "SCORE"]
    for rn, r in data.get("OPP", {}).get("records", []):
        i = rid("OPP", r)
        if gi < GATES.index("G7") and any(not blank(r.get(f)) for f in score_fields):
            res.fail("VR-24", "OPP", i, score_fields[0], f"Scores entered before Gate 7 (current {gate})", "Scores stay blank until Gate 7 anchors are approved.")
        if not blank(r.get("composite_score")) and blank(r.get("weight_set_decision_id")):
            res.fail("VR-24", "OPP", i, "composite_score", "Composite score without approved weight set", "Weights are not frozen (D-029).")
        if r.get("rating_frozen") == "YES":
            for f in ("freeze_decision_id", "freeze_date", "attractiveness_rating"):
                if blank(r.get(f)):
                    res.fail("VR-24", "OPP", i, f, f"Frozen rating without {f}", "Record the freeze decision, date and rating.")
        if any(t in ("FAIL", "UNRESOLVED") for t in (r.get(f) for f in ("ff_legal", "ff_offtake", "ff_site_constraint", "ff_technical", "ff_evidence"))) and blank(r.get("ff_notes")):
            res.fail("VR-24", "OPP", i, "ff_notes", "Fatal-flaw FAIL/UNRESOLVED without notes", "Explain the fatal-flaw result.")
        for x in split_ids(r.get("evidence_chain_data_ids")):
            m = mdr.get(x)
            if m and (m.get("acceptance_status") != "ACCEPTED" or m.get("record_status") != "ACTIVE"):
                res.fail("VR-28", "OPP", i, "evidence_chain_data_ids", f"{x} is not ACCEPTED and ACTIVE", "Evidence chains may cite only accepted, active records.")
    if any("alendei" in f[0].lower() for f in data.get("OPP", {}).get("fields", [])):
        res.fail("VR-24", "OPP", "*", "-", "Alendei field present in WS-27 register", "WS-27 is Alendei-neutral (D-028).")
    res.ran("VR-24", "ALP")
    for rn, r in data.get("ALP", {}).get("records", []):
        i = rid("ALP", r)
        o = opp.get(str(r.get("opp_id")))
        if o is None:
            continue  # VR-05 already reports the missing reference
        if o.get("rating_frozen") != "YES":
            res.fail("VR-24", "ALP", i, "opp_id", "Opportunity rating not frozen", "WS-28 may assess only frozen WS-27 opportunities.")
        if not blank(r.get("opp_attractiveness_at_freeze")) and r.get("opp_attractiveness_at_freeze") != o.get("attractiveness_rating"):
            res.fail("VR-24", "ALP", i, "opp_attractiveness_at_freeze", "Rating differs from the frozen WS-27 rating", "WS-28 cannot alter WS-27 ratings.")
        for s in split_ids(r.get("capability_evidence_source_ids")):
            if s in src and src[s].get("origin") != "OWNER_SUPPLIED":
                res.fail("VR-24", "ALP", i, "capability_evidence_source_ids", f"{s} is not OWNER_SUPPLIED", "Alendei capability evidence may come only from the user.")
        if r.get("tier_classification") in ("TIER_1_PURSUE_IMMEDIATELY", "TIER_2_DEVELOP"):
            if o.get("attractiveness_rating") not in ELIGIBLE_RATINGS:
                res.warn("VR-24", "ALP", i, "tier_classification", "Tier 1/2 for an opportunity rated below CONDITIONALLY_ATTRACTIVE", "Provisional eligibility rule (P-011); review.")
            if blank(r.get("capability_evidence_source_ids")):
                res.fail("VR-24", "ALP", i, "capability_evidence_source_ids", "Tier 1/2 without user-supplied capability evidence", "No Alendei capability may be asserted without user evidence.")
        if not blank(r.get("tier_classification")) and blank(r.get("classification_rationale")):
            res.fail("VR-24", "ALP", i, "classification_rationale", "Classification without rationale", "Record the rationale.")

    res.finalize()
    return res


def main(argv=None):
    ap = argparse.ArgumentParser(description="Validate the project registers (read-only).")
    ap.add_argument("--root", default=".")
    ap.add_argument("--gate", default="G2C", choices=GATES, help="current project gate (drives gate-dependent rules)")
    ap.add_argument("--format", default="text", choices=["text", "tsv"])
    ap.add_argument("--hide-pass", action="store_true")
    ap.add_argument("--strict", action="store_true", help="treat WARNING as failure for the exit code")
    a = ap.parse_args(argv)
    try:
        res = validate(a.root, a.gate)
    except Exception as ex:  # noqa: BLE001
        print(f"ERROR: {ex}", file=sys.stderr)
        return 2
    cols = ("STATUS", "RULE", "REGISTER", "RECORD", "FIELD", "REASON", "REMEDIATION")
    if a.format == "tsv":
        print("\t".join(cols))
    for it in res.items:
        if a.hide_pass and it[0] == "PASS":
            continue
        print("\t".join(it) if a.format == "tsv" else " | ".join(it))
    c = res.counts()
    print(f"SUMMARY: PASS={c['PASS']} FAIL={c['FAIL']} WARNING={c['WARNING']} (gate {a.gate})")
    return 1 if c["FAIL"] or (a.strict and c["WARNING"]) else 0


if __name__ == "__main__":
    sys.exit(main())
