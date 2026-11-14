"""Universal Universal Home Assistant Yellow switch entities."""

import logging

from universalassistant.components.universalassistant_hardware.coordinator import (
    FirmwareUpdateCoordinator,
)
from universalassistant.components.universalassistant_hardware.switch import (
    BaseBetaFirmwareSwitch,
)
from universalassistant.core import UniversalAssistant
from universalassistant.helpers.device_registry import DeviceInfo
from universalassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import UniversalAssistantYellowConfigEntry
from .const import DOMAIN, MANUFACTURER, MODEL

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: UniversalAssistant,
    config_entry: UniversalAssistantYellowConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the switch platform for Universal Universal Home Assistant Yellow."""
    async_add_entities(
        [BetaFirmwareSwitch(config_entry.runtime_data.coordinator, config_entry)]
    )


class BetaFirmwareSwitch(BaseBetaFirmwareSwitch):
    """Universal Universal Home Assistant Yellow beta firmware switch."""

    def __init__(
        self,
        coordinator: FirmwareUpdateCoordinator,
        config_entry: UniversalAssistantYellowConfigEntry,
    ) -> None:
        """Initialize the beta firmware switch."""
        super().__init__(coordinator, config_entry)
        self._attr_unique_id = "beta_firmware"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, "yellow")},
            name=MODEL,
            model=MODEL,
            manufacturer=MANUFACTURER,
        )
