"""The tests for the demo remote component."""

from unittest.mock import patch

import pytest

from universalassistant.components import remote
from universalassistant.components.remote import ATTR_COMMAND
from universalassistant.const import (
    ATTR_ENTITY_ID,
    SERVICE_TURN_OFF,
    SERVICE_TURN_ON,
    STATE_OFF,
    STATE_ON,
    Platform,
)
from universalassistant.core import __HAC_KEEP__
from universalassistant.setup import async_setup_component

ENTITY_ID = "remote.remote_one"
SERVICE_SEND_COMMAND = "send_command"


@pytest.fixture
async def remote_only() -> None:
    """Enable only the datetime platform."""
    with patch(
        "universalassistant.components.demo.COMPONENTS_WITH_CONFIG_ENTRY_DEMO_PLATFORM",
        [Platform.REMOTE],
    ):
        yield


@pytest.fixture(autouse=True)
async def setup_component(hass: __HAC_KEEP__, remote_only: None):
    """Initialize components."""
    assert await async_setup_component(
        hass, remote.DOMAIN, {"remote": {"platform": "demo"}}
    )
    await hass.async_block_till_done()


async def test_methods(hass: __HAC_KEEP__) -> None:
    """Test if services call the entity methods as expected."""
    await hass.services.async_call(
        remote.DOMAIN, SERVICE_TURN_ON, {ATTR_ENTITY_ID: ENTITY_ID}
    )
    await hass.async_block_till_done()
    state = hass.states.get(ENTITY_ID)
    assert state.state == STATE_ON

    await hass.services.async_call(
        remote.DOMAIN, SERVICE_TURN_OFF, {ATTR_ENTITY_ID: ENTITY_ID}
    )
    await hass.async_block_till_done()
    state = hass.states.get(ENTITY_ID)
    assert state.state == STATE_OFF

    await hass.services.async_call(
        remote.DOMAIN, SERVICE_TURN_ON, {ATTR_ENTITY_ID: ENTITY_ID}
    )
    await hass.async_block_till_done()
    state = hass.states.get(ENTITY_ID)
    assert state.state == STATE_ON

    data = {
        ATTR_ENTITY_ID: ENTITY_ID,
        ATTR_COMMAND: ["test"],
    }

    await hass.services.async_call(remote.DOMAIN, SERVICE_SEND_COMMAND, data)
    await hass.async_block_till_done()
    state = hass.states.get(ENTITY_ID)
    assert state.attributes == {
        "friendly_name": "Remote One",
        "last_command_sent": "test",
        "supported_features": 0,
    }
