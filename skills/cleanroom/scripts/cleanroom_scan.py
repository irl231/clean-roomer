#!/usr/bin/env python3
"""Clean-room scan: checks a repository against cleanroom/deny-list.txt.

Twin of cleanroom_scan.ps1 with the same deny-list format, the same output lines and the same exit
codes. Needs Python 3.8 or later and nothing else. Use whichever of the two runs on the machine.

Deny-list format (one entry per line, '#' starts a comment):
  term:   <text>   case-insensitive text that must not appear in text files
  notice: <text>   like term, reported as a vendor notice (copyright lines, trademarks)
  meta:   <text>   case-insensitive bytes that must not appear in the first 256 KiB of ANY file
  ext:    .abc     file extension that must not be tracked
  path:   <glob>   path glob that must not be tracked (for example plan/**)
  allow:  <glob>   TEXT files exempt from term / notice / meta. Binary files are never exempt;
                   ext and path are never exempt.

Scanned files: in a git work tree, tracked plus untracked-not-ignored files; otherwise every file
except .git, node_modules, target, dist, build, .venv, __pycache__. Text is detected as UTF-8
(default) or UTF-16 LE/BE (BOM or byte pattern) and scanned line by line at any size. Nothing is
skipped silently: unreadable or unlocatable files are reported as 'error'.

Exit status: 0 clean, 1 findings, 2 configuration error.

Usage:
  python3 cleanroom_scan.py [--root DIR] [--deny-list FILE]
  python3 cleanroom_scan.py --self-test
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from typing import Dict, List, Optional, Tuple

SKIP_DIRS = {".git", "node_modules", "target", "dist", "build", ".venv", "__pycache__"}
META_BYTES = 256 * 1024


def glob_to_regex(glob: str) -> re.Pattern:
    out = []
    i = 0
    while i < len(glob):
        c = glob[i]
        if c == "*":
            if glob.startswith("**/", i):
                out.append("(?:.*/)?")
                i += 3
                continue
            if glob.startswith("**", i):
                out.append(".*")
                i += 2
                continue
            out.append("[^/]*")
        elif c == "?":
            out.append("[^/]")
        else:
            out.append(re.escape(c))
        i += 1
    return re.compile("^" + "".join(out) + "$")


def read_deny_list(path: str) -> Dict:
    cfg: Dict = {"terms": [], "meta": [], "exts": [], "paths": [], "allow": []}
    with open(path, "r", encoding="utf-8-sig") as fh:
        for n, raw in enumerate(fh, start=1):
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            idx = line.find(":")
            if idx < 1:
                raise ValueError(f"{path}:{n}: expected 'kind: value'")
            kind = line[:idx].strip()
            value = line[idx + 1:].strip()
            if not value:
                raise ValueError(f"{path}:{n}: empty value")
            if kind in ("term", "notice"):
                cfg["terms"].append((kind, value))
            elif kind == "meta":
                cfg["meta"].append(value)
            elif kind == "ext":
                e = value.lower()
                cfg["exts"].append(e if e.startswith(".") else "." + e)
            elif kind == "path":
                cfg["paths"].append((glob_to_regex(value), value))
            elif kind == "allow":
                cfg["allow"].append(glob_to_regex(value))
            else:
                raise ValueError(f"{path}:{n}: unknown kind '{kind}'")
    return cfg


def repo_files(root: str) -> Tuple[List[str], List[str]]:
    """Returns (files, missing). missing: listed by git but absent on disk."""
    root = os.path.abspath(root)
    git = shutil.which("git")
    if git:
        try:
            r = subprocess.run([git, "-C", root, "rev-parse", "--is-inside-work-tree"],
                               capture_output=True, timeout=30)
            if r.returncode == 0 and r.stdout.strip() == b"true":
                r = subprocess.run([git, "-c", "core.quotepath=off", "-C", root, "ls-files", "-z",
                                    "--cached", "--others", "--exclude-standard"],
                                   capture_output=True, timeout=120)
                if r.returncode == 0:
                    files, missing = [], []
                    for raw in r.stdout.split(b"\0"):
                        if not raw:
                            continue
                        rel = os.fsdecode(raw)
                        p = os.path.join(root, rel)
                        if os.path.isfile(p):
                            files.append(rel)
                        elif not os.path.isdir(p):  # directories are submodules
                            missing.append(rel)
                    return files, missing
        except (OSError, subprocess.SubprocessError):
            pass
    files = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for f in filenames:
            rel = os.path.relpath(os.path.join(dirpath, f), root).replace(os.sep, "/")
            files.append(rel)
    return files, []


def text_kind(buf: bytes) -> str:
    """'utf8', 'utf16le', 'utf16be' or 'binary'."""
    if buf[:2] == b"\xff\xfe":
        return "utf16le"
    if buf[:2] == b"\xfe\xff":
        return "utf16be"
    probe = buf[:8192]
    if b"\0" not in probe:
        return "utf8"
    nul_even = sum(1 for i in range(0, len(probe), 2) if probe[i] == 0)
    nul_odd = sum(1 for i in range(1, len(probe), 2) if probe[i] == 0)
    half = len(probe) // 2
    if half >= 8:
        if nul_odd >= half * 0.6 and nul_even <= half * 0.05:
            return "utf16le"
        if nul_even >= half * 0.6 and nul_odd <= half * 0.05:
            return "utf16be"
    return "binary"


_ENC = {"utf8": "utf-8-sig", "utf16le": "utf-16-le", "utf16be": "utf-16-be"}


def scan(root: str, cfg: Dict) -> List[str]:
    root = os.path.abspath(root)
    findings: List[str] = []
    files, missing = repo_files(root)
    for m in missing:
        findings.append(f"error  {m.replace(os.sep, '/')}: listed by git but not found on disk (encoding or case problem); fix before trusting this scan")
    meta_raw = [m.encode("utf-8").lower() for m in cfg["meta"]]
    meta_low = [m.lower() for m in cfg["meta"]]
    for rel in sorted(files):
        rel = rel.replace("\\", "/")
        low = rel.lower()
        for rx, src in cfg["paths"]:
            if rx.match(rel):
                findings.append(f"path   {rel}: matches forbidden path '{src}'")
        for ext in cfg["exts"]:
            if low.endswith(ext):
                findings.append(f"ext    {rel}: forbidden extension '{ext}'")
        allowed = any(a.match(rel) for a in cfg["allow"])
        full = os.path.join(root, rel)
        try:
            with open(full, "rb") as fh:
                buf = fh.read(META_BYTES)
        except OSError as e:
            findings.append(f"error  {rel}: cannot read ({e})")
            continue
        kind = text_kind(buf)
        is_text = kind != "binary"
        if allowed and is_text:
            continue  # allow exempts text files only
        if cfg["meta"]:
            if kind in ("utf16le", "utf16be"):
                head = buf.decode(_ENC[kind], errors="replace").lower()
                for m, ml in zip(cfg["meta"], meta_low):
                    if ml in head:
                        findings.append(f"meta   {rel}: contains '{m}' in file metadata area")
            else:
                head_b = buf.lower()  # bytes.lower() folds ASCII only, matching the needle folding
                for m, mr in zip(cfg["meta"], meta_raw):
                    if mr in head_b:
                        findings.append(f"meta   {rel}: contains '{m}' in file metadata area")
        if not is_text or not cfg["terms"]:
            continue
        try:
            with open(full, "r", encoding=_ENC[kind], errors="replace", newline=None) as fh:
                for n, line in enumerate(fh, start=1):
                    ll = line.lower()
                    for kind_t, value in cfg["terms"]:
                        if value.lower() in ll:
                            findings.append(f"{kind_t:<6} {rel}:{n}: '{value}'")
        except OSError as e:
            findings.append(f"error  {rel}: cannot read as text ({e})")
    return findings


# ----------------------------------------------------------------------------------------------
# Self-test: prove the check can fail.

def _w(base: str, rel: str, data: bytes) -> None:
    p = os.path.join(base, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "wb") as fh:
        fh.write(data)


def _assert(label: str, found: str, expected: List[str], unexpected: List[str], failures: List[str]) -> None:
    missing = [e for e in expected if e not in found]
    wrong = [u for u in unexpected if u in found]
    if missing or wrong:
        failures.append(f"[{label}] missing: {'; '.join(missing)} | unexpected: {'; '.join(wrong)}\n{found}")


def self_test() -> int:
    failures: List[str] = []
    u16le = "utf-16-le"
    u16be = "utf-16-be"

    # Part A: plain folder, one of every kind
    tmp = tempfile.mkdtemp(prefix="cleanroom_selftest_")
    try:
        _w(tmp, "deny.txt", b"term: forbidden-name\nnotice: (c) acme\nmeta: made-by-acme\next: .acmepreset\npath: plan/**\nallow: deny.txt\nallow: docs/**\n")
        _w(tmp, "src/a.txt", b"hello\nuses Forbidden-Name here\n")
        _w(tmp, "src/b.txt", b"Copyright (C) Acme Corp\n")
        _w(tmp, "fixtures/x.bin", b"\0\0\0Made-By-Acme\0\0")
        _w(tmp, "assets/p.acmepreset", b"x")
        _w(tmp, "plan/notes.md", b"observation notes")
        _w(tmp, "docs/profile.md", b"forbidden-name is the target; (c) acme; producer string made-by-acme\n")
        _w(tmp, "docs/vendor-export.bin", b"\0\x01\0made-by-acme")
        _w(tmp, "src/res.rc", b"\xff\xfe" + "STRINGTABLE\nCopyright (C) Acme\n".encode(u16le))
        _w(tmp, "src/nobom.txt", "plain text line\nforbidden-name without bom\n".encode(u16le))
        _w(tmp, "src/be.txt", b"\xfe\xff" + "made-by-acme in utf-16be text\n".encode(u16be))
        big = ("padding line of text to grow the file well beyond five megabytes\n" * 120000
               + "forbidden-name at the end of a large file\n")
        _w(tmp, "src/huge.txt", big.encode("utf-8"))
        _w(tmp, "src/clean.txt", b"nothing to see\n")
        found = "\n".join(scan(tmp, read_deny_list(os.path.join(tmp, "deny.txt"))))
        _assert("folder", found, [
            "term   src/a.txt:2", "notice src/b.txt:1", "meta   fixtures/x.bin", "ext    assets/p.acmepreset",
            "path   plan/notes.md", "meta   docs/vendor-export.bin", "notice src/res.rc:2", "term   src/nobom.txt:2",
            "meta   src/be.txt", "term   src/huge.txt:120001",
        ], ["docs/profile.md", "src/clean.txt", "deny.txt"], failures)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # Part B: real git repository
    git = shutil.which("git")
    if git:
        tmp = tempfile.mkdtemp(prefix="cleanroom_selftest_git_")
        try:
            def g(*args: str) -> None:
                subprocess.run([git, "-C", tmp, *args], capture_output=True, check=False)
            g("init", "-q", ".")
            g("config", "user.email", "selftest@example.invalid")
            g("config", "user.name", "selftest")
            g("config", "core.autocrlf", "false")
            _w(tmp, "cleanroom/deny-list.txt", b"term: forbidden-name\nmeta: made-by-acme\npath: plan/**\nallow: cleanroom/**\n")
            _w(tmp, ".gitignore", b"ignored/\n")
            _w(tmp, "src/gr\u00f6\u00dfe.txt", b"forbidden-name in a file with a non-ascii name\n")
            _w(tmp, "src/with space.txt", b"forbidden-name\n")
            _w(tmp, "cleanroom/export.bin", b"\0\0Made-By-Acme")
            _w(tmp, "cleanroom/PROJECT-PROFILE.md", b"producer string: made-by-acme; forbidden-name\n")
            _w(tmp, "src/ok.txt", b"fine\n")
            g("add", "-A")
            g("commit", "-q", "-m", "init")
            _w(tmp, "plan/notes.md", b"untracked observation note")
            _w(tmp, "ignored/scratch.txt", b"forbidden-name in an ignored file\n")
            found = "\n".join(scan(tmp, read_deny_list(os.path.join(tmp, "cleanroom/deny-list.txt"))))
            _assert("git", found, [
                "term   src/gr\u00f6\u00dfe.txt:1", "term   src/with space.txt:1", "meta   cleanroom/export.bin", "path   plan/notes.md",
            ], ["cleanroom/PROJECT-PROFILE.md", "cleanroom/deny-list.txt", "src/ok.txt", "ignored/scratch.txt", "error"], failures)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    else:
        print("selftest note: git not found, repository listing not tested")

    if failures:
        print("selftest FAILED")
        for f in failures:
            print(f)
        return 1
    print("selftest ok: every planted violation was detected (folder and git modes), allowed text files were skipped")
    return 0


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="Clean-room scan against cleanroom/deny-list.txt")
    ap.add_argument("--root", default=".")
    ap.add_argument("--deny-list", default="")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv)
    if args.self_test:
        return self_test()
    deny = args.deny_list or os.path.join(args.root, "cleanroom", "deny-list.txt")
    try:
        cfg = read_deny_list(deny)
    except (OSError, ValueError) as e:
        print(f"configuration error: {e}", file=sys.stderr)
        return 2
    findings = scan(args.root, cfg)
    for f in findings:
        print(f)
    if findings:
        print(f"\n{len(findings)} finding(s). Fix the cause; do not edit the deny-list to pass.", file=sys.stderr)
        return 1
    print("clean-room scan: no findings")
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    except Exception:
        pass
    sys.exit(main())
