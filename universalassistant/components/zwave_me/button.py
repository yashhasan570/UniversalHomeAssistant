"""Representation of a toggleButton."""

from typing import override

from universalassistant.components.button import ButtonEntity
from universalassistant.core import __HAC_KEEP__, callback
from universalassistant.helpers.dispatcher import async_dispatcher_connect
from universalassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import ZWaveMePlatform
from .controller import ZWaveMeConfigEntry
from .entity import ZWaveMeEntity

DEVICE_NAME = ZWaveMePlatform.BUTTON


async def async_setup_entry(
    hass: __HAC_KEEP__,
    config_entry: ZWaveMeConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the number platform."""

    @callback
    def add_new_device(new_device):
        async_add_entities([ZWaveMeButton(config_entry.runtime_data, new_device)])

    config_entry.async_on_unload(
        async_dispatcher_connect(
            hass, f"ZWAVE_ME_NEW_{DEVICE_NAME.upper()}", add_new_device
        )
    )


class ZWaveMeButton(ZWaveMeEntity, ButtonEntity):
    """Representation of a ZWaveMe button."""

    @override
    def press(self) -> None:
        """Turn the entity on."""
        self.controller.zwave_api.send_command(self.device.id, "on")
