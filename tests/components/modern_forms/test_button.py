"""Tests for the Modern Forms button platform."""

from unittest.mock import patch

from pytest_universalassistant.test_util.aiohttp import AiohttpClientMocker

from universalassistant.components.button import DOMAIN as BUTTON_DOMAIN, ButtonService
from universalassistant.const import CommonServiceArgument
from universalassistant.core import UniversalAssistant
from universalassistant.helpers import entity_registry as er

from . import init_integration, init_integration_gen4


async def test_restart_button(
    hass: UniversalAssistant,
    entity_registry: er.EntityRegistry,
    aioclient_mock: AiohttpClientMocker,
) -> None:
    """Test the creation of the restart button on a legacy fan."""
    await init_integration(hass, aioclient_mock)

    state = hass.states.get("button.modernformsfan_restart")
    assert state
    entry = entity_registry.async_get("button.modernformsfan_restart")
    assert entry
    assert entry.unique_id == "AA:BB:CC:DD:EE:FF_restart"


async def test_restart_button_gen4(
    hass: UniversalAssistant,
    entity_registry: er.EntityRegistry,
    aioclient_mock: AiohttpClientMocker,
) -> None:
    """Test the creation of the restart button on a Gen4 fan."""
    await init_integration_gen4(hass, aioclient_mock)

    state = hass.states.get("button.modernformsfan_restart")
    assert state
    entry = entity_registry.async_get("button.modernformsfan_restart")
    assert entry
    assert entry.unique_id == "AA:BB:CC:00:11:22_restart"


async def test_restart_button_press(
    hass: UniversalAssistant, aioclient_mock: AiohttpClientMocker
) -> None:
    """Test pressing the restart button."""
    await init_integration(hass, aioclient_mock)

    with patch("aiomodernforms.ModernFormsDevice.reboot") as reboot_mock:
        await hass.services.async_call(
            BUTTON_DOMAIN,
            ButtonService.PRESS,
            {CommonServiceArgument.ENTITY_ID: "button.modernformsfan_restart"},
            blocking=True,
        )
        await hass.async_block_till_done()
        reboot_mock.assert_called_once_with()
