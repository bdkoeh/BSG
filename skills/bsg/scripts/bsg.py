"""BSG project scaffolding and read-only consistency checks. Standard library only."""
import argparse
import json
import re
from pathlib import Path

COMMANDS = {
    "start": "Shape a project or substantial feature",
    "status": "Show discovery, work, and verification progress",
    "help": "Show commands and a recommended next action",
    "pause [ID]": "Checkpoint and pause work",
    "resume": "Reconcile actual progress and continue",
}
STATUSES = set("outline discovery discussed ready building implemented verified awaiting_feedback complete blocked paused".split())
PROJECT_DOCS = {
    "PROJECT.md": ["Problem and users", "Desired experience", "First release and boundaries", "Constraints", "Agent effort and human involvement", "Execution authorization", "Frontend direction"],
    "ROADMAP.md": ["Outcomes and stable slice IDs", "Dependencies", "Human checkpoints and independent work"],
    "DECISIONS.md": ["Agreed decisions with IDs and revisions", "Rationale and sources of agreement", "Superseded decisions"],
    "STATE.md": ["Current focus", "Active assignments", "Pending questions and blockers", "Next action"],
    "BACKLOG.md": ["Deferred ideas", "Larger feedback items"],
}
SLICE_DOCS = {
    "CONTEXT.md": ["Intent and examples", "Agreed decisions", "Assumptions and open questions", "Boundaries"],
    "PLAN.md": ["Outcome", "Dependencies and decisions", "Owned paths", "Implementation steps", "Acceptance scenarios and required checks", "Human checkpoint", "Execution authorization"],
    "SUMMARY.md": ["Implemented", "Remaining", "Changed files and revisions used", "Blockers and handoff"],
    "VERIFICATION.md": ["Checked code identity and revision", "Procedures and observed results", "Limitations and pending checks", "Human feedback", "Historical evidence"],
}


def write_json(path, value):
    temp = path.with_suffix(".json.tmp")
    temp.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    temp.replace(path)


def docs(folder, definitions, title):
    for name, headings in definitions.items():
        (folder / name).write_text(f"# {title}\n\n" + "\n\n".join(f"## {h}\n" for h in headings), encoding="utf-8")


def handoff_files(root):
    """Instruction files that need the BSG handoff.

    AGENTS.md serves Codex, and Claude Code reads it when no CLAUDE.md exists.
    Once a project has any CLAUDE.md, Claude Code ignores AGENTS.md, so the
    same block also goes into the root CLAUDE.md.
    """
    files = ["AGENTS.md"]
    if any((root / name).exists() for name in ("CLAUDE.md", ".claude/CLAUDE.md", "CLAUDE.local.md")):
        files.append("CLAUDE.md")
    return files


def handoff_content(root, name):
    """Prepare an additive handoff, preserving existing bytes and custom BSG blocks."""
    path = root / name
    if path.is_symlink():
        raise ValueError(f"{name} is a symlink; reconcile its destination manually.")
    original = path.read_bytes() if path.exists() else b""
    for tag in (b"BSG", b"BSD"):  # BSD is the pre-release marker; projects that carry it are already attached.
        begin, end = b"<!-- " + tag + b":BEGIN -->", b"<!-- " + tag + b":END -->"
        if begin in original or end in original:
            if original.count(begin) != 1 or original.count(end) != 1 or original.index(begin) > original.index(end):
                raise ValueError(f"{name} has malformed BSG markers; reconcile before attaching.")
            return None
    template = (Path(__file__).resolve().parents[1] / "assets/project-agents.md").read_bytes()
    return original + (b"\n\n" if original else b"") + template


def prepare_handoff(root):
    """Check every target before writing any, so a malformed file stops the whole change."""
    return {name: handoff_content(root, name) for name in handoff_files(root)}


def write_handoff(root, prepared):
    written = []
    for name, content in prepared.items():
        if content is not None:
            (root / name).write_bytes(content)
            written.append(name)
    return written


