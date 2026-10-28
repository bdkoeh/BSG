import importlib.util
import tempfile
import unittest
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
TEST_WORK = BASE / ".test-work"


def temporary_project():
    TEST_WORK.mkdir(exist_ok=True)
    temp = tempfile.TemporaryDirectory(dir=TEST_WORK)
    if not Path(temp.name).resolve().is_relative_to(TEST_WORK.resolve()):
        raise RuntimeError("Test cleanup must stay inside .test-work")
    return temp


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


bsg = module("bsg", BASE / "skills/bsg/scripts/bsg.py")
installer = module("installer", BASE / "scripts/install.py")


class Records(unittest.TestCase):
    def setUp(self):
        self.temp = temporary_project()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        bsg.init(self.root, "Example")
        bsg.add_slice(self.root, "First outcome")
        self.data = bsg.load(self.root)
        self.slice = self.data["slices"][0]

    def evidence(self):
        folder = self.root / self.slice["path"]
        (folder / "CONTEXT.md").write_text("# Context\nUser requested the first outcome; behavior agreed in discovery.\n", encoding="utf-8")
        (folder / "PLAN.md").write_text("# Plan\nImplement the first outcome and verify the agreed behavior.\n", encoding="utf-8")
        (folder / "SUMMARY.md").write_text("Implemented the agreed outcome.\n", encoding="utf-8")
        (folder / "VERIFICATION.md").write_text("Checked the agreed behavior at revision 1; observed expected output.\n", encoding="utf-8")
        evidence = self.slice["path"] + "/VERIFICATION.md"
        self.slice["checks"] = [dict(id="behavior", required=True, result="pass", revision=1, evidence=evidence)]
        self.slice["acceptance"] = dict(required=False, status="not_required", revision=None, evidence=None)
        return evidence

    def test_scaffold_is_valid_and_does_not_overwrite(self):
        self.assertEqual([], bsg.validate(self.root, self.data))
        with self.assertRaises(ValueError):
            bsg.init(self.root, "Replacement")
        self.assertEqual("Example", bsg.load(self.root)["project"])

    def test_stable_ids_after_reordering(self):
        bsg.add_slice(self.root, "Second")
        data = bsg.load(self.root)
        data["slices"].reverse()
        bsg.write_json(self.root / ".planning/state.json", data)
        self.assertEqual(3, bsg.add_slice(self.root, "Third")["id"])

    def test_complete_requires_evidence_and_human_acceptance(self):
        self.slice["status"] = "complete"
        errors = bsg.validate(self.root, self.data)
        self.assertTrue(any("required checks" in e for e in errors))
        self.assertTrue(any("feedback is pending" in e for e in errors))
        evidence = self.evidence()
        self.slice["acceptance"] = dict(required=True, status="accepted", revision=1, evidence=evidence)
        self.assertEqual([], bsg.validate(self.root, self.data))

    def test_revision_change_invalidates_pass_and_acceptance(self):
        evidence = self.evidence()
        self.slice["status"] = "complete"
        self.slice["acceptance"] = dict(required=True, status="accepted", revision=1, evidence=evidence)
        self.slice["revision"] = 2
        errors = bsg.validate(self.root, self.data)
        self.assertTrue(any("passed check" in e for e in errors))
        self.assertTrue(any("human acceptance lacks" in e for e in errors))

    def test_decision_change_is_detected(self):
        self.data["decisions"] = [dict(id="D-001", revision=2, status="agreed")]
        self.slice["decision_refs"] = {"D-001": 1}
        self.assertTrue(any("stale" in e for e in bsg.validate(self.root, self.data)))

    def test_dependencies_and_cycles(self):
        bsg.add_slice(self.root, "Second")
        data = bsg.load(self.root)
        data["slices"][0]["depends_on"] = [2]
        data["slices"][0]["status"] = "building"
        data["slices"][1]["depends_on"] = [1]
        errors = bsg.validate(self.root, data)
        self.assertTrue(any("unfinished" in e for e in errors))
        self.assertTrue(any("cycle" in e for e in errors))

    def test_help_is_read_only_and_does_not_recommend_blocked_build(self):
        bsg.add_slice(self.root, "Second")
        data = bsg.load(self.root)
        data["slices"][1].update(status="ready", depends_on=[1])
        folder = self.root / data["slices"][1]["path"]
        (folder / "CONTEXT.md").write_text("User requested the second outcome after the first.\n", encoding="utf-8")
        (folder / "PLAN.md").write_text("Implement the second outcome after its dependency completes.\n", encoding="utf-8")
        data["slices"][1]["checks"] = [dict(id="behavior", required=True, result="pending", revision=None, evidence=None)]
        bsg.write_json(self.root / ".planning/state.json", data)
        before = {p: p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        output, code = bsg.report(self.root, True)
        self.assertEqual(0, code)
        self.assertNotIn("Recommended: Review slice 2's approach", output)
        self.assertEqual(before, {p: p.read_bytes() for p in self.root.rglob("*") if p.is_file()})

    def test_stale_help_requests_reconciliation(self):
        self.slice["status"] = "complete"
        bsg.write_json(self.root / ".planning/state.json", self.data)
        output, code = bsg.report(self.root, True)
        self.assertEqual(1, code)
        self.assertIn("Reconciliation required", output)
        self.assertNotIn("All recorded slices are complete", output)

    def test_evidence_cannot_escape_project(self):
        self.evidence()
        self.slice["checks"][0]["evidence"] = "../outside.md"
        self.assertTrue(bsg.validate(self.root, self.data))

    def test_malformed_records_report_errors(self):
        self.slice["checks"] = [None]
        self.slice["acceptance"] = None
        self.assertTrue(bsg.validate(self.root, self.data))

    def test_execution_readiness_requires_defined_checks(self):
        for status in ("ready", "building", "implemented"):
            self.slice["status"] = status
            self.assertTrue(any("define required checks" in e for e in bsg.validate(self.root, self.data)))

    def test_failed_check_requires_valid_evidence(self):
        self.slice["checks"] = [dict(id="behavior", required=True, result="fail", revision="invalid", evidence="../outside.md")]
        errors = bsg.validate(self.root, self.data)
        self.assertTrue(any("invalid revision" in e for e in errors))
        self.assertTrue(any("invalid evidence path" in e for e in errors))

    def test_pause_and_human_gate_recommendations(self):
        self.data["paused"] = True
        self.assertIn("resume", bsg.recommend(self.data))
        self.data["paused"] = False
        self.slice["status"] = "awaiting_feedback"
        self.assertIn("human feedback", bsg.recommend(self.data))

    def test_existing_non_bsg_planning_not_reinitialized(self):
        (self.root / ".planning/state.json").unlink()
        output, code = bsg.report(self.root, True)
        self.assertEqual(1, code)
        self.assertIn("Inspect before migration", output)


    def test_draft_plan_does_not_substitute_for_slice_context(self):
        (self.root / self.slice["path"] / "PLAN.md").write_text("# Draft\nDetailed implementation proposal.\n", encoding="utf-8")
        self.slice["status"] = "discussed"
        errors = bsg.validate(self.root, self.data)
        self.assertTrue(any("capture discussion in CONTEXT.md" in e for e in errors))
        bsg.write_json(self.root / ".planning/state.json", self.data)
        output, code = bsg.report(self.root, True)
        self.assertEqual(1, code)
        self.assertIn("Reconciliation required", output)
        self.assertNotIn("Recommended: Continue planning", output)

    def test_ready_requires_populated_plan(self):
        self.evidence()
        self.slice["status"] = "ready"
        (self.root / self.slice["path"] / "PLAN.md").write_text("# Plan\n## Steps\nTBD\n<!-- pending -->\n", encoding="utf-8")
        self.assertTrue(any("populate PLAN.md" in e for e in bsg.validate(self.root, self.data)))


    def test_lazy_records_enforce_stage_requirements(self):
        folder = self.root / self.slice["path"]
        self.assertEqual({"CONTEXT.md"}, {p.name for p in folder.iterdir()})
        self.assertFalse((self.root / ".planning/BACKLOG.md").exists())
        self.assertFalse((self.root / ".planning/DECISIONS.md").exists())
        (folder / "CONTEXT.md").write_text("User agreed to the first outcome.", encoding="utf-8")
        self.slice["status"] = "discussed"
        self.assertEqual([], bsg.validate(self.root, self.data))
        self.slice["status"] = "ready"
        self.slice["checks"] = [dict(id="behavior", required=True, result="pending", revision=None, evidence=None)]
        self.assertTrue(any("PLAN.md" in e for e in bsg.validate(self.root, self.data)))
        (folder / "PLAN.md").write_text("Implement and check the agreed outcome.", encoding="utf-8")
        self.assertEqual([], bsg.validate(self.root, self.data))
        self.slice["status"] = "implemented"
        self.assertTrue(any("SUMMARY.md" in e for e in bsg.validate(self.root, self.data)))
        (folder / "SUMMARY.md").write_text("Implemented the outcome; checks pending.", encoding="utf-8")
        self.assertEqual([], bsg.validate(self.root, self.data))
        self.slice["status"] = "verified"
        self.assertTrue(any("VERIFICATION.md" in e for e in bsg.validate(self.root, self.data)))

    def test_early_failed_check_requires_existing_evidence(self):
        evidence = self.slice["path"] + "/VERIFICATION.md"
        self.slice["checks"] = [dict(id="probe", required=True, result="fail", revision=1, evidence=evidence)]
        self.assertTrue(any("evidence path" in e for e in bsg.validate(self.root, self.data)))
        (self.root / evidence).write_text("Probe failed: output was empty.", encoding="utf-8")
        self.assertEqual([], bsg.validate(self.root, self.data))

    def test_decisions_document_needed_only_with_indexed_decisions(self):
        self.data["decisions"] = [dict(id="D-001", revision=1, status="proposed")]
        self.assertTrue(any("DECISIONS.md" in e for e in bsg.validate(self.root, self.data)))
        (self.root / ".planning/DECISIONS.md").write_text("D-001: proposed import flow.", encoding="utf-8")
        self.assertEqual([], bsg.validate(self.root, self.data))

    def test_sync_preserves_legacy_notes_and_is_idempotent(self):
        planning = self.root / ".planning"
        legacy = b"# My roadmap\r\nCustom checkpoint notes.\r\n"
        (planning / "ROADMAP.md").write_bytes(legacy)
        bsg.sync(self.root)
        first = {name: (planning / name).read_bytes() for name in ("ROADMAP.md", "STATE.md")}
        self.assertTrue(first["ROADMAP.md"].startswith(legacy))
        self.assertIn(b"First outcome", first["ROADMAP.md"])
        bsg.sync(self.root)
        self.assertEqual(first, {name: (planning / name).read_bytes() for name in first})
        with (planning / "STATE.md").open("ab") as output:
            output.write(b"\nUnanswered: choose a preview.\n")
        self.slice.update(status="blocked", blocker="Need fixture", agent="old-handle")
        bsg.write_json(planning / "state.json", self.data)
        index_before = (planning / "state.json").read_bytes()
        bsg.sync(self.root)
        state = (planning / "STATE.md").read_text()
        self.assertIn("Need fixture", state)
        self.assertIn("old-handle", state)
        self.assertTrue(state.endswith("Unanswered: choose a preview.\n"))
        self.assertEqual(index_before, (planning / "state.json").read_bytes())

    def test_sync_preflights_both_files(self):
        planning = self.root / ".planning"
        (planning / "ROADMAP.md").write_text("Preserve me", encoding="utf-8")
        (planning / "STATE.md").write_text("<!-- BSG:GENERATED:BEGIN -->", encoding="utf-8")
        before = {p: p.read_bytes() for p in planning.rglob("*") if p.is_file()}
        with self.assertRaises(ValueError):
            bsg.sync(self.root)
        self.assertEqual(before, {p: p.read_bytes() for p in planning.rglob("*") if p.is_file()})

    def test_sync_refuses_invalid_index_without_writing(self):
        self.slice["status"] = "complete"
        bsg.write_json(self.root / ".planning/state.json", self.data)
        before = {p: p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        with self.assertRaises(ValueError):
            bsg.sync(self.root)
        self.assertEqual(before, {p: p.read_bytes() for p in self.root.rglob("*") if p.is_file()})

    def test_missing_generated_views_do_not_block_status(self):
        for name in ("ROADMAP.md", "STATE.md"):
            (self.root / ".planning" / name).unlink()
        before = {p: p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        output, code = bsg.report(self.root)
        self.assertEqual(0, code)
        self.assertIn("First outcome", output)
        self.assertEqual(before, {p: p.read_bytes() for p in self.root.rglob("*") if p.is_file()})
        bsg.sync(self.root)
        self.assertTrue((self.root / ".planning/STATE.md").is_file())

    def test_legacy_full_scaffold_still_valid(self):
        bsg.docs(self.root / ".planning", bsg.PROJECT_DOCS, "Legacy project")
        bsg.docs(self.root / self.slice["path"], bsg.SLICE_DOCS, "Legacy slice")
        self.assertEqual([], bsg.validate(self.root, self.data))
        before = {p: p.read_bytes() for p in (self.root / self.slice["path"]).iterdir()}
        bsg.sync(self.root)
        self.assertEqual(before, {p: p.read_bytes() for p in before})

    def test_generated_cells_cannot_inject_markers_or_rows(self):
        self.slice["title"] = "A | B\n<!-- BSG:GENERATED:END -->"
        bsg.write_json(self.root / ".planning/state.json", self.data)
        bsg.sync(self.root)
        bsg.sync(self.root)
        roadmap = (self.root / ".planning/ROADMAP.md").read_text()
        self.assertEqual(1, roadmap.count("<!-- BSG:GENERATED:END -->"))
        self.assertIn("A &#124; B", roadmap)

    def test_sync_refuses_symlink_output(self):
        planning = self.root / ".planning"
        target = self.root / "notes.md"
        target.write_text("Preserve", encoding="utf-8")
        (planning / "STATE.md").unlink()
        try:
            (planning / "STATE.md").symlink_to(target)
        except OSError:
            self.skipTest("Symlinks unavailable")
        roadmap = (planning / "ROADMAP.md").read_bytes()
        with self.assertRaises(ValueError):
            bsg.sync(self.root)
        self.assertEqual("Preserve", target.read_text())
        self.assertEqual(roadmap, (planning / "ROADMAP.md").read_bytes())


class ProjectHandoff(unittest.TestCase):
    def test_init_creates_handoff(self):
        with temporary_project() as tmp:
            root = Path(tmp)
            bsg.init(root, "New project")
            text = (root / "AGENTS.md").read_text(encoding="utf-8")
            self.assertIn(".planning/state.json", text)
            self.assertIn("installed `bsg` skill", text)

    def test_init_preserves_existing_instructions_byte_for_byte(self):
        with temporary_project() as tmp:
            root = Path(tmp)
            original = "# Project rules\r\nKeep café names intact.\r\n".encode("utf-8")
            (root / "AGENTS.md").write_bytes(original)
            bsg.init(root, "Existing app")
            result = (root / "AGENTS.md").read_bytes()
            self.assertTrue(result.startswith(original))
            self.assertEqual(1, result.count(b"<!-- BSG:BEGIN -->"))

    def test_attach_preserves_records_and_customized_handoff(self):
        with temporary_project() as tmp:
            root = Path(tmp)
            bsg.init(root, "Earlier BSG project")
            (root / "AGENTS.md").unlink()
            records = {p: p.read_bytes() for p in (root / ".planning").rglob("*") if p.is_file()}
            bsg.attach(root)
            path = root / "AGENTS.md"
            customized = path.read_bytes().replace(b"## BSG project workflow", b"## Our customized workflow")
            path.write_bytes(customized)
            bsg.attach(root)
            self.assertEqual(customized, path.read_bytes())
            self.assertEqual(records, {p: p.read_bytes() for p in records})

    def test_malformed_handoff_prevents_partial_initialization(self):
        with temporary_project() as tmp:
            root = Path(tmp)
            original = b"User rules\n<!-- BSG:BEGIN -->\nIncomplete block"
            (root / "AGENTS.md").write_bytes(original)
            with self.assertRaises(ValueError):
                bsg.init(root, "Example")
            self.assertFalse((root / ".planning").exists())
            self.assertEqual(original, (root / "AGENTS.md").read_bytes())

    def test_attach_requires_existing_bsg_project(self):
        with temporary_project() as tmp:
            root = Path(tmp)
            with self.assertRaises(OSError):
                bsg.attach(root)
            self.assertFalse((root / "AGENTS.md").exists())

    def test_agents_md_alone_serves_both_hosts(self):
        with temporary_project() as tmp:
            root = Path(tmp)
            bsg.init(root, "Codex or Claude")
            self.assertTrue((root / "AGENTS.md").exists())
            self.assertFalse((root / "CLAUDE.md").exists())

    def test_existing_claude_md_also_receives_handoff(self):
        for existing in ("CLAUDE.md", ".claude/CLAUDE.md", "CLAUDE.local.md"):
            with temporary_project() as tmp:
                root = Path(tmp)
                original = b"# Claude rules\nUse tabs.\n"
                (root / existing).parent.mkdir(parents=True, exist_ok=True)
                (root / existing).write_bytes(original)
                bsg.init(root, "Claude project")
                for name in ("AGENTS.md", "CLAUDE.md"):
                    self.assertEqual(1, (root / name).read_bytes().count(b"<!-- BSG:BEGIN -->"), (existing, name))
                if existing == "CLAUDE.md":
                    self.assertTrue((root / "CLAUDE.md").read_bytes().startswith(original))
                else:
                    self.assertEqual(original, (root / existing).read_bytes())

    def test_pre_release_markers_count_as_attached(self):
        with temporary_project() as tmp:
            root = Path(tmp)
            legacy = b"# Rules\n<!-- BSD:BEGIN -->\nold block\n<!-- BSD:END -->\n"
            (root / "AGENTS.md").write_bytes(legacy)
            bsg.init(root, "Older project")
            self.assertEqual(legacy, (root / "AGENTS.md").read_bytes())

    def test_malformed_claude_md_prevents_any_handoff_write(self):
        with temporary_project() as tmp:
            root = Path(tmp)
            (root / "CLAUDE.md").write_bytes(b"<!-- BSG:END -->\n<!-- BSG:BEGIN -->")
            with self.assertRaises(ValueError):
                bsg.init(root, "Example")
            self.assertFalse((root / "AGENTS.md").exists())
            self.assertFalse((root / ".planning").exists())


class Installation(unittest.TestCase):
    def test_single_skill_and_five_command_menu(self):
        self.assertEqual({"start", "help", "status", "pause [ID]", "resume"}, set(bsg.COMMANDS))
        with temporary_project() as tmp:
            root = Path(tmp)
            installer.install(BASE / "skills", root, "codex")
            self.assertEqual(["bsg"], sorted(p.name for p in (root / ".agents/skills").iterdir()))
            self.assertFalse((root / ".claude").exists())
            output, code = bsg.report(root, True)
            self.assertEqual(0, code)
            self.assertIn("BSG start", output)
            self.assertNotIn("$bsg-", output)

    def test_fresh_project_gets_both_hosts_by_default(self):
        with temporary_project() as tmp:
            root = Path(tmp)
            count = installer.install(BASE / "skills", root)
            self.assertTrue((root / ".agents/skills/bsg/SKILL.md").is_file())
            self.assertTrue((root / ".claude/skills/bsg/SKILL.md").is_file())
            self.assertEqual(0, count % 2)

    def test_auto_detects_existing_host_folder(self):
        for folder, expected, absent in ((".claude", ".claude/skills", ".agents"), (".agents", ".agents/skills", ".claude")):
            with temporary_project() as tmp:
                root = Path(tmp)
                (root / folder).mkdir()
                installer.install(BASE / "skills", root)
                self.assertTrue((root / expected / "bsg/SKILL.md").is_file())
                self.assertFalse((root / absent).exists())

    def test_plugin_manifest_matches_skill(self):
        import json
        plugin = json.loads((BASE / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
        marketplace = json.loads((BASE / ".claude-plugin/marketplace.json").read_text(encoding="utf-8"))
        self.assertEqual("bsg", plugin["name"])
        self.assertEqual(["bsg"], [p["name"] for p in marketplace["plugins"]])
        self.assertEqual(".", marketplace["plugins"][0]["source"])
        self.assertTrue((BASE / "skills/bsg/SKILL.md").is_file())

    def test_install_is_idempotent_and_preserves_modified_files(self):
        with temporary_project() as tmp:
            root = Path(tmp)
            self.assertGreater(installer.install(BASE / "skills", root, "claude"), 0)
            self.assertEqual(0, installer.install(BASE / "skills", root, "claude"))
            target = root / ".claude/skills/bsg/SKILL.md"
            target.write_text("User changes", encoding="utf-8")
            with self.assertRaises(ValueError):
                installer.install(BASE / "skills", root, "claude")
            self.assertEqual("User changes", target.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
