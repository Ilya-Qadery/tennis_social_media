"""
Pytest fixtures for Varzesha project.
"""
import pytest
from rest_framework.test import APIClient

from varzesha.users.models import BaseUser


@pytest.fixture
def api_client():
    """Return an API client for testing."""
    return APIClient()


@pytest.fixture
def authenticated_client(api_client):
    """Return an authenticated API client."""
    user = BaseUser.objects.create_user(
        phone="09123456789",
        password="testpass123",
        is_phone_verified=True,
    )
    api_client.force_authenticate(user=user)
    return api_client, user


@pytest.fixture
def test_user():
    """Create and return a test user."""
    return BaseUser.objects.create_user(
        phone="09123456788",
        password="testpass123",
        is_phone_verified=True,
        first_name="Test",
        last_name="User",
    )


@pytest.fixture
def test_coach():
    """Create and return a test coach user."""
    user = BaseUser.objects.create_user(
        phone="09123456787",
        password="testpass123",
        is_phone_verified=True,
        is_coach=True,
        first_name="Coach",
        last_name="Test",
    )
    return user
