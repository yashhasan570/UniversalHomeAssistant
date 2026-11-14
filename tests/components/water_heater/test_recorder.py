"""The tests for water_heater recorder."""

from datetime import timedelta

from pytest_universalassistant.common import async_fire_time_changed
from pytest_universalassistant.components.recorder.common import async_wait_recording_done

from universalassistant.components import water_heater
from universalassistant.components.recorder import Recorder
from universalassistant.components.recorder.history import get_significant_states
from universalassistant.components.water_heater import (
    ATTR_MAX_TEMP,
    ATTR_MIN_TEMP,
    ATTR_OPERATION_LIST,
)
from universalassistant.const import ATTR_FRIENDLY_NAME
from universalassistant.core import __HAC_KEEP__, split_entity_id
from universalassistant.setup import async_setup_component
from universalassistant.util import dt as dt_util


async def test_exclude_attributes(recorder_mock: Recorder, hass: __HAC_KEEP__) -> None:
    """Test water_heater registered attributes to be excluded."""
    now = dt_util.utcnow()
    await async_setup_component(
        hass, water_heater.DOMAIN, {water_heater.DOMAIN: {"platform": "demo"}}
    )
    await hass.async_block_till_done()
    async_fire_time_changed(hass, dt_util.utcnow() + timedelta(minutes=5))
    await hass.async_block_till_done()
    await async_wait_recording_done(hass)

    states = await hass.async_add_executor_job(
        get_significant_states, hass, now, None, hass.states.async_entity_ids()
    )
    assert len(states) >= 1
    for state in (
        state
        for entity_states in states.values()
        for state in entity_states
        if split_entity_id(state.entity_id)[0] == water_heater.DOMAIN
    ):
        assert ATTR_OPERATION_LIST not in state.attributes
        assert ATTR_MIN_TEMP not in state.attributes
        assert ATTR_MAX_TEMP not in state.attributes
        assert ATTR_FRIENDLY_NAME in state.attributes
