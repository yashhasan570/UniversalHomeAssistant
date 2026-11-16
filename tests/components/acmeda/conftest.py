"""Define fixtures available for all Acmeda tests."""

from collections.abc import Generator
from unittest.mock import AsyncMock, patch

import pytest
from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.acmeda.const import DOMAIN
from universalassistant.const import CONF_HOST
from universalassistant.core import UniversalAssistant


@pytest.fixture
def mock_config_entry(hass: UniversalAssistant) -> MockConfigEntry:
    """Return the default mocked config entry."""
    mock_config_entry = MockConfigEntry(
        domain=DOMAIN,
        data={CONF_HOST: "127.0.0.1"},
    )
    mock_config_entry.add_to_hass(hass)
    return mock_config_entry


@pytest.fixture
def mock_hub_run() -> Generator[AsyncMock]:
    """Mock the hub run method."""
    with patch("universalassistant.components.acmeda.hub.aiopulse.Hub.run") as mock_run:
        yield mock_run