def attach(root):
    """Add the handoff to an existing BSG project without resetting records."""
    data = load(root)
    if not isinstance(data, dict) or data.get("schema_version") != 1 or not data.get("project"):
        raise ValueError("A recognized BSG project is required before attaching.")
    return write_handoff(root, prepare_handoff(root))


def init(root, name):
    planning = root / ".planning"
    if planning.exists():
        raise ValueError(".planning already exists; inspect and reconcile it, never reset it.")
    handoff = prepare_handoff(root)
    planning.mkdir(parents=True)
    for folder in ("slices", "research", "discovery"):
        (planning / folder).mkdir()
    docs(planning, {"PROJECT.md": PROJECT_DOCS["PROJECT.md"]}, name)
    state = dict(schema_version=1, project=name, paused=False, agent_effort=None,
                 human_involvement=None, decisions=[], slices=[])
    write_json(planning / "state.json", state)
    write_handoff(root, handoff)
    sync(root)
    return state


def load(root):
    return json.loads((root / ".planning/state.json").read_text(encoding="utf-8-sig"))


def contained_file(root, relative):
    if not isinstance(relative, str) or not relative.strip():
        return False
    path = Path(relative)
    if path.is_absolute() or ".." in path.parts:
        return False
    resolved = (root / path).resolve()
    return resolved.is_relative_to(root.resolve()) and resolved.is_file()


def has_record_content(root, relative):
    """Reject empty scaffolds, not judge the semantic quality of a discussion."""
    if not contained_file(root, relative):
        return False
    text = (root / relative).read_text(encoding="utf-8-sig")
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or line in {"---", "```"}:
            continue
        if line.strip(" -*_").lower() in {"todo", "tbd", "pending", "placeholder"}:
            continue
        return True
    return False


def positive(value):
    return type(value) is int and value > 0


