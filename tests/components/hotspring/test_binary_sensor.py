"""Tests for the Hot Spring binary sensor platform."""

import pytest
from pytest_universalassistant.common import MockConfigEntry, snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.const import Platform
from universalassistant.core import UniversalAssistant
from universalassistant.helpers import entity_registry as er

from . import setup_with_selected_platforms


@pytest.mark.usefixtures("entity_registry_enabled_by_default", "mock_hotspring")
async def test_binary_sensors(
    hass: UniversalAssistant,
    mock_config_entry: MockConfigEntry,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test the binary sensor platform state."""
    await setup_with_selected_platforms(
        hass, mock_config_entry, [Platform.BINARY_SENSOR]
    )
    await snapshot_platform(hass, entity_registry, snapshot, mock_config_entry.entry_id)
