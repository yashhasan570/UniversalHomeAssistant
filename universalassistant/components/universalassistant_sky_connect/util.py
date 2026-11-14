"""Utility functions for __HA_KEEP__ SkyConnect integration."""

import logging

from universalassistant.helpers.service_info.usb import UsbServiceInfo

from . import __HAC_KEEP__SkyConnectConfigEntry
from .const import HardwareVariant

_LOGGER = logging.getLogger(__name__)


def get_usb_service_info(
    config_entry: __HAC_KEEP__SkyConnectConfigEntry,
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


def get_hardware_variant(
    config_entry: __HAC_KEEP__SkyConnectConfigEntry,
) -> HardwareVariant:
    """Get the hardware variant from the config entry."""
    return HardwareVariant.from_usb_product_name(config_entry.data["product"])
