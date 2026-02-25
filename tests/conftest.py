"""Shared test fixtures for the Runbook Agent."""

import os
import sys

# Add src/ to path so tests can import modules directly
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import _chromadb_compat  # noqa: F401 — must be before chromadb
import pytest


@pytest.fixture(scope="session")
def project_root():
    """Return the project root directory."""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture(scope="session")
def runbooks_dir(project_root):
    """Return the runbooks directory path."""
    return os.path.join(project_root, "runbooks")


@pytest.fixture(scope="session")
def sample_runbook_text():
    """Return sample runbook markdown for testing."""
    return """# RB-999: Test Runbook

## Category

Testing

## Symptoms

- Test symptom one
- Test symptom two

## Prerequisites

- Test prerequisite

## Resolution Steps

1. First step of resolution.

2. Second step of resolution.

3. Third step of resolution.

## Escalation Criteria

- Escalate if steps fail

## Related Runbooks

- RB-001
"""
