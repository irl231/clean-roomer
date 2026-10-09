---
name: <<project-slug>>-audit
description: Audits <<PROJECT NAME>> for clean-room compliance and honest status: runs the scan and checks, reviews provenance, assets, dependencies, claims and docs, and writes a report. Use before a milestone review, a release, a handover, or when the user asks whether the project is still clean.
---

# Clean-room audit for <<PROJECT NAME>>

Rules: `cleanroom/rules/CLEANROOM-RULES.md` sections 8 to 11. Checks spec: `cleanroom/templates/checks-spec.md`.

## Steps

1. **Automated:** run `<<gate command>>` and `<<scan command>>` (see the `stack` skill). Record the
   output. Any finding is a stop (see below).
2. **Prove the checks still bite:** run the scan self-test (`-SelfTest` / `--self-test`), the asset
   check's planted violation test, and the do-not-read guard's `--self-test` (`cleanroom/do-not-read.txt`
   is current with profile section 4; the agent's hook configuration named in profile section 8
   still wires the guard).
3. **Provenance:** every module that implements a format, codec or behaviour area has a "Provenance
   and clean-room" section that is current. List the modules without one. Spot-check three recent
   modules for recalled code (R7.11): identifiers, comments or constants that match a named
   implementation rather than the cited spec; each hit is a doubt report.
4. **Assets:** index complete; no vendor-named author or source; screenshots only of our app; fonts
   per policy. Sample 10 records and open the sources.
5. **Dependencies:** licences on the allowlist, including transitive ones; any copyleft or unknown
   licence is a finding.
6. **Claims:** `parity_report.py --check` passes on a fresh test run with the pinned corpora and
   oracles present; floors hold and none was lowered without an ADR; the roadmap's T9 block quotes
   the scorecard of a recent commit and labels every estimate (R10.7, R10.8). Sample five live rows
   and drive them with the `drive` skill: a live row whose command does nothing visible or useful is
   a finding. Count controls that change nothing.
7. **Control channel (R13.6 to R13.8):** loopback or stdio only, token required, file roots set,
   the bad-parameter test covers every registered command, and nothing in the configuration points
   at the target. If a target bridge exists (R5.11 to R5.13): it is outside the product build, its
   call log shows only synthetic inputs, nothing it returned is tracked, and its names are still in
   `cleanroom/do-not-read.txt` (unless the ADR lets implementers call it).
8. **Docs and wording:** no vendor wording beyond feature and menu names; no vendor logos; naming of
   the target in README or marketing is an **owner decision** (trademark): list every place it occurs.
   Translations are written from our own text, not taken from vendor localisation (R6.6).
9. **Observation hygiene (P2/P3):** nothing tracked under the observation folder; `git log` shows no
   such files in history.
10. **Report:** write `cleanroom/reports/YYYY-MM-DD-audit.md` with findings (blocking, major, minor),
   evidence, and what the owner must decide.

## Stop conditions

Any vendor material, copyleft code, unattributed asset or tracked observation file: stop, remove it
from the working tree and outputs, file a T6 report, tell the owner before doing anything else.
