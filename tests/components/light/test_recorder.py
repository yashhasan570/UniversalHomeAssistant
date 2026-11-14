"""The tests for light recorder."""

from datetime import timedelta
from unittest.mock import patch

import pytest
from pytest_universalassistant.common import async_fire_time_changed
from pytest_universalassistant.components.recorder.common import async_wait_recording_done

from universalassistant.components import light
from universalassistant.components.light import (
    ATTR_BRIGHTNESS,
    ATTR_COLOR_MODE,
    ATTR_COLOR_TEMP_KELVIN,
    ATTR_EFFECT,
    ATTR_EFFECT_LIST,
    ATTR_HS_COLOR,
    ATTR_MAX_COLOR_TEMP_KELVIN,
    ATTR_MIN_COLOR_TEMP_KELVIN,
    ATTR_RGB_COLOR,
    ATTR_RGBW_COLOR,
    ATTR_RGBWW_COLOR,
    ATTR_SUPPORTED_COLOR_MODES,
    ATTR_XY_COLOR,
    DOMAIN,
)
from universalassistant.components.recorder import Recorder
from universalassistant.components.recorder.history import get_significant_states
from universalassistant.const import ATTR_FRIENDLY_NAME, Platform
from universalassistant.core import UniversalAssistant
from universalassistant.setup import async_setup_component
from universalassistant.util import dt as dt_util


@pytest.fixture(autouse=True)
async def light_only() -> None:
    """Enable only the light platform."""
    with patch(
        "universalassistant.components.demo.COMPONENTS_WITH_CONFIG_ENTRY_DEMO_PLATFORM",
        [Platform.LIGHT],
    ):
        yield


async def test_exclude_attributes(recorder_mock: Recorder, hass: UniversalAssistant) -> None:
    """Test light registered attributes to be excluded."""
    now = dt_util.utcnow()
    assert await async_setup_component(hass, "universalassistant", {})
    await async_setup_component(
        hass, light.DOMAIN, {light.DOMAIN: {"platform": "demo"}}
    )
    await hass.async_block_till_done()
    async_fire_time_changed(hass, dt_util.utcnow() + timedelta(minutes=5))
    await hass.async_block_till_done()
    await async_wait_recording_done(hass)

    states = await hass.async_add_executor_job(
        get_significant_states, hass, now, None, hass.states.async_entity_ids(DOMAIN)
    )
    assert len(states) >= 1
    for entity_states in states.values():
        for state in entity_states:
            assert ATTR_SUPPORTED_COLOR_MODES not in state.attributes
            assert ATTR_EFFECT_LIST not in state.attributes
            assert ATTR_FRIENDLY_NAME in state.attributes
            assert ATTR_MAX_COLOR_TEMP_KELVIN not in state.attributes
            assert ATTR_MIN_COLOR_TEMP_KELVIN not in state.attributes
            assert ATTR_BRIGHTNESS not in state.attributes
            assert ATTR_COLOR_MODE not in state.attributes
            assert ATTR_COLOR_TEMP_KELVIN not in state.attributes
            assert ATTR_EFFECT not in state.attributes
            assert ATTR_HS_COLOR not in state.attributes
            assert ATTR_RGB_COLOR not in state.attributes
            assert ATTR_RGBW_COLOR not in state.attributes
            assert ATTR_RGBWW_COLOR not in state.attributes
            assert ATTR_XY_COLOR not in state.attributes
