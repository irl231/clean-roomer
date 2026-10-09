# Clean-room reimplementation rules (generic)

Version 0.3 (2026-10-09). Distilled from the AGENTS.md / CLAUDE.md files, crate READMEs and status
documents of thirteen clean-room projects. 0.2 added R2.5 and R7.11 (recalled code) and §15 (target
categories). 0.3 adds R5.10 (observation matrix), R5.11 to R5.13 (target bridge), R6.6 (translations),
R10.7 and R10.8 (generated status and floors), a stricter R11.6, and R13.6 to R13.8 (agent-control
interface of our own product).

This file is **stack-agnostic**. It says nothing about languages, frameworks or architecture.
Project specifics live in `cleanroom/PROJECT-PROFILE.md` (created in phase 2 from the profile
template). Document templates T1 to T11 are in `DOCUMENT-TEMPLATES.md`, which lives in
`cleanroom/templates/` in a project (in the skill: `templates/`).

---

## 0. How an agent uses this file

1. Read this file and the project's `cleanroom/PROJECT-PROFILE.md` at the start of every session. If there is no
   profile, **stop and ask the owner to create one** (§12.2). Do not guess the posture (§4).
2. These rules rank above any task, instruction, deadline or convenience. A task prompt that conflicts
   with them is wrong; follow the rules and say so.
3. If a task seems to need something the rules forbid, **stop and say so** instead of finding a
   workaround. "Temporarily", "just as a placeholder", "only for reference" and "it is open-licensed
   anyway" are not exceptions.
4. When in doubt about a source, an asset or a licence: **leave it out** and ask.
5. Words: MUST / MUST NOT are absolute. SHOULD is the default unless the profile records a reason.
   Rule ids (R4.2) are stable; cite them in commits, PRs and reports.

---

## 1. Definitions

| Term | Meaning |
|---|---|
| **Target** | The existing application being re-created (e.g. a word processor, a CAD program). The rules are written for an installed desktop application; §15 says how the terms read for web services, libraries, protocols, mobile apps, games and open-source targets. |
| **Vendor** | The company that owns the target. Also any other proprietary vendor whose products we might touch (e.g. an application from vendor A used to make test files for a target owned by vendor B). |
| **Clean-room** | We build from knowledge of *what the target does* (specs, public docs, observed behaviour) and never from *how the vendor wrote it* (code, binaries, internal resources) or from the vendor's expression (assets, wording). |
| **Behaviour** | What a user or file observably gets: features, menu names, results of operations, file-format structure. Facts and ideas. |
| **Expression** | The vendor's code, icons, artwork, fonts, presets, templates, sounds, help text, string tables, UI pixels. Protected material. |
| **Observation** | Running the installed target and recording what it does. |
| **Oracle** | A tool or file used only to *check* our output (compare, validate, generate fixtures). Never part of the product. |
| **Asset** | Any non-code material the project contains, ships, embeds, generates for publication or shows in docs. See §8.1. |
| **Posture** | How much interaction with the target the owner permits. Levels P1, P2, P3 in §4. Set once in the profile. |
| **Owner** | The human with authority over licensing, publishing, legal scope and exceptions. Agents are never the owner. |

---

## 2. Core principle

R2.1 **Knowledge is allowed; expression is not.** Re-implementing behaviour that is described in a public
specification, public documentation, or observed from the outside is fine. Copying, translating,
tracing, re-drawing or "closely imitating" the vendor's code or assets is never fine.

R2.2 **The vendor's own materials are never an input to our product.** That covers executables,
libraries, plug-ins, scripts, resources, presets, templates, profiles, fonts, icons, help files,
localisation tables and sample files, whether read from the install, a download, a document or a
website.

R2.3 **Separate what you learned from what you write.** Behaviour is recorded in your own words
(§6), then implemented. Never write code while looking at third-party implementation source for the
same feature (§7.3).

R2.4 **Every claim of "we did it clean" must be provable** from the repository: sources cited,
assets attributed, hashes pinned, checks automated (§10, §11).

R2.5 **What the agent already knows is a source too.** An AI agent may hold memorised fragments of
the vendor's code, of a copyleft clone, or of a reference implementation. Reproducing them is copying
even though nothing was opened in this session. Write from the specification or behaviour entry in
front of you (§6, §7); a passage that arrives whole, with names, comments or structure you did not
derive, is discarded and re-derived (R7.11).

---

## 3. Source classification

Everything you learn from or use must fit one of these classes. Record the class (§10).

### 3.1 Allowed

