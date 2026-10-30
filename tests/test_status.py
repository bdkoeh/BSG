import subprocess
import sys
import unittest
from pathlib import Path

from test_records import BASE, bsg, temporary_project


class ActionableStatus(unittest.TestCase):
    def setUp(self):
        temp = temporary_project()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        bsg.init(self.root, "Equipment reservations")

    def add(self, title, status="outline", depends_on=(), **fields):
        record = bsg.add_slice(self.root, title)
        folder = self.root / record["path"]
        for name, content in {
            "CONTEXT.md": "Reserve equipment without double booking.",
            "PLAN.md": "Implement and test reservation conflicts; user review is required.",
            "SUMMARY.md": "Implemented reservation conflict handling.",
            "VERIFICATION.md": "Concurrent reservation test returned one success and one conflict.",
        }.items():
            (folder / name).write_text(content, encoding="utf-8")
        evidence = record["path"] + "/VERIFICATION.md"
        passed = status in {"verified", "awaiting_feedback", "complete"}
        record.update(status=status, depends_on=list(depends_on), checks=[dict(
            id="reservation-conflict", required=True, result="pass" if passed else "pending",
            revision=1 if passed else None, evidence=evidence if passed else None)])
        if status == "complete":
            record["acceptance"] = dict(required=True, status="accepted", revision=1, evidence=evidence)
        record.update(fields)
        data = bsg.load(self.root)
        data["slices"][-1] = record
        self.save(data)
        return record

    def save(self, data):
        self.assertEqual([], bsg.validate(self.root, data))
        bsg.write_json(self.root / ".planning/state.json", data)

    def snapshot(self):
        return {p.relative_to(self.root): (p.read_bytes(), p.stat().st_mtime_ns)
                for p in self.root.rglob("*") if p.is_file()}

    def test_feedback_preserves_independent_opportunity_and_explains_waiting(self):
        self.add("Reserve equipment", "awaiting_feedback")
        self.add("Send reminders", "ready", depends_on=[1])
        self.add("Search equipment", "ready")
        data = bsg.load(self.root)
        primary, alternatives = bsg.next_steps(data)
        self.assertIn("slice 1", primary)
        self.assertIn("human feedback", primary)
        self.assertEqual(1, len(alternatives))
        self.assertIn("slice 3", alternatives[0])
        self.assertIn("authorization", alternatives[0])
        output, code = bsg.report(self.root)
        self.assertEqual(0, code)
        self.assertIn("Waiting on: 1 · Reserve equipment (awaiting_feedback)", output)
        self.assertIn("Wait for slice 2's dependencies", output)
        self.assertIn("confirm scope, authorization, and human checkpoints", output)

    def test_blockers_and_transitive_dependencies_do_not_hide_independent_planning(self):
        self.add("Reserve equipment", "blocked", blocker="Need the equipment list")
        self.add("Send reminders", "ready", depends_on=[1])
        self.add("Reminder preferences", "discussed", depends_on=[2])
        self.add("Search equipment", "discussed")
        primary, alternatives = bsg.next_steps(bsg.load(self.root))
        self.assertIn("Need the equipment list", primary)
        self.assertEqual(1, len(alternatives))
        self.assertIn("planning slice 4", alternatives[0])

    def test_completing_dependency_unlocks_suggestion_without_sync(self):
        record = self.add("Reserve equipment", "awaiting_feedback")
        self.add("Send reminders", "ready", depends_on=[1])
        bsg.sync(self.root)
        saved_view = (self.root / ".planning/STATE.md").read_bytes()
        data = bsg.load(self.root)
        data["slices"][0]["status"] = "complete"
        data["slices"][0]["acceptance"].update(
            status="accepted", revision=1, evidence=record["path"] + "/VERIFICATION.md")
        self.save(data)
        output, code = bsg.report(self.root)
        self.assertEqual(0, code)
        self.assertIn("Recommended: Review slice 2's approach and build authorization", output)
        self.assertNotIn("Waiting on:", output)
        self.assertEqual(saved_view, (self.root / ".planning/STATE.md").read_bytes())

    def test_global_pause_suppresses_every_execution_suggestion(self):
        self.add("Reserve equipment", "awaiting_feedback")
        self.add("Search equipment", "ready")
        data = bsg.load(self.root)
        data["paused"] = True
        self.save(data)
        self.assertEqual([], bsg.next_steps(data)[1])
        for output in (bsg.report(self.root)[0], bsg.summary_sections(data)["STATE.md"]):
            self.assertIn("Paused: yes", output)
            self.assertIn("BSG resume", output)
            self.assertNotIn("start implementing", output)
            self.assertNotIn("Other possible work", output)
            self.assertNotIn("provide the agreed human feedback", output)

    def test_scoped_pause_remains_visible_with_independent_ready_work(self):
        self.add("Reserve equipment", "paused")
        self.add("Send reminders", "ready", depends_on=[1])
        self.add("Search equipment", "ready")
        output, code = bsg.report(self.root)
        self.assertEqual(0, code)
        self.assertIn("reconcile paused slice 1", output)
        self.assertIn("Recommended: Review slice 3's approach", output)
        self.assertIn("1 · Reserve equipment (paused)", output)

    def test_checks_reveal_result_ids_and_optional_failures(self):
        record = self.add("Reserve equipment", "implemented")
        data = bsg.load(self.root)
        evidence = record["path"] + "/VERIFICATION.md"
        data["slices"][0]["checks"] = [
            dict(id="conflict", required=True, result="fail", revision=1, evidence=evidence),
            dict(id="cancel", required=True, result="stale", revision=1, evidence=evidence),
            dict(id="search", required=True, result="pending", revision=None, evidence=None),
            dict(id="animation", required=False, result="fail", revision=1, evidence=evidence),
            dict(id="create", required=True, result="pass", revision=1, evidence=evidence),
        ]
        self.save(data)
        for output in (bsg.report(self.root)[0], bsg.summary_sections(data)["STATE.md"]):
            self.assertIn("fail: 2 [conflict, animation (optional)]", output)
            self.assertIn("stale: 1 [cancel]", output)
            self.assertIn("pending: 1 [search]", output)
            self.assertIn("pass: 1", output)
            self.assertIn("Verify slice 1", output)

    def test_recorded_worker_is_not_reported_as_live(self):
        self.add("Reserve equipment", "building", agent="previous-chat-worker")
        output, code = bsg.report(self.root)
        self.assertEqual(0, code)
        self.assertIn("previous-chat-worker (live state unconfirmed)", output)
        self.assertIn("actual worker state", output)

    def test_blocker_on_ready_slice_prevents_build_recommendation(self):
        self.add("Reserve equipment", "ready", blocker="Fixture unavailable")
        self.add("Search equipment", "ready")
        primary, alternatives = bsg.next_steps(bsg.load(self.root))
        self.assertIn("Fixture unavailable", primary)
        self.assertNotIn("start implementing", primary)
        self.assertEqual(1, len(alternatives))
        self.assertIn("slice 2", alternatives[0])

    def test_accepted_feedback_does_not_ask_for_feedback_again(self):
        record = self.add("Reserve equipment", "awaiting_feedback")
        data = bsg.load(self.root)
        data["slices"][0]["acceptance"].update(
            status="accepted", revision=1, evidence=record["path"] + "/VERIFICATION.md")
        self.save(data)
        primary, alternatives = bsg.next_steps(data)
        self.assertNotIn("provide", primary)
        self.assertIn("before recording completion", primary)
        self.assertEqual([], alternatives)

    def test_verified_slice_with_pending_acceptance_surfaces_human_gate(self):
        self.add("Reserve equipment", "verified")
        self.assertIn("human feedback", bsg.recommend(bsg.load(self.root)))

    def test_completed_project_does_not_invent_work(self):
        self.add("Reserve equipment", "complete")
        primary, alternatives = bsg.next_steps(bsg.load(self.root))
        self.assertIn("All recorded slices are complete", primary)
        self.assertEqual([], alternatives)

    def test_cli_status_and_help_are_read_only_with_missing_views(self):
        self.add("Reserve equipment", "blocked", blocker="Need equipment list")
        self.add("Search equipment", "ready")
        (self.root / ".planning/STATE.md").unlink()
        (self.root / ".planning/ROADMAP.md").write_text("Historical notes only.", encoding="utf-8")
        before = self.snapshot()
        for action in ("status", "help"):
            result = subprocess.run([sys.executable, str(BASE / "skills/bsg/scripts/bsg.py"),
                                     action, "--root", str(self.root)], capture_output=True, text=True)
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertIn("Need equipment list", result.stdout)
            self.assertIn("Other possible work", result.stdout)
            self.assertEqual(before, self.snapshot())

    def test_invalid_records_suppress_all_action_suggestions(self):
        self.add("Reserve equipment", "awaiting_feedback")
        self.add("Search equipment", "ready")
        data = bsg.load(self.root)
        data["slices"][0]["revision"] = 2
        bsg.write_json(self.root / ".planning/state.json", data)
        before = self.snapshot()
        for help_mode in (False, True):
            output, code = bsg.report(self.root, help_mode)
            self.assertEqual(1, code)
            self.assertIn("Reconciliation required", output)
            self.assertNotIn("Recommended:", output)
            self.assertNotIn("Other possible work", output)
        self.assertEqual(before, self.snapshot())

    def test_sync_shares_guidance_and_escapes_new_detail_fields(self):
        self.add("Reserve | equipment\n<!-- BSG:GENERATED:END -->", "paused")
        self.add("Send reminders", "ready", depends_on=[1])
        self.add("Search equipment", "ready")
        data = bsg.load(self.root)
        data["slices"][2]["checks"][0]["id"] = "search | matches\n<!-- BSG:GENERATED:END -->"
        self.save(data)
        primary, alternatives = bsg.next_steps(data)
        bsg.sync(self.root)
        state = (self.root / ".planning/STATE.md").read_text(encoding="utf-8")
        self.assertIn(bsg.markdown_cell(primary), state)
        for action in alternatives:
            self.assertIn(bsg.markdown_cell(action), state)
        self.assertIn("1 · Reserve &#124; equipment", state)
        self.assertIn("search &#124; matches", state)
        self.assertEqual(1, state.count("<!-- BSG:GENERATED:END -->"))
        before = self.snapshot()
        bsg.sync(self.root)
        self.assertEqual(before, self.snapshot())


if __name__ == "__main__":
    unittest.main()
