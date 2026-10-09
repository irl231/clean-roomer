#!/usr/bin/env python3
"""Parity report: generates parity.md and scorecard.md from the feature catalogue and build evidence.

Nobody writes a status by hand. The owner-approved catalogue says which features exist in the
target; the build writes evidence (registry commands, acceptance tests, real-input comparisons);
this script joins the two. Needs Python 3.8 or later and nothing else.

Catalogue, cleanroom/parity/features.tsv (tab-separated, '#' starts a comment, header required):
  id  area  feature  source  scope
  F-001  File  Open  S2  in
  F-090  Cloud  Sync  -  out:ADR-0004
  scope is 'in' or 'out:<reference>' (the ADR or roadmap entry that declares it out of scope).

Evidence, cleanroom/parity/evidence/*.tsv (written by the test run, never by hand, header required):
  feature  kind  ref  result
  F-001  command  file.open  wired
  F-001  test  tests/file_open::minimal  pass
  F-001  real  corpus/doc-001  fail
  kind command: a registry command id; result wired (reachable from every control surface the
                agent-control ADR names) or unwired.
  kind test:    an acceptance test; result pass, fail or skip.
  kind real:    one real input (corpus file, oracle comparison); result pass, fail or skip.

Status of an in-scope feature:
  live     every acceptance test that ran passed, at least one did, and (with --commands required)
           at least one command is wired.
  partial  some evidence exists but the feature is not live.
  missing  no wired command and no passing test.
Real-input results are reported next to the status, never folded into it: a feature can be live and
still fail on real files. Percentages round down.

Floors, cleanroom/parity/floors.tsv (optional, header required): measured minimums that only rise.
  area  live  real_pass
  File  12  140
  *  40  300
  area '*' is the total. A blank or '-' cell sets no floor. Below a floor is a finding; above it, a
  note says the floor can be raised. Lowering a floor is an owner decision (ADR).

Exit status: 0 ok, 1 findings (invalid evidence, a floor broken, or --check found stale or
hand-edited output), 2 configuration error.

Usage:
  python3 parity_report.py [--root DIR] [--commands required|optional|none] [--check]
                           [--features FILE] [--evidence DIR] [--floors FILE] [--out DIR]
  python3 parity_report.py --self-test
"""
from __future__ import annotations

import argparse
import glob
import os
import re
import shutil
import sys
import tempfile
from typing import Dict, List, Optional, Tuple

FEATURE_HEADER = ["id", "area", "feature", "source", "scope"]
EVIDENCE_HEADER = ["feature", "kind", "ref", "result"]
FLOOR_HEADER = ["area", "live", "real_pass"]
RESULTS = {
    "command": {"wired", "unwired"},
    "test": {"pass", "fail", "skip"},
    "real": {"pass", "fail", "skip"},
}
ID_RX = re.compile(r"^[A-Za-z][A-Za-z0-9._-]*$")


class ConfigError(Exception):
    pass


def _rows(path: str, header: List[str]) -> List[Tuple[int, List[str]]]:
    out: List[Tuple[int, List[str]]] = []
    seen_header = False
    with open(path, "r", encoding="utf-8-sig", newline="") as fh:
        for n, raw in enumerate(fh, start=1):
            line = raw.rstrip("\r\n")
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            cells = [c.strip() for c in line.split("\t")]
            if not seen_header:
                if [c.lower() for c in cells] != header:
                    raise ConfigError(f"{path}:{n}: expected header '{chr(9).join(header)}' (tab-separated)")
                seen_header = True
                continue
            out.append((n, cells))
    if not seen_header:
        raise ConfigError(f"{path}: no header line")
    return out


def read_features(path: str) -> Tuple[List[Dict], List[str]]:
    features: List[Dict] = []
    findings: List[str] = []
    ids: Dict[str, int] = {}
    for n, cells in _rows(path, FEATURE_HEADER):
        where = f"{path}:{n}"
        if len(cells) != len(FEATURE_HEADER):
            findings.append(f"catalog  {where}: expected {len(FEATURE_HEADER)} columns, got {len(cells)}")
            continue
        fid, area, name, source, scope = cells
        if not ID_RX.match(fid):
            findings.append(f"catalog  {where}: invalid id '{fid}'")
            continue
        if fid in ids:
            findings.append(f"catalog  {where}: duplicate id '{fid}' (first on line {ids[fid]})")
            continue
        if not area or not name:
            findings.append(f"catalog  {where}: area and feature must not be empty")
            continue
        if scope == "in":
            out_ref = ""
        elif scope.startswith("out:") and scope[4:].strip():
            out_ref = scope[4:].strip()
        else:
            findings.append(f"catalog  {where}: scope must be 'in' or 'out:<ADR or roadmap reference>', got '{scope}'")
            continue
        ids[fid] = n
        features.append({"id": fid, "area": area, "name": name, "source": source or "-", "out": out_ref})
    return features, findings


