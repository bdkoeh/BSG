# Durable project records

All paths below are relative to the target project, not the skill folder. The agent maintains these; the user works through conversation. Initialize using the helper when possible. Never overwrite an existing planning system or reset records on `start`.

## Layout and ownership

The root `AGENTS.md` provides a short handoff for future chats in either host. `init` creates it or appends the marked block from [project-agents.md](../assets/project-agents.md), preserving existing content. Claude Code ignores `AGENTS.md` once a project has a `CLAUDE.md`, `.claude/CLAUDE.md`, or `CLAUDE.local.md`, so in that case the helper adds the same block to the root `CLAUDE.md` too. For an older BSG project, use `bsg.py attach --root <project>` on start/resume; never rerun init over existing records. An existing marked BSG block is preserved, including user customizations. Malformed markers in any target require reconciliation before anything is written. If Python is unavailable, append the same template once manually to the same files. Do not change other instructions or store live progress in this block; progress belongs in `.planning`. Do not modify these files during read-only help/status.

## Create records when needed

`init` creates PROJECT.md, state.json, generated ROADMAP.md/STATE.md views, and the instruction handoff. Research/discovery directories can remain empty until useful findings exist. `slice` allocates the stable ID and directory and creates only CONTEXT.md. Write other documents directly when their stage needs them; do not fill future files with placeholders.

| Record | Create or populate when |
| --- | --- |
| PROJECT.md | Initialization; capture intent, boundaries, effort, involvement and execution scope |
| DECISIONS.md | First indexed decision; retain rationale, provenance and superseded decisions |
| BACKLOG.md | First deferred item worth retaining |
| CODEBASE.md, discovery/, research/ | Relevant inspection, proposals, experiments or research produce useful context |
| slices/001-name/CONTEXT.md | Slice creation; populate before `discussed` |
| PLAN.md | Planning begins; populate before `ready` or execution |
| SUMMARY.md | First meaningful implementation progress or implementation handoff; populate before `implemented` |
| VERIFICATION.md | First check result or human feedback; populate before `verified`, `awaiting_feedback` or `complete` |

Evidence referenced by an executed check or accepted feedback must already exist, regardless of the slice's status. A failed early check therefore needs its evidence immediately. A blocked or paused slice keeps all existing documents and records partial progress in the relevant report or handoff notes. Never delete older files merely because an earlier stage would not create them today.

The lead owns shared records and state.json; workers own assigned slice reports. state.json is authoritative for indexed lifecycle metadata. Markdown holds reasoning, evidence and user provenance. Actual code and fresh verification take precedence over stale records. Update these after consequential discussions, dispatch, meaningful progress, blockers, feedback and before a pause/handoff; store concise decisions, not transcripts.

## Generated summaries and compatibility

After updating the index, run `bsg.py sync --root <project>`. It validates records, then refreshes only the `<!-- BSG:GENERATED:BEGIN -->` / `<!-- BSG:GENERATED:END -->` sections of ROADMAP.md and STATE.md. Roadmap rows derive IDs, titles, statuses, dependencies and revisions from state.json. State rows derive checks (including failures and stale results), human acceptance, recorded agents and blockers, plus a suggested next step. Do not hand-edit these sections or copy their fields into other status tables.

Keep provisional roadmap ideas, checkpoint rationale, current conversational focus, unanswered questions, execution-authorization references and resume details outside the generated sections. These notes supply context the index does not contain. A suggested next step never supplies build authorization, and a recorded agent handle never proves a live worker.

Existing schema-version-1 projects remain supported. On the first sync, files without generated markers keep their original bytes and receive an appended generated section; reconcile old status prose into concise notes or historical context rather than maintaining two current status lists. Existing marked sections are replaced without changing surrounding notes. Malformed markers or unsafe output paths stop the sync before either file is written. Sync does not change the index, grant acceptance, or run during read-only help/status. Those commands read the index directly, so a stale or absent generated file cannot determine their recommendation.

If Python is unavailable, maintain the same derived sections manually from the index and disclose that automated validation/sync was unavailable. Do not require ROADMAP.md or STATE.md to exist before inspecting an older or partially restored project; regenerate them on an authorized write path. PROJECT.md remains required, and DECISIONS.md is required when the index contains decisions.

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

ROADMAP notes: proposed outcomes; testing checkpoints; what feedback teaches us; whether unrelated work may proceed. Indexed fields are generated.

CONTEXT: intent; user examples; agreed decisions with revisions; assumptions; open questions; scope boundaries.

PLAN: outcome; dependencies; decisions; owned paths; implementation steps; acceptance scenarios; required checks; human gate; execution authorization; risks/experiments.

SUMMARY: implemented; remaining; changed files; decision/slice revisions used; blockers; handoff.

VERIFICATION: checked code identity/revision; procedure; expected/observed; result; evidence; limitations; human feedback; historical checks invalidated by changes.

The helper validates bookkeeping consistency, not truth. The lead must verify code and evidence contents before completion. If records conflict, show the discrepancy and reconcile; do not silently recommend new work from an invalid ledger.

A scaffolded CONTEXT.md is a placeholder; create other records only when needed. `discussed` requires populated slice context; `ready` and subsequent execution states also require a populated plan. The helper rejects empty/headings-only scaffolds in those states, but cannot establish whether the content reflects actual agreement. The lead checks that provenance, unresolved choices, and research links support the transition. Keep proposed approaches in discovery/research until context is captured; label incomplete plans as drafts and do not treat them as executable.