| Class | Examples | Conditions |
|---|---|---|
| **S1. Public standards and specifications** | ISO / IEC / ITU / ECMA, IETF RFCs, W3C, Unicode, other standards bodies, and file-format references that a vendor has published openly | Record the exact edition or version used (R7.2). Prefer this class over all others. |
| **S2. Public vendor documentation** | Help pages, published shortcut lists, published user guides, public scripting / expression references, public forum posts | Behaviour only. Cite the URL. Do not copy the wording beyond feature and menu names (R6.3). |
| **S3. Observation of the running target** | Using the installed app with synthetic inputs | **Only if the posture allows it** (§4) and under the protocol in §5. |
| **S4. Files the owner or users own** | A file a user sends us and owns | Use locally; never commit; no personal data. |
| **S5. Third-party public files with a licence** | CC0 / MIT / Apache-2.0 sample files and corpora | Fetch pinned by commit and SHA-256, never commit large binaries, record licence (§9). |
| **S6. Third-party permissive code as a dependency** | MIT, Apache-2.0, BSD, ISC, Zlib, Unicode, CC0, BSL-1.0; MPL-2.0 only if the profile allows it and only unmodified | Used as a dependency with its licence recorded. Not the same as *reading it to learn* (R7.3). |
| **S7. Our own earlier work** | Another project of the same team | Allowed if the profile says so (R7.9). Record it as such. |

### 3.2 Forbidden, always

R3.1 MUST NOT read, open, disassemble, decompile, strings-dump, debug or copy anything **inside the
target's install or bundle**. File names and directory listings are the only allowed contact.
Examples that are explicitly off-limits: binaries, frameworks, plug-ins, `Resources/`, bundled
scripts (never open a vendor `JavaScripts/` or equivalent folder), presets, templates, fonts, ICC
profiles, localisation files, help files.

R3.2 MUST NOT copy, port, translate, link or *read for learning* **copyleft code** (GPL, LGPL, AGPL,
and by default MPL; see the profile), for the same feature we are implementing. Open-source
competitors of the target are the most dangerous source. The profile lists the names to watch (§12.1).
Copyleft tools MAY be run as **external oracle processes** under R7.5 only.

R3.3 MUST NOT use any asset from the vendor (§8).

R3.4 MUST NOT copy vendor wording (help text, tooltips, dialog text, string tables, error messages)
beyond feature names and menu/command names. Translations are written from the meaning of our own
English text, never from another product's string tables.

R3.5 MUST NOT commit files **produced by the vendor's software** (documents, exports, screenshots,
presets) unless the profile explicitly allows a named exception (§4, P3). Default: never.

R3.6 MUST NOT capture or keep personal data, account data, recent-file lists, home screens, licences,
serial numbers, cloud-library contents or machine paths while observing or generating anything.

### 3.3 Borderline: needs a recorded decision

R3.7 **Reading a permissively licensed third-party implementation of a format that has no public
spec** (e.g. an MIT library that documents a proprietary file format) is a grey area. The projects
differed on it. Default: **do not**. It is allowed only when ALL hold:
(a) no public specification exists, (b) the owner approved it in an ADR (R10.3), (c) the licence is
permissive and recorded with the exact commit, (d) you re-describe the format in your own words
*before* writing code and never translate code, (e) every structure is then verified against public
files and the result is checked loudly (checksums, self-describing types), (f) the module README
states exactly what was read (R10.2).

