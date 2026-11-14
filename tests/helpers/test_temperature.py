"""Tests __HA_KEEP__ temperature helpers."""

import pytest

from universalassistant.const import (
    PRECISION_HALVES,
    PRECISION_TENTHS,
    PRECISION_WHOLE,
    UnitOfTemperature,
)
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers.temperature import display_temp

TEMP = 24.636626


def test_temperature_not_a_number(hass: __HAC_KEEP__) -> None:
    """Test that temperature is a number."""
    temp = "Temperature"
    with pytest.raises(Exception) as exception:
        display_temp(hass, temp, UnitOfTemperature.CELSIUS, PRECISION_HALVES)

    assert f"Temperature is not a number: {temp}" in str(exception.value)


def test_celsius_halves(hass: __HAC_KEEP__) -> None:
    """Test temperature to celsius rounding to halves."""
    assert display_temp(hass, TEMP, UnitOfTemperature.CELSIUS, PRECISION_HALVES) == 24.5


def test_celsius_tenths(hass: __HAC_KEEP__) -> None:
    """Test temperature to celsius rounding to tenths."""
    assert display_temp(hass, TEMP, UnitOfTemperature.CELSIUS, PRECISION_TENTHS) == 24.6


def test_fahrenheit_wholes(hass: __HAC_KEEP__) -> None:
    """Test temperature to fahrenheit rounding to wholes."""
    assert display_temp(hass, TEMP, UnitOfTemperature.FAHRENHEIT, PRECISION_WHOLE) == -4
