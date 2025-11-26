"""
Pytest configuration and shared fixtures.
"""

import pytest


@pytest.fixture
def test_user_data() -> dict:
    """Sample user data for testing."""
    return {
        "email": "test@example.com",
        "password": "testpassword123",
    }
