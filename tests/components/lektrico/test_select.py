"""Tests for the Lektrico select platform."""

from unittest.mock import AsyncMock, patch

from pytest_universalassistant.common import MockConfigEntry, snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.const import Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import entity_registry as er

from . import setup_integration


async def test_all_entities(
    hass: __HAC_KEEP__,
    snapshot: SnapshotAssertion,
    mock_device: AsyncMock,
    mock_config_entry: MockConfigEntry,
    entity_registry: er.EntityRegistry,
) -> None:
    """Test all entities."""
    with patch.multiple(
        "universalassistant.components.lektrico",
        CHARGERS_PLATFORMS=[Platform.SELECT],
        LB_DEVICES_PLATFORMS=[Platform.SELECT],
    ):
        await setup_integration(hass, mock_config_entry)

    await snapshot_platform(hass, entity_registry, snapshot, mock_config_entry.entry_id)
