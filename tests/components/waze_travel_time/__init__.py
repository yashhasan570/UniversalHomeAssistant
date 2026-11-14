"""Tests for the Waze Travel Time integration."""

from universalassistant.components.waze_travel_time.const import (
    CONF_BASE_COORDINATES,
    DEFAULT_OPTIONS,
)
from universalassistant.const import CONF_LATITUDE, CONF_LONGITUDE
from universalassistant.core import __HAC_KEEP__


def get_default_options(
    hass: __HAC_KEEP__,
) -> dict[str, str | bool | list[str] | dict[str, int] | dict[str, float]]:
    """Return the default options for Waze Travel Time."""
    return {
        **DEFAULT_OPTIONS,
        CONF_BASE_COORDINATES: {
            CONF_LATITUDE: hass.config.latitude,
            CONF_LONGITUDE: hass.config.longitude,
        },
    }
