# BSG — Brief, Slice, Go

**Give your coding agents a clear understanding of what to build before they start building.** BSG guides you through detailed conversations that turn an idea into shared context, explicit decisions, and actionable plans. It asks focused questions, explores tradeoffs, and investigates uncertainty so implementation starts with more than a prompt and a few assumptions.

Then planning and delivery overlap. Your lead agent coordinates subagents building and verifying approved slices while you work through the details of what comes next. You establish the overall direction upfront, deepen each slice before it’s built, and keep room to adapt as you learn.

Built for Claude Code and Codex.

## Start here

BSG is one skill, `skills/bsg`, that works in either host. Pick the install path for your host. The workflow and records are shared; available interaction and delegation tools differ by host. A project initialized in one host can be continued in the other.

### Install through conversation

Paste this into Claude Code or Codex. The agent figures out which host it is and installs accordingly:

```text
Install BSG from https://github.com/bdkoeh/BSG for use across my projects.
For a personal install in Claude Code: run `claude plugin marketplace add bdkoeh/BSG` then
`claude plugin install bsg@bsg`; if plugins are unavailable, copy the complete
skills/bsg folder into ~/.claude/skills/bsg instead.
For a personal install in Codex: use $skill-installer to install skills/bsg
from bdkoeh/BSG on main into its personal destination.
For a project-only install in either host: instead copy the complete skills/bsg
folder into this project's .claude/skills (Claude Code) or .agents/skills (Codex).
Do not perform a personal install when I request project-only installation.
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

**Codex**, across projects: ask `$skill-installer` to install `skills/bsg` from `bdkoeh/BSG`. For a manual copy, put the complete folder at `~/.agents/skills/bsg`, the personal location in the [Codex skills documentation](https://learn.chatgpt.com/docs/build-skills). The bundled installer tested here instead defaults to `$CODEX_HOME/skills` (usually `~/.codex/skills`); that location was also discovered successfully. Use one personal location to avoid duplicate entries.

**Either host**, into one existing project. Clone or download this repository, then run from its folder:

```powershell
python scripts/install.py --project C:\path\to\your-project
```

The installer detects whether the project already has a `.claude` or `.agents` folder and installs the skill there; a project with neither gets both, so it works wherever you open it. Use `--host claude`, `--host codex`, or `--host both` to choose explicitly. It refuses to replace different existing files. Python 3.10+ is required for this installer and the optional local helpers; the conversational skill operates without Python.

### Invoke BSG

| Host | Start | Help |
| --- | --- | --- |
| Claude Code plugin | `/bsg:bsg start` with your idea | `/bsg:bsg help` |
| Claude Code copied skill | `/bsg start` with your idea | `/bsg help` |
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

The index supplies the status fields in `ROADMAP.md` and `STATE.md`. The agent runs `python <skill>/scripts/bsg.py sync --root <project>` after index changes to refresh their generated sections while preserving surrounding notes. You can run it manually, but do not need to remember periodic syncs. Existing planning files remain compatible and are preserved. Help and status read the index without writing files.

Initialization creates or extends the project's root `AGENTS.md` with a short BSG handoff. If the project has `CLAUDE.md`, `.claude/CLAUDE.md`, or `CLAUDE.local.md`, the helper also adds the block to root `CLAUDE.md`. Existing instructions are preserved. Codex reads `AGENTS.md`; Claude Code's support depends on its version and instruction settings, and ancestor Claude instruction files can suppress it. See [installation details](docs/INSTALLATION.md#project-instruction-files) if the handoff is not loaded. For an older BSG project, use BSG resume with the updated skill to add the handoff without resetting plans.

## First-version boundaries

Slices are named for testable capabilities, such as “Reserve available equipment.” Discovery examples inform their requirements; they do not automatically become delivery boundaries. BSG reviews growing plans for useful intermediate checkpoints, carries prior decisions into the resulting slices, and asks before starting the agreed build scope.

- Skills guide the agent; they are not a background scheduler or an enforcement engine. Parallelism, model overrides, interactive pickers, and continued activity while awaiting input depend on the host's available tools. BSG discloses a sequential fallback and never claims workers are running without checking.
- The lead cannot switch its own model through a skill. Select the lead model in the app if desired. Workers use the host's available model options; the routing policy is configurable guidance, not a promised token saving.
- Local status checks validate recorded evidence and dependencies. They cannot prove software correctness; the lead must inspect code, run relevant checks, and reconcile actual worker results.
- No automatic publishing, deployments, external messages, or global configuration changes are implied by project approval.
- The workflow records are host-neutral. Host-specific behavior lives in one adapter file per host inside the skill.

## Repository

`skills/bsg/` contains the single installable skill, with `references/codex.md` and `references/claude-code.md` as the host adapters. `.claude-plugin/` makes the repository installable as a Claude Code plugin marketplace. `scripts/install.py` installs the skill into a project for either host. `tests/` checks helper invariants. `docs/` explains design and behavioral validation.

BSG's own development records in the root `.planning/` folder are local and ignored by Git. They are absent from the current tracked tree and skill package; older Git history still contains them. Projects using BSG create their own `.planning/` records; those projects choose whether to version them.

Run checks with `python -m unittest discover -s tests -v`.

## License

MIT. See [LICENSE](LICENSE).

## Inspiration

- [GSD](https://github.com/gsd-build/get-shit-done): questioning, phase context, scoped execution, progress, codebase mapping, verification.
- [Shape Up](https://basecamp.com/shapeup/3.4-chapter-13): distinguish unresolved questions from understood execution.
- [Continuous discovery and delivery](https://www.svpg.com/dual-track-agile/): learn while delivering.
- [OpenSpec](https://github.com/Fission-AI/OpenSpec): distinguish proposed changes from current behavior.
- [Codex skill discovery](https://learn.chatgpt.com/docs/build-skills) and [Claude Code skills](https://code.claude.com/docs/en/skills): local installation and invocation.
