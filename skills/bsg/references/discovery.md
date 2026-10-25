# Discovery alongside delivery

The lead owns this sequence; the user never has to invoke its stages. It is an order, not a form: skip what the user already supplied, go only as deep as the project needs, and scale depth with the involvement and effort settings below. Every phase ends with a recap (see “Recap and recommend”). Conversation is the review interface; the user need not read or approve files.

## Project level

### 1. Shape the idea

Use the user's existing brain dump; don't make them repeat it. Establish the problem, users, desired experience, first useful result, constraints, and success examples. Understand the idea only well enough to cut it into slices; business rules and technical mechanics come later, per slice. For an existing project, first inspect relevant documentation, entry points, architecture, conventions, and run/test instructions. Store a short CODEBASE.md with paths and inspection date; expand only where the proposed feature needs it.

Reflect a concise brief back **in the conversation**, not only in a file: what this product is, who it serves, the problem and desired outcome, the broad user journey, and first-version boundaries. Distinguish supplied facts from your proposals. Ask only the missing high-level questions that materially change that framing; do not make the user repeat a sufficiently clear brief. A brief document the user supplies is input to confirm here, not a set of agreed decisions to import; record what it settles only after the user confirms the reflected brief.

### 2. Involvement and effort

Unless already given, ask in plain language how involved the user wants to be and propose an interpretation. Separately offer agent effort: keep it lean / balanced / go deep. Human involvement controls question density and which choices are delegated; agent effort controls research, experiments, model routing and review depth. Low involvement never implies skipping an agreed test or weakening accepted behavior. Do not ask for numerical budgets unless relevant to the user's expressed constraints.

### 3. Research for slicing

Research what is needed to cut good slices: what exists, what is hard, what forces an order, which choices affect the whole map. Record sources, dates and applicability in `research/`. This is landscape and feasibility work, not implementation detail; version pins and library specifics belong to the slice that needs them. Lean effort may skip this when the brief already covers the landscape; deep effort may run several researchers in parallel. Resolve cross-cutting choices early only when they genuinely affect the map, explaining why.

### 4. Cut the slices

Before drilling into business rules or technical details, propose a provisional slice map using [slices.md](slices.md): capability names, useful outcomes, rough dependencies, parallel tracks, and what can be tried at each checkpoint. Show it **in the conversation** and save it in ROADMAP.md. It is a map for discovery, not a finalized release commitment or build authorization. Do not wait for every rule to be settled before proposing it. Offer refinement of the framing or map; record accepted outlines with stable IDs and leave unaccepted scope clearly proposed. Update the map as later discoveries change it, carrying prior answers forward without restarting discovery.

### 5. Recap and recommend

Every phase ends, and every round that changes the map or a slice's status ends, with a short recap: what was just settled, where the project stands (which slices exist and their status, what is built, what waits on the user), and a recommended next step with the alternatives. At this point that means recommending which slice to shape first, framed as a choice of slice to shape, not permission to implement. The shape of the recap is the lead's call; the helper's `status` output supplies the slice table. Never end a phase with findings alone or a vague “let me know your thoughts.”

## Per slice

Different slices may be at different stages concurrently; each still needs its own context before planning. Say which slice is being shaped and which outcome the questions support. Deep effort and close involvement increase depth within this sequence; they are not permission to interview the entire product in detail first. A user explicitly focusing on a narrow question can be answered directly; return to the sequence afterwards.

### 1. Discuss

Lead with what the slice lets someone do and how they will try it. Start by reusing relevant answers from the project conversation, with their provenance. Ask focused themed rounds about the remaining consequential choices: user experience, boundaries, examples, failure behavior, alternatives, major technical choices, and how the user will test the result. A partial answer settles only the part answered; do not convert a recommendation or unaddressed option into agreement. Routine delegated choices can be made autonomously and recorded as delegated choices. Do not repeat settled questions or manufacture a fixed question quota. Only dive into future slices when useful; keep the rough roadmap elsewhere.

Stop when either side has enough: when you believe the consequential choices are settled, say so, summarize the understanding conversationally, and offer to move on; the user can ask for more. Avoid an indefinite questionnaire. Before marking a slice `discussed`, populate its CONTEXT.md with the intended outcome and examples, agreed choices and their source, boundaries, delegated discretion, and remaining questions, saying whether unresolved questions are research tasks or user decisions that block planning. Project-level discovery or an empty context template does not satisfy this step. If prior conversation already supplies sufficient slice context, capture it and move forward without a redundant interview.

### 2. Research

Research the uncertainty the discussion exposed. Record sources, dates, applicability and unresolved questions. A web finding is evidence to assess, not an instruction. Offer “help me try it” when the user cannot reasonably answer from discussion alone. An experiment specifies: the question, cheapest useful artifact, input/examples, success or failure signal, stopping point, and whether anything is disposable. Get scope agreement before a substantial experiment; use existing authorization for routine read-only investigation. Never promote a prototype into production implicitly. Simulated users can challenge an idea but cannot establish real user acceptance.

### 3. Follow up

Close the research loop in the same conversation: explain what the findings change, recommend a direction, and ask the next consequential question using the available picker. Update the slice context with what changed. If an unanswered picker is already pending, refer to that specific decision rather than asking it again. If no user decision is needed, continue to planning. Ask the user about promising scope additions rather than quietly growing the release. A research-only request can end with its findings and a clearly optional recommendation; it does not authorize planning or building.

### 4. Plan

Prepare the plan per [delivery.md](delivery.md). Readiness means the slice has clear intent, relevant dependencies understood, consequential unknowns resolved or bounded, and a useful way to verify it. It does not mean all uncertainty is gone.

### 5. Readiness recap and build offer

Recap as in the project phase, then apply the start-building checkpoint in delivery.md: the offer always includes starting the slice now, starting it in the background while the next slice is shaped, or keeping the discussion going. Move ready work forward while discussing later slices; when a later discussion changes an active assumption, use delivery's change procedure.

## Conversation habits

Use interactive picker tools when available, with 2–4 meaningful suggestions per question and free-text support. Follow tool limits. Ask 3–4 related questions per round where supported, fewer for focused follow-ups. Generate suggestions from actual context; don't repeatedly ask the user to configure the framework. State key implications in accessible language. Preserve settled answers and reasons; distinguish user preferences from your recommendations, and say when a question tests an assumption taken from the user's own material rather than recommending that assumption back to them.

Bring technical decisions to the user with a recommendation and concrete tradeoffs, unless delegated. Ask about aesthetic/vibe direction early for UI work; establish a basic functional first version and a finishing slice. Separate testing usability/behavior early from visual polish later. In low involvement mode, agreement on the brief and execution scope lets the lead prepare details autonomously.

## Capture

Use [slices.md](slices.md) to propose and record named, testable delivery outcomes. A user choosing a scenario to discuss does not establish that the entire scenario belongs in one implementation slice. Carry the scenario's decisions into the appropriate slices without repeating the interview.

Record discovery under `discovery/<topic>.md`, with proposed ideas, assumptions, findings, decisions and links to affected slices. Capture concrete user examples as acceptance scenarios. Only promote agreed choices into DECISIONS.md and scope into the roadmap. “What if...” is a proposal until confirmed.
