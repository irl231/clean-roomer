# Phase 4: Plan

**Purpose:** turn the feature catalogue into an ordered, testable plan that respects the clean-room constraints.
**Entry gate:** phase 3 approved. **Rules to read:** sections 7, 9, 10.

## Steps

1. **Architecture options.** If the stack's architecture is not decided, propose 2 or 3 options with
   trade-offs and a recommendation. Clean-room constraints that must hold in any option:
   - modules that implement a spec stand alone and can be tested against conformance data;
   - oracles never enter the build; tests that need them skip when absent;
   - every module has a place for its provenance README;
   - the gate command can run all checks C1 to C7;
   - assets and fonts follow the profile's policy, and the product builds without optional inputs.
   The owner picks one. Record it as an ADR and update the `stack` skill. Then **implement the
   checks that phase 2 deferred** (typically C3 dependency licences and C5 embedded content), prove
   each on a planted violation, wire them into the gate, and append the evidence to
   `cleanroom/reports/setup-log.md`. The plan is not approved while a check is still deferred
   without a reason in the profile.
2. **Milestones.** Order by user impact and dependency. M1 is a thin vertical slice that exercises
   the whole path: a spec-driven module, a test, provenance, tracker update, gate. Each milestone
   lists its tracker rows, the sources for each, the acceptance tests, and the oracles used.
3. **Task format.** One task id per commit. Each task names: feature row, sources (T7 entries), tests,
   files expected, and what could force an owner question.
4. **Baseline honesty.** Write the assessment block (`T9`) at the top of `ROADMAP.md` with the current
   numbers marked measured or estimated. Estimates carry a range and the assumption behind them.
5. **Risks.** Legal (posture, naming), technical (no spec, large formats), process (parallel agents).
6. **Parallel work.** If several agents will work, define module ownership, one worktree and one build
   directory per agent, and merge order (R13.2, R13.3).
7. **Further project skills.** Add or adjust domain skills that the plan makes obvious; list them in STATE.md.

## Exit gate

The owner approves the architecture ADR, milestones, the first ten tasks and the risk list. Record
it. Dial 4 stops here.
