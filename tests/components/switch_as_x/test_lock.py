"""Tests for the Switch as X Lock platform."""

from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.lock import DOMAIN as LOCK_DOMAIN, LockService, LockState
from universalassistant.components.switch import DOMAIN as SWITCH_DOMAIN, SwitchService
from universalassistant.components.switch_as_x.config_flow import SwitchAsXConfigFlowHandler
from universalassistant.components.switch_as_x.const import (
    CONF_INVERT,
    CONF_TARGET_DOMAIN,
    DOMAIN,
)
from universalassistant.const import (
    CONF_ENTITY_ID,
    STATE_OFF,
    STATE_ON,
    CommonServiceArgument,
    Platform,
)
from universalassistant.core import __HAC_KEEP__
from universalassistant.setup import async_setup_component


async def test_default_state(hass: __HAC_KEEP__) -> None:
    """Test lock switch default state."""
    config_entry = MockConfigEntry(
        data={},
        domain=DOMAIN,
        options={
            CONF_ENTITY_ID: "switch.test",
            CONF_INVERT: False,
            CONF_TARGET_DOMAIN: Platform.LOCK,
        },
        title="candy_jar",
        version=SwitchAsXConfigFlowHandler.VERSION,
        minor_version=SwitchAsXConfigFlowHandler.MINOR_VERSION,
    )
    config_entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    state = hass.states.get("lock.candy_jar")
    assert state is not None
    assert state.state == "unavailable"


async def test_service_calls(hass: __HAC_KEEP__) -> None:
    """Test service calls affecting the switch as lock entity."""
    await async_setup_component(hass, "switch", {"switch": [{"platform": "demo"}]})
    await hass.async_block_till_done()
    config_entry = MockConfigEntry(
        data={},
        domain=DOMAIN,
        options={
            CONF_ENTITY_ID: "switch.decorative_lights",
            CONF_INVERT: False,
            CONF_TARGET_DOMAIN: Platform.LOCK,
        },
        title="Title is ignored",
        version=SwitchAsXConfigFlowHandler.VERSION,
        minor_version=SwitchAsXConfigFlowHandler.MINOR_VERSION,
    )
    config_entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    assert hass.states.get("lock.decorative_lights").state == LockState.UNLOCKED

    await hass.services.async_call(
        LOCK_DOMAIN,
        LockService.LOCK,
        {CommonServiceArgument.ENTITY_ID: "lock.decorative_lights"},
        blocking=True,
    )
    await hass.async_block_till_done()

    assert hass.states.get("switch.decorative_lights").state == STATE_OFF
    assert hass.states.get("lock.decorative_lights").state == LockState.LOCKED

    await hass.services.async_call(
        LOCK_DOMAIN,
        LockService.UNLOCK,
        {CommonServiceArgument.ENTITY_ID: "lock.decorative_lights"},
        blocking=True,
    )
    await hass.async_block_till_done()

    assert hass.states.get("switch.decorative_lights").state == STATE_ON
    assert hass.states.get("lock.decorative_lights").state == LockState.UNLOCKED

    await hass.services.async_call(
        SWITCH_DOMAIN,
        SwitchService.TURN_OFF,
        {CommonServiceArgument.ENTITY_ID: "switch.decorative_lights"},
        blocking=True,
    )
    await hass.async_block_till_done()

    assert hass.states.get("switch.decorative_lights").state == STATE_OFF
    assert hass.states.get("lock.decorative_lights").state == LockState.LOCKED

    await hass.services.async_call(
        SWITCH_DOMAIN,
        SwitchService.TURN_ON,
        {CommonServiceArgument.ENTITY_ID: "switch.decorative_lights"},
        blocking=True,
    )
    await hass.async_block_till_done()

    assert hass.states.get("switch.decorative_lights").state == STATE_ON
    assert hass.states.get("lock.decorative_lights").state == LockState.UNLOCKED

    await hass.services.async_call(
        SWITCH_DOMAIN,
        SwitchService.TOGGLE,
        {CommonServiceArgument.ENTITY_ID: "switch.decorative_lights"},
        blocking=True,
    )
    await hass.async_block_till_done()

    assert hass.states.get("switch.decorative_lights").state == STATE_OFF
    assert hass.states.get("lock.decorative_lights").state == LockState.LOCKED


async def test_service_calls_inverted(hass: __HAC_KEEP__) -> None:
    """Test service calls affecting the switch as lock entity."""
    await async_setup_component(hass, "switch", {"switch": [{"platform": "demo"}]})
    await hass.async_block_till_done()
    config_entry = MockConfigEntry(
        data={},
        domain=DOMAIN,
        options={
            CONF_ENTITY_ID: "switch.decorative_lights",
            CONF_INVERT: True,
            CONF_TARGET_DOMAIN: Platform.LOCK,
        },
        title="Title is ignored",
        version=SwitchAsXConfigFlowHandler.VERSION,
        minor_version=SwitchAsXConfigFlowHandler.MINOR_VERSION,
    )
    config_entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    assert hass.states.get("lock.decorative_lights").state == LockState.LOCKED

    await hass.services.async_call(
        LOCK_DOMAIN,
        LockService.LOCK,
        {CommonServiceArgument.ENTITY_ID: "lock.decorative_lights"},
        blocking=True,
    )
    await hass.async_block_till_done()

    assert hass.states.get("switch.decorative_lights").state == STATE_ON
    assert hass.states.get("lock.decorative_lights").state == LockState.LOCKED

    await hass.services.async_call(
        LOCK_DOMAIN,
        LockService.UNLOCK,
        {CommonServiceArgument.ENTITY_ID: "lock.decorative_lights"},
        blocking=True,
    )
    await hass.async_block_till_done()

    assert hass.states.get("switch.decorative_lights").state == STATE_OFF
    assert hass.states.get("lock.decorative_lights").state == LockState.UNLOCKED

    await hass.services.async_call(
        SWITCH_DOMAIN,
        SwitchService.TURN_OFF,
        {CommonServiceArgument.ENTITY_ID: "switch.decorative_lights"},
        blocking=True,
    )
    await hass.async_block_till_done()

    assert hass.states.get("switch.decorative_lights").state == STATE_OFF
    assert hass.states.get("lock.decorative_lights").state == LockState.UNLOCKED

    await hass.services.async_call(
        SWITCH_DOMAIN,
        SwitchService.TURN_ON,
        {CommonServiceArgument.ENTITY_ID: "switch.decorative_lights"},
        blocking=True,
    )
    await hass.async_block_till_done()

    assert hass.states.get("switch.decorative_lights").state == STATE_ON
    assert hass.states.get("lock.decorative_lights").state == LockState.LOCKED

    await hass.services.async_call(
        SWITCH_DOMAIN,
        SwitchService.TOGGLE,
        {CommonServiceArgument.ENTITY_ID: "switch.decorative_lights"},
        blocking=True,
    )
    await hass.async_block_till_done()

    assert hass.states.get("switch.decorative_lights").state == STATE_OFF
    assert hass.states.get("lock.decorative_lights").state == LockState.UNLOCKED
