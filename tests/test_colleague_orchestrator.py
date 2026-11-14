"""
Unit tests for ColleagueOrchestrator and specialized AI colleagues.
"""

import unittest
from src.colleague_orchestrator import ColleagueOrchestrator, Colleague

class TestColleagueOrchestrator(unittest.TestCase):
    def setUp(self):
        self.orchestrator = ColleagueOrchestrator()

    def test_colleague_initialization(self):
        expected_roles = {"research", "content", "outbound", "support", "verification"}
        self.assertEqual(set(self.orchestrator.colleagues.keys()), expected_roles)

    def test_default_dispatch_workflow(self):
        trace = self.orchestrator.dispatch_workflow("Audit competitive landscape")
        self.assertIn("workflow_id", trace)
        self.assertEqual(trace["colleagues_involved"], 3)  # default roles: research, content, verification
        self.assertEqual(len(trace["subtask_results"]), 3)
        self.assertGreater(trace["total_cu"], 0.0)
        self.assertGreater(trace["latency_ms"], 0.0)
        self.assertIn("confidence", trace)

    def test_custom_roles_dispatch(self):
        roles = ["outbound", "support"]
        trace = self.orchestrator.dispatch_workflow("Engage community", roles=roles)
        self.assertEqual(trace["call_chain"], roles)
        self.assertEqual(trace["colleagues_involved"], 2)

    def test_subtask_execution_increments_counter(self):
        colleague = self.orchestrator.colleagues["research"]
        initial_count = colleague.tasks_completed
        res = colleague.execute_subtask("Find DoraHacks AI trends", {})
        self.assertEqual(colleague.tasks_completed, initial_count + 1)
        self.assertIn("cu_used", res)
        self.assertIn("generated_artifacts", res)

if __name__ == "__main__":
    unittest.main()
