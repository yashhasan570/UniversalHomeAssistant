"""Fixtures for Hanna Instruments integration tests."""

from unittest.mock import patch

import pytest
from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.hanna.const import DOMAIN
from universalassistant.const import CONF_EMAIL, CONF_PASSWORD


@pytest.fixture
def mock_setup_entry():
    """Mock setting up a config entry."""
    with patch("universalassistant.components.hanna.async_setup_entry", return_value=None):
        yield


@pytest.fixture
def mock_hanna_client():
    """Mock HannaCloudClient."""
    with (
        patch(
            "universalassistant.components.hanna.config_flow.HannaCloudClient", autospec=True
        ) as mock_client,
        patch("universalassistant.components.hanna.HannaCloudClient", new=mock_client),
    ):
        client = mock_client.return_value
        yield client


@pytest.fixture
def mock_config_entry() -> MockConfigEntry:
    """Mock a config entry."""
    return MockConfigEntry(
        domain=DOMAIN,
        data={CONF_EMAIL: "test@example.com", CONF_PASSWORD: "test-password"},
        title="test@example.com",
        unique_id="test@example.com",
    )
