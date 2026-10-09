---
name: <<project-slug>>-drive
description: Drives the running <<PROJECT NAME>> app (never the target) through its command registry, CLI or agent server, inspects its state and captures its own output, so an agent can check its work. Use after implementing or fixing a feature, when verifying a UI or rendering change, and when writing command evidence for the parity record.
---

# Drive and capture <<PROJECT NAME>> (our app only)

Rules: `cleanroom/rules/CLEANROOM-RULES.md` R13.4 and R13.6 to R13.8. Decision: `<<agent-control ADR path>>`.
Stack skill: `<<project>>-stack` (start, build and port commands).

**This skill drives our product only.** Never point the control channel, the CLI or the agent server
at the target or any vendor software (R13.7). Observation of the target, where the posture allows it,
uses `<<project>>-observe` and nothing here.

## Surfaces

| Surface | How to reach it |
|---|---|
| Command registry (list, with enabled state) | `<<list commands>>` |
| Run a command by id | `<<run command id with params>>` |
| CLI (headless) | `<<cli command>>` |
| Agent server (for example MCP) | `<<agent server command>>` |
| Inspect UI and document state | `<<inspect command>>` |
| Capture our app or its output | `<<offscreen render or window capture by id>>` |

Per-agent isolation: port or socket `<<scheme>>`, build directory `<<scheme>>`, scratch folder
`<<scheme>>` (R13.2). Token: `<<where the token file lives>>`; never print it into logs or commits.

## Loop

1. **Start** our app or headless runner on your own port with a token and file roots limited to
   the project (R13.8).
2. **Prepare** a fixture document built in code from allowed assets only (R8.4, R9.1). No personal
   files, no files made by vendor software.
3. **Act** by command id. Use the id from the catalogue row (`cleanroom/parity/features.tsv`).
   A behaviour that is reachable only by a UI handler is a C8 finding: move it into the registry.
4. **Inspect** the state the command left, then **capture**, preferably offscreen (no window, no
   focus stealing). Never capture the desktop or other windows.
5. **Look** at the capture and compare it with the behaviour notes (T7), never with vendor imagery.
   A capture shows composition; the acceptance test proves behaviour (R13.4). Keep both.
6. **Record** evidence: the command test writes `command` rows (`wired` only if every surface in the
   ADR reaches the command); regenerate the parity reports (`<<parity command>>`).
7. **Clean up**: stop the app, delete scratch output; captures stay out of the repository unless
   everything visible is allowed (R8.4).

## Stop and ask

A command needs a vendor asset or a file made by vendor software; a capture would show anything not
ours; the only way to verify seems to be comparing with the target at a posture that forbids it; the
channel would have to listen beyond loopback or without a token.