R3.8 **Studying a proprietary file format by analysing public sample files** (black-box format
analysis of CC0 files, not the vendor's software) is allowed as S5, same recording duties. Whether a
whole format may be studied this way is an owner decision (e.g. a project/document format with no
public spec). Until decided, mark the feature **out of clean-room scope** (§12.4); do not start.

---

## 4. Posture: how much may we touch the target

The owner sets **one posture per project** in the profile. If the profile is missing or silent, apply
**P1**. A vendor's terms of use / EULA decide this, not engineering convenience (R4.1).

| Posture | Name | May run the target? | Summary |
|---|---|---|---|
| **P1** | Documents only | **No** | Never launch, script, automate, screenshot, measure or compare against the target or any vendor app. Behaviour comes only from S1, S2, S4, S5. Strictest. Used when the vendor's terms forbid reverse engineering including observing inputs and outputs. |
| **P2** | Black-box observation | Yes, read-only | May run the installed target with **synthetic** inputs and record behaviour under §5. Never read its internals, never commit what it produced. |
| **P3** | P2 + vendor-authored fixtures | Yes | Like P2, and additionally the owner allows committing a **small, named set of test files generated from scratch** with the vendor tool by committed generator scripts, in a separate corpus repository. See §9.4. This is a narrow, explicit exception. |

R4.1 **Check the vendor's terms before choosing a posture.** If the terms forbid reverse engineering
and you cannot establish that observation is allowed, the posture is P1. The owner decides after
reading the terms; an agent MUST NOT decide that observation is fine.

R4.2 At P1 the following are also forbidden: using the vendor tool to make "synthetic" test files;
comparing our output against the vendor's output; scripting the vendor app (OS scripting
interfaces, the app's own scripting languages, UI automation); keeping screenshots of the vendor app.

R4.3 At P1, behaviour reference notes are cited to a public URL and re-checked against the document
at the time of use. Grade conformance against the **documentation**, not against the product.

R4.4 A different vendor's tool counts as a vendor tool for these rules. Example: do not use an
application from vendor A to generate fixtures for a target owned by vendor B unless the posture for
*vendor A* allows it.

R4.5 Changing the posture is an owner decision recorded in an ADR (R10.3). Never loosen it yourself.

---

## 5. Observation protocol (P2 and P3 only)

R5.1 **Synthetic inputs only.** Create the documents, drawings, sessions or projects you open in the
target yourself, from scratch, with no personal content. Never open a user's real work in it.

R5.2 **Read-only toward user state.** The installed target may be tied to a personal account or cloud
library (e.g. a photo library that syncs). Never import, edit, rate, delete, save to, sign in to or
change settings in anything that belongs to the user.

R5.3 **Capture the target window only, by window id.** Never capture the whole desktop: the machine runs
other work. Never capture a home screen, recent files, account panes, licence dialogs, file browsers
or notification areas.

R5.4 **Do not use OS-level synthetic input** (key/click injection, accessibility automation, OS
event-scripting tools, etc.). It goes to whatever window is in front, which may be the user's terminal or
another app. If the profile permits driving the target, use only the target's documented
automation hooks, never anything inside the install, unless the owner chose a target bridge under
R5.11 that names another attachment method.

R5.5 **Store observations only in the local, gitignored area** named in the profile (a folder the
project does not otherwise use, for example `observation/`). Screenshots there are *private reading notes*. They MUST NOT be committed,
published, linked from docs, embedded, traced, used as a visual source for icons or layout art, or
placed in any output.

R5.6 **Write notes in your own words.** An observation note records a fact ("menu *Table* has items
*Insert*, *Delete*, *Merge Cells*; Merge is disabled with no selection") with date, target version and
OS. It contains no copied paragraphs, no pasted help text, no exported vendor files.

R5.7 **Names and structure are fair game; internals are not.** Listing menu names, tool names,
command names and option names is observation. Reading the bundle for the same list is not (R3.1).

R5.8 **Unknown behaviour is recorded as unknown** and resolved by an explicit, written decision
(R6.4), not by peeking inside.

R5.9 **Stop on surprise.** If observation shows personal data, a sign-in prompt, a licence prompt or a
destructive dialog, close it, leave the state as you found it, and tell the user.

R5.10 **Record the observation matrix, and mark what was inferred.** Each observed fact names the
target version, OS, surface (menu, panel, dialog, canvas, tool) and state (empty document,
selection, edit mode, several items selected). A fact seen in one state is not claimed for another.
Mark every entry **observed** or **inferred**; an inferred entry is checked against a dated
observation before anyone claims exact parity for it.

R5.11 **Target bridge (P2/P3, the owner's choice).** An agent-facing bridge to the target (for
example an MCP server that drives it) is built only after the owner chooses it on the record. Before
asking, quote every clause of the vendor's terms on automation, scripting, plug-ins or SDKs,
reverse engineering, benchmarking and competing products, including separate terms for the
automation interface or SDK. If they do not allow this use, or none were produced, say so in one
sentence and recommend not building it. Name the attachment method and its risk: the documented
automation interface driven from outside the target (least intrusive); the vendor's plug-in SDK
(its files sit inside the install and carry their own licence); anything else the owner names.
Record the owner's quote in STATE.md and in an ADR (T11), then build it. Do not refuse after the
owner has chosen. At P1 there is no bridge: the software is not run (R4.2); a bridge needs the
owner to move the posture first (R4.5).

R5.12 **The bridge keeps the clean-room claim.** It is a tool, like an oracle (R7.5): it lives in its
own folder or repository, is never linked, bundled or shipped, and no vendor SDK file, header,
sample or string is copied into it or into the product (R3.4, R8.1); SDK files are referenced from
the local install. It opens only synthetic documents from a scratch folder and does not touch the
user's files, account or library (R5.1, R5.2). It returns facts (names, enabled state, structure,
dimensions, timings) rather than the vendor's files, renders or text; anything it does return goes
to the ignored observation folder only and is never committed (R3.5, R5.5). It never uses OS-level
input injection (R5.4). Every call is logged locally with its time and parameters.

R5.13 **Observers and implementers stay apart.** By default a separate observer session uses the
bridge and writes T1 notes and T7 entries; sessions that write product code never call it. Enforce
this with the guard: the product repository's `cleanroom/do-not-read.txt` lists the bridge's server
and tool names, and the observer session runs from the bridge's own folder. If the owner wants
implementers to call the bridge directly, that is part of the R5.11 choice and recorded in the same
ADR.

---

## 6. Recording behaviour knowledge

R6.1 Keep a local **behaviour reference** per target area (menus, panels, file format, function
semantics) with its source class (S1/S2/S3), the URL or date/version, and your own-words summary.

R6.2 Every behaviour decision in code or docs SHOULD be traceable to a source class entry. A reviewer
must be able to ask "where did you learn this?" and get an answer.

R6.3 Feature names, menu names and command names may be reused so users can find things. Nothing
longer than that is copied: not sentences, not tooltips, not dialog text, not preset names that are
distinctive creative works (see R8.9 for names of plug-ins and presets).

R6.4 **Undocumented behaviour:** choose what users of this class of application most commonly expect,
implement it, and **record the choice** in the module's README ("Decisions"). Do not resolve a gap by
reading the vendor's internals or a copyleft clone.

R6.5 Parity and quality claims are graded against the public documentation (or, at P2/P3, against
observation), not against whether a menu item exists. Scores are self-assessed, so **err low**
(R10.4).

R6.6 **Translations are ours.** Our UI text in other languages is written from the meaning of our own
source text, in ordinary vocabulary. Never take it from the vendor's localisation resources, string
tables or translated help. The vendor's translated menu and command names, read from localised
public documentation or (at P2/P3) observed in the localised UI, are names under R6.3 and nothing
longer.

---

## 7. Implementation rules

R7.1 **Spec first.** For every format, protocol or algorithm that has a public specification,
implement from the specification text. Where tables or constants are in the spec, **extract them with
a committed script** instead of retyping or copying them from another implementation.

R7.2 **Record the spec and its edition** in the module README (title, version/edition, sections used).

R7.3 **Do not read other implementations while implementing** a format that has a public specification:
not even permissively licensed ones (for example the reference and popular open-source codec implementations). Use
spec text and conformance vectors only. R3.7 covers the narrow case where no spec exists.

R7.4 **Derive, don't transcribe.** Geometry, tables, hatch patterns, linetypes, preset shapes, default
typographic rules and similar data are re-derived by us from specs and first principles, in our own
definitions, and live in our own source files.

R7.5 **Oracles are external processes.** Third-party tools (including copyleft ones and the vendor's
competitors) may be run to generate fixtures or compare output, but are never linked, bundled,
vendored, shipped or required to build the product. Tests that need an oracle skip with a clear
message when it is not installed. Record each oracle and version in the test docs.

R7.6 **No vendor-compatible identifiers that are expression.** Our plug-ins, presets, themes, styles,
templates and sample content have our own names and our own content. Matching a *command or function
name* for compatibility is fine (R6.3); cloning a preset library is not.

R7.7 **Dependencies** use licences on the profile's allowlist. Check transitive licences in CI.
Unknown or unclear licence means the dependency is rejected.

R7.8 **Fonts, data tables and profiles** that the target relies on (font metrics, colour profiles, lens
or camera data, hyphenation, locale data) come from open sources or are generated by us. Where a
proprietary font is requested by a document, render with an installed system font or a
metric-compatible open substitute; never bundle the proprietary font.

R7.9 **Reuse between our own projects** is allowed only if the profile says so, only for code we wrote
ourselves, and is recorded as S7. An "independent copy" of a reader shared between siblings is fine.

R7.10 **If a feature cannot be built clean-room** (no spec, no permitted source, or the posture
forbids what's needed) it is declared out of scope (§12.4), not hacked.

R7.11 **No recalled third-party code (R2.5).** While implementing, keep the spec section or T7 entry
in view and derive the structure from it. Treat a passage as recalled rather than derived when:
identifiers, comments, magic constants or error strings match a known implementation; a block appears
complete before the relevant spec section has been read; or the impulse is "how does <project> do
this". Discard such a passage and write the spec-derived version. Never deliberately recall a named
implementation of the feature being built. Tables and constants come from the spec by script (R7.1),
which also closes the recall path. If a recalled passage was already committed, treat it as a doubt
(§14.5): report it, replace it, and note the replacement in the module README.

---

## 8. Assets

### 8.1 What counts as an asset

Any image, icon, cursor, logo, illustration, screenshot, font, colour profile, LUT, preset, template,
theme, swatch/brush/pattern/style library, sound, music, video, 3D model, sample/demo/test document,
or other non-code media. It counts whether it is a file in the repo, bytes embedded in code
(`include_bytes!`, base64, data URIs), data hard-coded to reproduce an image (e.g. point lists traced
from someone else's icon), or fetched at build time or bundled through a dependency.

### 8.2 Absolute rules

R8.1 **No vendor assets, ever.** Not from the target, not from any other product by the same vendor,
not from its installers, website, documents or packages. This includes fonts shipped with the
vendor's software and sample files.

R8.2 **No traced, redrawn, recoloured or "inspired-by" copies** of vendor icons or artwork. Our icons
may follow generic conventions (a play triangle, a razor blade, a stopwatch), but each is drawn from
scratch **without looking at the vendor's artwork**. Preferred: draw them in code.

R8.3 **This applies even to the vendor's open-licensed visual design.** If a vendor publishes fonts,
icons or art under OFL/MIT/etc., do not use them when the material is *visual design* tied to the
vendor's identity (seen: a vendor's open-licensed type families, including a CJK family that is the
same design under another brand). The profile may record a single named owner exception (for example a maintainer exception kept in a decision record). Pure
technical data required for interoperability may be allowed only through a **closed list** in the
profile, each entry attributed with a flag marking its vendor origin.

R8.4 **Screenshots of the vendor product are never committed or published** (R5.5). Screenshots of
*our* app are allowed only if everything visible in them is allowed: our UI, our icons, openly
licensed fonts and content, documents built only from allowed assets. Never screenshot a document
that uses proprietary fonts or images.

R8.5 **Every asset is open or original.** One of: original work by a contributor who licenses it
under the project licence; OSI open source; public domain / CC0; Creative Commons that permits
redistribution (CC-BY, CC-BY-SA; no NC, no ND). Anything whose licence you cannot prove from the
**original source** (author repo / release, not a mirror) is forbidden. Examples: system fonts that
are not openly licensed, vendor emoji artwork, stock photos, "free for personal use" material,
screenshots of other people's software.

R8.6 **"When in doubt, leave it out."** Draw it or generate it yourself.

### 8.3 Attribution

R8.7 **Every asset has a provenance record in the same commit that adds it**: path/URL, title, author,
source (URL + exact version or commit), licence (SPDX), licence file if the licence requires shipping
it, SHA-256 where fetched, date added and by whom, how it is used, modifications. Use one
machine-readable index and a generated human-readable view if the project can; see
`DOCUMENT-TEMPLATES.md` T3. Code-drawn assets are recorded as "original work".

R8.8 The licence text is stored next to the asset when the licence requires it; required notices go
in the project's NOTICE file.

R8.9 **Own names for own things.** Plug-ins, presets, templates and themes we ship have our own names
and content (R7.6).

R8.10 **Fonts** (project policy decides where they live): never commit proprietary fonts. If the team
keeps fonts in a separate repository, fonts are an **optional build input**; the product MUST build,
test and run when it is absent (tests on its glyphs skip). Do not add the font repository as a code
dependency.

R8.11 **Third-party brand exception.** Only the project's own brand marks may be non-open, only under
their own recorded licence, only unmodified. This never extends to a third party's marks (the target
vendor, code-hosting or chat platforms, etc.): draw a generic icon.

R8.12 **If you find a violating asset:** stop, remove it from the repository and every output (docs,
screenshots, generated files, packages), and tell the owner at once with path and how it got there.
Rewriting pushed history is the owner's call (R12.3).

---

## 9. Test data and corpora

R9.1 **Prefer synthetic test inputs written from scratch in code**, from the public specifications.
This is the default at every posture.

R9.2 **Real-file corpora** live outside the product repository. They are **fetched pinned by commit and
verified by SHA-256**, never committed as large binaries. Pin changes go through review.

R9.3 **Only content we own or that is openly licensed (CC0 preferred)** goes into any corpus. No
personal images, no private documents, no content scraped from a user's disk or screen, no personal
details in file contents, metadata, layer names, file names, XMP or paths. Check metadata before
committing.

R9.4 **Vendor-authored fixtures (P3 only).** If the owner allows them: (a) a separate corpus
repository, one folder per source application, (b) every file is generated from scratch by a
**committed generator script** (never hand-made), (c) keep files tiny and single-feature, (d) the
vendor's own assets (presets, patterns, fonts, profiles, samples) never enter, fonts are referenced
by name only, (e) a checksum list is updated in the same commit, (f) the pin in the product repo is
bumped by PR, (g) **never rewrite or force-push history**: old pins must stay fetchable.

R9.5 **Do not commit oracle output** that contains someone else's expression. You may commit our
comparison *scores* and harness, not the vendor's frames or files (R5.5).

R9.6 When fetching anything from the network use a generic, non-personal user agent and no personal
details in requests.

---

## 10. Provenance and documentation

R10.1 **Per-module README "Provenance / Clean-room" section.** Every module, crate or package that
implements a format, codec, algorithm or behaviour area has one. Use `DOCUMENT-TEMPLATES.md` T2. It states:
spec edition(s) used; what was observed and when; which oracles; what was **not** read; what is
unverified; known deviations.

R10.2 **Say exactly what was read.** For any exception (R3.7/R3.8) the README lists the third-party
source, licence, exact commit, what was learned from it, and how it was re-described and verified.

R10.3 **Record decisions in ADRs** (short written decisions): posture (R4.5), exceptions (R3.7), a
dependency licence debated (R7.7), a feature declared out of scope (R12.4), any asset exception
(R8.3). Template `DOCUMENT-TEMPLATES.md` T4.

R10.4 **Keep an honest status** (roadmap/parity tracker): say whether a number is *measured* (test,
diff, benchmark someone can rerun) or *estimated*; count stubs and partial features as partial;
list known limitations next to what works; do not raise a percentage without evidence a reviewer
can rerun. A "live" status means "wired and tested", not "as good as the target"; when you find
otherwise, add the failing test or real input so the generated status drops (R10.7).

R10.5 **Commits** carry a task id and describe what was learned from where when it is relevant (e.g.
"M3.2: edit lists per <spec title, edition> §8.6.6").

R10.6 **Privacy of the notes.** The local observation folder may contain sensitive context. It is
gitignored, never uploaded, and not shared with third-party services.

R10.7 **Status is generated, not written.** The parity tracker and the scorecard are generated from
the owner-approved feature catalogue and from evidence the test run writes (registry commands,
acceptance tests, real-input comparisons); nobody types a status. They keep the dimensions apart,
because each one overstates the next:
- *wired*: a command exists and every control surface reaches it (R13.6);
- *live*: wired, and its acceptance tests pass;
- *real inputs*: the pass rate on corpus files and oracle comparisons;
- *validated*: users or the owner confirmed it on real work. This is the only estimated dimension,
  and it is labelled as an estimate.
A fully wired menu tree says nothing about behaviour; a live feature can still fail on real files
and in users' hands. A control that exists but changes nothing (a setting no code reads, a button
with no effect) counts as missing. What cannot be measured yet is reported as "not measurable
yet" with the reason, never as a guessed number. Where a generated number and an estimate
disagree, the generated number wins.

