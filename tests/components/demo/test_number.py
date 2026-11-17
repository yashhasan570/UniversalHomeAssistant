"""The tests for the demo number component."""

from collections.abc import Generator
from unittest.mock import patch

import probatio
import pytest

from universalassistant.components.number import (
    ATTR_MAX,
    ATTR_MIN,
    ATTR_STEP,
    DOMAIN as NUMBER_DOMAIN,
    NumberMode,
    NumberService,
    NumberServiceArgument,
)
from universalassistant.const import ATTR_MODE, Platform, TargetKey
from universalassistant.core import UniversalAssistant
from universalassistant.exceptions import ServiceValidationError
from universalassistant.setup import async_setup_component

ENTITY_VOLUME = "number.volume"
ENTITY_PWM = "number.pwm_1"
ENTITY_LARGE_RANGE = "number.large_range"
ENTITY_SMALL_RANGE = "number.small_range"


@pytest.fixture
def number_only() -> Generator[None]:
    """Enable only the number platform."""
    with patch(
        "universalassistant.components.demo.COMPONENTS_WITH_CONFIG_ENTRY_DEMO_PLATFORM",
        [Platform.NUMBER],
    ):
        yield


@pytest.fixture(autouse=True)
async def setup_demo_number(hass: UniversalAssistant, number_only: None) -> None:
    """Initialize setup demo Number entity."""
    assert await async_setup_component(
        hass, NUMBER_DOMAIN, {"number": {"platform": "demo"}}
    )
    await hass.async_block_till_done()


def test_setup_params(hass: UniversalAssistant) -> None:
    """Test the initial parameters."""
    state = hass.states.get(ENTITY_VOLUME)
    assert state.state == "42.0"


def test_default_setup_params(hass: UniversalAssistant) -> None:
    """Test the setup with default parameters."""
    state = hass.states.get(ENTITY_VOLUME)
    assert state.attributes.get(ATTR_MIN) == 0.0
    assert state.attributes.get(ATTR_MAX) == 100.0
    assert state.attributes.get(ATTR_STEP) == 1.0
    assert state.attributes.get(ATTR_MODE) == NumberMode.SLIDER

    state = hass.states.get(ENTITY_PWM)
    assert state.attributes.get(ATTR_MIN) == 0.0
    assert state.attributes.get(ATTR_MAX) == 1.0
    assert state.attributes.get(ATTR_STEP) == 0.01
    assert state.attributes.get(ATTR_MODE) == NumberMode.BOX

    state = hass.states.get(ENTITY_LARGE_RANGE)
    assert state.attributes.get(ATTR_MIN) == 1.0
    assert state.attributes.get(ATTR_MAX) == 1000.0
    assert state.attributes.get(ATTR_STEP) == 1.0
    assert state.attributes.get(ATTR_MODE) == NumberMode.AUTO

    state = hass.states.get(ENTITY_SMALL_RANGE)
    assert state.attributes.get(ATTR_MIN) == 1.0
    assert state.attributes.get(ATTR_MAX) == 255.0
    assert state.attributes.get(ATTR_STEP) == 1.0
    assert state.attributes.get(ATTR_MODE) == NumberMode.AUTO


async def test_set_value_bad_attr(hass: UniversalAssistant) -> None:
    """Test setting the value without required attribute."""
    state = hass.states.get(ENTITY_VOLUME)
    assert state.state == "42.0"

    with pytest.raises(probatio.Invalid):
        await hass.services.async_call(
            NUMBER_DOMAIN,
            NumberService.SET_VALUE,
            {
                NumberServiceArgument.VALUE: None,
                TargetKey.ENTITY_ID: ENTITY_VOLUME,
            },
            blocking=True,
        )
    await hass.async_block_till_done()

    state = hass.states.get(ENTITY_VOLUME)
    assert state.state == "42.0"


async def test_set_value_bad_range(hass: UniversalAssistant) -> None:
    """Test setting the value out of range."""
    state = hass.states.get(ENTITY_VOLUME)
    assert state.state == "42.0"

    with pytest.raises(ServiceValidationError):
        await hass.services.async_call(
            NUMBER_DOMAIN,
            NumberService.SET_VALUE,
            {
                NumberServiceArgument.VALUE: 1024,
                TargetKey.ENTITY_ID: ENTITY_VOLUME,
            },
            blocking=True,
        )
    await hass.async_block_till_done()

    state = hass.states.get(ENTITY_VOLUME)
    assert state.state == "42.0"


async def test_set_set_value(hass: UniversalAssistant) -> None:
    """Test the setting of the value."""
    state = hass.states.get(ENTITY_VOLUME)
    assert state.state == "42.0"

    await hass.services.async_call(
        NUMBER_DOMAIN,
        NumberService.SET_VALUE,
        {
            NumberServiceArgument.VALUE: 23,
            TargetKey.ENTITY_ID: ENTITY_VOLUME,
        },
        blocking=True,
    )
    await hass.async_block_till_done()

    state = hass.states.get(ENTITY_VOLUME)
    assert state.state == "23.0"
