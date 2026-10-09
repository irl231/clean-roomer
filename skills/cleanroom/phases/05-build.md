# Phase 5: Build loop

**Purpose:** implement the plan feature by feature without breaking any rule, and keep the record honest.
**Entry gate:** phase 4 approved, or dial set to 5 or 6 with an approved plan. **Rules to read:** sections 3, 6, 7, 8, 10, 11, 13.

## Each iteration

Follow the generated `<project>-implement-feature` skill. In short:

1. **Orient:** read STATE.md, the task, the tracker row, the module README, the profile's posture.
2. **Sources first:** T7 entries exist (use `<project>-spec-lookup`); observation only at P2 or P3
   (`<project>-observe`) and only for questions the documents cannot answer.
3. **Tests first,** then implement from the spec. Do not open anything on the do-not-read list or other
   implementations of the same feature, and do not write from recall of one: a passage that arrives
   whole before you have read the spec section is discarded and re-derived (R7.11).
4. **Verify:** the gate command, and look at visual results of our own app.
5. **Record:** provenance section, tracker row with evidence, status numbers marked measured or
   estimated, ROADMAP update when a milestone moves.
6. **Commit** with the task id. Green gate only. Update STATE.md.

## Cadence

- **Audit** (`<project>-audit`) at the end of every milestone, before any release, and after every
  ten commits if the work is fast. A failing audit stops the loop.
- **Checks prove themselves:** rerun the scan self-test after any change to the checks.
- **Repetition:** when the same multi-step task appears a third time, propose a new project skill
  and add it after the owner agrees; record it in STATE.md.
- **Handover or crash:** rebuild context from STATE.md, `git status`, worktrees, unmerged commits.

## Stop and ask (owner decisions, rules section 12.3)

A licence outside the allowlist; an asset of unclear origin; a need for a source on the do-not-read
list; a format with no public spec; a request to change the posture; publishing or pushing to a new
remote; secrets; money; personal data; destructive repository operations; any doubt about a rule.
Everything else: decide within the rules, record the decision, continue (R6.4).

## Violations

On any suspected or confirmed violation: stop the iteration, remove material from the working tree
and outputs, file a T6 report, update STATE.md, tell the owner. Do not rewrite pushed history.

## Exit gate

The phase 5 limit from STATE.md is reached, or the owner stops the loop. Write a status report
(what shipped with evidence, what is partial, what is blocked, next three tasks) and update the
assessment block. Dial 5 stops here.
