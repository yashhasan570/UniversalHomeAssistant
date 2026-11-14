"""The tests for sun recorder."""

from datetime import timedelta

from pytest_universalassistant.common import async_fire_time_changed
from pytest_universalassistant.components.recorder.common import async_wait_recording_done

from universalassistant.components.recorder import Recorder
from universalassistant.components.recorder.history import get_significant_states
from universalassistant.components.sun import DOMAIN
from universalassistant.components.sun.const import SunEntityStateAttribute
from universalassistant.const import ATTR_FRIENDLY_NAME
from universalassistant.core import UniversalAssistant
from universalassistant.setup import async_setup_component
from universalassistant.util import dt as dt_util


async def test_exclude_attributes(recorder_mock: Recorder, hass: UniversalAssistant) -> None:
    """Test sun attributes to be excluded."""
    now = dt_util.utcnow()
    await async_setup_component(hass, DOMAIN, {})
    await hass.async_block_till_done()
    async_fire_time_changed(hass, dt_util.utcnow() + timedelta(minutes=5))
    await hass.async_block_till_done()
    await async_wait_recording_done(hass)

    states = await hass.async_add_executor_job(
        get_significant_states, hass, now, None, hass.states.async_entity_ids()
    )
    assert len(states) >= 1
    for entity_states in states.values():
        for state in entity_states:
            assert SunEntityStateAttribute.AZIMUTH not in state.attributes
            assert SunEntityStateAttribute.ELEVATION not in state.attributes
            assert SunEntityStateAttribute.NEXT_DAWN not in state.attributes
            assert SunEntityStateAttribute.NEXT_DUSK not in state.attributes
            assert SunEntityStateAttribute.NEXT_MIDNIGHT not in state.attributes
            assert SunEntityStateAttribute.NEXT_NOON not in state.attributes
            assert SunEntityStateAttribute.NEXT_RISING not in state.attributes
            assert SunEntityStateAttribute.NEXT_SETTING not in state.attributes
            assert SunEntityStateAttribute.RISING not in state.attributes
            assert ATTR_FRIENDLY_NAME in state.attributes
