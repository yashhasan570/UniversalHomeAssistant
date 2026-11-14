"""Tests the binary sensors provided by the Garages Amsterdam integration."""

from unittest.mock import AsyncMock, patch

from pytest_universalassistant.common import snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.const import Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import entity_registry as er

from . import setup_integration


async def test_all_binary_sensors(
    hass: __HAC_KEEP__,
    mock_garages_amsterdam: AsyncMock,
    mock_config_entry: AsyncMock,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test all binary sensors."""
    with patch(
        "universalassistant.components.garages_amsterdam.PLATFORMS", [Platform.BINARY_SENSOR]
    ):
        await setup_integration(hass, mock_config_entry)

    await snapshot_platform(hass, entity_registry, snapshot, mock_config_entry.entry_id)
