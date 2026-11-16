"""Tests for the Stookwijzer sensor platform."""

import pytest
from pytest_universalassistant.common import MockConfigEntry, snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.core import UniversalAssistant
from universalassistant.helpers import entity_registry as er


@pytest.mark.usefixtures("init_integration")
async def test_entities(
    hass: UniversalAssistant,
    mock_config_entry: MockConfigEntry,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test the Stookwijzer entities."""
    await snapshot_platform(hass, entity_registry, snapshot, mock_config_entry.entry_id)
