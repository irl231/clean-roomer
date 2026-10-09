# Phase 6: Release

**Purpose:** prove that what ships is clean, attributed and honestly described, and prepare the release for the owner to publish.
**Entry gate:** a build the owner wants to release; the dial allows phase 6. **Rules to read:** sections 8, 10, 11, 12.

## Steps

1. Copy `templates/RELEASE-CHECKLIST.md` to `cleanroom/reports/<version>-release.md`.
2. Run `<project>-audit` on the release commit. Blocking and major findings stop the release.
3. Build a clean checkout from scratch and run the gate. Build packages for each platform the owner
   named; smoke-test each.
4. Collect third-party licence texts and notices into the NOTICE file. Verify the dependency licence
   list and the asset index against the packages (not only against the repository).
5. Review every place the target or vendor is named in shipped files and web or store text; list
   them for the owner. **Naming and trademark use is the owner's decision**; the agent proposes
   neutral, factual wording and flags anything that implies affiliation.
6. Prepare version, changelog, release notes (honest: known limitations next to features), tag. Do
   not push, sign, notarise, submit or publish.
7. Present the filled checklist and the report to the owner.

## Exit gate

The owner signs off the checklist and performs or explicitly delegates the publishing actions.
Record who did what and when in STATE.md. The process ends here; later releases repeat phases 5 and 6.