def read_evidence(folder: str, features: List[Dict]) -> Tuple[Dict[str, List[Tuple[str, str, str]]], List[str]]:
    by_id = {f["id"]: f for f in features}
    evidence: Dict[str, List[Tuple[str, str, str]]] = {f["id"]: [] for f in features}
    findings: List[str] = []
    if not os.path.isdir(folder):
        return evidence, findings
    for path in sorted(glob.glob(os.path.join(folder, "*.tsv"))):
        for n, cells in _rows(path, EVIDENCE_HEADER):
            where = f"{path.replace(os.sep, '/')}:{n}"
            if len(cells) != len(EVIDENCE_HEADER):
                findings.append(f"evidence {where}: expected {len(EVIDENCE_HEADER)} columns, got {len(cells)}")
                continue
            fid, kind, ref, result = cells
            if fid not in by_id:
                findings.append(f"evidence {where}: unknown feature id '{fid}' (not in the catalogue)")
                continue
            if kind not in RESULTS:
                findings.append(f"evidence {where}: unknown kind '{kind}' (command, test, real)")
                continue
            if result not in RESULTS[kind]:
                findings.append(f"evidence {where}: result '{result}' not valid for {kind} ({', '.join(sorted(RESULTS[kind]))})")
                continue
            if not ref:
                findings.append(f"evidence {where}: empty ref")
                continue
            if by_id[fid]["out"]:
                findings.append(f"evidence {where}: '{fid}' is out of scope ({by_id[fid]['out']}) but has evidence; change the scope or remove the evidence")
                continue
            evidence[fid].append((kind, ref, result))
    for fid in evidence:
        evidence[fid].sort()
    return evidence, findings


def assess(feature: Dict, ev: List[Tuple[str, str, str]], commands: str) -> Dict:
    wired = sorted({r for k, r, res in ev if k == "command" and res == "wired"})
    unwired = sorted({r for k, r, res in ev if k == "command" and res == "unwired"} - set(wired))
    t = {res: [r for k, r, x in ev if k == "test" and x == res] for res in ("pass", "fail", "skip")}
    real = {res: [r for k, r, x in ev if k == "real" and x == res] for res in ("pass", "fail", "skip")}
    need_cmd = commands == "required"
    if t["pass"] and not t["fail"] and (wired or not need_cmd):
        status = "live"
    elif wired or t["pass"] or t["fail"] or unwired:
        status = "partial"
    else:
        status = "missing"
    return {"status": status, "wired": wired, "unwired": unwired, "tests": t, "real": real}


def _pct(n: int, d: int) -> str:
    return f"{(100 * n) // d}%" if d else "-"


def _cell(s: str) -> str:
    return s.replace("|", "\\|").replace("\n", " ")


def _counts(d: Dict[str, List[str]], empty: str = "not measured") -> str:
    ran = len(d["pass"]) + len(d["fail"])
    if not ran and not d["skip"]:
        return empty
    s = f"{len(d['pass'])}/{ran} pass" if ran else "none ran"
    if d["skip"]:
        s += f", {len(d['skip'])} skipped"
    return s


HEADER_NOTE = ("Generated by `parity_report.py` from `features.tsv` and the evidence files of the last "
               "test run. Do not edit: change the catalogue or the code and regenerate. Every number "
               "is measured; a reviewer reruns the gate to reproduce it.")


