"""Test the MELCloud binary sensor platform."""

import pytest
from pytest_universalassistant.common import MockConfigEntry, snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.const import Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import entity_registry as er

from . import setup_platform


@pytest.mark.usefixtures("entity_registry_enabled_by_default", "mock_get_devices")
async def test_all_entities(
    hass: __HAC_KEEP__,
    snapshot: SnapshotAssertion,
    mock_config_entry: MockConfigEntry,
    entity_registry: er.EntityRegistry,
) -> None:
    """Test all binary sensor entities with snapshot."""
    await setup_platform(hass, mock_config_entry, [Platform.BINARY_SENSOR])
    await snapshot_platform(hass, entity_registry, snapshot, mock_config_entry.entry_id)
