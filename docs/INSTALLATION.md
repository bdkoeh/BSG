# Installing BSG

BSG is one skill, with five public commands: start, help, status, pause, and resume. Discussion, research, planning, implementation and verification are guided through conversation. The same `skills/bsg` folder works in Claude Code and Codex; only where it is placed differs.

| Host | Personal (all projects) | One project | Invoke |
| --- | --- | --- | --- |
| Claude Code | plugin install, or `~/.claude/skills/bsg` | `<project>/.claude/skills/bsg` | `/bsg help` |
| Codex | skill-installer personal destination | `<project>/.agents/skills/bsg` | `$bsg help` |

The repository is public; no GitHub sign-in is needed to install.

## Claude Code

Preferred: install as a plugin, which keeps it updatable.

```bash
claude plugin marketplace add bdkoeh/BSG
```

```bash
claude plugin install bsg@bsg
```

Inside a session the same steps are `/plugin marketplace add bdkoeh/BSG` and `/plugin install bsg@bsg`. Without an SSH key for GitHub, set `CLAUDE_CODE_PLUGIN_PREFER_HTTPS=1` so the clone uses HTTPS. The skill then appears as `/bsg` (fully qualified `/bsg:bsg`).

Without plugins: copy the complete `skills/bsg` folder to `~/.claude/skills/bsg` for all projects, or to `<project>/.claude/skills/bsg` for one project. The local installer below does the per-project copy.

## Codex

Use the installation prompt in the [README](../README.md). The built-in skill-installer can install `skills/bsg` from `bdkoeh/BSG` on branch `main`, using `--repo bdkoeh/BSG --path skills/bsg`. Use its personal destination for all projects or an explicit `<project>/.agents/skills` destination for one project.

## Local installer, either host

Clone or download the repository and run `python scripts/install.py --project <existing-project-folder>` (Python 3.10+; quote paths containing spaces). It detects an existing `.claude` or `.agents` folder in the project and installs there; a project with neither gets both copies. Pass `--host claude`, `--host codex`, or `--host both` to override. It refuses to replace files that differ from the source.

Alternatively copy the complete `skills/bsg` directory into the host's skill folder yourself. Preserve references, assets, scripts and metadata. Do not copy this repository's `.planning` history into another project.

Start a new chat and say “BSG help”, or use `/bsg help` in Claude Code or `$bsg help` in Codex. If it is not discovered, restart the app. Installation does not authorize implementation or initialize a project.

## Project instruction files

BSG writes its handoff block to the project's `AGENTS.md`, which both hosts read. Claude Code stops reading `AGENTS.md` once a project has a `CLAUDE.md`, `.claude/CLAUDE.md`, or `CLAUDE.local.md`, so when any of those exists BSG also adds the same block to the root `CLAUDE.md`. Existing content in either file is preserved byte for byte.

## Updating

Personal and project installations can both appear in the same project; normally use one scope. The Claude Code plugin updates through `claude plugin marketplace update bsg`. A copied skill folder is updated by copying again; the local installer refuses files that differ from the source, so compare and preserve customizations first.
