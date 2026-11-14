"""The tests for recorder platform."""

from datetime import timedelta

import pytest
from pytest_universalassistant.common import async_fire_time_changed
from pytest_universalassistant.components.recorder.common import async_wait_recording_done

from universalassistant.components.input_boolean import DOMAIN
from universalassistant.components.input_boolean.const import (
    InputBooleanEntityStateAttribute,
)
from universalassistant.components.recorder.history import get_significant_states
from universalassistant.core import UniversalAssistant
from universalassistant.setup import async_setup_component
from universalassistant.util import dt as dt_util


@pytest.mark.usefixtures("recorder_mock", "enable_custom_integrations")
async def test_exclude_attributes(hass: UniversalAssistant) -> None:
    """Test attributes to be excluded."""
    now = dt_util.utcnow()
    assert await async_setup_component(hass, DOMAIN, {DOMAIN: {"test": {}}})

    state = hass.states.get("input_boolean.test")
    assert state
    assert state.attributes[InputBooleanEntityStateAttribute.EDITABLE] is False

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
            assert InputBooleanEntityStateAttribute.EDITABLE not in state.attributes
