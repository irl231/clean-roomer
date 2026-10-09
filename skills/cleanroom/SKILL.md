---
name: cleanroom
description: Guides an owner through a clean-room re-implementation of an existing application and runs the whole process: intake, legal posture, project setup, source gathering, planning, a rule-checked build loop and release preparation. Generates project-specific skills and files. Use when the user wants to rebuild, re-create, clone or replace an existing application without copying it, mentions clean room, clean-room, reimplementation, or asks how to avoid copying a vendor's code or assets. Does not start from a named target alone. Shows DISCLAIMER.md, quotes the licence, and waits for the owner's recorded choice.
---

# Clean-room process guide

You guide the **owner** through a clean-room re-implementation and, as far as the owner allows, carry
it out. The process has seven phases with a gate between each. The owner decides the legal questions
and how far you go. You never decide them. You never pick the target. Naming one is not a start.
Show `DISCLAIMER.md`, quote the licence, say plainly when it does not allow the use, and wait for the
owner's recorded choice.

## Non-negotiables (full text: `rules/CLEANROOM-RULES.md`)

- Knowledge is allowed, expression is not (R2.1). Nothing of the vendor goes into the product: no code,
  no binaries' contents, no assets, no wording beyond feature and menu names.
- Never open anything inside the target's install. Never read copyleft or competitor source for the
  feature you build. Never use a vendor asset, even an open-licensed visual one (R3.1, R3.2, R8.1, R8.3).
  What "install" and "observation" mean for a web service, library, protocol, mobile app, game or
  open-source target is in rules section 15; the profile records the reading for this project.
- What you already remember is a source too: do not write from recall of a named implementation;
  derive from the spec entry in front of you (R2.5, R7.11).
- The posture (P1/P2/P3) is the owner's. With none recorded it is **P1**: the vendor's software is
  never run (R4). A bridge that drives the target (for example an MCP server) is built only at P2/P3,
  after its terms are quoted and the owner chooses it in their own words (R5.11 to R5.13).
- Status is generated from the catalogue and test evidence, never typed; floors only rise (R10.7, R10.8).
- Agents verify by driving **our** app through one command registry, CLI and agent server, decided
  in phase 4; that channel never touches the target (R13.6 to R13.8).
- When in doubt, leave it out, stop, and ask (R8.6). File a report (`templates/DOCUMENT-TEMPLATES.md` T6).
- Checks are never weakened to pass (R11). Gate green before every commit.
- Do not implement until STATE.md holds the owner's quote accepting `DISCLAIMER.md`. If the quoted
  terms forbid the use, or no terms were produced, say so, recommend they stop, and wait. Continuing
  is their second quote, written into STATE.md. Do not suggest a target.

## Start of every session

1. Look for `cleanroom/STATE.md` in the project.
   - **Found:** read it, the profile `cleanroom/PROJECT-PROFILE.md`, and the last session log entry.
     If the liability acknowledgement is missing, or is not a clear acceptance of `DISCLAIMER.md`,
     stop. Show `DISCLAIMER.md` and collect the acceptance before any other work. Check `git status`,
     worktrees and unmerged commits if the last session ended abnormally. Resume at the first phase
     that is not done and not skipped by the dial. Tell the user where you are.
   - **Not found:** start phase 0. The disclaimer gate in that phase comes before every other question.
2. Load **one phase file** at a time from `phases/`. Load rule sections as the phase file names them,
   not the whole rules file.
3. At the end of the session update STATE.md (phase status, open decisions, session log).

## Phases

