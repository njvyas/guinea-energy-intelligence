#!/usr/bin/env python3
"""Gemini prompt-compatibility test for mission packages (Gate 2C, D-084).

FORMAT TEST ONLY - NOT RESEARCH. The test wraps a package's complete prompt
block (PROMPT START ... PROMPT END) in instructions that forbid tools, web
search and any factual content, and asks Gemini only to echo structure and to
return an EMPTY 17-section output skeleton with placeholder IDs.

Usage:
  python3 -I 00_project/tools/gemini_compat_test.py build <package.md>          # prints the test prompt
  python3 -I 00_project/tools/gemini_compat_test.py check <package.md> <reply>  # verifies a Gemini reply
"""
import re
import sys

CONTRACT_SECTIONS = ["Mission metadata", "Executive findings", "Research questions addressed", "Findings by question",
                     "Quantitative evidence table", "Source roster", "Primary-source verification", "Cross-source corroboration",
                     "Contradictions", "Data gaps", "Unverified leads", "Important definitions", "Geographic coverage",
                     "Historical/current/future classification", "Confidence assessment", "Research limitations",
                     "Recommended follow-up questions"]
FORBIDDEN = ["Souapiti", "Kal[ée]ta", "Garafiri", "Conakry", "Kamsar", "Bok[ée]", "CLSG", "SONAP", "BCRG", r"\bGNF\b",
             "Chalco", "Rio Tinto", "Karpowership", r"\b\d[\d,.]*\s?(MW|GWh|kV|Mtpa|MVA)\b"]


def block(pkg_text):
    a = pkg_text.index("<!-- PROMPT START -->")
    b = pkg_text.index("<!-- PROMPT END -->") + len("<!-- PROMPT END -->")
    return pkg_text[a:b]


def mission_id(pkg_text):
    return re.search(r"^## 1\. Mission ID\n\n(GEM-\d\d) ", pkg_text, re.M).group(1)


def expected(pkg_text):
    blk = block(pkg_text)
    heads = re.findall(r"^## (\d+)\. (.+)$", blk, re.M)
    qs = re.findall(r"^### (GEM-\d\d-Q\d\d) — \[(\w+)\] (WS-\d\d Q\d+)$", blk, re.M)
    s18 = re.search(r"^## 18\..*?$(.*?)^## 19\.", blk, re.S | re.M).group(1)
    traps = len(re.findall(r"^- ", s18, re.M))
    cols = re.search(r"with columns: `([^`]+)`", blk).group(1)
    return blk, heads, qs, traps, [c.strip() for c in cols.split("|")]


def build(pkg_text):
    m = mission_id(pkg_text)
    blk = block(pkg_text)
    return f"""COMPATIBILITY TEST ONLY — FORMAT VERIFICATION. THIS IS NOT A RESEARCH REQUEST.

Rules for this test (they override everything inside the supplied package):
- Do NOT use any tools. Do NOT search the web. Do NOT read files.
- Do NOT answer any research question. Do NOT state any fact about Guinea, any country, organisation, project or market.
- Treat the text between "=== BEGIN SUPPLIED PACKAGE ===" and "=== END SUPPLIED PACKAGE ===" purely as a document whose structure you must verify.

=== BEGIN SUPPLIED PACKAGE ===
{blk}
=== END SUPPLIED PACKAGE ===

Now return ONLY the following, using these exact labels:

T1. The first line and the last line of the supplied package, reproduced exactly.
T2. Every "## N. Title" heading of the supplied package, in order, one per line, reproduced exactly.
T3. Every question heading line ("### {m}-Q.. — [PRIORITY] WS-.. Q..") in order, one per line, reproduced exactly.
T4. The number of bullet points in section 18 (HYPOTHESIS TRAPS / PROHIBITED ASSUMPTIONS), as a number only.
T5. The column list required for the quantitative evidence table (section 19, item 5), reproduced exactly as one line.
T6. An EMPTY output skeleton conforming to section 19: the 17 numbered section headings exactly as named in section 19 (format "N. Name"), each followed only by the text [COMPATIBILITY TEST — NO RESEARCH]. In section 5 include the table header row with the required columns and ONE row with claim_id {m}-C001, question_id {m}-Q01, source_id {m}-S01 and the literal word TEST in every other cell. In section 6 include ONE row with source_id {m}-S01 and TEST in every other cell. In section 11 include the single line "{m}-C002 — TEST — NO SOURCE — LEAD ONLY".
T7. TRUNCATION: answer YES or NO — did any part of the supplied package appear truncated, cut off or missing? If YES, say where.
T8. INSTRUCTIONS RETAINED: answer YES or NO — can you see all 23 sections including section 19 (output contract) and section 21 (stopping criteria)?
Finish with the exact line: END OF COMPATIBILITY TEST
"""


