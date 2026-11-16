"""The tests for the Switch component."""

import pytest
from pytest_universalassistant.common import MockUser, setup_test_component_platform

from universalassistant import core
from universalassistant.components import switch
from universalassistant.components.switch import DOMAIN
from universalassistant.const import CONF_PLATFORM
from universalassistant.core import UniversalAssistant
from universalassistant.setup import async_setup_component

from . import common
from .common import MockSwitch


@pytest.fixture(autouse=True)
def entities(
    hass: UniversalAssistant, mock_switch_entities: list[MockSwitch]
) -> list[MockSwitch]:
    """Initialize the test switch."""
    setup_test_component_platform(hass, switch.DOMAIN, mock_switch_entities)
    return mock_switch_entities


@pytest.mark.usefixtures("enable_custom_integrations")
async def test_methods(hass: UniversalAssistant, entities: list[MockSwitch]) -> None:
    """Test is_on, turn_on, turn_off methods."""
    switch_1, switch_2, switch_3 = entities
    assert await async_setup_component(
        hass, switch.DOMAIN, {switch.DOMAIN: {CONF_PLATFORM: "test"}}
    )
    await hass.async_block_till_done()
    assert switch.is_on(hass, switch_1.entity_id)
    assert not switch.is_on(hass, switch_2.entity_id)
    assert not switch.is_on(hass, switch_3.entity_id)

    await common.async_turn_off(hass, switch_1.entity_id)
    await common.async_turn_on(hass, switch_2.entity_id)

    assert not switch.is_on(hass, switch_1.entity_id)
    assert switch.is_on(hass, switch_2.entity_id)

    # Turn all off
    await common.async_turn_off(hass)

    assert not switch.is_on(hass, switch_1.entity_id)
    assert not switch.is_on(hass, switch_2.entity_id)
    assert not switch.is_on(hass, switch_3.entity_id)

    # Turn all on
    await common.async_turn_on(hass)

    assert switch.is_on(hass, switch_1.entity_id)
    assert switch.is_on(hass, switch_2.entity_id)
    assert switch.is_on(hass, switch_3.entity_id)


@pytest.mark.usefixtures("enable_custom_integrations")
async def test_switch_context(
    hass: UniversalAssistant,
    entities,
    hass_admin_user: MockUser,
) -> None:
    """Test that switch context works."""
    assert await async_setup_component(hass, DOMAIN, {"switch": {"platform": "test"}})

    await hass.async_block_till_done()

    state = hass.states.get("switch.ac")
    assert state is not None

    await hass.services.async_call(
        "switch",
        "toggle",
        {"entity_id": state.entity_id},
        True,
        core.Context(user_id=hass_admin_user.id),
    )

    state2 = hass.states.get("switch.ac")
    assert state2 is not None
    assert state.state != state2.state
    assert state2.context.user_id == hass_admin_user.id
