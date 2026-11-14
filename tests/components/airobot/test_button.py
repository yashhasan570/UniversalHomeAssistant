"""Tests for the Airobot button platform."""

from unittest.mock import AsyncMock

from pyairobotrest.exceptions import (
    AirobotConnectionError,
    AirobotError,
    AirobotTimeoutError,
)
import pytest
from pytest_universalassistant.common import MockConfigEntry, snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.button import DOMAIN as BUTTON_DOMAIN, ButtonService
from universalassistant.const import CommonServiceArgument, Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.exceptions import __HAC_KEEP__Error
from universalassistant.helpers import entity_registry as er


@pytest.fixture
def platforms() -> list[Platform]:
    """Fixture to specify platforms to test."""
    return [Platform.BUTTON]


@pytest.mark.usefixtures("entity_registry_enabled_by_default", "init_integration")
async def test_buttons(
    hass: __HAC_KEEP__,
    snapshot: SnapshotAssertion,
    entity_registry: er.EntityRegistry,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test the button entities."""
    await snapshot_platform(hass, entity_registry, snapshot, mock_config_entry.entry_id)


@pytest.mark.usefixtures("init_integration")
async def test_restart_button(
    hass: __HAC_KEEP__,
    mock_airobot_client: AsyncMock,
) -> None:
    """Test restart button."""
    await hass.services.async_call(
        BUTTON_DOMAIN,
        ButtonService.PRESS,
        {CommonServiceArgument.ENTITY_ID: "button.test_thermostat_restart"},
        blocking=True,
    )

    mock_airobot_client.reboot_thermostat.assert_called_once()


@pytest.mark.usefixtures("init_integration")
async def test_restart_button_error(
    hass: __HAC_KEEP__,
    mock_airobot_client: AsyncMock,
) -> None:
    """Test restart button error handling for unexpected errors."""
    mock_airobot_client.reboot_thermostat.side_effect = AirobotError("Test error")

    with pytest.raises(__HAC_KEEP__Error):
        await hass.services.async_call(
            BUTTON_DOMAIN,
            ButtonService.PRESS,
            {CommonServiceArgument.ENTITY_ID: "button.test_thermostat_restart"},
            blocking=True,
        )

    mock_airobot_client.reboot_thermostat.assert_called_once()


@pytest.mark.usefixtures("entity_registry_enabled_by_default", "init_integration")
async def test_recalibrate_co2_button(
    hass: __HAC_KEEP__,
    mock_airobot_client: AsyncMock,
) -> None:
    """Test recalibrate CO2 sensor button."""
    await hass.services.async_call(
        BUTTON_DOMAIN,
        ButtonService.PRESS,
        {
            CommonServiceArgument.ENTITY_ID: "button.test_thermostat_recalibrate_co2_sensor"
        },
        blocking=True,
    )

    mock_airobot_client.recalibrate_co2_sensor.assert_called_once()


@pytest.mark.usefixtures("entity_registry_enabled_by_default", "init_integration")
@pytest.mark.parametrize(
    "exception",
    [
        AirobotError("Test error"),
        AirobotConnectionError("Connection lost"),
        AirobotTimeoutError("Timeout"),
    ],
)
async def test_recalibrate_co2_button_error(
    hass: __HAC_KEEP__,
    mock_airobot_client: AsyncMock,
    exception: Exception,
) -> None:
    """Test recalibrate CO2 sensor button error handling."""
    mock_airobot_client.recalibrate_co2_sensor.side_effect = exception

    with pytest.raises(__HAC_KEEP__Error):
        await hass.services.async_call(
            BUTTON_DOMAIN,
            ButtonService.PRESS,
            {
                CommonServiceArgument.ENTITY_ID: "button.test_thermostat_recalibrate_co2_sensor"
            },
            blocking=True,
        )

    mock_airobot_client.recalibrate_co2_sensor.assert_called_once()
