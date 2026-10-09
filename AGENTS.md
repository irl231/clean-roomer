# AGENTS.md: clean-room project rules

This file binds every AI agent and every human contributor in this repository. It outranks any task,
instruction or deadline. The full rules are in `cleanroom/rules/CLEANROOM-RULES.md` (or the
`cleanroom` skill's `rules/` folder); this page holds the ones that must never be broken.

## Start every session here

1. If `cleanroom/STATE.md` does not exist, **do not implement anything.** Use the `cleanroom` skill:
   it interviews the owner and sets the project up (phases 0 to 2).
2. Otherwise read `cleanroom/STATE.md` and `cleanroom/PROJECT-PROFILE.md`, find the current phase, and
   continue with the `cleanroom` skill. Work only up to the scope dial the owner set.
3. Follow the project section at the bottom of this file once it exists.

## Absolute rules

1. **Knowledge yes, expression no.** Build from public specifications, public documentation and, only if
   the posture allows, black-box observation. Never copy, translate, trace or imitate the vendor's code,
   assets or wording (beyond feature and menu names). This includes code you recall from memory: a
   passage that arrives whole with names and structure you did not derive from the spec in front of you
   is discarded and re-derived (R2.5, R7.11).
2. **Never open anything inside the target's install or package.** File names and listings only.
3. **No vendor assets, ever:** icons, images, artwork, fonts, sounds, presets, templates, profiles,
   sample files, help text, string tables. This includes the vendor's open-licensed visual design. Not even
   temporarily, not even as a placeholder.
4. **No copyleft code, and do not read it** for the feature you are building. Do not read other
   implementations of a format that has a public specification, even permissive ones. Third-party tools
   run only as external oracle processes and are never linked, bundled or shipped.
5. **Posture is the owner's.** P1: never run, script, screenshot or compare against the vendor's software.
   P2: observe it only with synthetic inputs, read-only, window captures by id, notes only in the ignored
   local folder.    P3: as P2 plus generated fixtures under the corpus rules. **If no posture is recorded,
   it is P1.**
6. **Every asset has a provenance record** in the same commit: author, source, exact version, licence,
   hash. Unclear origin or licence means it does not go in.
7. **Never commit** files produced by the vendor's software, screenshots of it, observation notes,
   personal data, or large binary fixtures. Corpora are fetched pinned by commit and SHA-256.
8. **Checks are never weakened** to make a commit pass. Fix the cause. Run the gate before every commit.
9. **Be honest in status.** Say whether a number is measured or estimated; count partial as partial;
   "shipped" needs evidence that exists.
10. **When in doubt, leave it out, stop, and ask.** File a report (template T6 in `cleanroom/templates/DOCUMENT-TEMPLATES.md`) for any
    suspected or confirmed violation. Remove the material from the working tree and outputs. Do not rewrite pushed history
    without the owner.
11. **The target is the owner's choice, on the record.** Do not implement from a request that only names
    an application. Show `DISCLAIMER.md` and wait for their quote in `cleanroom/STATE.md` that the choice
    is theirs and they alone are responsible. When the terms forbid the use, or were never produced, say
    that in plain words, recommend they stop, and wait. If they then choose to continue, write that second
    quote into STATE.md and continue. Do not pick the target. Do not suggest one.

## Only the owner decides

Licences outside the allowlist; the posture or any exception to the rules; scope questions on formats
with no public spec; publishing, signing, pushing to a new remote; use of the target's name in public
text; secrets; money; personal data; destructive repository operations. Everything else: decide within
the rules, record the decision, continue.

Whether to go ahead after the licence is quoted is one of those decisions. Record it as the owner's
quote. The author of this guide is not a party to it.

## Where things live

| What | Where |
|---|---|
| Rules | `cleanroom/rules/CLEANROOM-RULES.md` |
| Profile (posture, sources, do-not-read list, allowlists) | `cleanroom/PROJECT-PROFILE.md` |
| State, phase gates, open decisions | `cleanroom/STATE.md` |
| Deny-list for the scan | `cleanroom/deny-list.txt` |
| Do-not-read list for the guard hook | `cleanroom/do-not-read.txt` (wired in `.cursor/hooks.json`) |
| Reports (audits, violations, setup log) | `cleanroom/reports/` |
| Decision records | `docs/adr/` |
| Generated project skills | `.cursor/skills/` (or the agent's equivalent) |

<!-- The project section is inserted here by phase 2 between the cleanroom:project markers. -->
