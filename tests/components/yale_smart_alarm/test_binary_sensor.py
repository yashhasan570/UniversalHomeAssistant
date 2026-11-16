"""The test for the Yale Smart Alarm binary sensor platform."""

from unittest.mock import Mock

import pytest
from pytest_universalassistant.common import MockConfigEntry, snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.const import Platform
from universalassistant.core import UniversalAssistant
from universalassistant.helpers import entity_registry as er


@pytest.mark.parametrize(
    "load_platforms",
    [[Platform.BINARY_SENSOR]],
)
async def test_binary_sensor(
    hass: UniversalAssistant,
    load_config_entry: tuple[MockConfigEntry, Mock],
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test the Yale Smart Alarm binary sensor."""
    entry = load_config_entry[0]
    await snapshot_platform(hass, entity_registry, snapshot, entry.entry_id)
