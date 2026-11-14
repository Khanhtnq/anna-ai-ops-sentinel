"""
Unit tests for Anna App Manifest Schema 4 validation.
Ensures compliance with Anna OS App specification (anna.partners/developers/apps/app-manifest).
"""

import unittest
import json
import os

class TestManifestSchema(unittest.TestCase):
    def setUp(self):
        self.manifest_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "anna.manifest.json"
        )
        with open(self.manifest_path, "r", encoding="utf-8") as f:
            self.manifest = json.load(f)

    def test_schema_version(self):
        self.assertEqual(self.manifest.get("schema"), 4)

    def test_required_executas(self):
        reqs = self.manifest.get("required_executas", [])
        self.assertIsInstance(reqs, list)
        self.assertGreater(len(reqs), 0)
        tool_ids = [r.get("tool_id") for r in reqs]
        self.assertIn("tool-anna-ops-verification", tool_ids)

    def test_forbidden_legacy_keys(self):
        # schema: 4 forbids legacy fields: permissions, host_capabilities
        self.assertNotIn("permissions", self.manifest)
        self.assertNotIn("host_capabilities", self.manifest)

    def test_ui_bundle_and_views(self):
        ui = self.manifest.get("ui")
        self.assertIsNotNone(ui)
        bundle = ui.get("bundle", {})
        self.assertEqual(bundle.get("format"), "static-spa")
        self.assertEqual(bundle.get("entry"), "index.html")

        views = ui.get("views", [])
        self.assertGreaterEqual(len(views), 1)
        self.assertLessEqual(len(views), 16)
        
        default_views = [v for v in views if v.get("default") is True]
        self.assertEqual(len(default_views), 1, "Exactly one view must be marked default: true")

        # Verify size baselines
        for v in views:
            self.assertIn("name", v)
            self.assertIn("title", v)
            if "min_size" in v:
                self.assertLessEqual(v["min_size"]["h"], 600, "min_size.h must be <= 600 CSS px")
                self.assertLessEqual(v["min_size"]["w"], 1024, "min_size.w should be <= 1024 CSS px")

    def test_system_prompt_addendum(self):
        prompt = self.manifest.get("system_prompt_addendum", "")
        self.assertGreater(len(prompt), 20)
        self.assertLessEqual(len(prompt), 4000)

if __name__ == "__main__":
    unittest.main()
