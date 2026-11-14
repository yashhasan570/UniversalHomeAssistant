"""Fixtures for Freedompro integration tests."""

from collections.abc import Generator
from copy import deepcopy
from typing import Any
from unittest.mock import AsyncMock, patch

import pytest
from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.freedompro.const import DOMAIN
from universalassistant.core import __HAC_KEEP__

from .const import DEVICES, DEVICES_STATE


@pytest.fixture
def mock_setup_entry() -> Generator[AsyncMock]:
    """Override async_setup_entry."""
    with patch(
        "universalassistant.components.freedompro.async_setup_entry", return_value=None
    ) as mock_setup_entry:
        yield mock_setup_entry


@pytest.fixture(autouse=True)
def mock_freedompro():
    """Mock freedompro get_list and get_states."""
    with (
        patch(
            "universalassistant.components.freedompro.coordinator.get_list",
            return_value={
                "state": True,
                "devices": DEVICES,
            },
        ),
        patch(
            "universalassistant.components.freedompro.coordinator.get_states",
            return_value=DEVICES_STATE,
        ),
    ):
        yield


@pytest.fixture
async def init_integration(hass: __HAC_KEEP__) -> MockConfigEntry:
    """Set up the Freedompro integration in __HA_KEEP__."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        title="Feedompro",
        unique_id="0123456",
        data={
            "api_key": "gdhsksjdhcncjdkdjndjdkdmndjdjdkd",
        },
    )

    entry.add_to_hass(hass)
    await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    return entry


@pytest.fixture
async def init_integration_no_state(hass: __HAC_KEEP__) -> MockConfigEntry:
    """Set up the Freedompro integration in __HA_KEEP__ without state."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        title="Feedompro",
        unique_id="0123456",
        data={
            "api_key": "gdhsksjdhcncjdkdjndjdkdmndjdjdkd",
        },
    )

    with (
        patch(
            "universalassistant.components.freedompro.coordinator.get_list",
            return_value={
                "state": True,
                "devices": DEVICES,
            },
        ),
        patch(
            "universalassistant.components.freedompro.coordinator.get_states",
            return_value=[],
        ),
    ):
        entry.add_to_hass(hass)
        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    return entry


def get_states_response_for_uid(uid: str) -> list[dict[str, Any]]:
    """Return a deepcopy of the device state list for specific uid."""
    return deepcopy([resp for resp in DEVICES_STATE if resp["uid"] == uid])
