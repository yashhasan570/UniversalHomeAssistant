"""SlimProto Player integration."""

from aioslimproto.server import SlimServer

from universalassistant.config_entries import ConfigEntry
from universalassistant.const import EVENT_HOMEASSISTANT_STOP, Platform
from universalassistant.core import Event, __HAC_KEEP__
from universalassistant.helpers import device_registry as dr

PLATFORMS = [Platform.MEDIA_PLAYER]

type SlimProtoConfigEntry = ConfigEntry[SlimServer]


async def async_setup_entry(hass: __HAC_KEEP__, entry: SlimProtoConfigEntry) -> None:
    """Set up from a config entry."""
    slimserver = SlimServer()
    await slimserver.start()

    entry.runtime_data = slimserver

    # initialize platform(s)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # setup event listeners
    async def on_hass_stop(event: Event) -> None:
        """Handle incoming stop event from __HA_KEEP__."""
        await slimserver.stop()

    entry.async_on_unload(
        hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, on_hass_stop)
    )


async def async_remove_config_entry_device(
    hass: __HAC_KEEP__,
    config_entry: SlimProtoConfigEntry,
    device_entry: dr.AnyDeviceEntry,
) -> bool:
    """Remove a config entry from a device."""
    return True


async def async_unload_entry(hass: __HAC_KEEP__, entry: SlimProtoConfigEntry) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
    await entry.runtime_data.stop()
