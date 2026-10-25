# BSG behavioral review

This is an independent simulated behavioral evaluation and static helper review, not a live end-to-end run. Reviewed `skills/bsg/SKILL.md`, the commands, delivery, records, and Codex references, and `scripts/bsg.py`. No implementation or installation files were changed. No network or external actions were taken. After the Windows Python alias failed, the bundled Python runtime ran four in-memory probes successfully. These exercised validate/recommend with synthetic dictionaries and stubbed file-existence checks; they are not filesystem integration tests. The outputs confirmed the scenario 1 recommendation and the three gaps below.

## 1. Help with failed verification and a dependent ready slice

Input: slice 1 is implemented with failed required checks; slice 2 is ready but depends on 1; slice 3 is in discovery.

Actions: read state.json, PROJECT.md, STATE.md, relevant slice evidence, and the command reference. Run helper help if a working interpreter is available. Reconcile its recommendation with the records without changing files or starting agents. Failed checks on an implemented slice are valid unfinished state, not grounds to mark it verified. The helper's recommendation loop selects verification of slice 1 before considering ready slice 2. Dependency filtering also prevents recommending build 2 while 1 is unfinished.

User-facing response: show the command menu and recommend verifying slice 1, explaining that its failed checks need investigation and repair before slice 2 can start. Say slice 3's discussion can proceed independently if its scope and checkpoint rules permit. Help itself does not start repairs or discovery. Display the failure explicitly rather than relying only on a checks-passed count.

Assessment: the core handles this scenario coherently. The helper only returns one recommendation and does not identify independent discovery; the lead must supply that context, as the command reference requires.

## 2. A proposed preview changes an automatic import

Input: an active worker is implementing automatic import under D-001 revision 1. The user first asks, “what if we preview imports before saving?” and later explicitly chooses preview.

Actions on exploration: treat the initial statement as a proposal, discuss the changed experience and tradeoffs, and record it separately from agreed scope. Do not silently overwrite D-001 or claim that exploratory wording authorized the change. Existing authorized work can continue subject to its established gates; the lead can explain that the proposed direction would affect the current import work.

Actions on explicit choice: identify all slices referencing D-001 and inspect indirect code/test impacts. Stop affected dispatch, notify or interrupt the affected worker using live tools, reconcile any writes already in flight, then record the newly agreed D-001 revision 2 with its source. Increment affected slice revisions, update plans and acceptance scenarios, and invalidate affected test evidence and human acceptance. Preserve unrelated work and historical results. Rebrief a worker against the new revisions and reject automatic integration of results based on revision 1. Verify preview-before-save behavior against real artifacts.

User-facing response: “Preview is now the agreed import flow. I’m updating the current work so users can review the import before it is saved. The earlier automatic-import checks need to be rerun against that behavior.” Ask only consequential unresolved questions, not for repeat permission to perform the already agreed change.

Assessment: clear distinction between exploration and commitment, with an explicit stale-result defense. No concrete contradiction found in this scenario. Decision references are correctly described as aids rather than proof of all affected work.

## 3. Resume with low involvement, deep effort, a pending gate, and old handles

Actions: read current records and pending questions, inspect the actual files and verification identities, and query live worker tools rather than treating yesterday's handles as proof of live agents. Reconcile unavailable handles in the shared records and preserve partial work. Check decision revisions, changed code, stale checks, execution authorization, and the checkpoint's permission for independent work. Do not blindly respawn every old assignment or redo settled discovery.

Low human involvement does not waive the pending gate. Deep effort permits more thorough agent investigation where justified; it neither creates acceptance nor expands execution authorization. “Resume” continues previously authorized work after reconciliation, but does not constitute a response to the unresolved acceptance question. Resume independent authorized work only if the checkpoint explicitly permits it. Otherwise prepare the usable preview and concise accept/fix/rethink choices, save the handoff, and wait. Disclose host persistence limitations if relevant without promising background execution.

User-facing response: “I’ve recovered the current files and checks. The earlier workers are no longer available. This milestone still needs your review: [preview and short things to try]. [Describe independent work only if the checkpoint permits it.]” This wording assumes the live-tool check has actually established unavailability; otherwise describe the uncertainty.

Assessment: the written workflow protects the gate and distinguishes effort from involvement. It does not require repeating settled preference questions.

## 4. Plan 5 without execution authorization

Actions: resolve stable slice ID 5 and read its context, relevant decisions, code, dependencies, and ownership. Discuss or investigate material unknowns. Prepare its executable plan, acceptance scenarios, required checks, human checkpoint, and explicitly absent execution authorization. Keep focus on 5 even if a different slice is ready. Planning/research delegation can be used when useful, but no implementation worker may be dispatched under the planning request alone.

User-facing response: summarize the intended outcome, boundaries, dependencies, checks, and any unresolved decision in ordinary language. State that slice 5 is planned and awaits build authorization if ready; if a prerequisite is unfinished, make that dependency visible. Do not require the user to read plan files. Do not begin other slices.

Assessment: both the command reference and delivery reference explicitly resolve the authorization boundary. No concrete contradiction found.

## Concrete helper gaps

1. **Required checks can be absent during execution.** `validate()` only requires a nonempty set of required checks for `verified`, `awaiting_feedback`, and `complete`. A `building` or `implemented` slice with `checks: []` otherwise passes this part of validation. The records reference requires checks to be listed before implementation. This allows the ledger to lose that guardrail until late verification. Enforce a meaningful required-check entry for execution states, while retaining pending/fail/stale as legitimate unfinished results. The helper cannot assess whether the check is meaningful, but can enforce its presence.

2. **Nonpassing check metadata is not validated against the declared schema.** `validate()` checks revision freshness and evidence containment only when result is `pass`. A failed check can therefore have a noninteger revision or an absolute/traversal/nonexistent evidence reference without a bookkeeping error. The records schema requires a positive integer or null revision and a project-relative path or null evidence. Validate types and path shape for every result; permit null for unrun checks and historical revisions for stale results. This is a recovery/evidence-quality issue, not a route around the final passing-check guard.

3. **Per-slice pause priority differs from the documented recommendation order.** `recommend()` handles a project-wide pause first, but considers a slice with status `paused` only after ready/discussed/discovery/outline slices. With global `paused: false`, slice 1 paused, and slice 2 ready, it recommends building 2 instead of first reconciling the pause. `commands.md` puts a requested pause ahead of ready work. Independent work can legitimately be allowed, but the helper has no machine-readable checkpoint/authorization field establishing that allowance. Clarify the documented priority to distinguish a global pause from a scoped pause, and require the lead to confirm that independent work is allowed before acting. A scoped pause should not suppress explicitly allowed independent work. This recommendation does not itself dispatch work, and the lead's required reconciliation limits the risk.

## Limits and non-findings

The helper is deliberately not an executor or acceptance authority. Its inability to inspect test truth, human feedback authenticity, authorization prose, or live workers is not itself a contradiction: the skill assigns those duties to the lead and explicitly disclaims product correctness from validation. Passing validation must never be presented as successful product verification. These scenarios support the intended behavior on paper; they do not demonstrate an installed invocation, real worker interruption, concurrent file handling, or successful recovery across host sessions.
