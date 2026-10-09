# Phase 1: Posture

**Purpose:** let the owner choose how much the project may touch the target (P1, P2, P3) on an informed basis, and record it.
**Entry gate:** phase 0 approved. **Rules to read:** section 4 (R4.1 to R4.5), section 3.3, section 9.4.

## The agent is not the lawyer

The agent never decides that observation is allowed (R4.1). Its job is to put the relevant text in
front of the owner and to default to the strict choice when nothing is decided. It also never decides
that a licence allows the project. See step 5.

## Steps

1. **Apply the target category** (rules section 15, from intake question 1). Say in two sentences
   what "the install" and "observation" mean for this category: for a web service the install is
   everything the browser downloads and observation is using the UI with a test account; for a
   library the install includes shipped headers and observation is calling the public API; for an
   open-source target the source repository is the install and running the program is always
   allowed. Record the readings in profile section 1 (R15.1 to R15.3), including any public material
   inside the install the owner declares to be S2, and the "typical owner decisions" of the row as
   open questions in STATE.md.
2. **Explain the three postures in plain words** (rules section 4), with one sentence on what each
   costs: P1 is safest and slowest to verify behaviour; P2 lets you check behaviour yourself but
   needs discipline and the vendor's agreement; P3 adds vendor-made fixtures for tests.
3. **Ask the owner for the vendor's terms** that cover the target (licence agreement, terms of use,
   terms for scripting or automation if separate; for a web service its terms of service and API
   terms; for an open-source target its licence text). Accept a link, pasted text or a file.
   Also ask for the terms of **any other vendor** whose tool might be used (R4.4).
4. **Extract, do not interpret.** Quote verbatim, with section numbers, every clause about:
   reverse engineering, decompiling, disassembling; observing or testing behaviour or
   benchmarking; automation or scripting; API use, scraping and rate limits (web services);
   derivative works; fonts, assets, templates and samples; file format use. If the text is not
   available, say so. That is step 5, not a posture.
5. **Say what the licence does, then let the owner choose.** If any quoted clause forbids reverse
   engineering, decompiling, disassembling, derivative works, or a competing implementation, say in
   one sentence that the licence does not allow this use. A normal use licence is not permission to
   rebuild the product. If no terms were produced, say that too: you cannot show a licence that
   allows it. Recommend they stop. Then ask:
   - **Stop.** (Recommended)
   - **Continue anyway.** I have read what you quoted. I choose to continue, and I alone am responsible.
   "Ok" is not the second option. Wait for their sentence. If they stop, record the stop in STATE.md
   and do not start phase 2. If they choose to continue, write that quote into the licence-choice row
   and into ADR-0001, then go on. Do not refuse after they have chosen. Do not suggest a different
   target. An open-source licence that allows derivative works is not this step: record "terms allow"
   and continue.
6. **Recommend:** P1 unless the owner, after reading the quotes, states that observation is
   permitted. Say that in one sentence. Do not give legal advice; suggest counsel if the owner wants
   certainty. P1 is about running the software. It is not a comment on whether the licence allows
   the project. That comment was step 5.
7. **If P2 or P3:** record the installed target version and OS (or service URL and test account
   owner, or device and emulator), the local observation folder, and how the target's window or
   screen will be captured. Add the rules in `project-skills/observe.SKILL.md` to the generated
   skills. If P3, also decide the corpus repository and its generator folder.
8. **Write ADR-0001** from the decision-record template: context, quoted clauses, options, decision,
   conditions and limits, how it is proven (checks C2 and C7 in `templates/checks-spec.md`).
9. **Existing tainted material** from phase 0 question 6: decide per item whether to delete, isolate
   or declare out of scope. Record it as ADR-0002 if any. Code in an existing repository is triaged
   in phase 2, not here.
10. **Naming note:** tell the owner that using the target's name in the product name, README or
   marketing is a separate trademark decision that is reviewed in phase 6.

## Exit gate

The owner approves ADR-0001 and states the posture. Record it in STATE.md. If step 5 ended in a stop,
there is no posture to approve. If step 5 ended in the owner's choice to continue, the ADR includes
their quote, and the posture question is only about whether the software may be run.
