"""Tests for the Smarty switch platform."""

from unittest.mock import AsyncMock, patch

from pytest_universalassistant.common import MockConfigEntry, snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.switch import DOMAIN as SWITCH_DOMAIN, SwitchService
from universalassistant.const import ATTR_ENTITY_ID, Platform
from universalassistant.core import UniversalAssistant
from universalassistant.helpers import entity_registry as er

from . import setup_integration


async def test_all_entities(
    hass: UniversalAssistant,
    snapshot: SnapshotAssertion,
    mock_smarty: AsyncMock,
    mock_config_entry: MockConfigEntry,
    entity_registry: er.EntityRegistry,
) -> None:
    """Test all entities."""
    with patch("universalassistant.components.smarty.PLATFORMS", [Platform.SWITCH]):
        await setup_integration(hass, mock_config_entry)

    await snapshot_platform(hass, entity_registry, snapshot, mock_config_entry.entry_id)


async def test_setting_value(
    hass: UniversalAssistant,
    mock_smarty: AsyncMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test setting value."""
    await setup_integration(hass, mock_config_entry)

    await hass.services.async_call(
        SWITCH_DOMAIN,
        SwitchService.TURN_ON,
        target={ATTR_ENTITY_ID: "switch.mock_title_boost"},
        blocking=True,
    )
    mock_smarty.enable_boost.assert_called_once_with()

    await hass.services.async_call(
        SWITCH_DOMAIN,
        SwitchService.TURN_OFF,
        target={ATTR_ENTITY_ID: "switch.mock_title_boost"},
        blocking=True,
    )
    mock_smarty.disable_boost.assert_called_once_with()
