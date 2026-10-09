# Phase 4: Plan

**Purpose:** turn the feature catalogue into an ordered, testable plan that respects the clean-room constraints, and decide how agents will drive and measure the product.
**Entry gate:** phase 3 approved. **Rules to read:** sections 7, 9, 10, 13.

## Steps

1. **Architecture options.** If the stack's architecture is not decided, propose 2 or 3 options with
   trade-offs and a recommendation. Clean-room constraints that must hold in any option:
   - modules that implement a spec stand alone and can be tested against conformance data;
   - oracles never enter the build; tests that need them skip when absent;
   - every module has a place for its provenance README;
   - the gate command can run all checks C1 to C8;
   - assets and fonts follow the profile's policy, and the product builds without optional inputs.
   The owner picks one. Record it as an ADR and update the `stack` skill. Then **implement the
   checks that phase 2 deferred** (typically C3 dependency licences and C5 embedded content), prove
   each on a planted violation, wire them into the gate, and append the evidence to
   `cleanroom/reports/setup-log.md`. The plan is not approved while a check is still deferred
   without a reason in the profile.
2. **Agent-control interface (required decision, R13.6 to R13.8).** Ask the owner, one question,
   with these options and the first one recommended:
   1. *One command registry, with UI, CLI and an agent server (for example an MCP server) all
      dispatching by id, plus an offscreen capture command* (Recommended). Every user-visible action
      becomes a command whose id is the catalogue id, so agents can drive and capture the app to
      check their own work, and several agents can work in parallel against their own instances.
   2. *Registry and CLI only*: no agent server; agents use the CLI and offscreen captures.
   3. *The category's natural interface*: the public API for a library, the CLI for a CLI tool, an
      HTTP API plus a headless browser on our own build for a web app.
   4. *None*, with the reason and what agents use instead to verify (R13.4).
   Write the decision with template T10 as an ADR. The interface serves **our product only**; it is
   never connected to the target (R13.7). Record the ADR in profile section 11 and STATE.md, set the
   `--commands` mode for the parity report (required for option 1 or 2), implement check C8 for the
   chosen surfaces, and generate the `drive` skill from `templates/project-skills/drive.SKILL.md`.
3. **Parity record wired into the build (R10.7, R10.8).** Make the test run write the evidence
   files (`templates/checks-spec.md`, "Evidence the test run writes"): command rows from the C8
   test, acceptance tests tagged with their feature id, real-input results from the corpus and
   oracle tests. Run `cleanroom/scripts/parity_report.py`, commit `parity.md` and `scorecard.md`,
   add `parity_report.py --check` to the gate after the tests, and copy
   `templates/parity/floors.template.tsv` to `cleanroom/parity/floors.tsv` with today's measured
   values. Prove C6 fails on a hand edit of the scorecard and on a broken floor.
4. **Milestones.** Order by user impact and dependency. **M1 is a thin vertical slice that builds the
   control path first:** the registry (or the chosen interface) with at least one real feature
   command reachable from every surface in the ADR, the agent server if chosen, the capture command,
   a bad-parameter test over every command, the evidence files, and the generated reports. Then one
   spec-driven module, a test, provenance and the gate. Each milestone lists its catalogue rows, the
   sources for each, the acceptance tests, and the oracles used.
5. **Task format.** One task id per commit. Each task names: catalogue row(s), sources (T7 entries),
   tests, the command id(s) it registers, files expected, and what could force an owner question.
6. **Baseline honesty.** Write the assessment block (`T9`) at the top of `ROADMAP.md`. Measured rows
   come from the generated scorecard of the same commit; estimates carry a range, the assumption
   behind them and the word "estimated".
7. **Risks.** Legal (posture, naming), technical (no spec, large formats), process (parallel agents),
   automation (control channel exposure, R13.8).
8. **Parallel work.** If several agents will work, split by scorecard area: one area per agent, its
   module ownership, one worktree, one build directory and one control port per agent, and the merge
   order (R13.2, R13.3). After each merge, rerun the tests, regenerate the reports and check the
   floors; generated reports are never merged by hand.
9. **Further project skills.** Add or adjust domain skills that the plan makes obvious; list them in STATE.md.

## Exit gate

The owner approves the architecture ADR, the agent-control ADR, milestones, the first ten tasks and
the risk list, and has seen the first generated scorecard. Record it. Dial 4 stops here.
