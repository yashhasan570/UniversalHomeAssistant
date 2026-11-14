"""The Z-Wave-Me WS integration."""

from universalassistant.core import __HAC_KEEP__
from universalassistant.exceptions import ConfigEntryNotReady
from universalassistant.helpers import device_registry as dr

from .const import PLATFORMS
from .controller import ZWaveMeConfigEntry, ZWaveMeController


async def async_setup_entry(hass: __HAC_KEEP__, entry: ZWaveMeConfigEntry) -> None:
    """Set up Z-Wave-Me from a config entry."""
    controller = ZWaveMeController(hass, entry)

    if not await controller.async_establish_connection():
        raise ConfigEntryNotReady

    entry.runtime_data = controller
    await async_setup_platforms(hass, entry, controller)
    registry = dr.async_get(hass)
    controller.remove_stale_devices(registry)


async def async_unload_entry(hass: __HAC_KEEP__, entry: ZWaveMeConfigEntry) -> None:
    """Unload a config entry."""

    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
    await entry.runtime_data.zwave_api.close_ws()


async def async_setup_platforms(
    hass: __HAC_KEEP__, entry: ZWaveMeConfigEntry, controller: ZWaveMeController
) -> None:
    """Set up platforms."""
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    controller.platforms_inited = True

    await hass.async_add_executor_job(controller.zwave_api.get_devices)
