---
name: bsg
description: Run BSG, a conversational discovery, planning, and delegated delivery workflow for new software projects or substantial features. Use for BSG commands or a requested BSG project; ordinary small fixes do not need the full workflow.
---

# BSG

Keep the user in one product conversation while ready work progresses through subagents. The user shapes intent and tests milestones; you maintain the plans and evidence. Prefer useful feedback and cheap changes of direction over keeping agents busy.

## Entry and routing

Resolve the target project before writing. If `.planning/state.json` exists, read it and `PROJECT.md`, plus `STATE.md` notes when present; load only context relevant to the requested action. If `.planning` belongs to another framework, inspect it and agree a migration or separate destination rather than replacing it.

On `start` or `resume`, ensure the project's instruction files (`AGENTS.md`, plus `CLAUDE.md` when one exists) carry the BSG handoff described in [records.md](references/records.md). Preserve existing instructions. Help and status remain read-only.

BSG is the only registered skill. Its public commands are start, help, status, pause, and resume; discovery, discussion, planning, building, and verification remain internal stages. In Codex the skill is mentioned as `$bsg`; in Claude Code it is the slash command `/bsg`. “BSG start” in plain language works in both.

Identify the host from the tools you actually have, then read that host's adapter: [codex.md](references/codex.md) when Codex tools are present, [claude-code.md](references/claude-code.md) when Claude Code tools such as `AskUserQuestion` and `Agent` are present. Read only one.

Read [commands.md](references/commands.md) to resolve the five commands and help/status recommendations. A request such as “let's work through slice 5” changes conversational focus, not authorization for unrelated execution. Stable slice IDs are never renumbered. Read mode references only as needed:

- Discovery, start, discuss: [discovery.md](references/discovery.md).
- Planning, execution, verification, pause/resume, change handling: [delivery.md](references/delivery.md).
- Creating or updating records: [records.md](references/records.md).
- Roadmap decomposition and slice scope review before build approval: [slices.md](references/slices.md).
- Tool capabilities, picker fallback, delegation, model routing: the host adapter chosen above ([codex.md](references/codex.md) or [claude-code.md](references/claude-code.md)).

## Shared principles

Conversation is the review interface; never require the user to read plan files. Reuse supplied answers and preferences. Act as a product partner: propose alternatives, challenge assumptions, and bring consequential scope or technical choices to the user unless delegated. Label proposals and assumptions; never record them as agreed decisions.

Outline the whole project and detail work as it approaches execution. Keep discovery and authorized delivery overlapping where dependencies and human checkpoints allow. Implementation, verification, human acceptance, and completion are different facts; apply [delivery.md](references/delivery.md) before starting a build or claiming completion.

End each phase or material roadmap/status change with a short conversational recap: what was settled, where work stands, and the recommended next step with alternatives. Make handoffs actionable: identify who acts next, ask a specific question when input is needed, or continue authorized unblocked work. Do not invent further work when the request is complete. Keep pending questions in the handoff notes and indexed progress in state.json, following [records.md](references/records.md).

Delegate independent substantial work when useful. This skill explicitly authorizes subagents for the BSG workflow and behavioral validation within the user's scope and host permissions. The lead owns shared records; workers own assigned files and reports. Do not promise background persistence or future wakeups without host support.

Each rule has a primary reference: discovery sequence and interview pacing in discovery.md; slice boundaries in slices.md; build authorization, changes and completion in delivery.md; record lifecycle and generated summaries in records.md; tool behavior in the host adapter. Follow those references at the relevant stage rather than maintaining alternate procedures here.

## Local helpers

Use an available Python 3.10+ interpreter with this skill's `scripts/bsg.py`:

```text
python <skill>/scripts/bsg.py init --root <project> --name <name>
python <skill>/scripts/bsg.py attach --root <existing-BSG-project>
python <skill>/scripts/bsg.py slice --root <project> --title <deliverable>
python <skill>/scripts/bsg.py help --root <project>
python <skill>/scripts/bsg.py status --root <project>
python <skill>/scripts/bsg.py validate --root <project>
python <skill>/scripts/bsg.py sync --root <project>
```

Init refuses an existing planning folder. Slice creation allocates a new stable ID and creates only CONTEXT.md. Sync refreshes generated ROADMAP/STATE sections from the index while preserving surrounding notes; run it after index changes, not during read-only help/status. Help/status are read-only and validate the ledger before recommending work. The helper never launches agents, marks tests passed, or grants acceptance. If Python is unavailable, maintain the same records directly and disclose that automated record validation was unavailable.