R10.8 **Floors only rise.** Measured counts that matter (live features, real inputs passing, per area
and in total) have committed floors that the gate enforces. Raise a floor in the commit that
exceeds it. Lowering one is an owner decision with an ADR. This keeps parallel agents from trading
one area's regressions for another area's gains.

---

## 11. Enforcement by automation

Prose rules are not enough. The project SHOULD have these checks in its main gate and agents MUST NOT
weaken them to make a commit pass; fix the cause instead.

R11.1 **Asset check:** fails when an asset file has no provenance record; when a hash does not match;
when a licence is off the allowlist; when a required licence file is missing; when a file name,
extension or metadata suggests vendor material (seen: vendor-specific preset, profile and template
file extensions; the target vendor named as author or source of an image, icon or font).

R11.2 **Clean-room check:** fails on vendor copyright notices in the repository (sources, tests, docs)
and on fixtures whose metadata shows they were made by a vendor application (creator/producer
fields, application signature). At P1 this is mandatory.

R11.3 **Dependency check:** licence allowlist over all (transitive) dependencies; fails on copyleft
unless the profile allows a specific, recorded case.

R11.4 **Corpus check:** every fetched fixture verified against its pinned hash; build never silently
uses an unpinned file.

R11.5 **Embedded-content check:** generated artefacts (e.g. a demo PDF) fail if they embed a font or
image not on the allowlist, catching silent fallbacks to a system font.

