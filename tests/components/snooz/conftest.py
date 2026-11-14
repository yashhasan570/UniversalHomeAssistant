"""Snooz test fixtures and configuration."""

import pytest

from universalassistant.core import __HAC_KEEP__

from . import SnoozFixture, create_mock_snooz, create_mock_snooz_config_entry


@pytest.fixture(autouse=True)
def mock_bluetooth(enable_bluetooth: None) -> None:
    """Auto mock bluetooth."""


@pytest.fixture
async def mock_connected_snooz(hass: __HAC_KEEP__):
    """Mock a Snooz configuration entry and device."""

    device = await create_mock_snooz()
    entry = await create_mock_snooz_config_entry(hass, device)

    return SnoozFixture(entry, device)
