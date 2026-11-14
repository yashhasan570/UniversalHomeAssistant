"""Test sensor platform."""

from unittest.mock import AsyncMock, patch

from freezegun.api import FrozenDateTimeFactory
from pytest_universalassistant.common import (
    MockConfigEntry,
    async_fire_time_changed,
    snapshot_platform,
)
from syrupy.assertion import SnapshotAssertion

from universalassistant.const import Platform
from universalassistant.core import UniversalAssistant
from universalassistant.helpers import entity_registry as er

from . import setup_integration


async def test_sensor(
    hass: UniversalAssistant,
    mock_config_entry: MockConfigEntry,
    mock_nintendo_client: AsyncMock,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test sensor platform."""
    with patch(
        "universalassistant.components.nintendo_parental_controls._PLATFORMS",
        [Platform.SENSOR],
    ):
        await setup_integration(hass, mock_config_entry)

    await snapshot_platform(hass, entity_registry, snapshot, mock_config_entry.entry_id)


async def test_player_sensor_none_handling(
    hass: UniversalAssistant,
    mock_config_entry: MockConfigEntry,
    mock_nintendo_client: AsyncMock,
    freezer: FrozenDateTimeFactory,
) -> None:
    """Test player sensor returns None when player is not in device players."""
    with patch(
        "universalassistant.components.nintendo_parental_controls._PLATFORMS",
        [Platform.SENSOR],
    ):
        await setup_integration(hass, mock_config_entry)

    entity_id = "sensor.universal_assistant_test_ha_gamer_used_screen_time"
    state = hass.states.get(entity_id)
    assert state is not None
    assert state.state == "110"
    assert state.attributes["entity_picture"] == "http://localhost/image.png"

    mock_nintendo_client.devices["testdevid"].players.remove_player("testplayerid")
    freezer.tick(60)
    async_fire_time_changed(hass)
    await hass.async_block_till_done()

    state = hass.states.get(entity_id)
    assert state is not None
    assert state.state == "unknown"
    assert "entity_picture" not in state.attributes
