"""Fixtures for sma tests."""

from collections.abc import Generator
from unittest.mock import AsyncMock, MagicMock, patch

from pysma.const import (
    ENERGY_METER_VIA_INVERTER,
    GENERIC_SENSORS,
    OPTIMIZERS_VIA_INVERTER,
)
from pysma.definitions.webconnect import sensor_map
from pysma.sensor import Sensors
import pytest
from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.sma.const import DOMAIN
from universalassistant.core import UniversalAssistant

from . import MOCK_DEVICE, MOCK_USER_INPUT


@pytest.fixture
def mock_config_entry(hass: UniversalAssistant) -> MockConfigEntry:
    """Return the default mocked config entry."""

    return MockConfigEntry(
        domain=DOMAIN,
        title=MOCK_DEVICE.name,
        unique_id=str(MOCK_DEVICE.serial),
        data=MOCK_USER_INPUT,
        minor_version=2,
        entry_id="sma_entry_123",
    )


@pytest.fixture
def mock_setup_entry() -> Generator[AsyncMock]:
    """Mock the setup entry."""
    with patch(
        "universalassistant.components.sma.async_setup_entry", return_value=None
    ) as mock_setup_entry:
        yield mock_setup_entry


@pytest.fixture
def mock_sma_client() -> Generator[MagicMock]:
    """Mock the SMA client."""
    with patch(
        "universalassistant.components.sma.coordinator.SMAWebConnect", autospec=True
    ) as sma_cls:
        sma_instance: MagicMock = sma_cls.return_value
        sma_instance.device_info = AsyncMock(return_value=MOCK_DEVICE)
        sma_instance.new_session = AsyncMock(return_value=True)
        sma_instance.close_session = AsyncMock(return_value=True)
        sma_instance.get_sensors = AsyncMock(
            return_value=Sensors(
                sensor_map[GENERIC_SENSORS]
                + sensor_map[OPTIMIZERS_VIA_INVERTER]
                + sensor_map[ENERGY_METER_VIA_INVERTER]
            )
        )

        default_sensor_values = {
            "6100_00499100": 5000,
            "6100_00499500": 230,
            "6100_00499200": 20,
            "6100_00499300": 50,
            "6100_00499400": 100,
            "6100_00499600": 10,
            "6100_00499700": 1000,
        }

        async def _async_mock_read(sensors) -> bool:
            for sensor in sensors:
                if sensor.key in default_sensor_values:
                    sensor.value = default_sensor_values[sensor.key]
            return True

        sma_instance.read = AsyncMock(side_effect=_async_mock_read)

        with (
            patch(
                "universalassistant.components.sma.config_flow.SMAWebConnect",
                new=sma_cls,
            ),
            patch("universalassistant.components.sma.SMAWebConnect", new=sma_cls),
            patch("pysma.SMAWebConnect", new=sma_cls),
        ):
            yield sma_instance
