#!/usr/bin/env python3
"""
Test runner for AnnaOps.
Runs all unit test modules in tests/ and reports coverage and pass rate.
"""

import unittest
import sys
import os

def run():
    tests_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tests")
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=tests_dir, pattern="test_*.py")

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    total = result.testsRun
    failed = len(result.failures)
    errors = len(result.errors)
    passed = total - failed - errors

    print("=" * 60)
    print(f"AnnaOps Test Summary: {passed}/{total} Passed ({(passed/total)*100:.1f}%)")
    print("=" * 60)

    if not result.wasSuccessful():
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    run()
