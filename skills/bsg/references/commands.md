# Commands and navigation

BSG is one registered skill with five public commands. Use natural language such as “BSG start”, mention `$bsg` followed by an action in Codex, or run `/bsg` followed by an action in Claude Code. Skill menus are host-dependent; do not claim shortcuts the host did not register. Preserve explicit user focus.

| Action | Behavior |
| --- | --- |
| start | Shape a new project or feature. Inspect existing BSG records first; offer resume or a new scope rather than reinitialize. |
| status | Show a compact table of slices, discovery, live worker state, pending checks/feedback, blockers, and next actions. Compare recorded agent handles with live tools; old handles are not proof of live work. |
| help | Show the command menu and one recommended next action with a reason. Include relevant independent work that can proceed. Read-only; do not launch work or write records. |
| pause [ID] | Stop new dispatch for the scope, ask workers to checkpoint or interrupt if needed, verify their status, preserve partial work and pending evidence. “Pause requested” until confirmed; do not claim stopped workers without evidence. |
| resume | Inspect actual files/code, live workers, changed decisions, stale checks, and user gates. Reconcile documents first, then continue previously authorized work. Do not duplicate still-running assignments or bypass unanswered human gates. |

Discussion, research, planning, implementation, and verification are internal workflow stages guided through conversation, not additional commands. A request such as “let’s explore slice 2” changes focus; “implement the prepared slice” can authorize that scope. Understand legacy command wording as natural-language intent without advertising or requiring the removed command skills.

## Next-step recommendation

For a ready slice without build authorization, recommend the start-building choice described in delivery.md: summarize the approach and offer start implementing / start it while shaping the next slice / keep discussing, once per readiness. A helper recommendation to build expresses readiness, not permission. Read-only status/help may report “ready; awaiting your build decision” but must not dispatch workers.

The lead navigates the discuss/context/research/plan sequence automatically during an authorized workflow. Explicit commands choose focus and scope; they do not bypass missing prerequisites. “Continue” means the next unmet step in the current scope. Before recommending plan/build, inspect the relevant context and plan contents, not only their filenames or indexed status. If records overstate progress, explain the gap and recover existing answers before asking targeted follow-ups.

The helper supplies a conservative suggestion from records; the lead reconciles it with live facts. Prioritize: inconsistent/stale records; global pause; actionable human checkpoint or blocker; verification of implemented work; ready authorized work; discuss/plan the next useful slice; discovery if no route exists. A per-slice pause does not suppress independent work already allowed to continue; surface the paused slice alongside the recommendation. Consider dependencies and explicit focus; never recommend building a blocked slice. At project completion offer the next user-requested activity, not invented work.

Status example: `5 · Categorization | discovery | testing correction flow`. Prefer concrete facts to completion percentages. Show “implemented; verification pending” instead of “done” for an agent that merely returned.
