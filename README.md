# Clean-room guide: skill and AGENTS.md

A skill plus a standing `AGENTS.md` that guide an owner through a clean-room re-implementation of an
existing application, and run the process as far as the owner allows. It is built on the generic
rules in `skills/cleanroom/rules/CLEANROOM-RULES.md`.

## Disclaimer

The same text ships in `skills/cleanroom/DISCLAIMER.md`. Read it before you install or start.

This guide is a method. It does not choose a target, and it does not start because you named one. The
agent shows the disclaimer, later quotes the target's licence, and waits. You decide. You are advised
not to use it on commercial software you are only licensed to use: that is often a breach of the
licence, even when you never copy the vendor's code. If you continue, the choice and the responsibility
are yours. The author does not authorise that use.

The guide is provided as is, with no warranty. To the maximum extent the law allows, the author is not liable for claims that result from your use, including licence disputes and claims by a vendor. This is not legal advice.

This disclaimer, and any claim against the author that arises from the guide or its use, are governed by Swiss law (excluding its conflict-of-law rules and the CISG). The exclusive place of jurisdiction is Lucerne, Switzerland, to the extent the law allows. Mandatory consumer protection in the user's country is not affected, and the GPL-2.0 licence of the files is unchanged.

## What you get

| Path | Purpose |
|---|---|
| `AGENTS.md` | Standing rules, short and absolute. Loaded in every session. |
| `skills/cleanroom/DISCLAIMER.md` | Shown before any work. The owner's choice is recorded in STATE.md. |
| `skills/cleanroom/SKILL.md` | The entry point: state machine, scope dial, gates, how to ask. |
| `skills/cleanroom/phases/` | Seven phases: intake, posture, setup, sources, plan, build loop, release. |
| `skills/cleanroom/rules/` | The generic ruleset (R-numbered), including section 15: how the rules read for web services, libraries, protocols, mobile apps, CLIs, games, open-source targets and firmware. |
| `skills/cleanroom/templates/` | Profile, state file, deny-list, project rules section, checks spec, document templates (T1 to T11, including the agent-control and target-bridge decisions), release checklist, templates for project-specific skills (including `drive`), `parity/` (feature catalogue and floors), and `hooks/` (the do-not-read guard). |
| `skills/cleanroom/scripts/` | The clean-room scan in two interchangeable implementations, `cleanroom_scan.ps1` (Windows PowerShell 5.1 / pwsh) and `cleanroom_scan.py` (Python 3.8+), and `parity_report.py`, which generates the parity tracker and scorecard. Each has a self-test. |

## Install

Into a target repository (recommended, so the process travels with the project):

1. Copy `AGENTS.md` to the repository root (or merge it into an existing one).
2. Copy `skills/cleanroom/` to `.cursor/skills/cleanroom/` (or `.claude/skills/cleanroom/`).

For all your projects (Cursor): copy `skills/cleanroom/` to `~/.cursor/skills/cleanroom/` and still put
`AGENTS.md` into each repository.

## Use

Open the repository in the agent and say, for example: "I want to rebuild <application> as a clean-room
open-source project." That sentence does not start the work. The skill shows the disclaimer, asks you
to accept that the target is your choice, then asks one question at a time and records the answers in
`cleanroom/STATE.md`. In phase 1 it quotes the licence. If those terms do not allow the use, it says so
and recommends you stop. Continuing after that is a second quote, in your words, written into STATE.md.
The skill stops at the scope dial you choose. Resume any time: the next session reads `cleanroom/STATE.md`.
The repository may be empty or may already hold code; phase 2 has a baseline step for the latter.

## How the pieces fit

```
AGENTS.md  --- always loaded; absolute rules; points to --->  cleanroom skill
cleanroom skill --- phase files, one at a time --->  generates in your project:
    cleanroom/ (profile, STATE, deny-list, do-not-read list, rules, scripts, reports)
    cleanroom/parity/ (feature catalogue, floors; generated parity.md and scorecard.md)
    AGENTS.md project section
    .cursor/hooks.json + .cursor/hooks/do_not_read_guard.py   (blocks reads of forbidden sources;
                                                               Claude Code: .claude/settings.json + .claude/hooks/)
    .cursor/skills/<project>-stack | add-asset | spec-lookup | implement-feature | audit | observe | drive | domain skills
    in the product itself (phase 4, milestone M1): one command registry, a CLI and an agent server
    (for example MCP) that all dispatch the same commands, plus an offscreen capture command
    optionally, at P2/P3 and only by the owner's recorded choice: a bridge that drives the target,
    in its own folder, used by a separate observer session
```

