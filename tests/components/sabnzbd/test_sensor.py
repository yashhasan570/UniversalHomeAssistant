"""Sensor tests for the Sabnzbd component."""

from unittest.mock import patch

import pytest
from pytest_universalassistant.common import MockConfigEntry, snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.const import Platform
from universalassistant.core import UniversalAssistant
from universalassistant.helpers import entity_registry as er


@patch("universalassistant.components.sabnzbd.PLATFORMS", [Platform.SENSOR])
@pytest.mark.usefixtures("entity_registry_enabled_by_default")
async def test_sensor(
    hass: UniversalAssistant,
    entity_registry: er.EntityRegistry,
    config_entry: MockConfigEntry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test sensor setup."""
    await hass.config_entries.async_setup(config_entry.entry_id)
    await snapshot_platform(hass, entity_registry, snapshot, config_entry.entry_id)
