# Specification of the automated checks (rules section 11)

The agent implements these in the project's own stack during phase 2 and wires them into the gate
command. `scripts/cleanroom_scan.ps1` and `scripts/cleanroom_scan.py` both cover check C2 (same
format, output and exit codes) and can be used as they are or re-implemented.
`scripts/parity_report.py` covers C6 from the evidence files the test run writes. Checks that need a
stack not yet chosen are marked "deferred to phase 4" and implemented there.
**Every check must be proven**: before relying on it, plant one violation, see it fail, remove it,
see it pass. Record that in the check's own test or in the setup log. A check that has never failed
is not evidence.

| Id | Check | Rule | Must fail when | Inputs |
|---|---|---|---|---|
| C1 | Asset check | R11.1 | an asset file has no provenance record; a recorded SHA-256 does not match; a licence is not on the allowlist; a required licence file is missing; a name, extension or metadata suggests vendor material; a record names the target vendor as author or source (unless flagged on the profile's closed list) | asset index, licence allowlist, deny-list |
| C2 | Clean-room scan | R11.2 | text in tracked or untracked-unignored files (UTF-8 or UTF-16, any size) matches a `term` or `notice`; a file's first 256 KiB matches a `meta` string (binaries are never exempt); a file has a forbidden extension or path; a file cannot be read or located (never skipped silently) | `cleanroom/deny-list.txt` |
| C3 | Dependency licences | R11.3 | any direct or transitive dependency has a licence off the allowlist (copyleft by default) or an unknown licence | lockfile and the stack's licence tool |
| C4 | Corpus pins | R11.4 | a fetched fixture hash differs from its pin; a fixture is used that is not pinned; a corpus file is tracked in the product repo | pin file |
| C5 | Embedded content | R11.5 | a generated artefact embeds a font or image not on the allowlist (only if the product generates such artefacts) | allowlist |
| C6 | Parity check (`parity_report.py --check`) | R11.6, R10.7, R10.8 | the committed `parity.md` or `scorecard.md` differs from what the catalogue and evidence generate (hand edit or not regenerated); an evidence row names an unknown feature, kind or result; an out-of-scope row has evidence; a floor in `floors.tsv` is broken; the catalogue has a duplicate id or a scope without a reference | `cleanroom/parity/features.tsv`, `evidence/*.tsv`, `floors.tsv` |
| C7 | Ignore guard | R11.7 | anything under the observation folder or oracle-output folder is tracked, or the folder is not ignored | `.gitignore` |
| C8 | Command coverage (if the agent-control ADR chose a registry) | R13.6, R13.8 | a UI action dispatches something that is not a registry command (pure view state excepted, listed in the ADR); a registry command is unreachable from a surface the ADR names; a command panics or hangs on bad parameters instead of returning an error | the registry, the ADR's surface list |
| G1 | Do-not-read guard (agent hook, not in the gate; Cursor and Claude Code templates) | R3.1, R3.2, R7.3 | the agent tries to read, fetch, clone or open anything matching `cleanroom/do-not-read.txt` (forbidden project names and URLs, target install paths); proven by the script's `--self-test` plus one denied and one allowed access in the real agent, logged in the setup log | `templates/hooks/`, `cleanroom/do-not-read.txt` |

## Evidence the test run writes (input to C6)

`parity_report.py` reads tab-separated files in `cleanroom/parity/evidence/` with the header
`feature  kind  ref  result`. The project's test harness writes them; nobody edits them.

| kind | ref | result | Written by |
|---|---|---|---|
| `command` | registry command id | `wired` (reachable from every surface in the ADR) or `unwired` | the C8 test, which lists the registry and the catalogue ids it implements |
| `test` | acceptance test name | `pass`, `fail`, `skip` | the test runner (a reporter, or a tag on each acceptance test naming its feature id) |
| `real` | corpus file or oracle comparison | `pass`, `fail`, `skip` | the corpus and oracle tests |

The evidence folder is build output and is ignored. The reports are committed. The gate runs the
tests, then `parity_report.py --check`. To update the reports, run `parity_report.py` without
`--check` after the tests and commit the result with the change that moved them.

## Notes for implementers

- Output: one line per finding with the file and a reason, exit status non-zero on any finding.
- No network access in the gate unless the corpus fetch step is explicit and pinned.
- The checks read data only; they never modify the repository.
- At P1, C2 must include `meta` strings for the vendor's producer fields and the vendor's extensions.
- Keep the deny-list and allowlists in committed files, reviewed like code.
- If the stack has no suitable licence tool, write a small script that reads the lockfile and compares
  to the allowlist, and say so in the setup log.
- A project may extend the scorecard with its own measured sources (performance budgets, a count of
  settings no code reads, per-area checklists verified against a named commit). The same rules
  apply: generated, never hand-edited, "not measurable yet" instead of a guess, floors only rise.
