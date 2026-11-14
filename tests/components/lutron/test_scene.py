"""Test Lutron scene platform."""

from unittest.mock import MagicMock, patch

import pytest
from pytest_universalassistant.common import MockConfigEntry, snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.scene import DOMAIN as SCENE_DOMAIN, SceneService
from universalassistant.const import CommonServiceArgument, Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import entity_registry as er


@pytest.fixture(autouse=True)
def setup_platforms():
    """Patch PLATFORMS for all tests in this file."""
    with patch("universalassistant.components.lutron.PLATFORMS", [Platform.SCENE]):
        yield


async def test_scene_setup(
    hass: __HAC_KEEP__,
    mock_lutron: MagicMock,
    mock_config_entry: MockConfigEntry,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test scene setup."""
    mock_config_entry.add_to_hass(hass)

    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    await snapshot_platform(hass, entity_registry, snapshot, mock_config_entry.entry_id)


async def test_scene_activate(
    hass: __HAC_KEEP__, mock_lutron: MagicMock, mock_config_entry: MockConfigEntry
) -> None:
    """Test scene activation."""
    mock_config_entry.add_to_hass(hass)

    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    entity_id = "scene.test_keypad_test_button"
    button = mock_lutron.areas[0].keypads[0].buttons[0]

    await hass.services.async_call(
        SCENE_DOMAIN,
        SceneService.TURN_ON,
        {CommonServiceArgument.ENTITY_ID: entity_id},
        blocking=True,
    )

    button.tap.assert_called_once()
