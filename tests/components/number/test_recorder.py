"""The tests for number recorder."""

from datetime import timedelta
from unittest.mock import patch

import pytest
from pytest_universalassistant.common import async_fire_time_changed
from pytest_universalassistant.components.recorder.common import async_wait_recording_done

from universalassistant.components import number
from universalassistant.components.number import ATTR_MAX, ATTR_MIN, ATTR_MODE, ATTR_STEP
from universalassistant.components.recorder import Recorder
from universalassistant.components.recorder.history import get_significant_states
from universalassistant.const import ATTR_FRIENDLY_NAME, Platform
from universalassistant.core import UniversalAssistant
from universalassistant.setup import async_setup_component
from universalassistant.util import dt as dt_util


@pytest.fixture(autouse=True)
async def number_only() -> None:
    """Enable only the number platform."""
    with patch(
        "universalassistant.components.demo.COMPONENTS_WITH_CONFIG_ENTRY_DEMO_PLATFORM",
        [Platform.NUMBER],
    ):
        yield


async def test_exclude_attributes(recorder_mock: Recorder, hass: UniversalAssistant) -> None:
    """Test number registered attributes to be excluded."""
    assert await async_setup_component(hass, "universalassistant", {})
    await async_setup_component(
        hass, number.DOMAIN, {number.DOMAIN: {"platform": "demo"}}
    )
    await hass.async_block_till_done()
    now = dt_util.utcnow()
    async_fire_time_changed(hass, now + timedelta(minutes=5))
    await hass.async_block_till_done()
    await async_wait_recording_done(hass)

    states = await hass.async_add_executor_job(
        get_significant_states, hass, now, None, hass.states.async_entity_ids()
    )
    assert len(states) > 1
    for entity_states in states.values():
        for state in entity_states:
            assert ATTR_MIN not in state.attributes
            assert ATTR_MAX not in state.attributes
            assert ATTR_STEP not in state.attributes
            assert ATTR_MODE not in state.attributes
            assert ATTR_FRIENDLY_NAME in state.attributes
