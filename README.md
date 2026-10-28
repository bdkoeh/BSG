# BSG — Brief, Slice, Go

A conversational development framework for Claude Code and Codex. Brief the idea, cut it into slices, and go build one when it is ready. Shape the product with your lead agent while subagents build the parts that are ready. Keep decisions, plans, progress, and verification in the project folder.

BSG is designed around my workflow: adaptive picker interviews, continuous discovery, experiments for uncertain questions, deliberate checkpoints, and inexpensive changes of direction.

## Start here

BSG is one skill, `skills/bsg`, that works in either host. Pick the install path for your host; nothing else differs. A project initialized in one host can be continued in the other.

### Install through conversation

Paste this into Claude Code or Codex. The agent figures out which host it is and installs accordingly:

```text
Install BSG from https://github.com/bdkoeh/BSG for use across my projects.
If you are Claude Code: run `claude plugin marketplace add bdkoeh/BSG` then
`claude plugin install bsg@bsg`; if plugins are unavailable, copy the complete
skills/bsg folder into ~/.claude/skills/bsg instead.
If you are Codex: use your skill-installer with --repo bdkoeh/BSG --path skills/bsg
and its personal destination.
Preserve existing customized skills. Then tell me how to start BSG.
```

The agent handles downloading and installing using its own tools. You do not need to clone the repository or run terminal commands yourself. It may ask permission to download files or write to your personal skills directory.

For installation into just one project, replace “for use across my projects” with “into this project only”, and the agent copies `skills/bsg` into `.claude/skills` (Claude Code) or `.agents/skills` (Codex). See [installation details](docs/INSTALLATION.md) for every option and the fallback steps.

### Manual installation

**Claude Code**, from any folder:

```bash
claude plugin marketplace add bdkoeh/BSG
```

```bash
claude plugin install bsg@bsg
```

**Either host**, into one existing project. Clone or download this repository, then run from its folder:

```powershell
python scripts/install.py --project C:\path\to\your-project
```

The installer detects whether the project already has a `.claude` or `.agents` folder and installs the skill there; a project with neither gets both, so it works wherever you open it. Use `--host claude`, `--host codex`, or `--host both` to choose explicitly. It refuses to replace different existing files. Python 3.10+ is required for this installer and the optional local helpers; the conversational skill operates without Python.

### Invoke BSG

| Host | Start | Help |
| --- | --- | --- |
| Claude Code | `/bsg start` with your idea | `/bsg help` |
| Codex | `$bsg start` with your idea | `$bsg help` |

Natural language works in both: “Use BSG to plan the next slice.” If the skill does not appear, start a new chat or restart the app. BSG does not override either app's own `/help`.

## Commands

| Command | Purpose |
| --- | --- |
| BSG start | Shape a new project or substantial feature |
| BSG help | Show these commands and recommend the next step |
| BSG status | Show progress, active work, and pending decisions |
| BSG pause | Pause work and preserve a handoff |
| BSG resume | Reconcile records and continue authorized progress |

Discussion, research, planning, implementation, and verification happen through conversation. You can focus on a numbered slice naturally. BSG still asks before starting implementation unless you have explicitly authorized that scope or delegated build starts.

## How a project runs

1. Establish a shared high-level product brief: users, problem, desired outcome, broad journey, and first-version boundaries. Choose agent effort separately from human involvement.
2. Propose a provisional map of named, testable slices before detailed questioning. Refine it together and choose which slice to deepen; later slices can stay rough.
3. Discuss and plan a ready slice. Test a consequential assumption when evidence would help.
4. Delegate implementation while the lead discusses subsequent slices with you.
5. Verify actual behavior, collect agreed feedback, and update affected work.
6. Finish the frontend after core behavior works, using the aesthetic direction discussed upfront.

The lead guides each slice through discussion, captured context, research, and planning automatically. You can use commands to steer, but do not need to run each stage manually. Prior answers carry forward; consequential gaps prompt focused follow-ups. Empty document templates do not count as completed discussion or a ready plan.

When a slice is ready, BSG summarizes its approach and offers **start implementing** or **keep discussing**. Picking the next slice does not start its build. You can explicitly authorize several slices or delegate future build starts; otherwise, BSG waits for your build decision, including for functional previews.

You work through conversation, not document approvals. The agent starts with a project brief and an index in `.planning/`. Each new slice gets a context file; plans, implementation summaries, and verification records appear when work reaches those stages. Decisions, backlog items, and research notes are recorded when needed.

The index supplies the status fields in `ROADMAP.md` and `STATE.md`. Run `python <skill>/scripts/bsg.py sync --root <project>` after index changes to refresh their generated sections while preserving surrounding notes. Existing planning files remain compatible and are preserved. Help and status read the index without writing files.

Initialization also creates or extends the project's root `AGENTS.md` with a short BSG handoff so future chats know which workflow and records to use. Both hosts read that file. If the project already has a `CLAUDE.md`, the same block is added there too, because Claude Code skips `AGENTS.md` when a `CLAUDE.md` exists. Existing instructions are preserved. For a project created with an older BSG version, use BSG resume with the updated skill to add the handoff without resetting plans.

## First-version boundaries

Slices are named for testable capabilities, such as “Reserve available equipment.” Discovery examples inform their requirements; they do not automatically become delivery boundaries. BSG reviews growing plans for useful intermediate checkpoints, carries prior decisions into the resulting slices, and asks before starting the agreed build scope.

- Skills guide the agent; they are not a background scheduler or an enforcement engine. Parallelism, model overrides, interactive pickers, and continued activity while awaiting input depend on the host's available tools. BSG discloses a sequential fallback and never claims workers are running without checking.
- The lead cannot switch its own model through a skill. Select the lead model in the app if desired. Workers use the host's available model options; the routing policy is configurable guidance, not a promised token saving.
- Local status checks validate recorded evidence and dependencies. They cannot prove software correctness; the lead must inspect code, run relevant checks, and reconcile actual worker results.
- No automatic publishing, deployments, external messages, or global configuration changes are implied by project approval.
- The workflow records are host-neutral. Host-specific behavior lives in one adapter file per host inside the skill.

## Repository

`skills/bsg/` contains the single installable skill, with `references/codex.md` and `references/claude-code.md` as the host adapters. `.claude-plugin/` makes the repository installable as a Claude Code plugin marketplace. `scripts/install.py` installs the skill into a project for either host. `tests/` checks helper invariants. `docs/` explains design and behavioral validation.

BSG's own development records in the root `.planning/` folder are local and ignored by Git. They are not part of the public distribution. Projects using BSG create their own `.planning/` records; those projects choose whether to version them.

Run checks with `python -m unittest discover -s tests -v`.

## License

MIT. See [LICENSE](LICENSE).

## Inspiration

- [GSD](https://github.com/gsd-build/get-shit-done): questioning, phase context, scoped execution, progress, codebase mapping, verification.
- [Shape Up](https://basecamp.com/shapeup/3.4-chapter-13): distinguish unresolved questions from understood execution.
- [Continuous discovery and delivery](https://www.svpg.com/dual-track-agile/): learn while delivering.
- [OpenSpec](https://github.com/Fission-AI/OpenSpec): distinguish proposed changes from current behavior.
- [Codex skill discovery](https://learn.chatgpt.com/docs/build-skills) and [Claude Code skills](https://code.claude.com/docs/en/skills): local installation and invocation.
