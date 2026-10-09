#!/usr/bin/env python3
"""Do-not-read guard (agent hook). Enforces the profile's do-not-read list (rules R3.1, R3.2, R7.3).

Reads the hook event JSON from stdin, flattens it to one string, and denies the action when any
entry of cleanroom/do-not-read.txt occurs in it (case-insensitive, path separators normalised).
Because it matches the whole input rather than named fields, the same script serves every event
that carries a path, URL or command: tool calls, shell commands, MCP calls.

Usage:
  do_not_read_guard.py --agent cursor   (default) prints {"permission": "deny"|"allow", ...}, exit 0
  do_not_read_guard.py --agent claude   on a hit prints the reason to stderr and exits 2
                                        (Claude Code: exit 2 blocks the tool call); exit 0 otherwise
  do_not_read_guard.py --self-test      proves the guard denies a listed path and allows an unlisted one

cleanroom/do-not-read.txt format: one literal per line, '#' starts a comment. Generated in phase 2
from profile section 4 (do-not-read list) and section 2 (target install paths). Typical entries:
  github.com/<org>/<forbidden-project>
  <forbidden-project-name>
  /Applications/<Target>.app
  C:/Program Files/<Vendor>

A missing list allows everything (phase 2 creates the file, even if empty). A crash is handled by
the agent's fail-closed setting where one exists; phase 2 proves the interpreter runs first.
"""
import json
import os
import sys
import tempfile

LIST_PATH = os.path.join("cleanroom", "do-not-read.txt")
RULES = "rules R3.1, R3.2, R7.3"


def norm(s: str) -> str:
    return s.replace("\\\\", "/").replace("\\", "/").lower()


def load_patterns(path: str):
    patterns = []
    with open(path, "r", encoding="utf-8-sig") as fh:
        for line in fh:
            line = line.strip()
            if line and not line.startswith("#"):
                patterns.append(norm(line))
    return patterns


def hits_for(raw: str, patterns) -> list:
    hay = norm(raw)
    return sorted({p for p in patterns if p and p in hay})


def agent_message(shown: str) -> str:
    return (
        f"Blocked by the clean-room do-not-read guard: the input matches '{shown}' from "
        f"cleanroom/do-not-read.txt ({RULES}). Do not retry or work around it. Use the public "
        "specification or documentation instead; if none exists, stop and ask the owner (R3.7, R12.3)."
    )


def decide(raw: str, patterns, agent: str) -> int:
    hits = hits_for(raw, patterns)
    if not hits:
        if agent == "cursor":
            print(json.dumps({"permission": "allow"}))
        return 0
    shown = ", ".join(hits[:3])
    if agent == "claude":
        print(agent_message(shown), file=sys.stderr)
        return 2
    print(json.dumps({
        "permission": "deny",
        "user_message": f"Clean-room guard: blocked access matching the do-not-read list ({shown}).",
        "agent_message": agent_message(shown),
    }))
    return 0


def self_test() -> int:
    tmp = tempfile.mkdtemp(prefix="guard_selftest_")
    cwd = os.getcwd()
    try:
        os.chdir(tmp)
        os.makedirs("cleanroom")
        with open(LIST_PATH, "w", encoding="utf-8") as fh:
            fh.write("# test\ngithub.com/acme/forbidden-clone\nC:/Program Files/Acme\n")
        pats = load_patterns(LIST_PATH)
        cases = [
            ('{"tool":"WebFetch","input":{"url":"https://GitHub.com/Acme/Forbidden-Clone/x.c"}}', True),
            ('{"tool_name":"Read","tool_input":{"file_path":"C:\\\\Program Files\\\\Acme\\\\a.dll"}}', True),
            ('{"command":"git clone https://github.com/acme/forbidden-clone.git"}', True),
            ('{"tool":"Read","input":{"path":"cleanroom/PROJECT-PROFILE.md"}}', False),
        ]
        bad = []
        for raw, expect_hit in cases:
            got = bool(hits_for(raw, pats))
            if got != expect_hit:
                bad.append(f"expected hit={expect_hit} for {raw}")
        if bad:
            print("guard selftest FAILED\n" + "\n".join(bad))
            return 1
        print("guard selftest ok: listed URL, escaped install path and clone command denied; unlisted path allowed")
        return 0
    finally:
        os.chdir(cwd)
        import shutil
        shutil.rmtree(tmp, ignore_errors=True)


def main(argv) -> int:
    agent = "cursor"
    if "--self-test" in argv:
        return self_test()
    if "--agent" in argv:
        i = argv.index("--agent")
        if i + 1 < len(argv):
            agent = argv[i + 1].lower()
    if agent not in ("cursor", "claude"):
        print(f"unknown agent '{agent}'", file=sys.stderr)
        return 1
    raw = sys.stdin.read()
    try:
        patterns = load_patterns(LIST_PATH)
    except OSError:
        if agent == "cursor":
            print(json.dumps({"permission": "allow"}))
        return 0
    return decide(raw, patterns, agent)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
