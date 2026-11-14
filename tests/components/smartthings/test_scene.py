"""Test for the SmartThings scene platform."""

from unittest.mock import AsyncMock

from pytest_universalassistant.common import MockConfigEntry
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.scene import DOMAIN as SCENE_DOMAIN, SceneService
from universalassistant.const import CommonServiceArgument, Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import entity_registry as er

from . import setup_integration, snapshot_smartthings_entities


async def test_all_entities(
    hass: __HAC_KEEP__,
    snapshot: SnapshotAssertion,
    mock_smartthings: AsyncMock,
    mock_config_entry: MockConfigEntry,
    entity_registry: er.EntityRegistry,
) -> None:
    """Test all entities."""
    await setup_integration(hass, mock_config_entry)

    snapshot_smartthings_entities(hass, entity_registry, snapshot, Platform.SCENE)


async def test_activate_scene(
    hass: __HAC_KEEP__,
    mock_smartthings: AsyncMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test activating a scene."""
    await setup_integration(hass, mock_config_entry)

    await hass.services.async_call(
        SCENE_DOMAIN,
        SceneService.TURN_ON,
        {CommonServiceArgument.ENTITY_ID: "scene.away"},
        blocking=True,
    )

    mock_smartthings.execute_scene.assert_called_once_with(
        "743b0f37-89b8-476c-aedf-eea8ad8cd29d"
    )
