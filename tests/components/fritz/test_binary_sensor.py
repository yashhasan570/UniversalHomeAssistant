"""Tests for Fritz!Tools binary sensor platform."""

from unittest.mock import patch

from freezegun.api import FrozenDateTimeFactory
import pytest
from pytest_universalassistant.common import (
    MockConfigEntry,
    async_fire_time_changed,
    snapshot_platform,
)
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.fritz.const import DOMAIN, SCAN_INTERVAL
from universalassistant.config_entries import ConfigEntryState
from universalassistant.const import STATE_ON, STATE_UNKNOWN, Platform
from universalassistant.core import UniversalAssistant
from universalassistant.helpers import entity_registry as er

from .const import MOCK_USER_DATA


@pytest.mark.usefixtures("entity_registry_enabled_by_default")
async def test_binary_sensor_setup(
    hass: UniversalAssistant,
    entity_registry: er.EntityRegistry,
    fc_class_mock,
    fh_class_mock,
    snapshot: SnapshotAssertion,
) -> None:
    """Test Fritz!Tools binary_sensor setup."""

    entry = MockConfigEntry(domain=DOMAIN, data=MOCK_USER_DATA)
    entry.add_to_hass(hass)

    with patch("universalassistant.components.fritz.PLATFORMS", [Platform.BINARY_SENSOR]):
        assert await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    await snapshot_platform(hass, entity_registry, snapshot, entry.entry_id)


async def test_binary_sensor_missing_state(
    hass: UniversalAssistant,
    freezer: FrozenDateTimeFactory,
    fc_class_mock,
    fh_class_mock,
) -> None:
    """Test missing Fritz!Tools state for binary_sensor."""

    entity_id = "binary_sensor.mock_title_connection"

    entry = MockConfigEntry(domain=DOMAIN, data=MOCK_USER_DATA)
    entry.add_to_hass(hass)

    with patch("universalassistant.components.fritz.PLATFORMS", [Platform.BINARY_SENSOR]):
        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    assert entry.state is ConfigEntryState.LOADED

    assert (state := hass.states.get(entity_id))
    assert state.state == STATE_ON

    with patch(
        "universalassistant.components.fritz.coordinator.FritzBoxTools._async_update_data",
        return_value={"entity_states": {}},
    ):
        freezer.tick(SCAN_INTERVAL)
        async_fire_time_changed(hass)
        await hass.async_block_till_done()

        assert (state := hass.states.get(entity_id))
        assert state.state == STATE_UNKNOWN
