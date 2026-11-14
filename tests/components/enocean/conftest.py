"""Fixtures for EnOcean integration tests."""

from typing import Final

import pytest
from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.enocean.const import DOMAIN
from universalassistant.const import CONF_DEVICE

ENTRY_CONFIG: Final[dict[str, str]] = {
    CONF_DEVICE: "/dev/ttyUSB0",
}


@pytest.fixture
def mock_config_entry() -> MockConfigEntry:
    """Return the default mocked config entry."""
    return MockConfigEntry(
        domain=DOMAIN,
        unique_id="device_chip_id",
        data=ENTRY_CONFIG,
    )
