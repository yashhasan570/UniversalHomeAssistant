"""The tests for the demo switch component."""

from collections.abc import Generator
from unittest.mock import patch

import pytest

from universalassistant.components.demo import DOMAIN
from universalassistant.components.switch import DOMAIN as SWITCH_DOMAIN, SwitchService
from universalassistant.const import STATE_OFF, STATE_ON, Platform, TargetKey
from universalassistant.core import UniversalAssistant
from universalassistant.setup import async_setup_component

SWITCH_ENTITY_IDS = ["switch.decorative_lights", "switch.ac"]


@pytest.fixture
def switch_only() -> Generator[None]:
    """Enable only the switch platform."""
    with patch(
        "universalassistant.components.demo.COMPONENTS_WITH_CONFIG_ENTRY_DEMO_PLATFORM",
        [Platform.SWITCH],
    ):
        yield


@pytest.fixture(autouse=True)
async def setup_comp(hass: UniversalAssistant, switch_only: None) -> None:
    """Set up demo component."""
    assert await async_setup_component(
        hass, SWITCH_DOMAIN, {SWITCH_DOMAIN: {"platform": DOMAIN}}
    )
    await hass.async_block_till_done()


@pytest.mark.parametrize("switch_entity_id", SWITCH_ENTITY_IDS)
async def test_turn_on(hass: UniversalAssistant, switch_entity_id: str) -> None:
    """Test switch turn on method."""
    await hass.services.async_call(
        SWITCH_DOMAIN,
        SwitchService.TURN_OFF,
        {TargetKey.ENTITY_ID: switch_entity_id},
        blocking=True,
    )
    await hass.async_block_till_done()

    state = hass.states.get(switch_entity_id)
    assert state.state == STATE_OFF

    await hass.services.async_call(
        SWITCH_DOMAIN,
        SwitchService.TURN_ON,
        {TargetKey.ENTITY_ID: switch_entity_id},
        blocking=True,
    )
    await hass.async_block_till_done()

    state = hass.states.get(switch_entity_id)
    assert state.state == STATE_ON


@pytest.mark.parametrize("switch_entity_id", SWITCH_ENTITY_IDS)
async def test_turn_off(hass: UniversalAssistant, switch_entity_id: str) -> None:
    """Test switch turn off method."""
    await hass.services.async_call(
        SWITCH_DOMAIN,
        SwitchService.TURN_ON,
        {TargetKey.ENTITY_ID: switch_entity_id},
        blocking=True,
    )
    await hass.async_block_till_done()

    state = hass.states.get(switch_entity_id)
    assert state.state == STATE_ON

    await hass.services.async_call(
        SWITCH_DOMAIN,
        SwitchService.TURN_OFF,
        {TargetKey.ENTITY_ID: switch_entity_id},
        blocking=True,
    )
    await hass.async_block_till_done()

    state = hass.states.get(switch_entity_id)
    assert state.state == STATE_OFF


@pytest.mark.parametrize("switch_entity_id", SWITCH_ENTITY_IDS)
async def test_turn_off_without_entity_id(
    hass: UniversalAssistant, switch_entity_id: str
) -> None:
    """Test switch turn off all switches."""
    await hass.services.async_call(
        SWITCH_DOMAIN,
        SwitchService.TURN_ON,
        {TargetKey.ENTITY_ID: "all"},
        blocking=True,
    )
    await hass.async_block_till_done()

    state = hass.states.get(switch_entity_id)
    assert state.state == STATE_ON

    await hass.services.async_call(
        SWITCH_DOMAIN,
        SwitchService.TURN_OFF,
        {TargetKey.ENTITY_ID: "all"},
        blocking=True,
    )
    await hass.async_block_till_done()

    state = hass.states.get(switch_entity_id)
    assert state.state == STATE_OFF
