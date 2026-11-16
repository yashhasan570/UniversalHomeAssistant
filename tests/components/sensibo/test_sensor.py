"""The test for the sensibo sensor platform."""

from datetime import timedelta
from unittest.mock import MagicMock

from freezegun.api import FrozenDateTimeFactory
from pysensibo.model import PureAQI
import pytest
from pytest_universalassistant.common import async_fire_time_changed, snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.config_entries import ConfigEntry
from universalassistant.const import STATE_UNKNOWN, Platform
from universalassistant.core import UniversalAssistant
from universalassistant.helpers import entity_registry as er


@pytest.mark.usefixtures("entity_registry_enabled_by_default")
@pytest.mark.parametrize(
    "load_platforms",
    [[Platform.SENSOR]],
)
async def test_sensor(
    hass: UniversalAssistant,
    load_int: ConfigEntry,
    mock_client: MagicMock,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
    freezer: FrozenDateTimeFactory,
) -> None:
    """Test the Sensibo sensor."""

    await snapshot_platform(hass, entity_registry, snapshot, load_int.entry_id)

    mock_client.async_get_devices_data.return_value.parsed[
        "AAZZAAZZ"
    ].pm25_pure = PureAQI(2)

    freezer.tick(timedelta(minutes=5))
    async_fire_time_changed(hass)
    await hass.async_block_till_done()

    state = hass.states.get("sensor.kitchen_kitchen_pure_aqi")
    assert state.state == "moderate"

    mock_client.async_get_devices_data.return_value.parsed[
        "AAZZAAZZ"
    ].pm25_pure = PureAQI(0)

    freezer.tick(timedelta(minutes=5))
    async_fire_time_changed(hass)
    await hass.async_block_till_done()

    state = hass.states.get("sensor.kitchen_kitchen_pure_aqi")
    assert state.state == STATE_UNKNOWN