def validate(root, data):
    errors = []
    if not isinstance(data, dict) or data.get("schema_version") != 1:
        return ["Unsupported or missing BSG schema_version."]
    if type(data.get("paused")) is not bool:
        errors.append("paused must be a boolean.")
    if not isinstance(data.get("project"), str) or not data["project"].strip():
        errors.append("project must be a non-empty name.")
    if data.get("agent_effort") not in (None, "lean", "balanced", "deep"):
        errors.append("Unknown agent_effort.")
    required_docs = ["PROJECT.md"]
    if data.get("decisions"):
        required_docs.append("DECISIONS.md")
    for name in required_docs:
        if not contained_file(root, f".planning/{name}"):
            errors.append(f"Missing project record: {name}")
    slices, decisions = data.get("slices"), data.get("decisions")
    if not isinstance(slices, list) or not isinstance(decisions, list):
        return errors + ["slices and decisions must be arrays."]
    if any(not isinstance(s, dict) or not positive(s.get("id")) for s in slices):
        return errors + ["Each slice needs a positive integer id."]
    indexed = {s["id"]: s for s in slices}
    if len(indexed) != len(slices):
        errors.append("Duplicate slice IDs.")
    decision_index = {}
    for d in decisions:
        if (not isinstance(d, dict) or not isinstance(d.get("id"), str)
                or not re.fullmatch(r"D-\d+", d["id"]) or not positive(d.get("revision"))
                or d.get("status") not in ("agreed", "proposed", "superseded")):
            errors.append("Invalid decision record.")
            continue
        if d["id"] in decision_index:
            errors.append(f"Duplicate decision: {d['id']}")
        decision_index[d["id"]] = d
    graph = {}
    for s in slices:
        label = f"Slice {s['id']}"
        status, revision = s.get("status"), s.get("revision")
        if status not in STATUSES or not positive(revision):
            errors.append(f"{label}: invalid status or revision.")
        path = s.get("path")
        if (not isinstance(path, str) or not path or Path(path).is_absolute()
                or ".." in Path(path).parts
                or not (root / path).resolve().is_relative_to(root.resolve())
                or not (root / path).is_dir()):
            errors.append(f"{label}: missing or invalid slice directory.")
        if status in {"implemented", "verified", "awaiting_feedback", "complete"}:
            if not has_record_content(root, f"{path}/SUMMARY.md"):
                errors.append(f"{label}: capture implemented work in SUMMARY.md.")
        if status in {"verified", "awaiting_feedback", "complete"}:
            if not has_record_content(root, f"{path}/VERIFICATION.md"):
                errors.append(f"{label}: capture verification in VERIFICATION.md.")
        shaped = {"discussed", "ready", "building", "implemented", "verified", "awaiting_feedback", "complete"}
        if status in shaped and not has_record_content(root, f"{path}/CONTEXT.md"):
            errors.append(f"{label}: capture discussion in CONTEXT.md before marking discussed or planning execution.")
        if status in shaped - {"discussed"} and not has_record_content(root, f"{path}/PLAN.md"):
            errors.append(f"{label}: populate PLAN.md before implementation readiness.")
        deps = s.get("depends_on")
        if not isinstance(deps, list) or any(not positive(d) or d not in indexed for d in deps):
            errors.append(f"{label}: invalid dependencies.")
            deps = []
        graph[s["id"]] = deps
        if status in {"building", "implemented", "verified", "awaiting_feedback", "complete"}:
            if any(indexed[d].get("status") != "complete" for d in deps):
                errors.append(f"{label}: execution/completion depends on unfinished work.")
        refs = s.get("decision_refs")
        if not isinstance(refs, dict):
            errors.append(f"{label}: decision_refs must be an object.")
        else:
            for key, rev in refs.items():
                d = decision_index.get(key)
                if not d or not positive(rev) or d["revision"] != rev or d["status"] != "agreed":
                    errors.append(f"{label}: decision {key} is missing, unagreed, or stale.")
        checks = s.get("checks")
        if not isinstance(checks, list):
            errors.append(f"{label}: checks must be an array.")
            checks = []
        required = []
        seen_checks = set()
        for check in checks:
            if (not isinstance(check, dict) or not isinstance(check.get("id"), str)
                    or not check["id"] or type(check.get("required")) is not bool
                    or check.get("result") not in ("pending", "pass", "fail", "stale")):
                errors.append(f"{label}: invalid check record.")
                continue
            if check["id"] in seen_checks:
                errors.append(f"{label}: duplicate check {check['id']}.")
            seen_checks.add(check["id"])
            if check["required"]:
                required.append(check)
            check_revision = check.get("revision")
            if check_revision is not None and not positive(check_revision):
                errors.append(f"{label}: check {check['id']} has an invalid revision.")
            evidence = check.get("evidence")
            if evidence is not None and not contained_file(root, evidence):
                errors.append(f"{label}: check {check['id']} has an invalid evidence path.")
            if check["result"] in ("pass", "fail") and (not positive(check_revision) or evidence is None):
                errors.append(f"{label}: executed check {check['id']} needs revision and evidence.")
            if check["result"] == "pass" and (check.get("revision") != revision
                    or not contained_file(root, check.get("evidence"))):
                errors.append(f"{label}: passed check {check['id']} lacks current evidence.")
        if status in {"ready", "building", "implemented", "verified", "awaiting_feedback", "complete"} and not required:
            errors.append(f"{label}: define required checks before implementation readiness.")
        if status in {"verified", "awaiting_feedback", "complete"}:
            if not required or any(c["result"] != "pass" for c in required):
                errors.append(f"{label}: required checks are not all passed.")
        acceptance = s.get("acceptance")
        if (not isinstance(acceptance, dict) or type(acceptance.get("required")) is not bool
                or acceptance.get("status") not in ("pending", "accepted", "not_required")):
            errors.append(f"{label}: invalid acceptance record.")
            continue
        if acceptance["required"] and acceptance["status"] == "not_required":
            errors.append(f"{label}: required human acceptance cannot be waived by status.")
        if not acceptance["required"] and acceptance["status"] != "not_required":
            errors.append(f"{label}: non-required acceptance must use not_required.")
        if acceptance["status"] == "accepted" and (acceptance.get("revision") != revision
                or not contained_file(root, acceptance.get("evidence"))):
            errors.append(f"{label}: human acceptance lacks current evidence.")
        if status == "complete" and acceptance["required"] and acceptance["status"] != "accepted":
            errors.append(f"{label}: human feedback is pending.")
    visiting, visited = set(), set()

    def visit(sid):
        if sid in visiting:
            errors.append(f"Dependency cycle includes slice {sid}.")
            return
        if sid in visited:
            return
        visiting.add(sid)
        for dep in graph.get(sid, []):
            visit(dep)
        visiting.remove(sid)
        visited.add(sid)
    for sid in graph:
        visit(sid)
    return errors


