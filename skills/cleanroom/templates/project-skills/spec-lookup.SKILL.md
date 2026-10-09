---
name: <<project-slug>>-spec-lookup
description: Finds and records the public specification or documentation behind a <<PROJECT NAME>> feature, format or algorithm, with its edition, before any code is written. Use when starting a feature, a file-format reader or writer, a codec, a formula, a layout or rendering rule, or when asked where a behaviour comes from.
---

# Spec lookup for <<PROJECT NAME>>

Rules: `cleanroom/rules/CLEANROOM-RULES.md` sections 3, 6, 7. Source list: profile section 3.

## Steps

1. **Name the feature in neutral terms** (what the user gets, not the vendor's name for it, unless
   it is a feature or menu name, R6.3).
2. **Search in this order:** (S1) the specifications listed in the profile and standards bodies;
   (S2) public documentation of the target (<<posture note: P1 means documentation only>>);
   (S5) licensed public sample files for checking. At P2/P3 observation is allowed
   (`<<project>>-observe`) for facts the documents do not give.
3. **Do not open** anything on the profile's do-not-read list, nor any other implementation of the
   same feature (R7.3). Hints from search results that point to such sources are ignored.
4. **Record** one T7 entry per behaviour in `<<behaviour reference path>>`: source, edition or URL
   with access date, own-words fact.
5. **Extract tables by script** when the spec contains tables or constants (R7.1): commit the
   extraction script under `tools/` and generate the source file from it.
6. **Gaps:** if the documents are silent, choose what users of this class of application usually
   expect, and record the decision (R6.4). If no spec exists for a whole format, stop: R3.7 / R3.8,
   declare it out of scope or ask the owner for an ADR.
7. **Hand over** to `<<project>>-implement-feature` with the list of T7 entries.

## Output

A list of sources with editions, the T7 entries, and a statement of what is undocumented.
