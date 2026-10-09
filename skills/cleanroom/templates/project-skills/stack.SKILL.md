---
name: <<project-slug>>-stack
description: Gives the build, test, gate, scan and run commands and the layout conventions of <<PROJECT NAME>> (<<language / toolchain>>). Use when building, testing, running, committing or setting up a worktree for the project.
---

# Stack notes for <<PROJECT NAME>>

Filled in during phase 2 and phase 4. Keep it short: only what the agent could not guess.

| Need | Command |
|---|---|
| Build | `<<command>>` |
| Test | `<<command>>` |
| Gate before every commit | `<<command>>` (includes asset check, clean-room scan, dependency licences, <<others>>) |
| Clean-room scan only | `<<command>>` (one of: `pwsh cleanroom/scripts/cleanroom_scan.ps1 -Root .`, `python3 cleanroom/scripts/cleanroom_scan.py --root .`, or the project's own) |
| Scan self-test (after any change to the checks) | `<<command>> -SelfTest` / `--self-test` |
| Run the app / CLI | `<<command>>` |
| Format / lint | `<<command>>` |

## Layout

<<modules or crates, and the dependency direction rules enforced by a check>>

## Conventions

- Commit message: `<<task id>>: <<summary>>`, one task per commit, green gate only.
- Parallel agents: one worktree, one build directory and one scratch folder per agent; never delete
  shared paths (R13.2).
- Machine quirks: <<shell aliases, display/permissions, ports>>.
- Error handling and safety conventions: <<project's own standard, if any>>.