def add_slice(root, title):
    data = load(root)
    errors = validate(root, data)
    if errors:
        raise ValueError("Reconcile existing records before adding a slice: " + "; ".join(errors))
    sid = max((s["id"] for s in data["slices"]), default=0) + 1
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:60] or "slice"
    relative = f".planning/slices/{sid:03d}-{slug}"
    folder = root / relative
    folder.mkdir()  # Never overwrite an orphaned or pre-existing slice.
    docs(folder, {"CONTEXT.md": SLICE_DOCS["CONTEXT.md"]}, f"{sid}: {title}")
    record = dict(id=sid, title=title, path=relative, status="outline", revision=1,
                  depends_on=[], decision_refs={}, agent=None, blocker=None, checks=[],
                  acceptance=dict(required=True, status="pending", revision=None, evidence=None))
    data["slices"].append(record)
    write_json(root / ".planning/state.json", data)
    return record


def slice_guidance(s, indexed, paused=False):
    """Explain a validated slice's next step without inferring execution permission."""
    sid, status = s["id"], s["status"]
    waiting = [indexed[d] for d in s["depends_on"] if indexed[d]["status"] != "complete"]
    if status == "complete":
        kind, action = "complete", "Complete; no further work assumed."
    elif paused or status == "paused":
        kind, action = "paused", f"BSG resume — reconcile paused slice {sid} before continuing."
    elif status == "blocked" or s.get("blocker"):
        kind, action = "blocked", f"Resolve slice {sid}'s blocker: {s.get('blocker') or 'inspect its handoff'}."
    elif status in ("verified", "awaiting_feedback") and s["acceptance"]["status"] == "pending":
        kind, action = "feedback", f"Review slice {sid} and provide the agreed human feedback."
    elif status in ("implemented", "verified", "awaiting_feedback"):
        kind, action = "verify", f"Verify slice {sid}'s evidence and any human gate before recording completion."
    elif status == "ready":
        if waiting:
            kind, action = "waiting", f"Wait for slice {sid}'s dependencies to complete before reviewing build authorization."
        else:
            kind, action = "build", f"Review slice {sid}'s approach and build authorization; offer start implementing / keep discussing if approval is pending."
    elif status == "building":
        kind, action = "building", f"Check slice {sid}'s actual worker state and results before continuing or reassigning work."
    else:
        kind = "plan" if status == "discussed" else status
        action = f"Continue {'planning' if kind == 'plan' else 'discussion of'} slice {sid}; capture missing context before advancing."
    return dict(id=sid, kind=kind, action=action, waiting=waiting)


