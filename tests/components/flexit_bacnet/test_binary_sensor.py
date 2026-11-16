"""Tests for the Flexit Nordic (BACnet) binary sensor entities."""

from unittest.mock import AsyncMock

from pytest_universalassistant.common import MockConfigEntry, snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.const import Platform
from universalassistant.core import UniversalAssistant
from universalassistant.helpers import entity_registry as er

from . import setup_with_selected_platforms


async def test_binary_sensors(
    hass: UniversalAssistant,
    snapshot: SnapshotAssertion,
    entity_registry: er.EntityRegistry,
    mock_flexit_bacnet: AsyncMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test binary sensor states are correctly collected from library."""

    await setup_with_selected_platforms(
        hass, mock_config_entry, [Platform.BINARY_SENSOR]
    )
    await snapshot_platform(hass, entity_registry, snapshot, mock_config_entry.entry_id)
