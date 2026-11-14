"""Tests for the CO2 Signal integration."""

from aioelectricitymaps import UniversalAssistantCarbonIntensityResponse
from aioelectricitymaps.models.universal_assistant import (
    UniversalAssistantCarbonIntensityData,
    UniversalAssistantCarbonIntensityUnit,
)

VALID_RESPONSE = UniversalAssistantCarbonIntensityResponse(
    status="ok",
    country_code="FR",
    data=UniversalAssistantCarbonIntensityData(
        carbon_intensity=45.98623190095805,
        fossil_fuel_percentage=5.461182741937103,
    ),
    units=UniversalAssistantCarbonIntensityUnit(
        carbon_intensity="gCO2eq/kWh",
    ),
)