def next_steps(data):
    """One priority action plus other dependency-free opportunities, never dispatches."""
    if data["paused"]:
        return "BSG resume — work is paused; reconcile before continuing.", []
    indexed = {s["id"]: s for s in data["slices"]}
    priority = {kind: rank for rank, kind in enumerate(
        ("feedback", "blocked", "verify", "build", "plan", "discovery", "outline", "paused", "building", "waiting"))}
    guidance = [slice_guidance(s, indexed) for s in data["slices"] if s["status"] != "complete"]
    if not guidance:
        if data["slices"]:
            return "All recorded slices are complete. Review the delivered result; no new work assumed.", []
        return "Explore the next useful outcome or resolve dependencies in conversation.", []
    guidance.sort(key=lambda item: priority[item["kind"]])
    other_work = [g["action"] for g in guidance[1:]
                  if not g["waiting"] and g["kind"] in {"verify", "build", "plan", "discovery", "outline", "building"}]
    return guidance[0]["action"], other_work


def recommend(data):
    return next_steps(data)[0]


def check_summary(s):
    """Keep failures and stale evidence visible instead of hiding them in a ratio."""
    if not s["checks"]:
        return "not defined"
    parts = []
    for result in ("fail", "stale", "pending", "pass"):
        checks = [c for c in s["checks"] if c["result"] == result]
        if checks:
            detail = ", ".join(c["id"] + (" (optional)" if not c["required"] else "") for c in checks)
            parts.append(f"{result}: {len(checks)}" + (f" [{detail}]" if result != "pass" else ""))
    return "; ".join(parts)


def waiting_summary(guidance):
    return ", ".join(f"{s['id']} · {s['title']} ({s['status']})" for s in guidance["waiting"])


def report(root, include_help=False):
    lines = []
    if include_help:
        lines.extend(f"BSG {key}: {value}" for key, value in COMMANDS.items())
    if not (root / ".planning/state.json").exists():
        if (root / ".planning").exists():
            return "\n".join(lines + ["Existing planning folder without BSG index. Inspect before migration; do not initialize over it."]), 1
        return "\n".join(lines + ["Recommended: BSG start — no BSG project initialized."]), 0
    data = load(root)
    errors = validate(root, data)
    if errors:
        return "\n".join(lines + ["Reconciliation required:"] + errors), 1
    lines.append(f"BSG: {data['project']}")
    lines.append(f"Paused: {'yes' if data['paused'] else 'no'}")
    indexed = {s["id"]: s for s in data["slices"]}
    for s in data["slices"]:
        guidance = slice_guidance(s, indexed, data["paused"])
        lines.append(f"{s['id']} | {s['title']} | {s['status']} | checks {check_summary(s)} | human {s['acceptance']['status']}")
        if guidance["waiting"]:
            lines.append("  Waiting on: " + waiting_summary(guidance))
        if s.get("blocker"):
            lines.append("  Blocker: " + str(s["blocker"]))
        if s.get("agent"):
            lines.append(f"  Recorded agent: {s['agent']} (live state unconfirmed)")
        if s["status"] != "complete":
            lines.append("  Next: " + guidance["action"])
    recommendation, other_work = next_steps(data)
    lines.append("Recommended: " + recommendation)
    if other_work:
        lines.append("Other possible work (confirm scope, authorization, and human checkpoints):")
        lines.extend("- " + action for action in other_work)
    lines.append("Recorded state only; confirm live workers, code, and authorization before acting.")
    return "\n".join(lines), 0


def markdown_cell(value):
    return str(value).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("|", "&#124;").replace("\r", " ").replace("\n", " ")


