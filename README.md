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

## What you get

| Path | Purpose |
|---|---|
| `AGENTS.md` | Standing rules, short and absolute. Loaded in every session. |
| `skills/cleanroom/DISCLAIMER.md` | Shown before any work. The owner's choice is recorded in STATE.md. |
| `skills/cleanroom/SKILL.md` | The entry point: state machine, scope dial, gates, how to ask. |
| `skills/cleanroom/phases/` | Seven phases: intake, posture, setup, sources, plan, build loop, release. |
| `skills/cleanroom/rules/` | The generic ruleset (R-numbered), including section 15: how the rules read for web services, libraries, protocols, mobile apps, CLIs, games, open-source targets and firmware. |
| `skills/cleanroom/templates/` | Profile, state file, deny-list, project rules section, checks spec, document templates, release checklist, templates for project-specific skills, and `hooks/` (the do-not-read guard). |
| `skills/cleanroom/scripts/` | The clean-room scan in two interchangeable implementations, `cleanroom_scan.ps1` (Windows PowerShell 5.1 / pwsh) and `cleanroom_scan.py` (Python 3.8+), each with a self-test. |

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
    AGENTS.md project section
    .cursor/hooks.json + .cursor/hooks/do_not_read_guard.py   (blocks reads of forbidden sources;
                                                               Claude Code: .claude/settings.json + .claude/hooks/)
    .cursor/skills/<project>-stack | add-asset | spec-lookup | implement-feature | audit | observe | domain skills
```

Three layers keep the clean-room claim honest:

- the **rules** say what may be learned from where, including that an agent's own memory of a named
  implementation counts as a source (R2.5, R7.11);
- the **guard hook** stops the agent from opening what the do-not-read list forbids (paths, URLs,
  clone commands) before it happens;
- the **scan and checks** stop vendor material from entering the repository, and each one proves it
  can fail before it is trusted.

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
- Source of truth for the rules is `../ruleset/`; `../ruleset/SOURCE-ANALYSIS.md` §7 records which
  rules come from the source projects and which were added in the product review (R2.5, R7.11,
  §15). The product copies are not byte-identical: when
  syncing, copy `CLEANROOM-RULES.md` and `TEMPLATES.md` to `skills/cleanroom/rules/` and
  `templates/DOCUMENT-TEMPLATES.md`, then remove the `SOURCE-ANALYSIS.md` references and keep the
  product's path wording in §0, R8.7, R10.1 and R10.3 (the product copy says where files live in a
  project).
- The generic rules do not cover engineering conventions (crash safety, layering, agent-control
  interfaces). Add those as your own project skill during phase 2 or 4 if you want them enforced.
- The disclaimer above is a condition the owner accepts in their own words. The skill quotes vendor
  terms, says when they do not allow the use, and records the owner's choice. It does not decide the
  target, and it does not treat a one-line request as that choice.
