---
name: <<project-slug>>-observe
description: Records black-box observations of the target application (named in cleanroom/PROJECT-PROFILE.md) for <<PROJECT NAME>> using synthetic inputs, under the clean-room observation protocol. Use only when the project posture allows observation (P2 or P3) and the documents do not answer a behaviour question.
---

# Observe the target (posture <<P2 / P3>> only)

**If the profile posture is P1, this skill must not exist and must not be used.** Rules:
`cleanroom/rules/CLEANROOM-RULES.md` section 5 (R5.1 to R5.9) and the category reading in section 15.
Profile: sections 1 and 2 (the target's name lives there, not here).

## Before you start

- [ ] The owner approved the posture and recorded the ADR: `<<ADR path>>`.
- [ ] The local observation folder `<<observation folder>>` exists and is **ignored by version control**
      (run `git check-ignore <<observation folder>>`).
- [ ] You have a **question** the public documents could not answer. Write it down first.

## Rules, short form

1. Use **synthetic inputs you create from scratch**. Never open the user's real files, libraries or
   accounts. The target may sync a personal library: stay read-only toward it.
2. Capture **only the target's window, by window id**: `<<capture command for this OS>>`. Never the
   desktop. Never home screens, recent files, account or licence dialogs, file browsers. Where the
   platform cannot capture a single window (some Wayland sessions, locked-down devices), do not
   capture at all: write the fact down instead.
   Web service: a test account the owner named, synthetic data only, no DevTools, no view-source,
   no network capture (section 15). Library: a test program against the public API only.
3. **No OS-level synthetic input** (key or click injection). Drive the target only by hand, through
   its documented hooks if the profile allows it, or through the target bridge if STATE.md records
   the owner's choice (R5.11): `<<bridge tools, or "no bridge">>`, used from the observer session in
   `<<bridge folder>>`, synthetic documents from `<<scratch folder>>` only. The bridge returns facts;
   anything larger stays in the observation folder (R5.12).
4. **Never read anything inside the target's install**; listing names is the limit (R3.1).
5. Stop if you meet personal data, a sign-in prompt or a destructive dialog. Close it, leave things as
   they were, tell the owner.

## Record

Write a T1 note in `<<observation folder>>/` (date, target version, OS, surface and state, input,
facts in your own words, open questions). Mark each fact **observed** or **inferred** (R5.10); a
fact seen in one state is not claimed for another. Move the *fact* into the behaviour reference as
a T7 entry with source class S3. Screenshots stay in the observation folder and are never
committed, traced or used as art. Never use the project's own control channel or `drive` skill on
the target (R13.7).

## Done when

The question is answered or recorded as "not observable", and `git status` shows nothing from the
observation folder.
