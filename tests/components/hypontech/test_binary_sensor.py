"""Tests for Hypontech binary sensors."""

from dataclasses import replace
from unittest.mock import AsyncMock, patch

from pytest_universalassistant.common import MockConfigEntry, snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.const import STATE_OFF, Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import entity_registry as er

from . import setup_integration


async def test_binary_sensors(
    hass: __HAC_KEEP__,
    mock_hyponcloud: AsyncMock,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test the Hypontech binary sensors."""
    with patch(
        "universalassistant.components.hypontech._PLATFORMS", [Platform.BINARY_SENSOR]
    ):
        await setup_integration(hass, mock_config_entry)

    await snapshot_platform(hass, entity_registry, snapshot, mock_config_entry.entry_id)


async def test_binary_sensor_unexpected_status(
    hass: __HAC_KEEP__,
    mock_hyponcloud: AsyncMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test the Hypontech binary sensor with an unexpected plant status."""
    mock_hyponcloud.get_list.return_value[0] = replace(
        mock_hyponcloud.get_list.return_value[0],
        status="maintenance",
    )

    with patch(
        "universalassistant.components.hypontech._PLATFORMS", [Platform.BINARY_SENSOR]
    ):
        await setup_integration(hass, mock_config_entry)

    state = hass.states.get("binary_sensor.balcon_connectivity")
    assert state is not None
    assert state.state == STATE_OFF
