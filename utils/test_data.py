"""
test_data.py

Generates clearly-identifiable, unique test employee names so that:
  1. Automation runs never collide with each other or with real data.
  2. Anyone reviewing the Employee List can immediately tell which
     rows were created by this test suite (per the assignment's
     instruction to use "clearly identifiable test data").
"""

import random
import string
import time


def _run_tag():
    """Short tag unique to this test run (timestamp-based)."""
    return str(int(time.time()))[-6:]


def generate_employee_names(count=4):
    """
    Returns a list of (first_name, last_name) tuples like:
    ("QA-482913-1", "AutoTest")
    """
    tag = _run_tag()
    return [(f"QA-{tag}-{i+1}", "AutoTest") for i in range(count)]


def random_suffix(length=4):
    return "".join(random.choices(string.ascii_uppercase, k=length))
