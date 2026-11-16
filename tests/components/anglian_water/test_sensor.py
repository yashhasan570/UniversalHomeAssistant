"""Test Anglian Water sensors."""

from unittest.mock import AsyncMock, patch

from pytest_universalassistant.common import MockConfigEntry, snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.recorder import Recorder
from universalassistant.const import Platform
from universalassistant.core import UniversalAssistant
from universalassistant.helpers import entity_registry as er

from . import setup_integration


async def test_sensor(
    recorder_mock: Recorder,
    hass: UniversalAssistant,
    mock_config_entry: MockConfigEntry,
    mock_anglian_water_client: AsyncMock,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test sensor platform."""
    with patch(
        "universalassistant.components.anglian_water._PLATFORMS",
        [Platform.SENSOR],
    ):
        await setup_integration(hass, mock_config_entry)

    await snapshot_platform(hass, entity_registry, snapshot, mock_config_entry.entry_id)
