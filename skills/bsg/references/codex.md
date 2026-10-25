# Codex adapter and effort policy

Use current tool availability as authority. Skill installation does not create native slash commands, worker slots, a background scheduler, or model access. Never edit global settings to manufacture capabilities without a user request.

## User interaction

Prefer the available interactive question/picker tool. If a picker is available only in Plan mode, do not call it from Default mode; use the asynchronous picker when available. Pending answers are not approvals. If no picker exists, use short numbered options with a free-text invitation. Do useful independent work while awaiting answers only within existing scope and checkpoint rules.

Use one `$bsg` skill with start, help, status, pause, and resume; for example, `$bsg help` or “BSG start.” Guide all delivery stages through conversation. Native skill menus may expose other shortcuts; do not promise them. Help means BSG help when the BSG context is explicit; do not intercept unrelated app help requests.

## Delegation

Prefer host subagent tools, not new user-owned chats. Inspect available model choices and concurrency. This skill requests model routing for delegated work; use the exact supported model identifiers. Where a tool requires fresh context to override models, use fresh context and supply a focused task packet. Keep shared paths and ownership explicit. The lead cannot switch its own model through a skill: if Astra is desired, explain how the user can select it without claiming a switch occurred.

Suggested roles when available: Astra for consequential reasoning and difficult tradeoffs; Sol for substantial implementation/debugging; Luna for bounded extraction, lookups, and routine work. A hard research synthesis may need Astra/Sol. A simple edit may fit Luna. A reviewer needs sufficient capability for the actual risk.

| Effort | Delegation and depth |
| --- | --- |
| lean | Narrow research to consequential unknowns, avoid speculative experiments and redundant reviewers, use capable lower-cost workers for bounded tasks. |
| balanced | Targeted research and experiments; independent review where likely to catch material errors. |
| deep | Investigate difficult alternatives and assumptions more thoroughly; stronger workers/review for consequential work. Still stop when evidence is sufficient. |

These are heuristics, not token accounting. Optimize total work including supervision, retries and rework. Do not promise savings without measurements. User involvement is independent: a low-involvement user can request deep agent work.

If model overrides or delegation are unavailable, disclose it once and use the available model/sequential work without claiming parallel execution. If execution cannot persist across user turns, checkpoint and resume within host behavior. Do not schedule follow-ups unless requested. For a single worker that is still useful, delegate; for a tiny task whose coordination would cost more, handle it directly.
