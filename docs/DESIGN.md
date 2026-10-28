# BSG v0.1 design

In BSG the user works through conversation; agents maintain durable records. Codex was the initial host; Claude Code is the second. Core records and product workflow are independent of the host. Each host has one adapter reference inside the skill (`codex.md`, `claude-code.md`) covering its picker, delegation tools, model names, and instruction-file rules; the lead reads only the adapter for the tools it actually has.

## Agreed product behavior

- New projects and substantial existing-project features; focused codebase orientation rather than an obligatory full map.
- High-level product alignment first, then deeper discovery for each slice as it approaches implementation.
- Adaptive themed picker rounds with suggested answers and free text. Product partnership includes challenges, alternatives, and research as questions arise.
- Independent settings for agent effort and human involvement. No mandatory numerical budget or deadline.
- One lead chat: discuss upcoming slices while workers implement ready ones. Major technical choices are conversational decisions unless delegated.
- Rough overall roadmap, stable slice IDs, detailed plans near execution, and explicit direct commands alongside automatic orchestration.
- Human checkpoints selected during planning. Agreement also determines whether independent work can continue while waiting.
- Small feedback fixes now, larger changes deferred unless blocking. Aesthetic direction upfront; major frontend finishing work after core behavior.
- Experiments resolve consequential uncertainty. Decision references support targeted replanning and stale-result detection during concurrent work.
- Read-only help includes a useful next action. Status distinguishes implementation, verification, human feedback, and completion.
- Agents maintain records as work progresses. The lead owns shared state; workers own assigned reports. Resume reconciles actual work with documents.

## Packaging decisions

One registered BSG skill owns behavior and exposes start, help, status, pause, and resume. The lead guides internal stages through conversation. Supporting references are loaded by mode. A standard-library Python helper creates records as needed, generates roadmap/status sections from the index, and provides conservative record checks; it does not execute projects or certify software.

The installer targets the project-local skill folder of whichever host the project already uses (`.claude/skills` or `.agents/skills`), both when neither exists, refusing differing existing files. The repository doubles as a Claude Code plugin marketplace so Claude users install with two commands. Invocation is `/bsg` in Claude Code and `$bsg` in Codex; plain “BSG start” works in both. The project handoff lives in `AGENTS.md`, mirrored into `CLAUDE.md` only when a project already has one, because Claude Code ignores `AGENTS.md` in that case. No global configuration, model switch, or background daemon is installed.

## GSD inspiration reviewed

Reviewed upstream workflow sources on 2026-10-21. BSG adopts concepts, not copied implementation:

| GSD source | BSG adaptation |
| --- | --- |
| [Questioning](https://github.com/gsd-build/get-shit-done/blob/main/get-shit-done/references/questioning.md) | Thinking partner; high-level alignment followed by focused slice discussion |
| [Map codebase](https://github.com/gsd-build/get-shit-done/blob/main/get-shit-done/workflows/map-codebase.md) | Relevant paths, conventions, and freshness; deepen selectively |
| [Execute phase](https://github.com/gsd-build/get-shit-done/blob/main/get-shit-done/workflows/execute-phase.md) | Delegated ready work, explicit ownership, reconcile worker results |
| [Progress](https://github.com/gsd-build/get-shit-done/blob/main/get-shit-done/workflows/progress.md) | State-aware next action including ongoing discovery and human gates |
| [Help](https://github.com/gsd-build/get-shit-done/blob/main/get-shit-done/workflows/help.md) | Small command menu plus project-specific recommendation |
| [Verify work](https://github.com/gsd-build/get-shit-done/blob/main/get-shit-done/workflows/verify-work.md) | Conversational testing with durable evidence; explicit feedback rather than treating empty input as acceptance |

## Limits to test through real use

Picker continuity and worker persistence depend on the host. Skill instructions cannot enforce atomic updates across independent agents or guarantee model compliance. The index catches common bookkeeping errors, but a lead must verify records against actual code and results. We should judge BSG by useful feedback, preserved decisions, avoided rework, and honest completion rather than number of agents spawned.