Three layers keep the clean-room claim honest:

- the **rules** say what may be learned from where, including that an agent's own memory of a named
  implementation counts as a source (R2.5, R7.11);
- the **guard hook** stops the agent from opening what the do-not-read list forbids (paths, URLs,
  clone commands, and the target bridge's tools in implementing sessions) before it happens;
- the **scan and checks** stop vendor material from entering the repository, and each one proves it
  can fail before it is trusted.

Two more things make the build fast and keep its claims honest:

- **Agents drive their own work.** Phase 4 makes the agent-control interface a required decision.
  The default: every user-visible action is a command in one registry, and the UI, a CLI and an
  agent server (for example an MCP server) all call it by id. The agent builds this itself in the
  first milestone. Agents then run commands, inspect state and capture our app to check their
  work, and several agents can work in parallel, each against its own instance (R13.6 to R13.8).
  This channel never touches the target.
- **Status is generated, not written.** The owner approves a feature catalogue of every feature the
  target has. The test run writes evidence, and `parity_report.py` turns catalogue and evidence into
  `parity.md` (each feature live, partial or missing) and `scorecard.md` (per area). The scorecard
  keeps wired, live and real-input pass rate apart, because a fully wired menu tree says nothing
  about how features behave on real files. The gate fails on a hand-edited or stale report and on
  a broken floor; floors only rise (R10.7, R10.8, R11.6). The scorecard areas are how work is split
  between parallel agents.

The target bridge is optional. Building an MCP server that drives the target itself is possible at
posture P2 or P3. The skill quotes the vendor's terms on automation, plug-ins and competing
products, says plainly when they do not allow it, and builds it only after the owner chooses it in
their own words. It is kept outside the product, returns facts rather than the vendor's output, and
by default is used only by a separate observer session (R5.11 to R5.13).

## Notes

- The product names no third-party products or vendors. The target and vendor appear only in the
  profile, STATE.md, ADRs and the deny-list that phases 0 to 2 create for your project; the deny-list
  carries both names as `term` entries so a leak into code, skills or shipped docs fails the scan.
- Scanner: use whichever implementation runs on the machine. Both read the same deny-list, print the
  same findings and exit with the same codes; the self-test (`-SelfTest` / `--self-test`) plants a
  violation of every kind in a plain folder and in a git repository, including UTF-16 text, non-ASCII
  file names, large files and binaries under allowed folders. The deny-list format is tool-neutral;
  a project may re-implement the scan in its own stack.
- Guard hook: templates for Cursor (`hooks.json`) and Claude Code (`claude-settings.json`), one
  script for both; needs a Python 3 interpreter on the machine. Other agents with a pre-tool hook can
  use the same script; without one, the profile records that the guard is prose-only.
- Parity generator: `parity_report.py` needs Python 3.8+ and nothing else. It reads tab-separated
  files: the catalogue, the evidence the test run writes, and optional floors (formats in its header
  and in `templates/checks-spec.md`). `--self-test` plants hand edits, stale reports, broken floors
  and bad evidence and checks that each one fails. A project may re-implement it in its own stack.
- The rules file (`skills/cleanroom/rules/CLEANROOM-RULES.md`) is the source of truth. Its header
  gives the version and lists what each version added.
- The generic rules cover what keeps the clean-room claim provable, and the agent-control interface
  that lets agents verify their own work. They do not cover other engineering conventions (crash
  safety, layering, performance budgets). Add those as your own project skills in phase 2 or 4 if
  you want them enforced.
- The disclaimer above is a condition the owner accepts in their own words. The skill quotes vendor
  terms, says when they do not allow the use, and records the owner's choice. It does not decide the
  target, and it does not treat a one-line request as that choice.
