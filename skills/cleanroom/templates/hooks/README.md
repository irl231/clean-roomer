# Do-not-read guard (hook template)

The deny-list scan stops vendor material from entering the repository. This hook stops the agent
from *reading* forbidden sources in the first place: the do-not-read list (rules R3.2, R7.3) and the
target's install (R3.1). Without it those rules rest on the model's discipline alone.

## Files

| Template | Installed as | Agent |
|---|---|---|
| `do_not_read_guard.py` | `.cursor/hooks/do_not_read_guard.py` or `.claude/hooks/do_not_read_guard.py` | both; Python 3.8+, no dependencies |
| `hooks.json` | `.cursor/hooks.json` (merge if one exists) | Cursor: `preToolUse` (Read, WebFetch, WebSearch, Glob), `beforeShellExecution`, `beforeMCPExecution`; the script prints a permission JSON |
| `claude-settings.json` | merged into `.claude/settings.json` under `hooks` | Claude Code: `PreToolUse` on Read, WebFetch, WebSearch, Glob, Bash and MCP tools; the script writes the reason to stderr and exits 2, which blocks the call |
| (generated) | `cleanroom/do-not-read.txt` | both: one literal per line, forbidden repository URLs, project names, install paths |

Other agents: if the agent has a pre-tool hook that passes the tool input on stdin, wire the script
with `--agent claude` (exit 2 = block) or `--agent cursor` (JSON permission) as fits, and record the
choice in profile section 8. If it has no hook mechanism, record "guard: not available, prose-only".

## Phase 2 steps

1. Replace `<<python>>` with the interpreter that runs on this machine (`python3`, `python`, or
   `py -3` on Windows). Verify: `<<python>> --version` and
   `<<python>> <path>/do_not_read_guard.py --self-test`.
2. Generate `cleanroom/do-not-read.txt` from profile section 4 (do-not-read list: project names and
   their repository URLs) and section 2 (install paths of the target and other vendor tools).
   Keep entries specific enough to avoid blocking the project's own files; the hook matches
   substrings of paths, URLs and commands, not file contents. If the owner chose a target bridge
   (R5.11), also add its MCP server name and tool names, so sessions in the product repository
   cannot call it (R5.13); the observer session runs from the bridge's own folder, which does not
   carry this list. Skip this only if the bridge ADR lets implementers call it.
3. Install the files for the agent in use (table above). Prove it bites in the real agent: ask it to
   read a path from the list and confirm the denial; then read an allowed file and confirm it passes.
   Log both in `cleanroom/reports/setup-log.md`.

## Limits

- Matches on tool input, not on content. A forbidden source reached through an unlisted mirror or a
  search-result snippet is not caught; R7.3 still applies.
- `Grep` is not matched, so audits can search the repository for forbidden names.
- Cursor `failClosed: true` blocks every matched action if the interpreter is missing; step 1 guards
  that. Claude Code treats a crashed hook as non-blocking, so step 1 matters there too.
