# Planning, orchestration, and verification

## Prepare a slice

Apply [slices.md](slices.md) before drafting a detailed plan and again before marking it ready. Check naming, testable outcome, prerequisites, and intermediate checkpoints. If the plan has grown into several deliverables, reconcile the split before the start-building choice; do not simply rename a giant plan.

Follow the per-slice discussion and research sequence in [discovery.md](discovery.md). Read the populated CONTEXT.md and linked findings before creating PLAN.md. If context is incomplete, recover known answers and close only the missing questions. Label incomplete plans as drafts and keep them out of `ready`; file existence is not stage completion.

Inspect the relevant code and current records. Define an outcome, boundaries, stable dependencies, decision IDs/revisions, acceptance scenarios, file ownership, implementation approach, verification checks, and any human checkpoint. Plan around the next useful thing to try, not an arbitrary task count. Resolve or experiment on consequential unknowns before committing dependent implementation. Do not create speculative infrastructure just to occupy agents.

Establish execution authorization from the conversation; `plan` alone only prepares. Record its scope. Once authorized, proceed through routine steps autonomously. Pause for changes to agreed behavior, scope, major technical choices, or human checkpoints unless already delegated. The user reviews through conversation, never mandatory file reading.

## Lead and worker contract

Before implementation, apply the start-building checkpoint below.

### Start-building checkpoint

By default, separate choosing a slice from authorizing its implementation. When context, research, and planning are sufficient, tell the user the slice is ready and briefly explain what it delivers, the approach, material assumptions or deferred questions, and how they will test it. Recommend the next step and offer an interactive choice with three shapes: “Start implementing this slice”, “Start it while we shape the next slice” (the build runs through workers while discussion continues), and “Keep discussing or refine the approach.” Wait for their choice before implementation or dispatching implementation workers. A functional preview is implementation too; do not bypass this checkpoint by calling it a preview.

Offer once per readiness. If the user keeps discussing, do not ask again; carry “slice N is ready, build not authorized” as a line in later recaps and let the user raise it, unless new readiness (a revised plan, a dependency completing) warrants a fresh offer.

Selecting what to tackle first, agreeing with the brief, delegating routine decisions, choosing low involvement, or saying “continue” during discovery/planning does not itself authorize a build. Keep a ready but unapproved slice marked `ready`; record “awaiting build decision” in the handoff notes outside STATE.md's generated section and pending execution authorization in PLAN.md. It is not `awaiting_feedback`, which is for testing an implemented result. Continue only separately authorized independent work while waiting.

An explicit build command or clear instruction to implement the prepared scope supplies authorization; do not ask again for the same approval. A user may also explicitly delegate future build starts for a defined scope. Record that delegation rather than inferring it from low involvement. Approval can cover multiple named slices; within that scope, proceed autonomously and pause only at agreed checkpoints or consequential changes. Approval to build one slice does not automatically authorize the next.

### Dispatch and reporting

Read the host adapter (codex.md or claude-code.md) for capabilities and model policy. The lead coordinates and stays available for discussion rather than doing all substantial implementation inline. Parallelize independent ready work within available slots; reserve capacity for necessary research/verification rather than maximizing occupancy.

Before spawn, record assignment ownership. Give each worker: objective, project/worktree path, slice ID and revision, decision IDs/revisions, relevant context and plan paths, acceptance examples, owned code/report paths, dependencies, limits, and expected evidence. Use focused context for routed models; do not blindly fork the entire chat. In a shared checkout assign disjoint files; serialize shared changes or use supported isolated worktrees. Do not overwrite other workers' or the user's changes.

Workers create SUMMARY.md when there is implementation progress to report, and VERIFICATION.md when checks or human feedback produce evidence; follow the lifecycle in [records.md](records.md). They report blockers and completed checks and return changed files, residual issues, decision revisions used, and evidence. They do not edit shared state.json, ROADMAP.md, DECISIONS.md, or STATE.md. Within one slice, assign separate report files if multiple workers participate; the lead consolidates them. The lead reconciles reports, updates state.json, and runs `sync` to refresh generated summaries. Keep only non-indexed handoff context in surrounding notes.

