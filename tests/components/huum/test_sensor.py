"""Tests for the Huum sensor entity."""

import pytest
from pytest_universalassistant.common import MockConfigEntry, snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.const import Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import entity_registry as er


@pytest.fixture
def platforms() -> list[Platform]:
    """Fixture to specify platforms to test."""
    return [Platform.SENSOR]


@pytest.mark.usefixtures("init_integration")
async def test_sensor(
    hass: __HAC_KEEP__,
    mock_config_entry: MockConfigEntry,
    snapshot: SnapshotAssertion,
    entity_registry: er.EntityRegistry,
) -> None:
    """Test the temperature sensor."""
    await snapshot_platform(hass, entity_registry, snapshot, mock_config_entry.entry_id)