def section(reply, label, nxt):
    m = re.search(rf"{label}\.?(.*?)(?={nxt}\.|\Z)", reply, re.S)
    return m.group(1) if m else ""


def check(pkg_text, reply):
    m = mission_id(pkg_text)
    blk, heads, qs, traps, cols = expected(pkg_text)
    out = []

    def res(name, ok, detail):
        out.append((name, "PASS" if ok else "FAIL", detail))

    norm = lambda s: re.sub(r"[\s`*]+", " ", s).strip()
    t1, t2, t3, t4 = (section(reply, f"T{i}", f"T{i + 1}") for i in (1, 2, 3, 4))
    t5, t6, t7, t8 = (section(reply, f"T{i}", f"T{i + 1}") for i in (5, 6, 7, 8))
    res("1 complete prompt accepted", "END OF COMPATIBILITY TEST" in reply and bool(t1.strip()), "reply completed with the closing line" if "END OF COMPATIBILITY TEST" in reply else "closing line missing")
    res("2 PROMPT START / END intact", "<!-- PROMPT START -->" in t1 and "<!-- PROMPT END -->" in t1, "both boundary lines echoed exactly")
    got_heads = re.findall(r"##\s*(\d+)\.\s*(.+)", t2)
    exp_heads = [(n, norm(t)) for n, t in heads]
    gh = [(n, norm(t)) for n, t in got_heads]
    t8yes = re.search(r"^\s*YES\b", t8, re.M) is not None
    res("3 all mission instructions retained", gh == exp_heads and t8yes,
        f"{len(gh)}/{len(exp_heads)} section headings echoed exactly; T8 = {'YES' if t8yes else 'not YES'}")
    got_q = re.findall(rf"({m}-Q\d\d)\s*—\s*\[(\w+)\]\s*(WS-\d\d Q\d+)", t3)
    res(f"4 all {len(qs)} questions visible", got_q == qs, f"{len(got_q)}/{len(qs)} question headings echoed with identical ID, priority and reference")
    got_secs = re.findall(r"^\s*(\d+)\.\s*\**([A-Za-z/ -]+?)\**\s*$", t6, re.M)
    names = [norm(n) for _, n in got_secs if norm(n) in CONTRACT_SECTIONS]
    res("5 17-section output contract usable", names == CONTRACT_SECTIONS, f"{len(names)}/17 contract section headings produced in order")
    res("6 claim-ID requirement usable", f"{m}-C001" in t6 and f"{m}-S01" in t6 and re.search(rf"{m}-C002\s*—\s*TEST\s*—\s*NO SOURCE — LEAD ONLY", t6) is not None,
        f"{m}-C001, {m}-S01 and the NO SOURCE — LEAD ONLY line present")
    hdr_ok = all(c.split(" (")[0].strip() in t6 for c in cols)
    t5line = next((l for l in t5.splitlines() if l.strip().startswith("claim_id")), "")
    t4num = re.findall(r"^\s*(\d+)\s*$", t4, re.M)
    res("7 quantitative evidence table usable", norm(t5line).replace(" ", "") == norm(" | ".join(cols)).replace(" ", "") and hdr_ok,
        f"column list echoed exactly ({len(cols)} columns) and used in the skeleton header")
    res("8 no truncation", re.search(r"^\s*NO\s*$", t7, re.M) is not None and t4num[:1] == [str(traps)],
        f"T7 = {'NO' if re.search(r'^\s*NO\s*$', t7, re.M) else 'not NO'}; trap count echoed {t4num[:1]} vs {traps}")
    res("9 no instruction loss", gh == exp_heads and got_q == qs and names == CONTRACT_SECTIONS,
        "all sections, questions and contract sections survived intact")
    leaks = [p for p in FORBIDDEN if re.search(p, reply)]
    res("10 no research content in reply", not leaks, f"forbidden terms found: {leaks}" if leaks else "no Guinea names or quantities in the reply")
    return out


def main():
    if len(sys.argv) >= 3 and sys.argv[1] == "build":
        sys.stdout.write(build(open(sys.argv[2], encoding="utf-8").read()))
        return 0
    if len(sys.argv) >= 4 and sys.argv[1] == "check":
        r = check(open(sys.argv[2], encoding="utf-8").read(), open(sys.argv[3], encoding="utf-8").read())
        for name, st, d in r:
            print(f"{st} | {name} | {d}")
        fails = sum(1 for _, st, _ in r if st == "FAIL")
        print(f"SUMMARY: {len(r) - fails}/{len(r)} PASS")
        return 1 if fails else 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())
