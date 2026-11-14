"""Test the OctoPrint services."""

from unittest.mock import patch

import pytest

from universalassistant.components.octoprint.const import DOMAIN
from universalassistant.components.octoprint.services import (
    OctoPrintService,
    OctoPrintServiceArgument,
)
from universalassistant.const import CommonServiceArgument, Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import device_registry as dr


@pytest.fixture
def platform() -> Platform:
    """Fixture to specify platform."""
    return Platform.SENSOR


@pytest.mark.usefixtures("init_integration")
async def test_connect_default(
    hass: __HAC_KEEP__, device_registry: dr.DeviceRegistry
) -> None:
    """Test the connect to printer service."""
    device = dr.async_entries_for_config_entry(device_registry, "uuid")[0]

    # Test pausing the printer when it is printing
    with patch("pyoctoprintapi.OctoprintClient.connect") as connect_command:
        await hass.services.async_call(
            DOMAIN,
            OctoPrintService.PRINTER_CONNECT,
            {
                CommonServiceArgument.DEVICE_ID: device.id,
            },
            blocking=True,
        )

        assert len(connect_command.mock_calls) == 1
        connect_command.assert_called_with(
            port=None, printer_profile=None, baud_rate=None
        )


@pytest.mark.usefixtures("init_integration")
async def test_connect_all_arguments(
    hass: __HAC_KEEP__, device_registry: dr.DeviceRegistry
) -> None:
    """Test the connect to printer service."""
    device = dr.async_entries_for_config_entry(device_registry, "uuid")[0]

    # Test pausing the printer when it is printing
    with patch("pyoctoprintapi.OctoprintClient.connect") as connect_command:
        await hass.services.async_call(
            DOMAIN,
            OctoPrintService.PRINTER_CONNECT,
            {
                CommonServiceArgument.DEVICE_ID: device.id,
                OctoPrintServiceArgument.PROFILE_NAME: "Test Profile",
                OctoPrintServiceArgument.PORT: "VIRTUAL",
                OctoPrintServiceArgument.BAUDRATE: 9600,
            },
            blocking=True,
        )

        assert len(connect_command.mock_calls) == 1
        connect_command.assert_called_with(
            port="VIRTUAL", printer_profile="Test Profile", baud_rate=9600
        )
