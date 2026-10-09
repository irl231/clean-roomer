# Phase 2: Setup

**Purpose:** put the guard rails in place before any behaviour is researched or code written: profile, project rules, deny-list, do-not-read guard, checks, folders, and the **project-specific skills and files** this project will use.
**Entry gate:** phase 1 approved. **Rules to read:** sections 8, 9, 11, 12, 13. **Templates:** `templates/`.

## Steps

1. **Fill the profile.** Copy `templates/PROJECT-PROFILE.template.md` to `cleanroom/PROJECT-PROFILE.md`.
   Fill sections 0 to 2 from intake and posture (including the target category readings from
   phase 1). Sections 3, 4, 5 and 9 are completed in phase 3; put the known entries in now. Ask the
   owner for what is missing, one question at a time.
2. **Create the layout.** `cleanroom/` (profile, STATE.md, deny-list.txt, do-not-read.txt, `rules/`,
   `scripts/`, `reports/`, `parity/`), `docs/adr/` (ADR-0001 from phase 1), the asset index, NOTICE,
   licence files, and a `.gitignore` that ignores the observation folder, oracle output and
   `cleanroom/parity/evidence/`. Copy `rules/` and `scripts/` (both scanners and
   `parity_report.py`) from the skill folder into `cleanroom/`, and
   `templates/DOCUMENT-TEMPLATES.md`, `templates/checks-spec.md` and `templates/RELEASE-CHECKLIST.md`
   into `cleanroom/templates/`, so the project and its generated skills are self-contained.
3. **Project rules.** Insert `templates/project-agents-section.md`, filled in, into the project's
   `AGENTS.md` between the markers. If the file does not exist, copy the product `AGENTS.md` first.
4. **Deny-list.** Generate `cleanroom/deny-list.txt` from `templates/deny-list.template.txt` and the
   profile. It must contain: the **target and vendor names as `term`** (so they cannot leak into
   code, tests or shipped docs; the allow block exempts the profile, STATE, ADRs and AGENTS.md),
   vendor notice lines, competitor and copyleft project names, producer strings, vendor file
   extensions, and the observation folder from the profile as `path`. Ask the owner for names you
   cannot know (internal code names, producer strings seen in files).
5. **Do-not-read guard.** Install `templates/hooks/` as described in its README for the agent in
   use: Cursor (`.cursor/hooks.json` merged into an existing one, `.cursor/hooks/do_not_read_guard.py`)
   or Claude Code (`claude-settings.json` merged into `.claude/settings.json`,
   `.claude/hooks/do_not_read_guard.py --agent claude`), plus `cleanroom/do-not-read.txt` generated
   from profile section 4 (project names, repository URLs) and section 2 (install paths of the
   target and of other vendor tools). Replace `<<python>>` with an interpreter that runs here; run
   the script's `--self-test`. Prove the guard bites in the real agent: one denied access, one
   allowed, both logged in `cleanroom/reports/setup-log.md`. If the agent has no hook mechanism,
   record "guard: not available, prose-only" in profile section 8.
6. **Target bridge** (only if STATE.md records the owner's choice from phase 1; R5.11 to R5.13).
   Build it from the T11 ADR, in its own folder or repository outside the product's build (for
   example a sibling repository `<project>-target-bridge`), never linked, bundled or shipped:
   - attach by the method the owner chose; reference vendor SDK files from the local install, never
     copy them; no OS-level input injection;
   - expose tools that return facts (menu and command names, enabled state, structure, dimensions,
     timings); anything larger (renders, exported files, strings beyond names) is written only to the
     ignored observation folder;
   - open documents only from a scratch folder of synthetic inputs; refuse other paths; never sign
     in, sync or change user settings;
   - listen on stdio or loopback with a token; log every call locally;
   - add the bridge's server and tool names to the product's `cleanroom/do-not-read.txt` so
     implementing sessions cannot call it (unless the ADR says they may), and prove it: one denied
     call from the product repository, one allowed call from the observer session in the bridge's
     folder, both in `cleanroom/reports/setup-log.md`;
   - add the bridge's tools to the `observe` skill.
7. **Checks.** Implement C1 to C7 from `templates/checks-spec.md` in the project's stack, or mark
   each "not applicable" with a reason, or "deferred to phase 4" when it needs a stack that is not
   chosen yet (typically C3 and C5). Wire the implemented ones into the gate command. **Prove each
   one fails** on a planted violation and passes afterwards; log the evidence in
   `cleanroom/reports/setup-log.md`. Run the self-test of whichever scanner runs on this machine:
   `cleanroom_scan.ps1 -SelfTest` (Windows PowerShell 5.1 or pwsh) or
   `python3 cleanroom_scan.py --self-test` (Python 3.8+). At least one must run; record which.
   Run `python3 cleanroom/scripts/parity_report.py --self-test` too; C6 itself is wired in phase 4,
   once the test run can write evidence.
8. **Project-specific skills and files.** Propose, then generate after approval:

   | Skill (template in `templates/project-skills/`) | When |
   |---|---|
   | `stack` | always |
   | `add-asset` | always |
   | `spec-lookup` | always |
   | `implement-feature` | always |
   | `audit` | always |
   | `observe` | only at P2 or P3 |
   | `drive` | generated in phase 4, once the agent-control ADR exists (R13.6); not now |
   | fixture / corpus skill | P3, or whenever a corpus repo is used (derive from `add-asset` and rules section 9) |
   | domain skills | when a repeated, domain-specific task is visible: one per major file-format family, a tracker-update skill, a UI-compare skill, a localisation skill, and similar. Propose names and one-line purposes. |

   Fill the placeholders from the profile. Write each to `.cursor/skills/<slug>-<name>/SKILL.md`
   (or the equivalent folder of the agent in use). Each description must say what and when, in third
   person. List every generated file in STATE.md. **Skills never contain the target or vendor name**
   (they say "the target" and point to the profile); the deny-list `term` entries from step 4 enforce
   this, since `.cursor/skills/` is not in the allow block.
9. **Existing repository** (intake question 5 said the repository already holds code, assets or
   dependencies). Before the gate:
   1. Run the scan and all implemented checks on the current tree and write the findings to
      `cleanroom/reports/baseline.md`. Do not fix anything yet.
   2. Triage every finding with the owner: remove, isolate (move out of the tree and out of the
      build), declare out of scope, or allow-list with a reason. Each decision is one line in the
      baseline report; anything that counts as vendor material or copyleft code also gets a T6 report.
   3. Existing modules that implement a format, codec or behaviour area get a "Provenance and
      clean-room" section (T2) stating what is known about their origin; unknown origin is written as
      unknown and listed as a doubt for the owner (R10.1, R12.3).
   4. Existing assets enter the asset index or are removed (R8.7). Existing dependencies go through
      C3 or, if C3 is deferred, through a manual licence list in the baseline report.
   5. History: list commits that touched removed material; purging history is an owner decision
      (R8.12). Record the owner's choice in the baseline report.
   Record the baseline report path in profile section 1.
10. **Run the gate.** On a new project it must pass on the empty tree. On an existing repository it
   must pass after step 9, with every allow-listed path justified in the baseline report.

## Exit gate

Show the owner: the profile, the project rules section, the deny-list, the do-not-read list, the
proof log for the checks and the guard, the target bridge and its guard proof (if chosen), the
baseline report (existing repository), and the list of generated skills. The owner approves, or lists changes. Record the approval.
