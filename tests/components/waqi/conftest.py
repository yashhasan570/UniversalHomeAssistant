"""Common fixtures for the World Air Quality Index (WAQI) tests."""

from collections.abc import AsyncGenerator, Generator
from unittest.mock import AsyncMock, patch

from aiowaqi import WAQIAirQuality
import pytest
from pytest_universalassistant.common import MockConfigEntry, async_load_json_object_fixture

from universalassistant.components.waqi.const import CONF_STATION_NUMBER, DOMAIN
from universalassistant.config_entries import ConfigSubentryData
from universalassistant.const import CONF_API_KEY
from universalassistant.core import UniversalAssistant


@pytest.fixture
def mock_setup_entry() -> Generator[AsyncMock]:
    """Override async_setup_entry."""
    with patch(
        "universalassistant.components.waqi.async_setup_entry", return_value=None
    ) as mock_setup_entry:
        yield mock_setup_entry


@pytest.fixture
def mock_config_entry() -> MockConfigEntry:
    """Mock config entry."""
    return MockConfigEntry(
        domain=DOMAIN,
        title="WAQI",
        data={CONF_API_KEY: "asd"},
        version=2,
        subentries_data=[
            ConfigSubentryData(
                data={CONF_STATION_NUMBER: 4585},
                subentry_id="ABCDEF",
                subentry_type="station",
                title="de Jongweg, Utrecht",
                unique_id="4585",
            )
        ],
    )


@pytest.fixture
async def mock_waqi(hass: UniversalAssistant) -> AsyncGenerator[AsyncMock]:
    """Mock WAQI client."""
    with (
        patch(
            "universalassistant.components.waqi.WAQIClient",
            autospec=True,
        ) as mock_waqi,
        patch(
            "universalassistant.components.waqi.config_flow.WAQIClient",
            new=mock_waqi,
        ),
    ):
        client = mock_waqi.return_value
        air_quality = WAQIAirQuality.from_dict(
            await async_load_json_object_fixture(
                hass, "air_quality_sensor.json", DOMAIN
            )
        )
        client.get_by_station_number.return_value = air_quality
        client.get_by_ip.return_value = air_quality
        client.get_by_coordinates.return_value = air_quality
        yield client
