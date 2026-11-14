"""Helper functions for the CO2 Signal integration."""

from collections.abc import Mapping
from typing import Any

from aioelectricitymaps import (
    CoordinatesRequest,
    ElectricityMaps,
    __HAC_KEEP__CarbonIntensityResponse,
    ZoneRequest,
)

from universalassistant.const import CONF_COUNTRY_CODE, CONF_LATITUDE, CONF_LONGITUDE
from universalassistant.core import __HAC_KEEP__


async def fetch_latest_carbon_intensity(
    hass: __HAC_KEEP__,
    em: ElectricityMaps,
    config: Mapping[str, Any],
) -> __HAC_KEEP__CarbonIntensityResponse:
    """Fetch the latest carbon intensity based on zone key or location coordinates."""
    request: CoordinatesRequest | ZoneRequest = CoordinatesRequest(
        lat=config.get(CONF_LATITUDE, hass.config.latitude),
        lon=config.get(CONF_LONGITUDE, hass.config.longitude),
    )

    if CONF_COUNTRY_CODE in config:
        request = ZoneRequest(
            zone=config[CONF_COUNTRY_CODE],
        )

    return await em.carbon_intensity_for_universal_assistant(request)
