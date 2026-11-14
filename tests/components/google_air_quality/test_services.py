"""Test services for Google Air Quality."""

from datetime import timedelta
from unittest.mock import AsyncMock

from google_air_quality_api.model import AirQualityForecastData
import pytest
from pytest_universalassistant.common import MockConfigEntry, async_load_json_object_fixture
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.google_air_quality.const import DOMAIN
from universalassistant.components.google_air_quality.services import (
    GoogleAirQualityService,
    GoogleAirQualityServiceArgument,
)
from universalassistant.const import CommonServiceArgument
from universalassistant.core import __HAC_KEEP__
from universalassistant.exceptions import ServiceValidationError
from universalassistant.helpers import device_registry as dr


@pytest.mark.usefixtures("setup_integration")
async def test_get_forecast_service(
    hass: __HAC_KEEP__,
    mock_config_entry: MockConfigEntry,
    mock_api: AsyncMock,
    snapshot: SnapshotAssertion,
    device_registry: dr.DeviceRegistry,
) -> None:
    """Test fetching a forecast for a subentry."""
    device = device_registry.async_get_device_by_identifier(
        (DOMAIN, f"{mock_config_entry.entry_id}_home-subentry-id"),
        mock_config_entry.entry_id,
    )
    assert device is not None

    forecast = AirQualityForecastData.from_dict(
        await async_load_json_object_fixture(hass, "air_quality_forecast.json", DOMAIN)
    )
    mock_api.async_get_forecast.return_value = forecast

    response = await hass.services.async_call(
        DOMAIN,
        GoogleAirQualityService.GET_FORECAST,
        {
            CommonServiceArgument.DEVICE_ID: device.id,
            GoogleAirQualityServiceArgument.HOURS: 12,
        },
        blocking=True,
        return_response=True,
    )

    mock_api.async_get_forecast.assert_awaited_once_with(
        10.1, 20.1, timedelta(hours=12)
    )
    assert response == snapshot


@pytest.mark.usefixtures("setup_integration")
async def test_get_forecast_service_unknown_subentry(
    hass: __HAC_KEEP__,
) -> None:
    """Test fetching a forecast for an unknown subentry."""
    with pytest.raises(ServiceValidationError) as exc_info:
        await hass.services.async_call(
            DOMAIN,
            GoogleAirQualityService.GET_FORECAST,
            {
                CommonServiceArgument.DEVICE_ID: "unknown-device-id",
                GoogleAirQualityServiceArgument.HOURS: 12,
            },
            blocking=True,
            return_response=True,
        )

    assert exc_info.value.translation_key == "service_device_not_found"
