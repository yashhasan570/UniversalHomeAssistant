"""The tests for the demo time component."""

from unittest.mock import patch

import pytest

from universalassistant.components.time import (
    DOMAIN as TIME_DOMAIN,
    TimeService,
    TimeServiceArgument,
)
from universalassistant.const import CommonServiceArgument, Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.setup import async_setup_component

ENTITY_TIME = "time.time"


@pytest.fixture
async def time_only() -> None:
    """Enable only the time platform."""
    with patch(
        "universalassistant.components.demo.COMPONENTS_WITH_CONFIG_ENTRY_DEMO_PLATFORM",
        [Platform.TIME],
    ):
        yield


@pytest.fixture(autouse=True)
async def setup_demo_datetime(hass: __HAC_KEEP__, time_only) -> None:
    """Initialize setup demo time."""
    assert await async_setup_component(
        hass, TIME_DOMAIN, {"time": {"platform": "demo"}}
    )
    await hass.async_block_till_done()


def test_setup_params(hass: __HAC_KEEP__) -> None:
    """Test the initial parameters."""
    state = hass.states.get(ENTITY_TIME)
    assert state.state == "12:00:00"


async def test_set_value(hass: __HAC_KEEP__) -> None:
    """Test set value service."""
    await hass.services.async_call(
        TIME_DOMAIN,
        TimeService.SET_VALUE,
        {
            CommonServiceArgument.ENTITY_ID: ENTITY_TIME,
            TimeServiceArgument.TIME: "01:02:03",
        },
        blocking=True,
    )
    state = hass.states.get(ENTITY_TIME)
    assert state.state == "01:02:03"
