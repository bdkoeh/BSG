# Installing BSG

BSG is one skill, with five public commands: start, help, status, pause, and resume. Discussion, research, planning, implementation and verification are guided through conversation. The same `skills/bsg` folder works in Claude Code and Codex; only where it is placed differs.

| Host | Personal (all projects) | One project | Invoke |
| --- | --- | --- | --- |
| Claude Code | plugin install, or `~/.claude/skills/bsg` | `<project>/.claude/skills/bsg` | `/bsg:bsg help` (plugin), `/bsg help` (copy) |
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

Inside a session the same steps are `/plugin marketplace add bdkoeh/BSG` and `/plugin install bsg@bsg`. Without an SSH key for GitHub, set `CLAUDE_CODE_PLUGIN_PREFER_HTTPS=1` so the clone uses HTTPS. Invoke the plugin skill as `/bsg:bsg help`; `/bsg help` is the copied-skill form.

Without plugins: copy the complete `skills/bsg` folder to `~/.claude/skills/bsg` for all projects, or to `<project>/.claude/skills/bsg` for one project. The local installer below does the per-project copy.

## Codex

Use the installation prompt in the [README](../README.md). The built-in skill-installer can install `skills/bsg` from `bdkoeh/BSG` on branch `main`, using `--repo bdkoeh/BSG --path skills/bsg`. Use its personal destination for all projects or `--dest <project>/.agents/skills` for one project. These are arguments to the installer's `scripts/install-skill-from-github.py`, not flags to the `codex` command.

The bundled installer tested on 2026-10-28 defaults to `$CODEX_HOME/skills` (usually `~/.codex/skills`). A fresh Codex app-server discovered BSG there as an enabled user skill. Current [Codex documentation](https://learn.chatgpt.com/docs/build-skills) lists `~/.agents/skills` for manual personal installations; copy the complete folder there as `~/.agents/skills/bsg` if installing manually. Use one personal location.

## Local installer, either host

Clone or download the repository and run `python scripts/install.py --project <existing-project-folder>` (Python 3.10+; quote paths containing spaces). It detects an existing `.claude` or `.agents` folder in the project and installs there; a project with neither gets both copies. Pass `--host claude`, `--host codex`, or `--host both` to override. It refuses to replace files that differ from the source.

Alternatively copy the complete `skills/bsg` directory into the host's skill folder yourself. Preserve references, assets, scripts and metadata. Each project creates its own `.planning` records when BSG starts; no development history is needed for installation.

Start a new chat and say “BSG help”, or use `/bsg:bsg help` for the Claude Code plugin (`/bsg help` for a copied skill) or `$bsg help` in Codex. If it is not discovered, restart the app. Installation does not authorize implementation or initialize a project.

## Project instruction files

BSG writes its handoff block to root `AGENTS.md`. If root `CLAUDE.md`, `.claude/CLAUDE.md`, or `CLAUDE.local.md` exists, the helper also adds the block to root `CLAUDE.md`, preserving existing content.

Codex loads `AGENTS.md`. [Claude Code's direct AGENTS.md support](https://code.claude.com/docs/en/memory#agentsmd) requires v2.1.277 or later and enabled support. By default, Claude instruction files in the working directory or its ancestors suppress direct `AGENTS.md` loading. The BSG helper checks the three project-local paths above; it does not detect ancestor files or host settings. If Claude does not load the handoff, add `@AGENTS.md` to root `CLAUDE.md` (preserving existing instructions) or configure Claude to read both.

## Updating

Personal and project installations can both appear in the same project; normally use one scope. Refresh the catalog with `claude plugin marketplace update bsg`, then update the installed plugin with `claude plugin update bsg@bsg`. A copied skill folder is updated by copying again; the local installer refuses files that differ from the source, so compare and preserve customizations first.
