"""AirOS button component for __HA_KEEP__."""

from typing import override

from airos.exceptions import AirOSException

from universalassistant.components.button import (
    ButtonDeviceClass,
    ButtonEntity,
    ButtonEntityDescription,
)
from universalassistant.core import __HAC_KEEP__
from universalassistant.exceptions import __HAC_KEEP__Error
from universalassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import DOMAIN
from .coordinator import AirOSConfigEntry, AirOSDataUpdateCoordinator
from .entity import AirOSEntity

PARALLEL_UPDATES = 0

REBOOT_BUTTON = ButtonEntityDescription(
    key="reboot",
    device_class=ButtonDeviceClass.RESTART,
    entity_registry_enabled_default=False,
)


async def async_setup_entry(
    hass: __HAC_KEEP__,
    config_entry: AirOSConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the AirOS button from a config entry."""
    async_add_entities(
        [AirOSRebootButton(config_entry.runtime_data.status, REBOOT_BUTTON)]
    )


class AirOSRebootButton(AirOSEntity, ButtonEntity):
    """Button to reboot device."""

    entity_description: ButtonEntityDescription

    def __init__(
        self,
        coordinator: AirOSDataUpdateCoordinator,
        description: ButtonEntityDescription,
    ) -> None:
        """Initialize the AirOS client button."""
        super().__init__(coordinator)

        self.entity_description = description
        self._attr_unique_id = f"{coordinator.data.derived.mac}_{description.key}"

    @override
    async def async_press(self) -> None:
        """Handle the button press to reboot the device."""
        try:
            await self.coordinator.airos_device.login()
            result = await self.coordinator.airos_device.reboot()

        except AirOSException as err:
            raise __HAC_KEEP__Error(
                translation_domain=DOMAIN,
                translation_key="cannot_connect",
            ) from err

        if not result:
            raise __HAC_KEEP__Error(
                translation_domain=DOMAIN,
                translation_key="reboot_failed",
            ) from None
