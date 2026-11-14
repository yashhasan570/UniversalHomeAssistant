"""Creates Button entities for the my-PV integration."""

from typing import Any, Final, override

from universalassistant.components.button import (
    ButtonDeviceClass,
    ButtonEntity,
    ButtonEntityDescription,
)
from universalassistant.const import EntityCategory
from universalassistant.core import __HAC_KEEP__
from universalassistant.exceptions import __HAC_KEEP__Error
from universalassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import DOMAIN
from .coordinator import MyPVConfigEntry
from .entity import MyPVBaseEntity

PARALLEL_UPDATES = 0

REBOOT_DEVICE_DESCRIPTION: Final = ButtonEntityDescription(
    key="reboot_device",
    device_class=ButtonDeviceClass.RESTART,
    entity_category=EntityCategory.DIAGNOSTIC,
)


async def async_setup_entry(
    hass: __HAC_KEEP__,
    config_entry: MyPVConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the my-PV button."""
    coordinator = config_entry.runtime_data

    config = coordinator.device.get_command_configuration(REBOOT_DEVICE_DESCRIPTION.key)
    if config and config.get("type") in ["any", "fixed"]:
        async_add_entities([MyPVCommandButton(coordinator, REBOOT_DEVICE_DESCRIPTION)])


class MyPVCommandButton(MyPVBaseEntity, ButtonEntity):
    """Base my-PV Button."""

    @override
    async def async_press(self, **kwargs: Any) -> None:
        """Handle the button press."""

        if not await self.coordinator.send_command(self.entity_description.key):
            raise __HAC_KEEP__Error(
                translation_domain=DOMAIN, translation_key="unknown_error"
            )
