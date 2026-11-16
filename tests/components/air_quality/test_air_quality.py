"""The tests for the Air Quality component."""

import pytest

from universalassistant.components.air_quality import DOMAIN, AirQualityEntityStateAttribute
from universalassistant.const import (
    ATTR_ATTRIBUTION,
    ATTR_UNIT_OF_MEASUREMENT,
    UnitOfDensity,
)
from universalassistant.core import UniversalAssistant
from universalassistant.setup import async_setup_component


@pytest.fixture(autouse=True)
async def setup_universalassistant(hass: UniversalAssistant):
    """Set up the universalassistant integration."""
    await async_setup_component(hass, "universalassistant", {})


async def test_state(hass: UniversalAssistant) -> None:
    """Test Air Quality state."""
    config = {"air_quality": {"platform": "demo"}}

    assert await async_setup_component(hass, DOMAIN, config)
    await hass.async_block_till_done()

    state = hass.states.get("air_quality.demo_air_quality_home")
    assert state is not None

    assert state.state == "14"


async def test_attributes(hass: UniversalAssistant) -> None:
    """Test Air Quality attributes."""
    config = {"air_quality": {"platform": "demo"}}

    assert await async_setup_component(hass, DOMAIN, config)
    await hass.async_block_till_done()

    state = hass.states.get("air_quality.demo_air_quality_office")
    assert state is not None

    data = state.attributes
    assert data.get(AirQualityEntityStateAttribute.PARTICULATE_MATTER_10) == 16
    assert data.get(AirQualityEntityStateAttribute.NITROGEN_OXIDE) is None
    assert data.get(AirQualityEntityStateAttribute.OZONE) is None
    assert data.get(ATTR_ATTRIBUTION) == "Powered by Universal Home Assistant"
    assert (
        data.get(ATTR_UNIT_OF_MEASUREMENT) == UnitOfDensity.MICROGRAMS_PER_CUBIC_METER
    )
