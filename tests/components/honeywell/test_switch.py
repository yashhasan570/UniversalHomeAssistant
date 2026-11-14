"""Tests for Honeywell switch component."""

from unittest.mock import MagicMock

from aiosomecomfort.exceptions import SomeComfortError
import pytest
from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.switch import DOMAIN as SWITCH_DOMAIN, SwitchService
from universalassistant.const import CommonServiceArgument
from universalassistant.core import UniversalAssistant
from universalassistant.exceptions import UniversalAssistantError

from . import init_integration


async def test_emheat_switch(
    hass: UniversalAssistant,
    config_entry: MockConfigEntry,
    device: MagicMock,
) -> None:
    """Test emergency heat switch."""

    await init_integration(hass, config_entry)
    entity_id = f"switch.{device.name}_emergency_heat"
    await hass.services.async_call(
        SWITCH_DOMAIN,
        SwitchService.TURN_ON,
        {CommonServiceArgument.ENTITY_ID: entity_id},
        blocking=True,
    )
    device.set_system_mode.assert_called_once_with("emheat")

    device.set_system_mode.reset_mock()

    device.system_mode = "emheat"
    await hass.services.async_call(
        SWITCH_DOMAIN,
        SwitchService.TURN_OFF,
        {CommonServiceArgument.ENTITY_ID: entity_id},
        blocking=True,
    )
    device.set_system_mode.assert_called_once_with("off")

    device.set_system_mode.reset_mock()
    device.system_mode = "heat"
    device.set_system_mode.side_effect = SomeComfortError
    with pytest.raises(UniversalAssistantError):
        await hass.services.async_call(
            SWITCH_DOMAIN,
            SwitchService.TURN_ON,
            {CommonServiceArgument.ENTITY_ID: entity_id},
            blocking=True,
        )
    device.set_system_mode.assert_called_once_with("emheat")

    device.set_system_mode.reset_mock()
    device.system_mode = "emheat"
    device.set_system_mode.side_effect = SomeComfortError
    with pytest.raises(UniversalAssistantError):
        await hass.services.async_call(
            SWITCH_DOMAIN,
            SwitchService.TURN_OFF,
            {CommonServiceArgument.ENTITY_ID: entity_id},
            blocking=True,
        )
    device.set_system_mode.assert_called_once_with("off")
