"""Validate Yardian button behavior."""

from unittest.mock import AsyncMock, patch

from pytest_universalassistant.common import MockConfigEntry, snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.button import DOMAIN as BUTTON_DOMAIN, ButtonService
from universalassistant.const import Platform, TargetKey
from universalassistant.core import UniversalAssistant
from universalassistant.helpers import entity_registry as er

from . import setup_integration


@patch("universalassistant.components.yardian.PLATFORMS", [Platform.BUTTON])
async def test_all_entities(
    hass: UniversalAssistant,
    snapshot: SnapshotAssertion,
    mock_yardian_client: AsyncMock,
    mock_config_entry: MockConfigEntry,
    entity_registry: er.EntityRegistry,
) -> None:
    """Test all button entities."""
    await setup_integration(hass, mock_config_entry)

    await snapshot_platform(hass, entity_registry, snapshot, mock_config_entry.entry_id)


@patch("universalassistant.components.yardian.button.BUTTON_REFRESH_DELAY", 0)
async def test_stop_all_button(
    hass: UniversalAssistant,
    mock_yardian_client: AsyncMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test pressing the stop irrigation button."""
    await setup_integration(hass, mock_config_entry)

    await hass.services.async_call(
        BUTTON_DOMAIN,
        ButtonService.PRESS,
        {TargetKey.ENTITY_ID: "button.yardian_smart_sprinkler_stop_irrigation"},
        blocking=True,
    )
    mock_yardian_client.stop_irrigation.assert_called_once()
