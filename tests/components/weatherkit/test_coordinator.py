"""Test WeatherKit data coordinator."""

from datetime import timedelta
from unittest.mock import patch

from apple_weatherkit.client import WeatherKitApiClientError
from freezegun.api import FrozenDateTimeFactory
from pytest_universalassistant.common import async_fire_time_changed

from universalassistant.const import STATE_UNAVAILABLE
from universalassistant.core import UniversalAssistant

from . import init_integration, mock_weather_response


async def test_update_uses_stale_data_before_threshold(
    hass: UniversalAssistant,
    freezer: FrozenDateTimeFactory,
) -> None:
    """Test stale data is used if update fails before threshold."""
    with mock_weather_response():
        await init_integration(hass)

    state = hass.states.get("weather.home")
    assert state
    assert state.state != STATE_UNAVAILABLE

    initial_state = state.state

    # Expect stale data to be used before one hour

    with patch(
        "universalassistant.components.weatherkit.WeatherKitApiClient.get_weather_data",
        side_effect=WeatherKitApiClientError,
    ):
        freezer.tick(timedelta(minutes=59))
        async_fire_time_changed(hass)
        await hass.async_block_till_done()

    state = hass.states.get("weather.home")
    assert state
    assert state.state == initial_state


async def test_update_becomes_unavailable_after_threshold(
    hass: UniversalAssistant,
    freezer: FrozenDateTimeFactory,
) -> None:
    """Test entity becomes unavailable if update fails after threshold."""
    with mock_weather_response():
        await init_integration(hass)

    # Expect state to be unavailable after one hour

    with patch(
        "universalassistant.components.weatherkit.WeatherKitApiClient.get_weather_data",
        side_effect=WeatherKitApiClientError,
    ):
        freezer.tick(timedelta(hours=1, minutes=5))
        async_fire_time_changed(hass)
        await hass.async_block_till_done()

    state = hass.states.get("weather.home")
    assert state
    assert state.state == STATE_UNAVAILABLE


async def test_update_recovers_after_failure(
    hass: UniversalAssistant,
    freezer: FrozenDateTimeFactory,
) -> None:
    """Test successful update after failures recovers entity state."""
    with mock_weather_response():
        await init_integration(hass)

    # Trigger a failure after threshold

    with patch(
        "universalassistant.components.weatherkit.WeatherKitApiClient.get_weather_data",
        side_effect=WeatherKitApiClientError,
    ):
        freezer.tick(timedelta(hours=1, minutes=5))
        async_fire_time_changed(hass)
        await hass.async_block_till_done()

    # Expect that a successful update recovers the entity

    with mock_weather_response():
        freezer.tick(timedelta(minutes=5))
        async_fire_time_changed(hass)
        await hass.async_block_till_done()

    state = hass.states.get("weather.home")
    assert state
    assert state.state != STATE_UNAVAILABLE