def render(features: List[Dict], evidence: Dict[str, List[Tuple[str, str, str]]], commands: str) -> Tuple[str, str]:
    results = {f["id"]: assess(f, evidence[f["id"]], commands) for f in features if not f["out"]}
    areas: List[str] = []
    for f in features:
        if f["area"] not in areas:
            areas.append(f["area"])
    cmd_rule = {"required": "a wired registry command is required for live",
                "optional": "registry commands are listed but not required for live",
                "none": "this project has no command registry (agent-control ADR)"}[commands]

    p: List[str] = ["# Parity tracker", "", HEADER_NOTE, "", f"Commands: {cmd_rule}.", ""]
    failing: List[str] = []
    for area in areas:
        rows = [f for f in features if f["area"] == area and not f["out"]]
        if not rows:
            continue
        p += [f"## {area}", ""]
        if commands == "none":
            p += ["| Id | Feature | Source | Status | Tests | Real inputs |", "|---|---|---|---|---|---|"]
        else:
            p += ["| Id | Feature | Source | Status | Commands | Tests | Real inputs |", "|---|---|---|---|---|---|---|"]
        for f in rows:
            a = results[f["id"]]
            cmds = ", ".join(f"`{c}`" for c in a["wired"]) or "-"
            if a["unwired"]:
                cmds += " (unwired: " + ", ".join(f"`{c}`" for c in a["unwired"]) + ")"
            cells = [f["id"], _cell(f["name"]), _cell(f["source"]), a["status"]]
            if commands != "none":
                cells.append(_cell(cmds))
            cells += [_counts(a["tests"], "no tests"), _counts(a["real"])]
            p.append("| " + " | ".join(cells) + " |")
            for r in a["tests"]["fail"]:
                failing.append(f"- {f['id']} test `{_cell(r)}`")
            for r in a["real"]["fail"]:
                failing.append(f"- {f['id']} real input `{_cell(r)}`")
        p.append("")
    out_rows = [f for f in features if f["out"]]
    if out_rows:
        p += ["## Out of clean-room scope", "", "| Id | Area | Feature | Reference |", "|---|---|---|---|"]
        p += [f"| {f['id']} | {_cell(f['area'])} | {_cell(f['name'])} | {_cell(f['out'])} |" for f in out_rows]
        p.append("")
    p += ["## Failing", ""]
    p += failing or ["none"]
    p.append("")

    s: List[str] = ["# Parity scorecard", "", HEADER_NOTE, "",
                    "Live: every acceptance test that ran passed" + (" and a registry command is wired." if commands == "required" else "."),
                    "Real inputs: pass rate on corpus files and oracle comparisons, reported separately because a "
                    "feature can be live and still fail on real files. Percentages round down.", ""]
    head = ["Area", "In scope"] + ([] if commands == "none" else ["Wired"]) + \
           ["Live", "Partial", "Missing", "Real inputs measured", "Real inputs passing", "Out of scope"]
    s += ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]

    def line(label: str, fs: List[Dict]) -> str:
        ins = [f for f in fs if not f["out"]]
        rs = [results[f["id"]] for f in ins]
        n = len(ins)
        wired = sum(1 for r in rs if r["wired"])
        live = sum(1 for r in rs if r["status"] == "live")
        part = sum(1 for r in rs if r["status"] == "partial")
        miss = sum(1 for r in rs if r["status"] == "missing")
        measured = sum(1 for r in rs if r["real"]["pass"] or r["real"]["fail"])
        rp = sum(len(r["real"]["pass"]) for r in rs)
        rr = rp + sum(len(r["real"]["fail"]) for r in rs)
        cells = [label, str(n)]
        if commands != "none":
            cells.append(f"{wired} ({_pct(wired, n)})")
        cells += [f"{live} ({_pct(live, n)})", str(part), str(miss), f"{measured} of {n}",
                  f"{rp} of {rr} ({_pct(rp, rr)})" if rr else "not measured", str(len(fs) - n)]
        return "| " + " | ".join(cells) + " |"

    for area in areas:
        s.append(line(_cell(area), [f for f in features if f["area"] == area]))
    s.append(line("**Total**", features))
    s.append("")
    return "\n".join(p), "\n".join(s)


def read_floors(path: str, features: List[Dict]) -> Tuple[Dict[str, Tuple[Optional[int], Optional[int]]], List[str]]:
    areas = {f["area"] for f in features} | {"*"}
    floors: Dict[str, Tuple[Optional[int], Optional[int]]] = {}
    findings: List[str] = []
    for n, cells in _rows(path, FLOOR_HEADER):
        where = f"{path.replace(os.sep, '/')}:{n}"
        if len(cells) != len(FLOOR_HEADER):
            findings.append(f"floors   {where}: expected {len(FLOOR_HEADER)} columns, got {len(cells)}")
            continue
        area, live, real = cells
        if area not in areas:
            findings.append(f"floors   {where}: unknown area '{area}' (not in the catalogue; '*' is the total)")
            continue
        if area in floors:
            findings.append(f"floors   {where}: duplicate area '{area}'")
            continue
        vals: List[Optional[int]] = []
        for v in (live, real):
            if v in ("", "-"):
                vals.append(None)
            elif v.isdigit():
                vals.append(int(v))
            else:
                findings.append(f"floors   {where}: '{v}' is not a whole number")
                break
        else:
            floors[area] = (vals[0], vals[1])
    return floors, findings


