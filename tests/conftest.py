# File: tests/conftest.py
# Pytest configuration with fixtures for proper test isolation. Ensures
# all tests start with clean state using proper reset mechanisms.
# All Rights Reserved Arodi Emmanuel

import sys
from pathlib import Path

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest


@pytest.fixture(autouse=True, scope='function')
def reset_engine_state():
    """Reset all engine state before each test."""
    # Import and reset before test
    from app.infra.bridge import reset
    reset()

    # Import all commands to ensure registration
    import app.commands  # noqa: F401

    yield

    # Reset after test
    reset()