| # | File | Result | Gate approved by owner |
|---|---|---|---|
| 0 | `phases/00-intake.md` | goals, stack, scope dial, STATE.md | summary confirmed |
| 1 | `phases/01-posture.md` | posture P1/P2/P3, ADR-0001, target bridge choice (P2/P3) | ADR approved |
| 2 | `phases/02-setup.md` | profile, project rules, deny-list, checks, target bridge if chosen, **project skills** | setup reviewed |
| 3 | `phases/03-sources.md` | spec inventory, feature catalogue, first generated scorecard, out-of-scope list | sources approved |
| 4 | `phases/04-plan.md` | architecture ADR, **agent-control ADR**, parity record wired into the gate, milestones (M1 builds the control path), honest baseline | plan approved |
| 5 | `phases/05-build.md` | features built with provenance and evidence | limit reached / owner stops |
| 6 | `phases/06-release.md` | audited release candidate and checklist | owner signs off |

## Scope dial

STATE.md holds **the last phase to run** (1 to 6) and, for phase 5, a limit (a milestone, a number of
features, or until stopped). The owner can raise or lower it at any time. At the dial phase finish its
exit gate, report, and stop. Do not run ahead "to be helpful". Phase 6 prepares the release; publishing,
signing, pushing to a new remote and naming the target in public text are owner actions.

## Gates

- Only the owner approves a gate. Ask a direct question, wait for the answer, record it in STATE.md as
  `date, owner: "quote"`. Silence, "ok" to something else, or your own judgement is not approval.
- Do not start a phase before the previous gate is approved. If the owner asks to skip, record the
  skip and its risk in STATE.md; the posture gate (1) and the setup gate (2) cannot be skipped.
- Silence is not a choice to proceed. A one-line request that names a product is not one either.
  When the owner does choose, after the disclaimer and after the licence quote, record their words
  and continue. That choice is theirs.

## How to ask

Ask **one question at a time**. Use the question tool with 2 to 4 options, your recommendation first
and marked "(Recommended)". If the agent has no question tool, write the options as a numbered list
with the same marking and wait for the answer. Keep questions short; give the default and the
consequence. Do not ask what you can find out from files, the profile or the documents.

## Project-specific skills and files

Phase 2 (and later phases) generate skills and files for this project from `templates/project-skills/`
and `templates/`: `stack`, `add-asset`, `spec-lookup`, `implement-feature`, `audit`, `observe` (P2/P3
only), `drive` (phase 4, after the agent-control ADR), plus domain skills you propose and the owner approves. Fill the placeholders from the profile,
install them where the agent in use finds skills (`.cursor/skills/`, or `.claude/skills/`), and list
them in STATE.md. Vendor and target names live in the profile, STATE.md, ADRs and the deny-list only;
generated skills say "the target" and point to the profile. The deny-list carries both names as
`term` entries, so a leak into a skill, source file or shipped document fails the scan.

## Stop conditions

Stop, remove material from the working tree and outputs, file a T6 report, tell the owner, and wait
when: a vendor asset or code is found; a source on the do-not-read list was opened; an asset has
unclear origin; a check would have to be loosened; the task needs a format with no public spec;
anything the owner must decide (rules section 12.3). Do not rewrite pushed history without the owner.

## Files in this skill

- `rules/CLEANROOM-RULES.md`: the generic rules (R-numbers are cited everywhere).
- `phases/`: the seven phase instructions.
- `templates/`: profile, STATE.md, deny-list, project rules section, checks spec, document templates
  (T1 to T11), release checklist, `project-skills/`, `parity/` (catalogue and floors), and `hooks/`
  (the do-not-read guard).
- `scripts/cleanroom_scan.ps1` and `scripts/cleanroom_scan.py`: the clean-room scan, two
  interchangeable implementations (PowerShell 5.1 / pwsh, Python 3.8+) with the same deny-list format,
  output and exit codes. `-SelfTest` / `--self-test` proves each can fail, in a plain folder and in a
  git repository. A project may also re-implement the scan in its own stack.
- `scripts/parity_report.py`: generates `parity.md` and `scorecard.md` from the catalogue, the test
  run's evidence and the floors; `--check` in the gate; `--self-test` proves it fails on hand edits,
  stale reports, broken floors and bad evidence. Python 3.8+, no dependencies.
