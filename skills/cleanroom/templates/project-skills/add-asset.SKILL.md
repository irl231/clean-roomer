---
name: <<project-slug>>-add-asset
description: Adds or changes an image, icon, font, sound, template, sample document or other asset in <<PROJECT NAME>> with a provenance record, following the clean-room asset rules. Use when adding, replacing or reviewing any non-code asset, or when the user mentions icons, images, fonts, samples, themes or presets.
---

# Add an asset to <<PROJECT NAME>>

Rules: `cleanroom/rules/CLEANROOM-RULES.md` section 8 (R8.1 to R8.12). Profile: `cleanroom/PROJECT-PROFILE.md` section 6.

## Steps

1. **Classify.** Is it vendor material (the target's vendor or any other vendor named in profile
   section 1)? Is it a copy, trace or "inspired-by" of vendor art? If yes or unsure: stop, do not
   add, file a doubt report, ask the owner.
2. **Prefer original.** Draw it in code (`<<where code-drawn icons live>>`) or generate it. Draw
   without looking at vendor artwork.
3. **If third-party:** find it at its **original source** (author repository or release, not a mirror).
   Record the exact version or commit. Confirm the licence is on the allowlist
   (`<<allowed licences>>`). Unclear licence means not added.
4. **Add the file and its record in the same commit:** index entry in `<<asset index path>>` (use T3
   in `cleanroom/templates/DOCUMENT-TEMPLATES.md`: path, title, author, source, SPDX licence,
   licence file, SHA-256, used for, added, modifications), and the licence text next to the asset when
   the licence requires it.
5. **Fonts:** <<font policy from profile>>. Never commit a proprietary font.
6. **Screenshots of our own app:** only if everything visible is allowed (our UI, our icons, open fonts
   and content). Never a screenshot of the vendor's product.
7. **Run** `<<asset check command>>` and `<<gate command>>`. Both must pass without editing the
   allowlists.

## Stop conditions

Vendor origin, unclear licence, missing record, a check that you would have to loosen. File a report
(T6) and ask the owner.
