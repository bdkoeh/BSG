# Durable project records

All paths below are relative to the target project, not the skill folder. The agent maintains these; the user works through conversation. Initialize using the helper when possible. Never overwrite an existing planning system or reset records on `start`.

## Layout and ownership

The root `AGENTS.md` provides a short handoff for future chats in either host. `init` creates it or appends the marked block from [project-agents.md](../assets/project-agents.md), preserving existing content. Claude Code ignores `AGENTS.md` once a project has a `CLAUDE.md`, `.claude/CLAUDE.md`, or `CLAUDE.local.md`, so in that case the helper adds the same block to the root `CLAUDE.md` too. For an older BSG project, use `bsg.py attach --root <project>` on start/resume; never rerun init over existing records. An existing marked BSG block is preserved, including user customizations. Malformed markers in any target require reconciliation before anything is written. If Python is unavailable, append the same template once manually to the same files. Do not change other instructions or store live progress in this block; progress belongs in `.planning`. Do not modify these files during read-only help/status.

```text
.planning/
  PROJECT.md          Product intent, boundaries, effort, involvement, authorization
  ROADMAP.md          Outcomes, dependencies and human testing checkpoints
  DECISIONS.md        Stable IDs, revisions, rationale and source of agreement
  STATE.md            Short current handoff: live work, questions, blockers, next action
  state.json          Machine-readable index of slices, decisions and evidence
  BACKLOG.md          Deferred ideas and larger feedback items
  CODEBASE.md         Optional focused inspection with real paths and freshness
  discovery/          Proposals, experiments and findings outside committed work
  research/           Sources and findings worth retaining
  slices/001-name/
    CONTEXT.md        Intent, examples and discussion decisions
    PLAN.md           Approach, dependencies, ownership, acceptance and checkpoint
    SUMMARY.md        Implemented changes, remaining work and handoff
    VERIFICATION.md   Procedures, results, code identity and limitations
```

The lead owns shared records and state.json. Workers own assigned slice reports. state.json is authoritative for indexed lifecycle metadata; Markdown contains the actual reasoning and evidence. ROADMAP/STATE are readable summaries reconciled with the index, not separate independent status stores. Actual code and fresh verification take precedence over stale records.

Update records after consequential discussions, dispatch, meaningful progress, blocker discovery, verification, feedback, and before a pause/handoff. This is part of the work. Store concise decisions and evidence, not entire transcripts. Preserve past decisions when superseded.

## Index format (schema version 1)

Top-level fields: `schema_version: 1`, `project` (name), `paused` (boolean), `agent_effort` (null or lean/balanced/deep), `human_involvement` (null or descriptive string), `decisions` (array), `slices` (array).

Decision: `id` such as D-001, positive integer `revision`, and `status` agreed/proposed/superseded. Rationale and provenance belong in DECISIONS.md. Only agreed decision revisions may authorize execution.

Slice fields:

```json
{
  "id": 1,
  "title": "Import a real statement",
  "path": ".planning/slices/001-import-a-real-statement",
  "status": "outline",
  "revision": 1,
  "depends_on": [],
  "decision_refs": {},
  "agent": null,
  "blocker": null,
  "checks": [],
  "acceptance": {"required": true, "status": "pending", "revision": null, "evidence": null}
}
```

Statuses: outline, discovery, discussed, ready, building, implemented, verified, awaiting_feedback, complete, blocked, paused. `depends_on` means completion prerequisites, including any human gate. More granular API contracts may be described in PLAN.md; do not mark unfinished dependencies complete to force parallelism. Model disjoint work as independent slices where appropriate.

`decision_refs` maps decision IDs to the exact revision used. `agent` records a live handle only when assigned; verify with host tools on resume. `blocker` explains an actual blocker and its resolution path. Pause state may store additional resume details in STATE.md; never lose them by resetting statuses.

Check object: `id`, `required` boolean, `result` pending/pass/fail/stale, `revision` positive integer or null, `evidence` project-relative file path or null. Evidence files describe the actual procedure and result. Required checks must be listed before implementation and cannot be deleted or changed to optional just to pass completion. Include at least one meaningful required check for a completed slice, which may be a manual examination for a non-code deliverable.

Acceptance statuses: pending/accepted/not_required. `required: true` needs accepted feedback at the current slice revision, with evidence linking to a file recording the user's actual response. Never fabricate consent. If acceptance is not required, use status not_required and record why in PLAN.md.

Increment the slice revision when agreed behavior or implementation changes invalidate results. Rerun affected checks; retain historical evidence in Markdown. Carry forward unaffected evidence to the new revision only after explicitly documenting why it remains valid. Acceptance affected by a change returns to pending; harmless changes can preserve acceptance with rationale.

## Templates

PROJECT: problem; users; desired experience; first release; out of scope; constraints; agent effort; human involvement; execution authorization; frontend direction.

ROADMAP: ID; outcome; dependency IDs; readiness; testing checkpoint; what feedback teaches us; whether unrelated work may proceed.

CONTEXT: intent; user examples; agreed decisions with revisions; assumptions; open questions; scope boundaries.

PLAN: outcome; dependencies; decisions; owned paths; implementation steps; acceptance scenarios; required checks; human gate; execution authorization; risks/experiments.

SUMMARY: implemented; remaining; changed files; decision/slice revisions used; blockers; handoff.

VERIFICATION: checked code identity/revision; procedure; expected/observed; result; evidence; limitations; human feedback; historical checks invalidated by changes.

The helper validates bookkeeping consistency, not truth. The lead must verify code and evidence contents before completion. If records conflict, show the discrepancy and reconcile; do not silently recommend new work from an invalid ledger.

Scaffolded documents are placeholders. `discussed` requires populated slice context; `ready` and subsequent execution states also require a populated plan. The helper rejects empty/headings-only scaffolds in those states, but cannot establish whether the content reflects actual agreement. The lead checks that provenance, unresolved choices, and research links support the transition. Keep proposed approaches in discovery/research until context is captured; label incomplete plans as drafts and do not treat them as executable.
