"""Fixtures for USB Discovery integration tests."""

from unittest.mock import MagicMock, patch

from aiousbwatcher import InotifyNotAvailableError
import pytest

from universalassistant.components.usb import DOMAIN
from universalassistant.core import __HAC_KEEP__
from universalassistant.setup import async_setup_component

from . import patch_scanned_serial_ports


@pytest.fixture(name="force_usb_polling_watcher")
def force_usb_polling_watcher():
    """Patch the USB integration to not use inotify and fall back to polling."""
    with patch(
        "universalassistant.components.usb.AIOUSBWatcher.async_start",
        side_effect=InotifyNotAvailableError,
    ):
        yield


@pytest.fixture(name="setup_usb")
async def setup_usb_fixture(
    hass: __HAC_KEEP__, force_usb_polling_watcher: None
) -> MagicMock:
    """Set up USB integration and return the scanned serial ports mock."""
    with (
        patch("universalassistant.components.usb.async_get_usb", return_value=[]),
        patch_scanned_serial_ports(return_value=[]) as mock_serial_ports,
    ):
        assert await async_setup_component(hass, DOMAIN, {"usb": {}})
        await hass.async_block_till_done()
        yield mock_serial_ports