Include a compact handoff requirement in every worker assignment, including research and review. Workers return the outcome, verification results (passed, failed, and untested), decisions or blockers needing attention, and paths to evidence and changed files, with the revisions used. Keep routine progress messages equally focused; surface consequential blockers promptly. Save detailed research with source links, relevant debugging findings, and test evidence in assigned project reports instead of pasting long transcripts or logs into the lead's conversation. Preserve information needed to reproduce failures; do not omit uncertainty, failed checks, or material risks to make a summary shorter. If saving evidence is unavailable, report that limitation and include the essential evidence directly.

The lead reads the underlying artifacts when needed to assess a claim, resolve a blocker, or verify integration; a compact summary is not proof of correctness. Bring product impact, meaningful progress, and decisions to the user rather than forwarding worker transcripts. Expand the detail when the user requests it or a consequential issue needs explanation.

While workers run, continue the next useful user conversation. Use nonblocking questions and bounded waits where supported; never busy-poll or invent runtime persistence. If the host cannot keep work active while awaiting a reply, save a checkpoint and explain the limitation. No user-owned extra chat is needed for subagent work.

## Changes during execution

1. Establish whether a statement is exploration or an agreed change. Confirm consequential changes in the conversation.
2. Find affected slices via decision references and inspect code/tests for indirect impact. References aid judgment; they are not an exhaustive dependency proof.
3. Pause affected dispatch. Notify/interrupt affected workers and reconcile writes already underway. Leave independent authorized work running when allowed by checkpoints.
4. Revise the decision record, increment affected slice revisions, update plans, and mark affected checks and human acceptance stale/pending. Preserve old results as historical evidence.
5. Rebrief affected workers using new revisions. Check returning results against current revisions before integration; stale results require review/adaptation and fresh relevant checks.
6. Update the user with the product impact and any decision needed. Do not repeatedly ask permission for already authorized implementation details.

## Verification and human feedback

Verify against agreed examples and current code, not just the executor's description. Run required project checks and proportionate tests for the change. For consequential work, use a separate reviewer with the actual acceptance criteria and raw artifacts. Avoid tests that only repeat generated wording or excessive audits for simple edits. Check integration after combining parallel work.

For each required check record the command or manual procedure, result, checked revision, observed outcome, and a project-relative evidence path. Failed/unrun/stale checks remain visible. A source commit/hash or file digest in VERIFICATION.md ties evidence to real code. Record limitations; passing helper validation is not proof that the product works.

At a human gate provide a usable preview when available, short things to try, what automated checks established, and accept / fix / rethink options. Wait for explicit feedback on that gate. Independent work may continue only as agreed when defining the checkpoint. Fix small issues in scope immediately; defer larger changes to a separate milestone unless blocking, discussing consequential scope changes. Rerun affected checks; request another human test only if the change invalidates the feedback or the user requested it. Human acceptance requires recorded feedback tied to the relevant revision.

Before `complete`: inspect actual work; ensure dependencies are complete, required evidence passes at the current revision, applicable human gates are accepted, decision references are current, and records are reconciled. Never infer completion from a worker turn ending.

## Recovery, pause, resume

Workers surface blockers to the lead first. Investigate using a helper or stronger model where justified. Do not repeat the same failed approach indefinitely; after two unproductive attempts reassess assumptions and approach. Bring the user a concrete blocker when their product judgment, access, or an external change is required.

On pause, stop dispatch and request worker checkpoints, then confirm live states. Preserve partial work and describe any unconfirmed worker stop. On resume, reconcile the ledger against files, revision evidence, current decisions, and live handles before dispatching. An old handle does not mean an agent still exists. Restore the intended next action and pending questions; never redo settled discovery or duplicate active work. A BSG pause is not authorization to change unrelated host goals or automations.
