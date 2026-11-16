"""Tests for the TotalConnect buttons."""

from unittest.mock import AsyncMock, patch

from pytest_universalassistant.common import MockConfigEntry, snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.button import DOMAIN as BUTTON_DOMAIN, ButtonService
from universalassistant.const import CommonServiceArgument, Platform
from universalassistant.core import UniversalAssistant
from universalassistant.helpers import entity_registry as er

from . import setup_integration


async def test_entity_registry(
    hass: UniversalAssistant,
    entity_registry: er.EntityRegistry,
    mock_client: AsyncMock,
    mock_config_entry: MockConfigEntry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test the button is registered in entity registry."""
    with patch("universalassistant.components.totalconnect.PLATFORMS", [Platform.BUTTON]):
        await setup_integration(hass, mock_config_entry)

    await snapshot_platform(hass, entity_registry, snapshot, mock_config_entry.entry_id)


async def test_bypass_button(
    hass: UniversalAssistant,
    mock_client: AsyncMock,
    mock_config_entry: MockConfigEntry,
    mock_location: AsyncMock,
) -> None:
    """Test pushing a bypass button."""
    await setup_integration(hass, mock_config_entry)
    await hass.services.async_call(
        BUTTON_DOMAIN,
        ButtonService.PRESS,
        {CommonServiceArgument.ENTITY_ID: "button.security_bypass"},
        blocking=True,
    )

    assert mock_location.zones[2].bypass.call_count == 1


async def test_clear_button(
    hass: UniversalAssistant,
    mock_client: AsyncMock,
    mock_config_entry: MockConfigEntry,
    mock_location: AsyncMock,
) -> None:
    """Test pushing the clear bypass button."""
    await setup_integration(hass, mock_config_entry)
    await hass.services.async_call(
        BUTTON_DOMAIN,
        ButtonService.PRESS,
        {CommonServiceArgument.ENTITY_ID: "button.test_clear_bypass"},
        blocking=True,
    )

    assert mock_location.clear_bypass.call_count == 1
