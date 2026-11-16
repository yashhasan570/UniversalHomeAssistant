"""Tests for the Bosch SHC valve platform."""

from collections.abc import Generator
from unittest.mock import patch

import pytest
from pytest_universalassistant.common import MockConfigEntry

from universalassistant.const import Platform
from universalassistant.core import UniversalAssistant

from .conftest import setup_integration, thermostat_device


@pytest.fixture(autouse=True)
def platforms() -> Generator[None]:
    """Restrict bosch_shc setup to the valve platform."""
    with patch("universalassistant.components.bosch_shc.PLATFORMS", [Platform.VALVE]):
        yield


@pytest.mark.parametrize(
    "device_buckets",
    [{"thermostats": [thermostat_device(position=42)]}],
    indirect=True,
)
@pytest.mark.usefixtures("mock_session")
async def test_thermostat_valve_position(
    hass: UniversalAssistant,
    mock_config_entry: MockConfigEntry,
) -> None:
    """A thermostat's valve tappet position is exposed as a valve entity."""
    await setup_integration(hass, mock_config_entry)

    state = hass.states.get("valve.thermostat_valve")
    assert state is not None
    assert state.attributes["current_position"] == 42
