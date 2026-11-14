"""Tests for the Zinvolt binary sensor."""

from unittest.mock import AsyncMock, patch

from pytest_universalassistant.common import (
    MockConfigEntry,
    async_load_fixture,
    snapshot_platform,
)
from syrupy.assertion import SnapshotAssertion
from zinvolt.models import BatteryState

from universalassistant.components.zinvolt.const import DOMAIN
from universalassistant.const import STATE_UNAVAILABLE, Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import entity_registry as er

from . import setup_integration


async def test_all_entities(
    hass: __HAC_KEEP__,
    snapshot: SnapshotAssertion,
    mock_zinvolt_client: AsyncMock,
    mock_config_entry: MockConfigEntry,
    entity_registry: er.EntityRegistry,
) -> None:
    """Test all entities."""
    with patch("universalassistant.components.zinvolt._PLATFORMS", [Platform.BINARY_SENSOR]):
        await setup_integration(hass, mock_config_entry)

    await snapshot_platform(hass, entity_registry, snapshot, mock_config_entry.entry_id)


async def test_offline_battery_on_grid_unknown(
    hass: __HAC_KEEP__,
    mock_zinvolt_client: AsyncMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """on_grid is unknown when the battery is offline."""
    mock_zinvolt_client.get_battery_status.return_value = BatteryState.from_json(
        await async_load_fixture(hass, "current_state_offline.json", DOMAIN)
    )
    await setup_integration(hass, mock_config_entry)

    assert (
        hass.states.get("binary_sensor.zinvolt_batterij_grid_connection").state
        == STATE_UNAVAILABLE
    )