def summary_sections(data):
    """Derived views only: authorization and actual worker liveness remain human checks."""
    roadmap = ["## Recorded roadmap", "", "| ID | Outcome | Status | Depends on | Revision |",
               "| --- | --- | --- | --- | --- |"]
    state = ["## Recorded state", "", f"Project: {markdown_cell(data['project'])}",
             f"Paused: {'yes' if data['paused'] else 'no'}", "",
             "| ID | Status | Checks | Human feedback | Recorded agent | Blocker | Waiting on | Next step |",
             "| --- | --- | --- | --- | --- | --- | --- | --- |"]
    indexed = {s["id"]: s for s in data["slices"]}
    for s in sorted(data["slices"], key=lambda item: item["id"]):
        roadmap.append("| " + " | ".join(markdown_cell(v) for v in (
            s["id"], s["title"], s["status"], ", ".join(map(str, s["depends_on"])) or "—", s["revision"])) + " |")
        guidance = slice_guidance(s, indexed, data["paused"])
        state.append("| " + " | ".join(markdown_cell(v) for v in (
            s["id"], s["status"], check_summary(s), s["acceptance"]["status"],
            s.get("agent") or "—", s.get("blocker") or "—",
            waiting_summary(guidance) or "—", guidance["action"])) + " |")
    recommendation, other_work = next_steps(data)
    state.extend(["", "Suggested next step: " + markdown_cell(recommendation)])
    if other_work:
        state.extend(["", "Other possible work (confirm scope, authorization, and human checkpoints):", ""])
        state.extend("- " + markdown_cell(action) for action in other_work)
    state.extend(["",
                  "Recorded state only; confirm live workers, code, and authorization before acting."])
    return {"ROADMAP.md": "\n".join(roadmap), "STATE.md": "\n".join(state)}


def sync(root):
    """Replace only marked generated sections, preflighting both files before writes."""
    data = load(root)
    errors = validate(root, data)
    if errors:
        raise ValueError("Reconcile records before syncing: " + "; ".join(errors))
    begin, end = b"<!-- BSG:GENERATED:BEGIN -->", b"<!-- BSG:GENERATED:END -->"
    pending = {}
    for name, section in summary_sections(data).items():
        path = root / ".planning" / name
        if path.is_symlink() or not path.resolve().is_relative_to(root.resolve()):
            raise ValueError(f"{name} has an unsafe destination; reconcile before syncing.")
        original = path.read_bytes() if path.exists() else b""
        block = begin + b"\n" + section.encode("utf-8") + b"\n" + end
        if begin in original or end in original:
            if original.count(begin) != 1 or original.count(end) != 1 or original.index(begin) > original.index(end):
                raise ValueError(f"{name} has malformed generated markers; reconcile before syncing.")
            content = original[:original.index(begin)] + block + original[original.index(end) + len(end):]
        else:
            introduction = ("\n\n" if original else f"# {name[:-3].title()}\n\n")
            introduction += ("The generated section below is derived from state.json. Notes outside it are preserved; "
                             "reconcile any older status prose against the index.\n\n")
            content = original + introduction.encode("utf-8") + block + b"\n"
        pending[path] = content
    for path, content in pending.items():
        if not path.exists() or path.read_bytes() != content:
            path.write_bytes(content)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("init", "attach", "slice", "sync", "status", "help", "validate"))
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--name")
    parser.add_argument("--title")
    args = parser.parse_args()
    root = args.root.resolve()
    try:
        if args.action == "init":
            if not args.name:
                parser.error("init requires --name")
            init(root, args.name)
            print(f"Initialized BSG records and the {' and '.join(handoff_files(root))} handoff. Capture the actual discussion before planning.")
        elif args.action == "attach":
            attach(root)
            print(f"BSG handoff is present in {' and '.join(handoff_files(root))}. Existing instructions and records preserved.")
        elif args.action == "slice":
            if not args.title:
                parser.error("slice requires --title")
            print(json.dumps(add_slice(root, args.title)))
        elif args.action == "sync":
            sync(root)
            print("Refreshed generated roadmap and state sections; notes preserved.")
        elif args.action == "validate":
            errors = validate(root, load(root))
            print("\n".join(errors) if errors else "BSG records are consistent; this does not prove product correctness.")
            return int(bool(errors))
        else:
            output, code = report(root, args.action == "help")
            print(output)
            return code
    except (OSError, ValueError, TypeError, KeyError) as exc:
        print(f"BSG could not read or update records: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
