"""Tests for Vodafone Station button platform."""

from unittest.mock import AsyncMock, patch

from aiovodafone.exceptions import (
    AlreadyLogged,
    CannotAuthenticate,
    CannotConnect,
    GenericLoginError,
)
import pytest
from pytest_universalassistant.common import MockConfigEntry, snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.button import DOMAIN as BUTTON_DOMAIN, ButtonService
from universalassistant.components.vodafone_station.const import DOMAIN
from universalassistant.const import CommonServiceArgument, Platform
from universalassistant.core import UniversalAssistant
from universalassistant.exceptions import UniversalAssistantError
from universalassistant.helpers import entity_registry as er

from . import setup_integration
from .const import TEST_SERIAL_NUMBER


async def test_all_entities(
    hass: UniversalAssistant,
    snapshot: SnapshotAssertion,
    mock_vodafone_station_router: AsyncMock,
    mock_config_entry: MockConfigEntry,
    entity_registry: er.EntityRegistry,
) -> None:
    """Test all entities."""
    with patch(
        "universalassistant.components.vodafone_station.PLATFORMS", [Platform.BUTTON]
    ):
        await setup_integration(hass, mock_config_entry)

    await snapshot_platform(hass, entity_registry, snapshot, mock_config_entry.entry_id)


async def test_pressing_button(
    hass: UniversalAssistant,
    mock_vodafone_station_router: AsyncMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test device restart button."""

    await setup_integration(hass, mock_config_entry)

    await hass.services.async_call(
        BUTTON_DOMAIN,
        ButtonService.PRESS,
        {
            CommonServiceArgument.ENTITY_ID: f"button.vodafone_station_{TEST_SERIAL_NUMBER}_restart"
        },
        blocking=True,
    )
    mock_vodafone_station_router.restart_router.assert_called_once()


@pytest.mark.parametrize(
    ("side_effect", "key", "error"),
    [
        (CannotConnect, "cannot_execute_action", "CannotConnect()"),
        (AlreadyLogged, "cannot_execute_action", "AlreadyLogged()"),
        (GenericLoginError, "cannot_execute_action", "GenericLoginError()"),
        (CannotAuthenticate, "cannot_authenticate", "CannotAuthenticate()"),
    ],
)
async def test_button_fails(
    hass: UniversalAssistant,
    mock_vodafone_station_router: AsyncMock,
    mock_config_entry: MockConfigEntry,
    side_effect: Exception,
    key: str,
    error: str,
) -> None:
    """Test button action fails."""

    await setup_integration(hass, mock_config_entry)

    mock_vodafone_station_router.restart_router.side_effect = side_effect

    with pytest.raises(UniversalAssistantError) as exc_info:
        await hass.services.async_call(
            BUTTON_DOMAIN,
            ButtonService.PRESS,
            {
                CommonServiceArgument.ENTITY_ID: f"button.vodafone_station_{TEST_SERIAL_NUMBER}_restart"
            },
            blocking=True,
        )

    assert exc_info.value.translation_domain == DOMAIN
    assert exc_info.value.translation_key == key
    assert exc_info.value.translation_placeholders == {"error": error}
