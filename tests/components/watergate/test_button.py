"""Tests for the Watergate button platform."""

from collections.abc import Generator

import pytest
from pytest_universalassistant.common import (
    AsyncMock,
    MockConfigEntry,
    patch,
    snapshot_platform,
)
from syrupy.assertion import SnapshotAssertion
from watergate_local_api import WatergateApiException, WatergateIndeterminateError

from universalassistant.components.button import DOMAIN as BUTTON_DOMAIN, ButtonService
from universalassistant.const import Platform, TargetKey
from universalassistant.core import UniversalAssistant
from universalassistant.exceptions import UniversalAssistantError
from universalassistant.helpers import entity_registry as er

from . import init_integration

ENTITY_ID = "button.sonic_reboot"


@pytest.mark.usefixtures("mock_watergate_client")
async def test_entities(
    hass: UniversalAssistant,
    snapshot: SnapshotAssertion,
    entity_registry: er.EntityRegistry,
    mock_entry: MockConfigEntry,
) -> None:
    """Test the button entities and their registry entries."""
    with patch("universalassistant.components.watergate.PLATFORMS", [Platform.BUTTON]):
        await init_integration(hass, mock_entry)

    await snapshot_platform(hass, entity_registry, snapshot, mock_entry.entry_id)


async def test_reboot_press(
    hass: UniversalAssistant,
    mock_watergate_client: Generator[AsyncMock],
    mock_entry: MockConfigEntry,
) -> None:
    """Pressing the button sends a reboot to the device."""
    await init_integration(hass, mock_entry)

    await hass.services.async_call(
        BUTTON_DOMAIN,
        ButtonService.PRESS,
        {TargetKey.ENTITY_ID: ENTITY_ID},
        blocking=True,
    )

    mock_watergate_client.async_reboot.assert_awaited_once_with()


async def test_reboot_outcome_unknown_is_not_an_error(
    hass: UniversalAssistant,
    mock_watergate_client: Generator[AsyncMock],
    mock_entry: MockConfigEntry,
) -> None:
    """A lost response (device rebooting) is expected and must not raise."""
    await init_integration(hass, mock_entry)
    mock_watergate_client.async_reboot.side_effect = WatergateIndeterminateError(
        "outcome unknown"
    )

    await hass.services.async_call(
        BUTTON_DOMAIN,
        ButtonService.PRESS,
        {TargetKey.ENTITY_ID: ENTITY_ID},
        blocking=True,
    )

    mock_watergate_client.async_reboot.assert_awaited_once_with()


async def test_reboot_failure(
    hass: UniversalAssistant,
    mock_watergate_client: Generator[AsyncMock],
    mock_entry: MockConfigEntry,
) -> None:
    """A definite API failure surfaces as UniversalAssistantError."""
    await init_integration(hass, mock_entry)
    mock_watergate_client.async_reboot.side_effect = WatergateApiException("boom")

    with pytest.raises(UniversalAssistantError, match="Failed to reboot the device"):
        await hass.services.async_call(
            BUTTON_DOMAIN,
            ButtonService.PRESS,
            {TargetKey.ENTITY_ID: ENTITY_ID},
            blocking=True,
        )

    mock_watergate_client.async_reboot.assert_awaited_once_with()
