# Release checklist (phase 6)

Copy to `cleanroom/reports/<version>-release.md`, tick each item with evidence (command output, link,
file). **Publishing, signing, pushing to a new remote and any use of the target's name are the
owner's actions or explicit decisions.** The agent prepares and verifies; it does not publish.

## A. Clean-room evidence

- [ ] `cleanroom-audit` run on the release commit; report attached; no blocking or major findings.
- [ ] Clean-room scan clean; self-test passes (folder and git modes).
- [ ] Do-not-read guard in place and its list current with profile section 4 (or recorded as not available).
- [ ] Recalled-code spot-check from the audit (R7.11): no open findings.
- [ ] Every module that implements a format, codec or behaviour area has a current provenance section.
- [ ] Open violation or doubt reports: none (or each closed with the owner's note).
- [ ] Posture ADR and all exception ADRs are present and still accurate.
- [ ] Out-of-scope list is current and visible in the roadmap.

## B. Assets and licences

- [ ] Asset index complete; hashes verified; licence files present.
- [ ] Third-party licence texts and notices collected into the NOTICE file shipped with the product.
- [ ] Dependency licences on the allowlist, including transitive ones; list attached.
- [ ] Fonts: policy kept; no proprietary font in any package; release builds include the optional
      font input if the policy says so.
- [ ] Screenshots, icons, demo content shown on the website and in stores are ours or open (R8.4).
- [ ] Own brand marks used unmodified under their recorded licence (R8.11).

## C. Honest status

- [ ] Roadmap "Where we stand" updated; numbers say measured or estimated (R10.4).
- [ ] Release notes list known limitations next to features.
- [ ] No claim of "parity" or "compatibility" without evidence a reviewer can rerun.

## D. Naming and legal (owner decisions)

- [ ] Product name contains no vendor or product mark.
- [ ] Wording that mentions the target (README, store pages, marketing) reviewed by the owner or counsel;
      factual and nominative only, no suggestion of affiliation. List of occurrences: <<paths>>.
- [ ] Licence of our code stated; contributor licence statement in place.
- [ ] Vendor's terms re-read for the final posture decision; ADR still valid.

## E. Build and packaging

- [ ] Gate green on the release commit from a clean checkout.
- [ ] Reproducible build instructions verified by building in a fresh directory.
- [ ] Packages built for each target platform; each smoke-tested.
- [ ] Version, changelog, tag prepared (not pushed unless the owner says so).
- [ ] Signing, notarisation, store submission, publication: **owner action**. Record who and when.

## F. Handover

- [ ] `cleanroom/STATE.md` final; session log written.
- [ ] Local observation folder archived or destroyed per the owner's wish (never shared, never committed).
