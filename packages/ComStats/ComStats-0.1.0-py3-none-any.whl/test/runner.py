# tests/runner.py
import unittest
import os
import sys

ROOT_FOLDER = os.path.realpath(os.path.dirname(os.path.realpath(__file__)) + '/../')

sys.path = [ROOT_FOLDER] + sys.path

# import your test modules
import test_stats

# initialize the test suite
loader = unittest.TestLoader()
suite  = unittest.TestSuite()

# add tests to the test suite
suite.addTests(loader.loadTestsFromModule(test_stats))

# initialize a runner, pass it your suite and run it
runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)