def check_floors(features: List[Dict], evidence: Dict[str, List[Tuple[str, str, str]]], commands: str,
                 floors: Dict[str, Tuple[Optional[int], Optional[int]]]) -> Tuple[List[str], List[str]]:
    findings: List[str] = []
    notes: List[str] = []
    for area, (live_floor, real_floor) in sorted(floors.items()):
        ins = [f for f in features if not f["out"] and (area == "*" or f["area"] == area)]
        rs = [assess(f, evidence[f["id"]], commands) for f in ins]
        measured = {"live": sum(1 for r in rs if r["status"] == "live"),
                    "real_pass": sum(len(r["real"]["pass"]) for r in rs)}
        label = "total" if area == "*" else f"area '{area}'"
        for key, floor in (("live", live_floor), ("real_pass", real_floor)):
            if floor is None:
                continue
            if measured[key] < floor:
                findings.append(f"floor    {label}: {key} {measured[key]} is below the floor {floor} (fix the regression; lowering a floor is an owner decision)")
            elif measured[key] > floor:
                notes.append(f"note: {label}: {key} {measured[key]} is above the floor {floor}; raise the floor in the same commit")
    return findings, notes


def run(features_path: str, evidence_dir: str, out_dir: str, commands: str, check: bool,
        floors_path: str = "") -> Tuple[List[str], List[str]]:
    """Returns (findings, notes). Raises ConfigError."""
    if not os.path.isfile(features_path):
        raise ConfigError(f"catalogue not found: {features_path}")
    features, findings = read_features(features_path)
    evidence, ev_findings = read_evidence(evidence_dir, features)
    findings += ev_findings
    notes: List[str] = []
    if not os.path.isdir(evidence_dir):
        notes.append(f"note: no evidence folder at {evidence_dir}; every in-scope feature reports missing")
    floors: Dict[str, Tuple[Optional[int], Optional[int]]] = {}
    if floors_path and os.path.isfile(floors_path):
        floors, fl_findings = read_floors(floors_path, features)
        findings += fl_findings
    if findings:
        return findings, notes
    fl_findings, fl_notes = check_floors(features, evidence, commands, floors)
    findings += fl_findings
    notes += fl_notes
    parity, score = render(features, evidence, commands)
    targets = [(os.path.join(out_dir, "parity.md"), parity), (os.path.join(out_dir, "scorecard.md"), score)]
    for path, text in targets:
        if check:
            try:
                with open(path, "r", encoding="utf-8", newline="") as fh:
                    current = fh.read().replace("\r\n", "\n")
            except OSError:
                current = None
            if current != text:
                findings.append(f"stale    {path.replace(os.sep, '/')}: differs from the catalogue and evidence (hand-edited or not regenerated)")
        else:
            os.makedirs(out_dir, exist_ok=True)
            with open(path, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(text)
            notes.append(f"wrote {path.replace(os.sep, '/')}")
    return findings, notes


# ----------------------------------------------------------------------------------------------
# Self-test: prove the report derives status from evidence and that the check can fail.

def _w(base: str, rel: str, text: str) -> None:
    p = os.path.join(base, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


def self_test() -> int:
    failures: List[str] = []
    T = "\t"

    def cat(*rows: str) -> str:
        return "# catalogue\n" + T.join(FEATURE_HEADER) + "\n" + "\n".join(rows) + "\n"

    def ev(*rows: str) -> str:
        return T.join(EVIDENCE_HEADER) + "\n" + "\n".join(rows) + "\n"

    def expect(label: str, cond: bool, detail: str = "") -> None:
        if not cond:
            failures.append(f"[{label}] {detail}")

    tmp = tempfile.mkdtemp(prefix="parity_selftest_")
    try:
        feats = os.path.join(tmp, "features.tsv")
        evd = os.path.join(tmp, "evidence")
        _w(tmp, "features.tsv", cat(
            T.join(["F-001", "File", "Open", "S2", "in"]),
            T.join(["F-002", "File", "Export", "S1", "in"]),
            T.join(["F-003", "File", "Print", "S2", "in"]),
            T.join(["F-004", "Edit", "Undo", "S2", "in"]),
            T.join(["F-005", "Edit", "Paste | special", "S2", "in"]),
            T.join(["F-090", "Cloud", "Sync", "-", "out:ADR-0004"]),
        ))
        _w(tmp, "evidence/run.tsv", ev(
            T.join(["F-001", "command", "file.open", "wired"]),
            T.join(["F-001", "test", "open_minimal", "pass"]),
            T.join(["F-001", "real", "corpus/a", "pass"]),
            T.join(["F-001", "real", "corpus/b", "fail"]),
            T.join(["F-001", "real", "corpus/c", "skip"]),
            T.join(["F-002", "test", "export_basic", "pass"]),
            T.join(["F-003", "command", "file.print", "wired"]),
            T.join(["F-003", "test", "print_page", "fail"]),
            T.join(["F-004", "command", "edit.undo", "wired"]),
            T.join(["F-004", "test", "undo_once", "pass"]),
            T.join(["F-004", "test", "undo_needs_oracle", "skip"]),
        ))

        # Status derivation, commands required
        features, f1 = read_features(feats)
        evidence, f2 = read_evidence(evd, features)
        expect("clean inputs", not f1 and not f2, "; ".join(f1 + f2))
        st = {f["id"]: assess(f, evidence[f["id"]], "required")["status"] for f in features if not f["out"]}
        expect("required", st == {"F-001": "live", "F-002": "partial", "F-003": "partial", "F-004": "live", "F-005": "missing"}, str(st))
        st = {f["id"]: assess(f, evidence[f["id"]], "optional")["status"] for f in features if not f["out"]}
        expect("optional", st["F-002"] == "live" and st["F-003"] == "partial", str(st))

        # Rendering: scorecard numbers, real inputs kept apart, escaping
        parity, score = render(features, evidence, "required")
        expect("scorecard total", "| **Total** | 5 | 3 (60%) | 2 (40%) | 2 | 1 | 1 of 5 | 1 of 2 (50%) | 1 |" in score, score)
        expect("scorecard area", "| File | 3 | 2 (66%) | 1 (33%) | 2 | 0 | 1 of 3 | 1 of 2 (50%) | 0 |" in score, score)
        expect("parity row", "| F-001 | Open | S2 | live | `file.open` | 1/1 pass | 1/2 pass, 1 skipped |" in parity, parity)
        expect("parity escape", "Paste \\| special" in parity, parity)
        expect("parity failing", "- F-003 test `print_page`" in parity and "- F-001 real input `corpus/b`" in parity, parity)
        expect("parity out of scope", "| F-090 | Cloud | Sync | ADR-0004 |" in parity, parity)
        _, score_none = render(features, evidence, "none")
        expect("no registry", "Wired" not in score_none, score_none)

        # Write, then check passes; a hand edit fails the check
        out = os.path.join(tmp, "out")
        fnd, _ = run(feats, evd, out, "required", check=False)
        expect("write", not fnd, "; ".join(fnd))
        fnd, _ = run(feats, evd, out, "required", check=True)
        expect("check clean", not fnd, "; ".join(fnd))
        with open(os.path.join(out, "scorecard.md"), "a", encoding="utf-8") as fh:
            fh.write("| Edit | 2 | 2 (100%) | 2 (100%) | 0 | 0 | 2 of 2 | 2 of 2 (100%) | 0 |\n")
        fnd, _ = run(feats, evd, out, "required", check=True)
        expect("check hand edit", any(x.startswith("stale") and "scorecard.md" in x for x in fnd), "; ".join(fnd))
        _w(tmp, "evidence/later.tsv", ev(T.join(["F-005", "test", "paste_plain", "pass"])))
        fnd, _ = run(feats, evd, out, "required", check=True)
        expect("check stale", any(x.startswith("stale") and "parity.md" in x for x in fnd), "; ".join(fnd))
        os.remove(os.path.join(evd, "later.tsv"))

        # Floors: held, broken, raisable, malformed
        def floors(*rows: str) -> str:
            _w(tmp, "floors.tsv", T.join(FLOOR_HEADER) + "\n" + "\n".join(rows) + "\n")
            return os.path.join(tmp, "floors.tsv")
        fnd, notes = run(feats, evd, out, "required", False, floors(T.join(["File", "1", "1"]), T.join(["*", "2", "-"])))
        expect("floors held", not fnd and not any("above the floor" in x for x in notes), "; ".join(fnd + notes))
        fnd, _ = run(feats, evd, out, "required", True, floors(T.join(["File", "2", "-"]), T.join(["*", "-", "2"])))
        joined = "\n".join(fnd)
        expect("floor broken", "area 'File': live 1 is below the floor 2" in joined and "total: real_pass 1 is below the floor 2" in joined, joined)
        fnd, notes = run(feats, evd, out, "required", True, floors(T.join(["Edit", "0", ""])))
        expect("floor raisable", not fnd and any("area 'Edit': live 1 is above the floor 0" in x for x in notes), "; ".join(fnd + notes))
        fnd, _ = run(feats, evd, out, "required", True, floors(T.join(["Nowhere", "1", "1"]), T.join(["File", "x", "1"]), T.join(["File", "1", "1"]), T.join(["Edit", "1", "1"]), T.join(["Edit", "1", "1"])))
        joined = "\n".join(fnd)
        for needle in ["unknown area 'Nowhere'", "'x' is not a whole number", "duplicate area 'Edit'"]:
            expect("floors " + needle, needle in joined, joined)

        # Planted violations in the catalogue
        _w(tmp, "bad/features.tsv", cat(
            T.join(["F-001", "File", "Open", "S2", "in"]),
            T.join(["F-001", "File", "Open again", "S2", "in"]),
            T.join(["F-002", "File", "Export", "S1", "out"]),
            T.join(["F-003", "File", "Print", "S2"]),
            T.join(["bad id", "File", "Save", "S2", "in"]),
            T.join(["F-004", "", "Undo", "S2", "in"]),
        ))
        _, fb = read_features(os.path.join(tmp, "bad/features.tsv"))
        joined = "\n".join(fb)
        for needle in ["duplicate id 'F-001'", "scope must be", "expected 5 columns", "invalid id 'bad id'", "must not be empty"]:
            expect("catalogue " + needle, needle in joined, joined)

        # Planted violations in the evidence
        _w(tmp, "evidence/bad.tsv", ev(
            T.join(["F-777", "test", "ghost", "pass"]),
            T.join(["F-001", "screenshot", "x", "pass"]),
            T.join(["F-001", "command", "file.open", "pass"]),
            T.join(["F-090", "test", "sync_basic", "pass"]),
            T.join(["F-001", "test", "", "pass"]),
        ))
        fnd, _ = run(feats, evd, out, "required", check=True)
        joined = "\n".join(fnd)
        for needle in ["unknown feature id 'F-777'", "unknown kind 'screenshot'", "not valid for command", "out of scope", "empty ref"]:
            expect("evidence " + needle, needle in joined, joined)
        expect("no output on bad evidence", not any(x.startswith("stale") for x in fnd), joined)

        # Configuration errors
        _w(tmp, "noheader.tsv", "F-001\tFile\tOpen\tS2\tin\n")
        try:
            read_features(os.path.join(tmp, "noheader.tsv"))
            expect("header", False, "missing header was accepted")
        except ConfigError:
            pass
        try:
            run(os.path.join(tmp, "absent.tsv"), evd, out, "required", check=True)
            expect("absent catalogue", False, "absent catalogue was accepted")
        except ConfigError:
            pass
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    if failures:
        print("selftest FAILED")
        for f in failures:
            print(f)
        return 1
    print("selftest ok: status derived from evidence, real inputs reported apart, floors enforced, every planted violation and every hand edit was detected")
    return 0


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="Generate parity.md and scorecard.md from the catalogue and build evidence")
    ap.add_argument("--root", default=".")
    ap.add_argument("--features", default="")
    ap.add_argument("--evidence", default="")
    ap.add_argument("--out", default="")
    ap.add_argument("--floors", default="")
    ap.add_argument("--commands", choices=["required", "optional", "none"], default="required")
    ap.add_argument("--check", action="store_true", help="do not write; fail if the committed reports differ")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv)
    if args.self_test:
        return self_test()
    base = os.path.join(args.root, "cleanroom", "parity")
    try:
        findings, notes = run(args.features or os.path.join(base, "features.tsv"),
                              args.evidence or os.path.join(base, "evidence"),
                              args.out or base, args.commands, args.check,
                              args.floors or os.path.join(base, "floors.tsv"))
    except (OSError, ConfigError) as e:
        print(f"configuration error: {e}", file=sys.stderr)
        return 2
    for n in notes:
        print(n, file=sys.stderr)
    for f in findings:
        print(f)
    if findings:
        print(f"\n{len(findings)} finding(s). Fix the evidence or regenerate; never edit the reports by hand.", file=sys.stderr)
        return 1
    print("parity report: " + ("up to date" if args.check else "generated"))
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    except Exception:
        pass
    sys.exit(main())
