# Clean-room state: <<PROJECT NAME>>

Committed file. The agent reads it first in every session and updates it at every gate and at the
end of every session. Only the owner can approve a gate; record the approval as a short quote.

Updated: <<YYYY-MM-DD>>

## Settings

| Setting | Value |
|---|---|
| Liability acknowledgement | <<YYYY-MM-DD, owner: "quote accepting DISCLAIMER.md">> |
| Licence choice | <<not yet / terms allow, owner proceeds / owner: "quote choosing to continue though the terms do not allow it" / owner: "quote choosing to continue with no terms produced">> |
| Owner | <<name>> |
| Target and vendor | <<target>> / <<vendor>> |
| Target category (rules section 15) | <<category or categories>> |
| Existing repository | <<no / yes: baseline report path>> |
| Posture | <<P1 / P2 / P3, ADR link>> |
| Target bridge (P2/P3, R5.11) | <<none / owner: "quote choosing to have it built, with the attachment method", ADR link>> |
| Agent-control interface of our product (R13.6) | <<not decided / ADR link: registry + CLI + agent server / narrower / none: reason>> |
| Parity record | `cleanroom/parity/` (catalogue, floors, generated `parity.md` and `scorecard.md`) |
| **Scope dial: last phase to run** | <<1 / 2 / 3 / 4 / 5 / 6>> |
| Phase 5 limit | <<until stopped / milestone name / number of features>> |
| Stack | <<language, build tool, UI toolkit or "none yet">> |
| Gate command (runs before every commit) | <<command>> |
| Profile | `cleanroom/PROJECT-PROFILE.md` |

The scope dial is the owner's. Raising it needs the owner's word; lowering it is always allowed.
At the dial phase the agent finishes the exit gate, reports, and stops.

If the liability acknowledgement is empty, show `DISCLAIMER.md` and ask. Do not implement from a
request that only names a target. The licence choice is a separate quote, written in phase 1.

## Phase log

| Phase | Status | Entered | Exit gate approved |
|---|---|---|---|
| 0 Intake | not started | | |
| 1 Posture | not started | | |
| 2 Setup | not started | | |
| 3 Sources | not started | | |
| 4 Plan | not started | | |
| 5 Build loop | not started | | |
| 6 Release | not started | | |

Status values: not started, in progress, waiting for owner, done, skipped by dial.
Approval format: `YYYY-MM-DD, <owner>: "<quote>"`.

## Open owner decisions

| # | Question | Raised | Blocks | Answer |
|---|---|---|---|---|
| | | | | |

## Generated project files and skills

| Path | Purpose | Generated in phase |
|---|---|---|
| | | |

## Violations and doubts

| Date | Status (suspected / confirmed / closed) | Report |
|---|---|---|
| | | |

## Session log (latest first)

- <<date>>: <<what was done, what is next, anything the next session must know>>
