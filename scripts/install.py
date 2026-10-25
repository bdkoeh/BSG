"""Install the single BSG skill into a project's skill directory without overwrites.

Codex discovers project skills in .agents/skills; Claude Code discovers them in
.claude/skills. By default the installer detects which host folders the project
already has and installs for those; a project with neither gets both.
"""
import argparse
import shutil
from pathlib import Path

HOSTS = {"codex": ".agents/skills", "claude": ".claude/skills"}


def detect_hosts(project):
    present = [host for host, folder in HOSTS.items() if (project / folder).parent.is_dir()]
    return present or list(HOSTS)


def install(source, project, host="auto"):
    source, project = source.resolve(), project.resolve()
    if not project.is_dir():
        raise ValueError("Target project must already exist.")
    hosts = detect_hosts(project) if host == "auto" else list(HOSTS) if host == "both" else [host]
    files = [p for p in (source / "bsg").rglob("*") if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc"]
    if not files:
        raise ValueError("No source skills found.")
    pending = []
    for name in hosts:
        destination = project / HOSTS[name]
        if not destination.resolve().is_relative_to(project):
            raise ValueError("Skill destination resolves outside the target project.")
        for path in files:
            target = destination / path.relative_to(source)
            if not target.resolve().is_relative_to(project):
                raise ValueError(f"Destination escapes project: {target}")
            if target.exists():
                if not target.is_file() or target.read_bytes() != path.read_bytes():
                    raise ValueError(f"Existing different file; reconcile manually before reinstalling: {target}")
            else:
                pending.append((path, target))
    for path, target in pending:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)
    return len(pending)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--host", choices=("auto", "codex", "claude", "both"), default="auto",
                        help="codex installs to .agents/skills, claude to .claude/skills (default: auto-detect, else both)")
    args = parser.parse_args()
    try:
        project = args.project.resolve()
        hosts = detect_hosts(project) if args.host == "auto" else list(HOSTS) if args.host == "both" else [args.host]
        count = install(Path(__file__).resolve().parents[1] / "skills", project, args.host)
        where = ", ".join(str(project / HOSTS[h]) for h in hosts)
        print(f"Installed {count} new files in {where}. No existing files replaced.")
    except (OSError, ValueError) as exc:
        parser.exit(1, f"BSG installation stopped: {exc}\n")
