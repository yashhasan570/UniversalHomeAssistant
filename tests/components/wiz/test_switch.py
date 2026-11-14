"""Tests for switch platform."""

import datetime as dt

import pytest
from pytest_universalassistant.common import async_fire_time_changed
from pywizlight.exceptions import WizLightConnectionError

from universalassistant.components.switch import DOMAIN as SWITCH_DOMAIN, SwitchService
from universalassistant.const import (
    STATE_OFF,
    STATE_ON,
    STATE_UNAVAILABLE,
    CommonServiceArgument,
)
from universalassistant.core import UniversalAssistant
from universalassistant.exceptions import UniversalAssistantError
from universalassistant.helpers import entity_registry as er
from universalassistant.util.dt import utcnow

from . import FAKE_MAC, FAKE_SOCKET, async_push_update, async_setup_integration


async def test_switch_operation(
    hass: UniversalAssistant, entity_registry: er.EntityRegistry
) -> None:
    """Test switch operation."""
    switch, _ = await async_setup_integration(hass, bulb_type=FAKE_SOCKET)
    entity_id = "switch.mock_title"
    assert entity_registry.async_get(entity_id).unique_id == FAKE_MAC
    assert hass.states.get(entity_id).state == STATE_ON

    await hass.services.async_call(
        SWITCH_DOMAIN,
        SwitchService.TURN_OFF,
        {CommonServiceArgument.ENTITY_ID: entity_id},
        blocking=True,
    )
    switch.turn_off.assert_called_once()

    await async_push_update(hass, switch, {"mac": FAKE_MAC, "state": False})
    assert hass.states.get(entity_id).state == STATE_OFF

    await hass.services.async_call(
        SWITCH_DOMAIN,
        SwitchService.TURN_ON,
        {CommonServiceArgument.ENTITY_ID: entity_id},
        blocking=True,
    )
    switch.turn_on.assert_called_once()

    await async_push_update(hass, switch, {"mac": FAKE_MAC, "state": True})
    assert hass.states.get(entity_id).state == STATE_ON


async def test_switch_operation_fails(hass: UniversalAssistant) -> None:
    """Test a switch command raises UniversalAssistantError when the socket does not answer."""
    switch, _ = await async_setup_integration(hass, bulb_type=FAKE_SOCKET)
    entity_id = "switch.mock_title"

    switch.turn_on.side_effect = WizLightConnectionError("Network is unreachable")
    with pytest.raises(
        UniversalAssistantError, match="Error while communicating with the WiZ device"
    ):
        await hass.services.async_call(
            SWITCH_DOMAIN,
            SwitchService.TURN_ON,
            {CommonServiceArgument.ENTITY_ID: entity_id},
            blocking=True,
        )


async def test_update_fails(
    hass: UniversalAssistant, entity_registry: er.EntityRegistry
) -> None:
    """Test switch update fails when push updates are not working."""
    switch, _ = await async_setup_integration(hass, bulb_type=FAKE_SOCKET)
    entity_id = "switch.mock_title"
    assert entity_registry.async_get(entity_id).unique_id == FAKE_MAC
    assert hass.states.get(entity_id).state == STATE_ON

    await hass.services.async_call(
        SWITCH_DOMAIN,
        SwitchService.TURN_OFF,
        {CommonServiceArgument.ENTITY_ID: entity_id},
        blocking=True,
    )
    switch.turn_off.assert_called_once()

    switch.updateState.side_effect = OSError

    async_fire_time_changed(hass, utcnow() + dt.timedelta(seconds=15))
    await hass.async_block_till_done()

    assert hass.states.get(entity_id).state == STATE_UNAVAILABLE
