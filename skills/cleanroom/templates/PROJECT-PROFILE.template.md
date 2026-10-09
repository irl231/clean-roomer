# Project profile (clean-room): <PROJECT NAME>

Copy this file to `cleanroom/PROJECT-PROFILE.md`, fill in every field, and have the owner approve
it. `CLEANROOM-RULES.md` applies in full; this file only sets the parameters it refers to. Anything
left blank means the **strictest** reading applies.

## 0. Process settings

| Field | Value |
|---|---|
| Scope dial: last phase to run (1 to 6) | |
| Phase 5 limit (until stopped / milestone / count) | |
| Stack (language, build tool, UI toolkit) | |
| Gate command run before every commit | |
| Observation / plan folder (gitignored) | |
| Repository layout (monorepo, product repo plus corpus repo, ...) | |

## 1. Identity

| Field | Value |
|---|---|
| Project name | |
| Target (the application we re-create) | |
| Target version(s) of interest | |
| Target category (rules §15; several allowed, strictest wins) | desktop / web or SaaS / library or SDK / server or protocol / mobile / CLI / game or engine / open-source target / firmware |
| Category readings recorded (R15.1 to R15.3): what "install" means, what observation means, which names may be reused, public material inside the install that counts as S2 | |
| Existing repository? (code, assets, dependencies and history already present; see phase 2 "existing repository") | no / yes: baseline report path |
| Vendor | |
| Other vendors whose tools might touch the project (R4.4) | |
| Owner (human with authority) | |
| Licence of our code and original assets | (e.g. MIT OR Apache-2.0) |
| Profile date / approved by | |

## 2. Posture (CLEANROOM-RULES §4)

| Field | Value |
|---|---|
| Posture | P1 / P2 / P3 |
| Basis (vendor terms read? link, date, who read them) | |
| If P2/P3: installed target version and OS | |
| If P2/P3: local observation folder (gitignored; becomes a `path:` entry in the deny-list) | e.g. `observation/` (avoid names the project uses for its own documents) |
| If P2/P3: how the target window is captured (R5.3) | e.g. by window id with OS tool |
| If P3: corpus repository and generator folder | |
| ADR recording this decision | |
| If P2/P3: target bridge (R5.11 to R5.13) | none / ADR link, attachment method, bridge folder, scratch folder, server and tool names listed in `cleanroom/do-not-read.txt`, implementers may call it: no / yes |

## 3. Allowed behaviour sources

| Class | Concrete sources for this project |
|---|---|
| S1 specifications | list: title, version/edition, URL |
| S2 public documentation | list of doc sites / manuals |
| S5 licensed sample corpora | list: name, licence, pinned commit |
| S6 dependency policy | licence allowlist; is MPL-2.0 allowed unmodified? yes / no |
| S7 reuse from sibling projects | allowed? yes / no, which |

## 4. Do-not-read list (R3.2)

Copyleft or competitor code the agent MUST NOT read, open, port or learn from. Include open-source
clones of the target and its file format libraries.

- 
- 

Permissively licensed implementations that are also **not to be read** while implementing the same
thing (R7.3), e.g. reference decoders:

- 

## 5. Oracles (R7.5)

| Tool | Version | Use | Run as external process only? |
|---|---|---|---|
| | | | yes |

## 6. Assets

| Field | Value |
|---|---|
| Provenance index file | (e.g. `ATTRIBUTION.md` / `ATTRIBUTION.toml`) |
| Licence allowlist for assets | |
| Vendor-open-licensed visual design exceptions (R8.3), closed list | none |
| Own brand marks and their licence (R8.11) | none |
| Font policy / font repository | |
| Where code-drawn icons live | |
| Asset check command | |

## 7. Corpora and tests

| Field | Value |
|---|---|
| Corpus repository | none |
| Pin file | |
| Fetch command (verifies hashes) | |
| Synthetic fixture generators | |

## 8. Automation (CLEANROOM-RULES §11)

| Check | Command | In the commit gate? |
|---|---|---|
| Asset check | | |
| Clean-room check (vendor notices / vendor-made fixtures) | | |
| Dependency licence check | | |
| Corpus hash check | | |
| Parity check (C6): `parity_report.py --check --commands <mode>` after the tests | | |
| Command coverage (C8), if the agent-control ADR chose a registry | | |
| Gitignore guard for observation folder | | |
| Do-not-read guard (agent hook, G1) | `.cursor/hooks.json` + `cleanroom/do-not-read.txt`, or "not available: prose-only" | hook |
| Scanner in use (`cleanroom_scan.ps1` / `cleanroom_scan.py` / own) and self-test command | | |

## 9. Out of clean-room scope (R12.4)

| Feature / format | Why | ADR | Owner decision pending? |
|---|---|---|---|
| | | | |

## 10. Escalation

Who to ask, and how, for the topics in CLEANROOM-RULES §12.3:

- Licences / asset origin:
- Posture / exceptions:
- Publishing / remotes / secrets:
- History purge after a violation:

## 11. Agent-control interface of our product (R13.6 to R13.8, decided in phase 4)

| Field | Value |
|---|---|
| ADR (template T10) | |
| Interface | registry + CLI + agent server / registry + CLI / category interface / none: reason |
| Registry location | |
| CLI and agent server commands | |
| Capture command (our app only, offscreen preferred) | |
| Per-agent port / build dir / scratch scheme | |
| Token and file roots | |
| Parity report `--commands` mode | required / optional / none |

## 12. Parity record (R10.7, R10.8)

| Field | Value |
|---|---|
| Catalogue | `cleanroom/parity/features.tsv` |
| Evidence folder (ignored build output) | `cleanroom/parity/evidence/` |
| Floors | `cleanroom/parity/floors.tsv` |
| Generated reports (committed) | `cleanroom/parity/parity.md`, `cleanroom/parity/scorecard.md` |
| Extra measured scorecard sources, if any | (e.g. settings no code reads, performance budgets) |
