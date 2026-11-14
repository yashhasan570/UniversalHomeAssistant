"""Provide common mystrom fixtures and mocks."""

from collections.abc import Generator
from unittest.mock import AsyncMock, patch

import pytest
from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.mystrom.const import DOMAIN
from universalassistant.const import CONF_HOST
from universalassistant.core import __HAC_KEEP__

DEVICE_NAME = "myStrom Device"
DEVICE_MAC = "6001940376EB"


@pytest.fixture
def mock_setup_entry() -> Generator[AsyncMock]:
    """Override async_setup_entry."""
    with patch(
        "universalassistant.components.mystrom.async_setup_entry", return_value=None
    ) as mock_setup_entry:
        yield mock_setup_entry


@pytest.fixture
def config_entry(hass: __HAC_KEEP__) -> MockConfigEntry:
    """Create and add a config entry."""
    config_entry = MockConfigEntry(
        domain=DOMAIN,
        unique_id=DEVICE_MAC,
        data={CONF_HOST: "1.1.1.1"},
        title=DEVICE_NAME,
    )
    config_entry.add_to_hass(hass)
    return config_entry
