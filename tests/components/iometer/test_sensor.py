"""Test the sensors provided by the Powerfox integration."""

from unittest.mock import MagicMock

import pytest
from pytest_universalassistant.common import MockConfigEntry, snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.const import Platform
from universalassistant.core import UniversalAssistant
from universalassistant.helpers import entity_registry as er

from . import setup_platform


@pytest.mark.usefixtures("entity_registry_enabled_by_default")
async def test_all_sensors(
    hass: UniversalAssistant,
    mock_iometer_client: MagicMock,
    mock_config_entry: MockConfigEntry,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test the Iometer sensors."""
    await setup_platform(hass, mock_config_entry, [Platform.SENSOR])

    await snapshot_platform(hass, entity_registry, snapshot, mock_config_entry.entry_id)
