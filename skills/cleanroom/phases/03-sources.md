# Phase 3: Sources

**Purpose:** establish where every behaviour will come from, and what cannot be done. Nothing is implemented in this phase.
**Entry gate:** phase 2 approved. **Rules to read:** sections 3, 6, 7.1 to 7.5, 12.4.

## Steps

1. **Specification inventory.** For each major area of the target (file formats, protocols,
   algorithms, rendering, text, units, localisation), find the public specification, record title,
   edition or version, URL and licence of the text. Ask the owner for specs they already know. Add
   them to profile section 3 (S1). Mark areas with **no public spec**.
2. **Documentation inventory (S2).** The vendor's public help, guides, published shortcut lists,
   scripting references and, for libraries and services, the public API reference. Record the URLs.
   Material the owner declared S2 in the category readings (profile section 1, R15.3) is listed
   with its path and nothing else inside the install is opened. At P1 this is the only behaviour
   source besides S1.
3. **Feature catalogue.** Build the parity tracker (`T8` in `templates/DOCUMENT-TEMPLATES.md`): one row
   per feature, **by feature or menu name only** (R6.3). At P1, take the names from public
   documentation. At P2 or P3, names may also be listed from observation of menus and panels
   (R5.7) using `<project>-observe`. Group by area and give each row an id.
4. **Behaviour reference.** Create the skeleton (`T7`) for areas where behaviour is not fully given by a
   spec. Do not fill it with copied text.
5. **Do-not-read list and oracles.** Name the copyleft and competitor implementations for each area
   (profile section 4), and the permissive implementations that are also not to be read while
   implementing (R7.3). Name oracle tools and versions (profile section 5); each runs only as an
   external process (R7.5). Update `cleanroom/deny-list.txt` and `cleanroom/do-not-read.txt` (the
   guard hook reads the latter: project names, repository URLs).
6. **Test data strategy.** Per area: synthetic generators (default), licensed public corpora (pinned
   by commit and SHA-256), no vendor-made files at P1 and P2, vendor-authored generated fixtures only
   at P3 under R9.4. Record in the profile section 7.
7. **Out of scope.** Features that cannot be done within the posture: no public spec, scripting
   bytecode, cloud services, vendor presets and data, models we may not ship (R12.4). Each gets a
   line in the tracker with status "out of scope" and an ADR if the owner wants it recorded. Put
   questions that need the owner (for example: may a whole undocumented format be studied from public
   sample files, R3.8) into STATE.md "Open owner decisions".
8. **Update the profile** sections 3, 4, 5, 7, 9 and regenerate the project section of `AGENTS.md`.

## Exit gate

The owner approves the spec inventory, the do-not-read list, the feature catalogue and the
out-of-scope list, and answers or defers each open decision. Record it. Dial 3 stops here.
