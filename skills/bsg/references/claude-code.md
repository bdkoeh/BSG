# Claude Code adapter and effort policy

Use current tool availability as authority. Skill installation does not create worker slots, a background scheduler, or model access. Never edit settings files to manufacture capabilities without a user request.

## User interaction

Use the `AskUserQuestion` tool as the picker. It takes one to four questions per call, each with two to four options plus an automatic free-text “Other” choice, and supports multi-select where answers are not exclusive. Put your recommended option first and mark it recommended. One round of 3–4 related questions fits a single call. Pending answers are not approvals.

BSG is one skill invoked as `/bsg` with start, help, status, pause, or resume, for example `/bsg help`. Inside a plugin the fully qualified form is `/bsg:bsg help`; natural language such as “BSG start” also works because the skill description matches BSG requests. Help means BSG help when the BSG context is explicit; do not intercept Claude Code's own `/help`.

## Project instructions

Claude Code reads `CLAUDE.md`. It reads `AGENTS.md` only when the project has no `CLAUDE.md`, `.claude/CLAUDE.md`, or `CLAUDE.local.md`. The helper therefore writes the handoff block to `AGENTS.md` and, when any `CLAUDE.md` exists, to the root `CLAUDE.md` as well. If Python is unavailable, follow the same rule manually; see records.md.

## Delegation

Use the `Agent` tool for workers; it runs them in the background by default and returns a report when each finishes. Prefer it over new user-owned sessions. Each call accepts a focused prompt, an optional `model` override, and optional worktree isolation for workers that edit code. Supply a focused task packet with every path, ID, and revision the worker needs; a fresh agent knows only its prompt. Use a fork of the lead's context only for work that genuinely needs the conversation. Keep shared paths and ownership explicit; give workers that edit code disjoint files or their own worktree.

The lead cannot switch its own model through a skill. If the user wants a different lead model, explain the app's model picker without claiming a switch occurred.

Suggested roles when available: Opus for consequential reasoning and difficult tradeoffs; Sonnet for substantial implementation and debugging; Haiku for bounded extraction, lookups, and routine work. A hard research synthesis may need Opus or Sonnet. A simple edit may fit Haiku. A reviewer needs sufficient capability for the actual risk. Omit the model to inherit the lead's model when unsure.

| Effort | Delegation and depth |
| --- | --- |
| lean | Narrow research to consequential unknowns, avoid speculative experiments and redundant reviewers, use capable lower-cost workers for bounded tasks. |
| balanced | Targeted research and experiments; independent review where likely to catch material errors. |
| deep | Investigate difficult alternatives and assumptions more thoroughly; stronger workers/review for consequential work. Still stop when evidence is sufficient. |

These are heuristics, not token accounting. Optimize total work including supervision, retries and rework. Do not promise savings without measurements. User involvement is independent: a low-involvement user can request deep agent work.

Background agents report when they finish; the lead is not notified mid-run, so checkpoint records before yielding and verify an agent's actual result before marking anything implemented. If delegation is unavailable, disclose it once and work sequentially without claiming parallel execution. Do not schedule follow-ups or recurring tasks unless requested. For a single worker that is still useful, delegate; for a tiny task whose coordination would cost more, handle it directly.