R11.6 **Parity check:** the committed parity tracker and scorecard are exactly what the catalogue and
the evidence generate (a hand edit or a stale report fails); every evidence row names a catalogue
feature; out-of-scope rows carry evidence of nothing; the floors hold (R10.7, R10.8). The gate
environment produces the same evidence as the one that committed the reports: it fetches the pinned
corpora and installs the oracles, or the check fails. A skipped input is shown, not hidden.

R11.7 **Gitignore guard:** the local observation folder and any oracle-output folder are ignored and
checked in CI that nothing under them is tracked.

R11.8 Run the full gate before **every commit**. Commit only green states.

---

## 12. Escalation and ownership

### 12.1 What the profile must say

Target and vendor, posture, spec list, forbidden names (copyleft competitors and vendor software),
dependency licence allowlist, observation folder, where fonts and corpora live, who the owner is.

### 12.2 Missing profile

Do not start implementing. Produce a filled `PROJECT-PROFILE.md` draft for the owner to approve.

### 12.3 Ask the human only about

- licences outside the allowlist, or an asset whose origin is unclear;
- the posture, or any exception to R3.x / R8.x (R3.7, R3.8, R8.3);
- a bridge that drives the target (R5.11), and whether implementers may call it (R5.13);
- lowering a parity floor (R10.8), or exposing the control channel beyond loopback (R13.8);
- scope questions on formats with no public spec (R3.8, R12.4);
- publishing, pushing to a new remote, secrets, spending money;
- personal data;
- destructive repository operations, including purging history after a violation (R8.12);
- anything the rules leave unclear.

