"""The tests for script recorder."""

import pytest
from pytest_universalassistant.common import async_mock_service
from pytest_universalassistant.components.recorder.common import async_wait_recording_done

from universalassistant.components import script
from universalassistant.components.recorder import Recorder
from universalassistant.components.recorder.history import get_significant_states
from universalassistant.components.script.const import DOMAIN, ScriptEntityStateAttribute
from universalassistant.const import ATTR_FRIENDLY_NAME
from universalassistant.core import Context, UniversalAssistant, ServiceCall, callback
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
    await hass.async_block_till_done()
    calls = []
    context = Context()

    @callback
    def record_call(service):
        """Add recorded event to set."""
        calls.append(service)

    hass.services.async_register("test", "script", record_call)

    assert await async_setup_component(
        hass,
        DOMAIN,
        {
            "script": {
                "test": {
                    "sequence": {
                        "action": "test.script",
                        "data_template": {"hello": "{{ greeting }}"},
                    }
                }
            }
        },
    )

    await hass.services.async_call(
        script.DOMAIN, "test", {"greeting": "world"}, context=context
    )
    await hass.async_block_till_done()
    await async_wait_recording_done(hass)
    assert len(calls) == 1

    states = await hass.async_add_executor_job(
        get_significant_states, hass, now, None, hass.states.async_entity_ids()
    )
    assert len(states) >= 1
    for entity_states in states.values():
        for state in entity_states:
            assert ScriptEntityStateAttribute.LAST_TRIGGERED not in state.attributes
            assert ScriptEntityStateAttribute.MODE not in state.attributes
            assert ScriptEntityStateAttribute.CURRENT not in state.attributes
            assert ScriptEntityStateAttribute.LAST_ACTION not in state.attributes
            assert ScriptEntityStateAttribute.MAX not in state.attributes
            assert ATTR_FRIENDLY_NAME in state.attributes
