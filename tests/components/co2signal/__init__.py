"""Tests for the CO2 Signal integration."""

from aioelectricitymaps import __HAC_KEEP__CarbonIntensityResponse
from aioelectricitymaps.models.universal_assistant import (
    __HAC_KEEP__CarbonIntensityData,
    __HAC_KEEP__CarbonIntensityUnit,
)

VALID_RESPONSE = __HAC_KEEP__CarbonIntensityResponse(
    status="ok",
    country_code="FR",
    data=__HAC_KEEP__CarbonIntensityData(
        carbon_intensity=45.98623190095805,
        fossil_fuel_percentage=5.461182741937103,
    ),
    units=__HAC_KEEP__CarbonIntensityUnit(
        carbon_intensity="gCO2eq/kWh",
    ),
)