Everything else: decide, record, continue. Do not stall on choices you can make within the rules
(R6.4).

### 12.4 Out of clean-room scope

Declare, with an ADR, and list in the roadmap under "out of clean-room scope", anything that cannot be
done within the posture. Typical members: proprietary project/document formats with no public spec;
scripting bytecode formats; vendor cloud and service integrations; vendor presets, LUTs, film
emulations and lens/camera data unless collected by us from permitted sources; features that need a
model or dataset we may not ship. Do not start such work without the owner's decision.

---

## 13. Working hygiene that protects the clean-room claim

R13.1 Keep the local plan/observation folder out of version control; make sure it is ignored before
creating anything in it.

R13.2 Parallel agents: separate git worktrees, separate build directories, separate scratch
sub-folders and, where an app exposes a control port, separate ports. Never delete shared paths.
Check `git status`, worktrees and unmerged commits before starting after a crash or handover.

R13.3 When merging parallel branches, merge one, run the gate, fix, then the next: two green
branches can break each other.

R13.4 Look at your output (render, screenshot of *our* app) before claiming a UI or rendering
feature works. Compare with the behaviour notes, never by dropping vendor imagery into the repo. A
capture proves what is visible; a command test proves what it does. Claims need both.

R13.5 Agents acting for a contributor do not invent credits or edit anyone else's contributor entry.

