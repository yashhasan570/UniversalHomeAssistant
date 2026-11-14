"""Utility functions for __HA_KEEP__ Connect ZBT-2 integration."""

import logging

from universalassistant.helpers.service_info.usb import UsbServiceInfo

from . import __HAC_KEEP__ConnectZBT2ConfigEntry

_LOGGER = logging.getLogger(__name__)


def get_usb_service_info(
    config_entry: __HAC_KEEP__ConnectZBT2ConfigEntry,
) -> UsbServiceInfo:
    """Return UsbServiceInfo."""
    return UsbServiceInfo(
        device=config_entry.data["device"],
        vid=config_entry.data["vid"],
        pid=config_entry.data["pid"],
        serial_number=config_entry.data["serial_number"],
        manufacturer=config_entry.data["manufacturer"],
        description=config_entry.data["product"],
    )
