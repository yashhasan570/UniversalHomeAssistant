"""Test the System Nexa 2 sensor platform."""

from unittest.mock import patch

import pytest
from pytest_universalassistant.common import MockConfigEntry, snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.const import Platform
from universalassistant.core import __HAC_KEEP__
import universalassistant.helpers.entity_registry as er


@pytest.mark.usefixtures("mock_system_nexa_2_device")
@pytest.mark.usefixtures("entity_registry_enabled_by_default")
async def test_sensor_entities(
    hass: __HAC_KEEP__,
    snapshot: SnapshotAssertion,
    entity_registry: er.EntityRegistry,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test the sensor entities."""
    mock_config_entry.add_to_hass(hass)

    # Only load the sensor platform for snapshot testing
    with patch(
        "universalassistant.components.systemnexa2.PLATFORMS",
        [Platform.SENSOR],
    ):
        await hass.config_entries.async_setup(mock_config_entry.entry_id)
        await snapshot_platform(
            hass, entity_registry, snapshot, mock_config_entry.entry_id
        )
