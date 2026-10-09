---
name: <<project-slug>>-implement-feature
description: Implements one <<PROJECT NAME>> feature, format or behaviour spec-first with tests, provenance documentation and an honest status update, then commits. Use for every feature task in the build loop, and whenever the user asks to build, add or fix a feature of the project.
---

# Implement one feature in <<PROJECT NAME>>

Rules: `cleanroom/rules/CLEANROOM-RULES.md` sections 6, 7, 10, 11. Stack skill: `<<project>>-stack` (build, test, gate commands).

## Loop

1. **Orient.** Read `cleanroom/STATE.md`, the tracker row for the feature (`<<tracker path>>`), and
   the module README. Confirm the posture and the do-not-read list.
2. **Sources.** Run `<<project>>-spec-lookup` if the feature has no T7 entries yet. No sources, no code.
3. **Tests first.** Write the acceptance test from the spec or documented behaviour: synthetic
   fixtures made in code; oracles only as external processes and skipping when absent (R7.5).
4. **Implement** from the spec, with the T7 entry or spec section in view. Do not open other
   implementations of the same feature (R7.3) and do not write from recall of one: a passage that
   arrives whole, with names or constants you did not derive, is discarded and re-derived (R7.11).
   Extract spec tables by script. Our own names, patterns and data (R7.4, R7.6).
5. **Verify.** Run `<<gate command>>`. Look at the result when it is visual (render, screenshot of our
   own app). Compare with the behaviour notes, never with vendor imagery.
6. **Record.** Update the module README "Provenance and clean-room" section (T2): spec editions,
   observations (P2/P3), oracles, what was not read, unverified parts, decisions where undocumented.
   Update the tracker row with evidence (T8) and say if the number is measured or estimated (R10.4).
7. **Commit** with the task id and the source in the message (R10.5). Only a green gate.
8. **Update** `cleanroom/STATE.md` session log.

## Stop and ask

A needed source is on the do-not-read list; the only source is another implementation (R3.7); the
feature needs a format with no public spec (R3.8, R12.4); an asset is needed (use `<<project>>-add-asset`);
a check fails and the only fix looks like loosening it.
