# Shape testable delivery slices

Use this when outlining a roadmap, preparing a plan, or revisiting a growing plan before build approval. The lead owns decomposition; users should not have to request it or repeat discovery for every slice.

## Examples explain behavior; slices deliver capabilities

A concrete story can span the whole product. Keep its people, sample objects, and dates in context and acceptance scenarios. Name a delivery slice for the capability or observable outcome it adds: “Reserve available equipment” or “Track pickup and return,” rather than “Alex's weekend drill.” A scenario title is appropriate only when that exact scenario is itself the requested deliverable, such as a bounded demonstration or experiment.

As soon as the high-level product is understood, propose a provisional roadmap of named outcomes, their dependencies, and what can be tested at each stopping point, before detailed per-slice questioning. Do not wait for exhaustive release rules or a finalized technical design. Mark uncertain scope as proposed and revise the map through discussion. Record accepted outcomes as stable slice IDs with outline status; only the next useful slices need detailed context and executable plans. Scope agreement is not build permission. Avoid keeping an entire release hidden inside one active slice while its other known outcomes exist only in prose.

## Scope review before a plan becomes ready

For each proposed slice, answer:

- What new capability will work at its end, and how can it be demonstrated or verified?
- What does it depend on, and what remains explicitly outside this slice?
- Could an earlier useful result be tested before the rest is built?
- Has it absorbed separate outcomes, prerequisites, deployment work, or finishing work merely because the example touches them?

If a plan contains several meaningful testing checkpoints, propose splitting it before asking to build. Explain the recommended boundaries conversationally. Prefer coherent end-to-end behavior over arbitrary frontend/backend/database divisions; include the layers needed to make that behavior real. A necessary technical foundation can be a slice when it has concrete verification and enables identified dependent work. Do not force every slice to be independently deployable, impose a fixed slice count, or split tiny work just to create more files.

Missing prerequisites must be explicitly scoped: either a small justified part of this deliverable or separately tracked dependencies. Do not silently absorb membership, catalog, booking, exception automation, notifications, and operations into a single “borrowing example” plan. For that example, listing equipment, reserving it, tracking return, and handling overdue loans may provide distinct testable outcomes; choose actual boundaries from the project rather than copying this list mechanically.

Keep a bounded integrated preview in one slice when its purpose, limits, and test are clear. A future full release does not need all details settled before a smaller approved slice can proceed. Define what is unavailable in earlier slices; do not quietly ship incomplete agreed behavior as complete.

## Repartition existing discussion without losing it

Reuse agreed decisions, research, and acceptance examples. Populate each affected slice's context with relevant answers and provenance, linking shared research rather than duplicating it. Ask only questions newly exposed by the split. Discuss the behavioral implications of a changed delivery boundary; never invent agreement.

Preserve stable IDs and history. For an unbuilt oversized slice, retain its ID for a coherent retained outcome, update its title and revision as needed, and allocate fresh IDs for extracted outcomes. Existing folder paths may remain stable even if titles improve. Record the old-to-new scope mapping and rationale, update dependency references and current roadmap/state summaries, and retain historical plans as clearly superseded material. Do not leave contradictory current summaries mixed with incremental updates.

Reassess readiness, checks, and execution authorization for every resulting slice; file copying does not confer discussed/ready status or authorize expanded work. If work has already started, follow delivery.md's change procedure before reassigning it. Never discard implementation, fabricate evidence, or renumber unrelated slices. Present build approval for the resulting concrete scope with the agreed human checkpoints.
