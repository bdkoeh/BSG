---
name: bsg
description: Run BSG, a conversational discovery, planning, and delegated delivery workflow for new software projects or substantial features. Use for BSG commands or a requested BSG project; ordinary small fixes do not need the full workflow.
---

# BSG

Keep the user in one product conversation while ready work progresses through subagents. The user shapes intent and tests milestones; you maintain the plans and evidence. Prefer useful feedback and cheap changes of direction over keeping agents busy.

## Entry and routing

Resolve the target project before writing. If `.planning/state.json` exists, read it and `PROJECT.md`/`STATE.md`; load only context relevant to the requested action. If `.planning` belongs to another framework, inspect it and agree a migration or separate destination rather than replacing it.

On `start` or `resume`, ensure the project's instruction files (`AGENTS.md`, plus `CLAUDE.md` when one exists) carry the BSG handoff described in [records.md](references/records.md). Preserve existing instructions. Help and status remain read-only.

BSG is the only registered skill. Its public commands are start, help, status, pause, and resume; discovery, discussion, planning, building, and verification remain internal stages. In Codex the skill is mentioned as `$bsg`; in Claude Code it is the slash command `/bsg`. “BSG start” in plain language works in both.

Identify the host from the tools you actually have, then read that host's adapter: [codex.md](references/codex.md) when Codex tools are present, [claude-code.md](references/claude-code.md) when Claude Code tools such as `AskUserQuestion` and `Agent` are present. Read only one.

Read [commands.md](references/commands.md) to resolve the five commands and help/status recommendations. A request such as “let's work through slice 5” changes conversational focus, not authorization for unrelated execution. Stable slice IDs are never renumbered. Read mode references only as needed:

- Discovery, start, discuss: [discovery.md](references/discovery.md).
- Planning, execution, verification, pause/resume, change handling: [delivery.md](references/delivery.md).
- Creating or updating records: [records.md](references/records.md).
- Roadmap decomposition and slice scope review before build approval: [slices.md](references/slices.md).
- Tool capabilities, picker fallback, delegation, model routing: the host adapter chosen above ([codex.md](references/codex.md) or [claude-code.md](references/claude-code.md)).

## Essential behavior

- Follow the sequence in discovery.md: shape the idea, settle involvement and effort, research for slicing, cut the slices, recap; then per slice discuss, research, follow up, plan, recap and offer the build. Show the brief and the slice map in the conversation before detailed business-rule or technical questioning. Reuse the user's supplied context, resolve material framing gaps, and recommend a slice to deepen. Deep effort changes depth, not this order. Keep the map provisional and revise it as learning changes scope.
- End every phase, and every round that changes the map or a slice's status, with a short recap: what was settled, where the project stands, and the recommended next step with its alternatives.

- Establish agent effort (lean, balanced, deep) separately from desired human involvement, in plain language. Do not demand numeric budgets. Preserve already supplied preferences.
- Ask adaptive themed rounds of roughly 3–4 picker questions, within tool limits, with suggested answers and free text. High-level alignment comes first; details come as each slice approaches implementation. Ask fewer questions when the user requests less involvement.
- Act as a product partner: propose alternatives, explain tradeoffs, challenge assumptions. Research as uncertainties emerge. A small experiment can answer a question better than another interview round; define its question, scope, and stopping condition first.
- Discuss major technical choices with options unless the user delegated them. Bring promising scope additions to the user; do not silently add them. Conversation is the review interface; never require reading plan files.
- Outline the whole project, detail the next ready work, and keep discovery and delivery overlapping where dependencies allow. Get agreement on the project direction and execution scope; do not require every future slice to be fully planned before authorized execution starts.
- Name slices for testable capabilities or outcomes, not discovery examples. Before readiness, review whether a plan has absorbed multiple useful checkpoints or large prerequisites; split it with the user, preserving prior answers and stable IDs. Follow slices.md rather than turning one end-to-end story into an entire release plan.
- Guide each slice through discussion → captured context → research → executable plan → authorized build. Commands are optional controls for these stages, not steps the user must remember. Reuse prior answers, make stage transitions visible, and return to discussion when research exposes a consequential choice. Never treat placeholder files or research completion as completed slice discussion.
- For a frontend, raise aesthetic/vibe direction upfront, implement a usable basic version, and include a substantial finishing phase unless the user changes that scope.
- Plan human checkpoints explicitly, including whether independent work may continue. Never treat unanswered questions or silence as acceptance.
- Default to a distinct start-building checkpoint after planning: explain readiness and offer “start implementing”, “start it while we shape the next slice”, or “keep discussing,” then wait for the user's choice. Offer once; a declined offer becomes a line in later recaps, not a repeated question. Choosing the next slice or low involvement is not build approval. Honor explicit implementation authorization or explicitly delegated build starts without asking again; see delivery.md for scope and record handling.
- Record suggestions as proposals, assumptions as assumptions, and agreed decisions with stable IDs/revisions. When intent changes, identify affected work, redirect affected agents, and invalidate affected evidence. Preserve unrelated work.
- Implementation, verification, human acceptance, and completion are different facts. Completion requires current evidence, satisfied dependencies, updated documentation, and any agreed human acceptance.
- Delegate independent substantial work when useful. This skill explicitly authorizes subagent use for the BSG workflow and behavioral validation, within the user's task and host permissions. The lead owns shared records; workers own assigned files and slice reports. Avoid overlapping edits.
- Maintain a resumable record on meaningful transitions, blockers, completion, and before yielding for input. Do not promise background execution or an automatic future wakeup without host support.
- Make each handoff actionable: state what happens next and who acts. If user input is needed, ask the specific question with a recommendation and the available picker; make clear what answer or test feedback is needed. If the next step is already authorized and unblocked, continue it rather than ending with an offer to proceed. When stopping for a blocker or host limitation, name what is needed to resume and whether any workers are actually still active. If the requested work is complete, say so without inventing another required step. Keep STATE.md's next action and pending questions consistent with the conversation. This does not broaden read-only help/status or planning-only authorization.

## Local helpers

Use an available Python 3.10+ interpreter with this skill's `scripts/bsg.py`:

```text
python <skill>/scripts/bsg.py init --root <project> --name <name>
python <skill>/scripts/bsg.py attach --root <existing-BSG-project>
python <skill>/scripts/bsg.py slice --root <project> --title <deliverable>
python <skill>/scripts/bsg.py help --root <project>
python <skill>/scripts/bsg.py status --root <project>
python <skill>/scripts/bsg.py validate --root <project>
```

Init refuses an existing planning folder. Slice creation allocates a new stable ID. Help/status are read-only and validate the ledger before recommending work. The helper never launches agents, marks tests passed, or grants acceptance. If Python is unavailable, maintain the same records directly and disclose that automated record validation was unavailable.
