"""Tests for the Vizio sensor platform."""

from collections.abc import Generator
from datetime import timedelta
from unittest.mock import patch

from freezegun.api import FrozenDateTimeFactory
import pytest
from pytest_universalassistant.common import (
    MockConfigEntry,
    async_fire_time_changed,
    snapshot_platform,
)
from syrupy.assertion import SnapshotAssertion

from universalassistant.const import STATE_UNKNOWN, Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import entity_registry as er

from .conftest import setup_integration

BATTERY_ENTITY_ID = "sensor.vizio_battery"


@pytest.fixture(autouse=True)
def sensor_only() -> Generator[None]:
    """Only set up the sensor platform."""
    with patch(
        "universalassistant.components.vizio.PLATFORMS",
        [Platform.SENSOR],
    ):
        yield


@pytest.mark.usefixtures("vizio_connect", "vizio_update", "vizio_battery")
async def test_sensor_entity_setup(
    hass: __HAC_KEEP__,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
    mock_crave_config_entry: MockConfigEntry,
) -> None:
    """Test the battery sensor is created for a Crave device."""
    await setup_integration(hass, mock_crave_config_entry)
    await snapshot_platform(
        hass, entity_registry, snapshot, mock_crave_config_entry.entry_id
    )


@pytest.mark.usefixtures("vizio_connect", "vizio_update", "vizio_battery")
async def test_sensor_values(
    hass: __HAC_KEEP__, mock_crave_config_entry: MockConfigEntry
) -> None:
    """Test battery sensor value."""
    await setup_integration(hass, mock_crave_config_entry)

    assert hass.states.get(BATTERY_ENTITY_ID).state == "80"


@pytest.mark.usefixtures("vizio_connect", "vizio_update", "vizio_battery")
async def test_sensor_values_unavailable_data(
    hass: __HAC_KEEP__,
    mock_crave_config_entry: MockConfigEntry,
    freezer: FrozenDateTimeFactory,
) -> None:
    """Test the battery sensor reports unknown when the device is off."""
    await setup_integration(hass, mock_crave_config_entry)

    with patch(
        "universalassistant.components.vizio.Vizio.get_power_state",
        return_value=False,
    ):
        freezer.tick(timedelta(minutes=1))
        async_fire_time_changed(hass)
        await hass.async_block_till_done()

    assert hass.states.get(BATTERY_ENTITY_ID).state == STATE_UNKNOWN


@pytest.mark.usefixtures("vizio_connect", "vizio_update")
async def test_no_sensors_for_soundbar(
    hass: __HAC_KEEP__, mock_speaker_config_entry: MockConfigEntry
) -> None:
    """Test no battery sensor is created for a soundbar."""
    await setup_integration(hass, mock_speaker_config_entry)

    assert hass.states.get(BATTERY_ENTITY_ID) is None
