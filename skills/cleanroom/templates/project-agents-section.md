<!-- cleanroom:project:start (generated in phase 2 from cleanroom/PROJECT-PROFILE.md; edit the profile, then regenerate) -->

## Project: <<PROJECT NAME>>

<<PROJECT NAME>> is a clean-room, <<licence>> re-creation of the workflow of <<TARGET CATEGORY>>.
Owner: <<owner>>. Profile: `cleanroom/PROJECT-PROFILE.md`. State: `cleanroom/STATE.md`.

### Posture: <<P1 / P2 / P3>>

<<One-paragraph statement of exactly what is allowed and forbidden at this posture for this vendor.
P1: the vendor's software is never run, scripted, screenshotted or compared against. P2: observation
of the installed target under rule section 5, notes only in `<<observation folder>>`. P3: as P2, plus
generated fixtures in `<<corpus repo>>` under rule R9.4.>>

### Target category and readings

<<Category row(s) from rules section 15 and the recorded readings: what counts as the install, what
observation means, which names may be reused, public material inside the install declared S2.>>

### Do-not-read list

<<Bulleted list copied from profile section 4.>> Enforced by the guard hook (<<hook configuration
path>>, `cleanroom/do-not-read.txt`): a denied access is final; use the public specification or ask
the owner.

### Where things live

| What | Where |
|---|---|
| Behaviour sources and reference notes | <<paths>> |
| Observation notes (local, gitignored) | <<path or "none: P1">> |
| Asset provenance index | <<path>> |
| Decision records | <<path>> |
| Parity / status tracker | <<path>> |
| Project skills (generated) | <<paths>> |

### Gate

Run `<<gate command>>` before every commit. It includes the asset check, the clean-room scan
(`cleanroom/deny-list.txt`), the dependency licence check and <<other checks>>. Never weaken a check
to make a commit pass.

### Out of clean-room scope

<<List from profile section 9, or "none yet".>>

### Owner contact for decisions in rule section 12.3

<<how to reach the owner, in this project>>

<!-- cleanroom:project:end -->
