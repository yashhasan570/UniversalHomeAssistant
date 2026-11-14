"""The tests for the geolocation component."""

import pytest

from universalassistant.components import geo_location
from universalassistant.components.geo_location import GeolocationEvent
from universalassistant.core import UniversalAssistant
from universalassistant.setup import async_setup_component


async def test_setup_component(hass: UniversalAssistant) -> None:
    """Simple test setup of component."""
    result = await async_setup_component(hass, geo_location.DOMAIN, {})
    assert result


async def test_event(hass: UniversalAssistant) -> None:
    """Simple test of the geolocation event class."""
    entity = GeolocationEvent()

    assert entity.state is None
    assert entity.distance is None
    assert entity.latitude is None
    assert entity.longitude is None
    with pytest.raises(AttributeError):
        assert entity.source is None