R13.6 **Agent-control interface (decided in phase 4, ADR).** Agents check their work by driving
*our* product, never by reading or watching the target. The default: every user-visible action is a
command in **one registry** (id, name, menu path, parameter description in our own words, enabled
condition, run). The UI, a CLI and an agent server (for example an MCP server) dispatch by id and
hold no behaviour of their own; a capture command renders our app or its output, offscreen where
possible. Command ids are the catalogue's ids or names, so registering a command is the evidence
that wires its row (R10.7). Only pure view state (zoom, panel layout) may stay in the UI. The owner
may choose a narrower interface or none; the ADR then records the reason and what agents use
instead to verify (R13.4). For other categories (§15): for a library the public API is the
registry; for a CLI, the CLI; for a web app, an HTTP API plus a headless browser on our own build.

R13.7 **The control channel serves our product only.** Never point it, the CLI or the agent server at
the target or at other vendor software. At P1 that is R4.2. At P2/P3, observation follows §5, and a
bridge to the target is a separate tool under R5.11 to R5.13, never this channel. Captures show our window or an offscreen render, never the desktop (R5.3 applies to
our own app too), and only fixture documents built from allowed assets (R8.4).

R13.8 **Control input is hostile.** Listen on loopback only, require a token, restrict file access to
named project roots, cap request and reply sizes. Every command fails with an error, never a crash,
on any parameters or state. A test drives every registered command with bad parameters.

---

## 14. Quick checklists

### 14.1 Starting a new clean-room project

- [ ] Owner has read the vendor's terms and chosen posture P1, P2 or P3 (R4.1).
- [ ] `PROJECT-PROFILE.md` filled in and committed (public part) / local part ignored.
- [ ] Local observation folder created and gitignored (R13.1).
- [ ] Asset index, NOTICE and licence allowlist created; asset check wired into the gate.
- [ ] Clean-room check wired (R11.2); at P1 also fails on vendor-made fixtures.
- [ ] List of public specs for the main formats written down with editions.
- [ ] Copyleft and competitor names listed as "do not read".
- [ ] Out-of-scope list started (§12.4).
- [ ] Corpus repository (if any) created with generator scripts and pinned hashes.
- [ ] Feature catalogue approved; parity tracker and scorecard generated from it (R10.7).
- [ ] Agent-control interface decided in an ADR (R13.6).

### 14.2 Before adding an asset

- [ ] Not vendor-made; not a copy/trace of vendor art (R8.1, R8.2).
- [ ] Licence provable from the original source; allowed licence (R8.5).
- [ ] Provenance record in the same commit (R8.7); licence file included if required.
- [ ] Asset check passes (R11.1).
- [ ] If anything is unclear: not added, owner asked.

### 14.3 Before implementing a format, codec or behaviour

- [ ] Public spec found and edition recorded (R7.1, R7.2), or posture allows observation, or it is out of scope.
- [ ] No third-party implementation of the same thing opened (R7.3, R3.2).
- [ ] No passage written from recall of a named implementation; structure derived from the cited spec or T7 entries (R7.11).
- [ ] Tables extracted by script or derived by us (R7.1, R7.4).
- [ ] Oracles identified, used only as external processes (R7.5).
- [ ] Module README has a Provenance section (R10.1).

