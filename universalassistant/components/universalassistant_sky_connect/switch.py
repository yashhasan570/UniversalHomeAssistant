"""__HA_KEEP__ SkyConnect switch entities."""

import logging

from universalassistant.components.universalassistant_hardware.coordinator import (
    FirmwareUpdateCoordinator,
)
from universalassistant.components.universalassistant_hardware.switch import (
    BaseBetaFirmwareSwitch,
)
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers.device_registry import DeviceInfo
from universalassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import __HAC_KEEP__SkyConnectConfigEntry
from .const import DOMAIN, PRODUCT, SERIAL_NUMBER, HardwareVariant

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: __HAC_KEEP__,
    config_entry: __HAC_KEEP__SkyConnectConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the switch platform for __HA_KEEP__ SkyConnect."""
    async_add_entities(
        [BetaFirmwareSwitch(config_entry.runtime_data.coordinator, config_entry)]
    )


class BetaFirmwareSwitch(BaseBetaFirmwareSwitch):
    """__HA_KEEP__ SkyConnect beta firmware switch."""

    def __init__(
        self,
        coordinator: FirmwareUpdateCoordinator,
        config_entry: __HAC_KEEP__SkyConnectConfigEntry,
    ) -> None:
        """Initialize the beta firmware switch."""
        super().__init__(coordinator, config_entry)

        variant = HardwareVariant.from_usb_product_name(
            self._config_entry.data[PRODUCT]
        )
        serial_number = self._config_entry.data[SERIAL_NUMBER]

        self._attr_unique_id = f"{serial_number}_beta_firmware"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, serial_number)},
            name=f"{variant.full_name} ({serial_number[:8]})",
            model=variant.full_name,
            manufacturer="Nabu Casa",
            serial_number=serial_number,
            via_device_id=config_entry.runtime_data.via_device_id,
        )
