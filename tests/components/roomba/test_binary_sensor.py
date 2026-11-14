"""Tests for the Roomba binary sensor platform."""

from unittest.mock import AsyncMock, patch

import pytest
from pytest_universalassistant.common import MockConfigEntry, snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.const import STATE_OFF, STATE_ON, Platform
from universalassistant.core import UniversalAssistant
from universalassistant.helpers import entity_registry as er


@pytest.mark.usefixtures("entity_registry_enabled_by_default")
async def test_entities(
    hass: UniversalAssistant,
    mock_config_entry: MockConfigEntry,
    mock_roomba: AsyncMock,
    snapshot: SnapshotAssertion,
    entity_registry: er.EntityRegistry,
) -> None:
    """Test roomba binary sensor entities."""
    with patch("universalassistant.components.roomba.PLATFORMS", [Platform.BINARY_SENSOR]):
        mock_config_entry.add_to_hass(hass)
        await hass.config_entries.async_setup(mock_config_entry.entry_id)
        await hass.async_block_till_done()

    await snapshot_platform(hass, entity_registry, snapshot, mock_config_entry.entry_id)


@pytest.mark.parametrize(
    ("phase", "expected"),
    [
        ("charge", STATE_ON),
        ("run", STATE_OFF),
    ],
)
async def test_charging(
    hass: UniversalAssistant,
    mock_config_entry: MockConfigEntry,
    mock_roomba: AsyncMock,
    phase: str,
    expected: str,
) -> None:
    """Test the charging binary sensor reflects the dock charge phase."""
    mock_roomba.master_state["state"]["reported"]["cleanMissionStatus"]["phase"] = phase

    with patch("universalassistant.components.roomba.PLATFORMS", [Platform.BINARY_SENSOR]):
        mock_config_entry.add_to_hass(hass)
        await hass.config_entries.async_setup(mock_config_entry.entry_id)
        await hass.async_block_till_done()

    state = hass.states.get("binary_sensor.test_roomba_charging")
    assert state is not None
    assert state.state == expected