### 14.4 Before every commit / PR

- [ ] Gate green (R11.8).
- [ ] No file produced by the vendor tool, no vendor notice, no vendor wording (R3.4, R3.5).
- [ ] Nothing from the local observation folder staged (R5.5).
- [ ] New data/tests contain no personal data (R9.3).
- [ ] Status/parity numbers honest and evidenced (R10.4); reports regenerated, not edited; floors
      hold and are raised where exceeded (R10.7, R10.8).
- [ ] New user-visible behaviour is a registry command with a bad-parameter test (R13.6, R13.8).
- [ ] Task id in the message (R10.5).

### 14.5 If you think you violated a rule

Stop. Remove the material from the working tree and outputs. Tell the owner: what, where, how,
whether it was committed or pushed. Do not hide it in a later commit message. Wait for instructions
about history (R8.12).

---

## 15. Readings by target category

The rules above were written with an installed desktop application in mind. They apply to every
target; this section says what the key terms mean for other categories. The profile records the
category (section 1) and any category-specific owner decision, before phase 3 starts.

| Category | "Install / bundle" (R3.1): never opened | Observation (S3, §4, §5) | Names that may be reused (R6.3) | Typical owner decisions |
|---|---|---|---|---|
| **Desktop application** (baseline) | installed files, packages, plug-ins, resources | running the app with synthetic documents | feature, menu, command names | formats without a public spec (R3.8) |
| **Web application / SaaS** | everything the browser downloads: HTML, scripts, style sheets, bundles, source maps, API responses. View-source, DevTools inspection of scripts, network capture and intercepting proxies are reading internals. | using the service through its normal UI with a test account and synthetic data, under its terms of service; no scraping; no automation beyond a documented public API; rate limits respected | page, menu, button and setting names; documented public API routes and fields | P2 against the terms of service; whether a public API may be exercised; who owns the test account |
| **Library, SDK, framework** | binaries, headers, source and docs shipped in the package. **Needs a profile entry:** headers or reference docs that the vendor publishes *as* its public API documentation may be read as S2 only if the owner records it; they describe behaviour but sit inside the install. | calling the public API from a test program (P2) | public API names, signatures, constants and error codes as documented: these are the "menu names" of a library | whether shipped headers or reference docs count as S2; whether ABI compatibility is in scope |
| **Server, service, protocol** | server binaries, configuration templates, bundled scripts, database files | running a client or server the project holds a licence for and exchanging **synthetic** traffic (P2). Capturing the wire protocol between your own client and your own server instance is observation; capturing anyone else's traffic never is. | protocol message names, documented fields, command names | whether an undocumented wire protocol may be studied by capture (R3.8 analogue); copyleft clones are common in this category |
| **Mobile application** | the APK, IPA or app bundle and everything in it: decompiling, unpacking resources, reading manifests beyond the store listing | using the app on a device or emulator with a test account (P2); captures of the app's screen only | screen, menu and setting names | store and vendor terms usually forbid reverse engineering outright: default P1 |
| **Command-line tool** | the executable and its data files | running it on synthetic inputs and recording outputs (P2) | command, flag and option names as given in `--help` or manual pages (S2) | whether byte-identical output is a goal |
| **Game or engine** | the game's data files, executables, scripts, assets | playing the owner's own copy (P2); no asset extraction | mechanic, menu and option names; never level design, story, characters, art, music | engines that read **user-owned original data files**: the data format usually has no public spec (R3.8); the owner decides whether a black-box study of files the user legally owns is in scope. Shipping no data and requiring the user's own copy is the established clean pattern. |
| **Open-source target** (copyleft or otherwise) | the source repository, its history, issues and any built artefact's resources | running the released program is allowed by any open licence (P2 at least); reading the source is R3.2 and never allowed for the features being built | the same as for the program's own category | the "vendor terms" of phase 1 are the licence text; the project itself heads the do-not-read list; its own documentation is S2 but its wording is still expression |
| **Firmware, driver, hardware-attached software** | the image, the driver package, vendor tools | exercising the device through documented interfaces (P2) | documented registers, commands, protocol names | whether bus or protocol capture is permitted; often out of clean-room scope |

R15.1 When a category is not listed, the owner records the readings of R3.1, S3 and R6.3 for it in
the profile before phase 3 starts, by analogy with the closest row.

R15.2 A target may fall into several rows (a desktop app with a cloud service, a library with a CLI).
Record every applicable row; where they conflict, the strictest reading wins.

R15.3 Public material that the vendor distributes *inside* the install (an SDK reference, a licence
file, a bundled spec) stays unopened under R3.1 unless the owner lists it in the profile as S2 with
its path. Prefer the same material from the vendor's public website.
