"""The tests for recorder platform."""

from datetime import timedelta

import pytest
from pytest_universalassistant.common import async_fire_time_changed
from pytest_universalassistant.components.recorder.common import async_wait_recording_done

from universalassistant.components.input_number import DOMAIN
from universalassistant.components.input_number.const import InputNumberEntityStateAttribute
from universalassistant.components.number import NumberEntityCapabilityAttribute
from universalassistant.components.recorder.history import get_significant_states
from universalassistant.core import __HAC_KEEP__
from universalassistant.setup import async_setup_component
from universalassistant.util import dt as dt_util


@pytest.mark.usefixtures("recorder_mock", "enable_custom_integrations")
async def test_exclude_attributes(hass: __HAC_KEEP__) -> None:
    """Test attributes to be excluded."""
    now = dt_util.utcnow()
    assert await async_setup_component(
        hass, DOMAIN, {DOMAIN: {"test": {"min": 0, "max": 100}}}
    )

    state = hass.states.get("input_number.test")
    assert state
    assert state.attributes[InputNumberEntityStateAttribute.EDITABLE] is False
    assert state.attributes[NumberEntityCapabilityAttribute.MIN] == 0
    assert state.attributes[NumberEntityCapabilityAttribute.MAX] == 100
    assert state.attributes[NumberEntityCapabilityAttribute.STEP] == 1
    assert state.attributes[NumberEntityCapabilityAttribute.MODE] == "slider"

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
            assert InputNumberEntityStateAttribute.EDITABLE not in state.attributes
            assert NumberEntityCapabilityAttribute.MIN not in state.attributes
            assert NumberEntityCapabilityAttribute.MAX not in state.attributes
            assert NumberEntityCapabilityAttribute.STEP not in state.attributes
            assert NumberEntityCapabilityAttribute.MODE not in state.attributes
