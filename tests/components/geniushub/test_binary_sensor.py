"""Tests for the Geniushub binary sensor platform."""

from unittest.mock import patch

import pytest
from pytest_universalassistant.common import MockConfigEntry, snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.const import Platform
from universalassistant.core import UniversalAssistant
from universalassistant.helpers import entity_registry as er

from . import setup_integration


@pytest.mark.usefixtures("mock_geniushub_cloud")
async def test_cloud_all_sensors(
    hass: UniversalAssistant,
    mock_cloud_config_entry: MockConfigEntry,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test the creation of the Genius Hub binary sensors."""
    with patch(
        "universalassistant.components.geniushub.PLATFORMS", [Platform.BINARY_SENSOR]
    ):
        await setup_integration(hass, mock_cloud_config_entry)

    await snapshot_platform(
        hass, entity_registry, snapshot, mock_cloud_config_entry.entry_id
    )
