"""Tests for the Cookidoo button platform."""

from unittest.mock import AsyncMock, patch

from cookidoo_api import CookidooRequestException
import pytest
from pytest_universalassistant.common import MockConfigEntry, snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.button import DOMAIN as BUTTON_DOMAIN, ButtonService
from universalassistant.config_entries import ConfigEntryState
from universalassistant.const import CommonServiceArgument, Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.exceptions import __HAC_KEEP__Error
from universalassistant.helpers import entity_registry as er

from . import setup_integration


@pytest.mark.usefixtures("entity_registry_enabled_by_default")
async def test_all_entities(
    hass: __HAC_KEEP__,
    snapshot: SnapshotAssertion,
    mock_cookidoo_client: AsyncMock,
    cookidoo_config_entry: MockConfigEntry,
    entity_registry: er.EntityRegistry,
) -> None:
    """Test all entities."""
    with patch("universalassistant.components.cookidoo.PLATFORMS", [Platform.BUTTON]):
        await setup_integration(hass, cookidoo_config_entry)

    assert cookidoo_config_entry.state is ConfigEntryState.LOADED

    await snapshot_platform(
        hass, entity_registry, snapshot, cookidoo_config_entry.entry_id
    )


@pytest.mark.usefixtures("entity_registry_enabled_by_default")
async def test_pressing_button(
    hass: __HAC_KEEP__,
    mock_cookidoo_client: AsyncMock,
    cookidoo_config_entry: MockConfigEntry,
) -> None:
    """Test pressing button."""
    await setup_integration(hass, cookidoo_config_entry)

    await hass.services.async_call(
        BUTTON_DOMAIN,
        ButtonService.PRESS,
        {
            CommonServiceArgument.ENTITY_ID: (
                "button.cookidoo_clear_shopping_list_and_additional_purchases"
            ),
        },
        blocking=True,
    )
    mock_cookidoo_client.clear_shopping_list.assert_called_once()


@pytest.mark.usefixtures("entity_registry_enabled_by_default")
async def test_pressing_button_exception(
    hass: __HAC_KEEP__,
    mock_cookidoo_client: AsyncMock,
    cookidoo_config_entry: MockConfigEntry,
) -> None:
    """Test pressing button with exception."""

    await setup_integration(hass, cookidoo_config_entry)

    assert cookidoo_config_entry.state is ConfigEntryState.LOADED

    mock_cookidoo_client.clear_shopping_list.side_effect = CookidooRequestException
    with pytest.raises(
        __HAC_KEEP__Error,
        match="Failed to clear all items from the Cookidoo shopping list",
    ):
        await hass.services.async_call(
            BUTTON_DOMAIN,
            ButtonService.PRESS,
            {
                CommonServiceArgument.ENTITY_ID: (
                    "button.cookidoo_clear_shopping_list_and_additional_purchases"
                ),
            },
            blocking=True,
        )
