"""The tests for automation recorder."""

import pytest
from pytest_universalassistant.common import async_mock_service
from pytest_universalassistant.components.recorder.common import async_wait_recording_done

from universalassistant.components import automation
from universalassistant.components.automation import ATTR_LAST_TRIGGERED
from universalassistant.components.recorder import Recorder
from universalassistant.components.recorder.history import get_significant_states
from universalassistant.const import ATTR_ENTITY_ID, ATTR_FRIENDLY_NAME, ATTR_MODE, CONF_ID
from universalassistant.core import UniversalAssistant, ServiceCall
from universalassistant.helpers.script import ATTR_CUR, ATTR_MAX
from universalassistant.setup import async_setup_component
from universalassistant.util import dt as dt_util


@pytest.fixture
def calls(hass: UniversalAssistant) -> list[ServiceCall]:
    """Track calls to a mock service."""
    return async_mock_service(hass, "test", "automation")


async def test_exclude_attributes(
    recorder_mock: Recorder, hass: UniversalAssistant, calls: list[ServiceCall]
) -> None:
    """Test automation registered attributes to be excluded."""
    now = dt_util.utcnow()
    assert await async_setup_component(
        hass,
        automation.DOMAIN,
        {
            automation.DOMAIN: {
                "trigger": {"trigger": "event", "event_type": "test_event"},
                "actions": {"action": "test.automation", "entity_id": "hello.world"},
            }
        },
    )
    await hass.async_block_till_done()
    hass.bus.async_fire("test_event")
    await hass.async_block_till_done()
    assert len(calls) == 1
    assert calls[0].data.get(ATTR_ENTITY_ID) == ["hello.world"]
    await async_wait_recording_done(hass)

    states = await hass.async_add_executor_job(
        get_significant_states, hass, now, None, hass.states.async_entity_ids()
    )
    assert len(states) == 1
    for entity_states in states.values():
        for state in entity_states:
            assert ATTR_LAST_TRIGGERED not in state.attributes
            assert ATTR_MODE not in state.attributes
            assert ATTR_CUR not in state.attributes
            assert CONF_ID not in state.attributes
            assert ATTR_MAX not in state.attributes
            assert ATTR_FRIENDLY_NAME in state.attributes
