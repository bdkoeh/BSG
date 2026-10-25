# Decisions

## D-001 revision 1 — Codex first; portable records
Agreed in the project discovery conversation. Package a Codex skill family now; consider Claude later.

## D-002 revision 1 — One conversation with overlapping discovery and delivery
Bob explicitly requested planning later slices while subagents implement ready ones. The lead owns shared records and coordinates dependencies.

## D-003 revision 1 — Conversation is the product interface
Adaptive themed pickers, suggested answers plus free text, independent agent/human effort, and conversational decisions instead of document approval. Agreed through the discovery rounds.

## D-004 revision 1 — Evidence and selected human checkpoints
Track implementation, verification, acceptance and completion separately. Pause at agreed human gates. Keep progress documentation current. Directly requested by Bob.

## D-005 revision 1 — Direct commands coexist with orchestration
Explicit discover/discuss/plan/build/help/status/pause/resume actions; help includes a next-step recommendation. Codex packaging uses skill invocation, not a claimed replacement of native /help.

## D-007 revision 1 — One skill for Claude Code and Codex
Bob asked on 2026-10-24 that the same repository serve both hosts with no host-specific chores for the person installing. One `skills/bsg` folder; one adapter reference per host (`codex.md`, `claude-code.md`) chosen by the lead from its actual tools; the repository doubles as a Claude Code plugin marketplace; the installer detects `.claude`/`.agents`; the handoff stays in `AGENTS.md` and is mirrored into `CLAUDE.md` only when a project already has one. Supersedes the “consider Claude later” part of D-001.

## D-006 revision 2 — Public GitHub repository under MIT
Bob made the repository public on 2026-10-25 and chose the MIT license, matching the permissive-core assumption in DESIGN.md. Revision 1 (2026-10-21) kept it private with a README ready for eventual public use.

## D-008 revision 1 — Dual host, both remotes
Every push goes to GitHub (`origin`) and Bob's local Gitea (`gitea`). Bob asked for this on 2026-10-24.
