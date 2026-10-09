# Phase 0: Intake

**Purpose:** understand what the user wants to build and how far they want the agent to go, then create the state file.
**Entry gate:** none (this is the start). **Rules to read:** sections 0, 1, 2 of the rules. **Also read:** `../DISCLAIMER.md`.

## Disclaimer first

Do this before the process explanation and before every other question. A request that already names a product is not a start. Do not suggest a target, and do not praise the one they named.

1. Show `../DISCLAIMER.md` in full. Do not shorten it.
2. Ask one question. The recommended option is the one that records their choice, not a refusal:
   - **Accept.** I have read the disclaimer. Any target I name is my choice, and I alone am responsible. (Recommended)
   - **Stop.** I do not want to continue.
3. **Stop** means stop. Create no files. Do not explain how to proceed.
4. **Accept** is the way forward. Remember their words. They go into STATE.md as the liability acknowledgement. "Ok" or "continue" is not enough. Ask once for a sentence that says the choice is theirs. If they still will not say it, stop and wait. Do not start anyway.
5. This acceptance is not a finding that the licence allows the target. Phase 1 quotes the terms and asks again if they do not.

## Say first (short)

Only after a clear acceptance. Explain in a few sentences: the process has seven phases; the agent only works from public
specifications, public documentation and (if the owner allows) black-box observation; nothing from
the vendor is ever copied; the owner approves every phase gate and decides the legal questions; the
owner sets how far the agent goes (the scope dial). Phase 1 will quote the licence. If it does not
allow the use, the agent will say so and wait for a separate choice.

## Ask, one question at a time

Use the question tool with a recommended default first. Skip what the user already told you.

1. **Target:** which application (name and version), and what category it is: desktop, web or
   SaaS, library or SDK, server or protocol, mobile, CLI, game or engine, open-source project,
   firmware (rules section 15; several may apply). The category decides what "install" and
   "observation" mean in phase 1. The name goes only into the profile and the deny-list, never into
   shipped files.
2. **Goal:** the whole workflow, a named subset, or one capability? Is the result open source, and
   under which licence? This sets the dependency and asset licence allowlist.
3. **Owner:** who holds authority over legal, licence and publishing decisions? Is that the user?
4. **Stack:** language, build tool, UI toolkit, target platforms. If the user has no preference,
   propose two options with trade-offs and a recommendation. Record "none yet" if phase 4 will decide.
5. **Repository setup:** a new repository or an existing one; one repo or product repo plus corpus
   repo; one agent or parallel agents; version control in use. If the repository already holds code,
   assets or dependencies, record it: phase 2 runs its "existing repository" steps before the gate.
6. **Existing material:** does the user already have the vendor software installed, vendor files,
   earlier notes or code written by someone who has seen the vendor's internals? If yes, record it:
   tainted code or notes must be handled under an owner decision (R3.1, R3.2) before anything else.
7. **Scope dial:** "How far should I go on my own?" Options:
   - 1: stop after the legal posture is decided;
   - 2: stop when the project is set up and checked;
   - 3: stop when sources and the feature catalogue are ready;
   - 4: stop when the plan is approved;
   - 5: build, up to a limit the user names (a milestone, a feature count, or until stopped);
   - 6: everything including release preparation (publication stays the owner's action).
   Recommend the lowest value that still gets the user what they want to review next.

## Do

1. Create `cleanroom/STATE.md` from `templates/STATE.md` with the answers.
2. Write the liability acknowledgement as `YYYY-MM-DD, owner: "<their acceptance quote>"`. Do not create STATE.md without it.
3. Read back a summary in five lines and ask the owner to confirm it. Include the acknowledgement in that summary.

## Exit gate

The owner confirms the summary and the dial. Record the approval in STATE.md and set phase 0 to done.
If the user only wanted the interview, stop here.
