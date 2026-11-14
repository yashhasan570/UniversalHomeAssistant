"""The Broadlink integration."""

from universalassistant.config_entries import ConfigEntry
from universalassistant.const import CONF_HOST
from universalassistant.core import __HAC_KEEP__
from universalassistant.exceptions import ConfigEntryError
from universalassistant.helpers import config_validation as cv
from universalassistant.helpers.typing import ConfigType

from .const import BROADLINK_DATA, DOMAIN, BroadlinkData
from .device import BroadlinkDevice
from .heartbeat import BroadlinkHeartbeat

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)


async def async_setup(hass: __HAC_KEEP__, config: ConfigType) -> bool:
    """Set up the Broadlink integration."""
    hass.data[BROADLINK_DATA] = BroadlinkData()
    return True


async def async_setup_entry(hass: __HAC_KEEP__, entry: ConfigEntry) -> None:
    """Set up a Broadlink device from a config entry."""
    data = hass.data[BROADLINK_DATA]

    device = BroadlinkDevice(hass, entry)
    if not await device.async_setup():
        raise ConfigEntryError(
            translation_domain=DOMAIN,
            translation_key="setup_failed",
            translation_placeholders={"host": entry.data[CONF_HOST]},
        )
    if data.heartbeat is None:
        data.heartbeat = BroadlinkHeartbeat(hass)
        hass.async_create_task(data.heartbeat.async_setup())


async def async_unload_entry(hass: __HAC_KEEP__, entry: ConfigEntry) -> None:
    """Unload a config entry."""
    data = hass.data[BROADLINK_DATA]

    device = data.devices.pop(entry.entry_id)
    result = await device.async_unload()

    if data.heartbeat and not data.devices:
        await data.heartbeat.async_unload()
        data.heartbeat = None

    if not result:
        raise ConfigEntryError(
            translation_domain=DOMAIN,
            translation_key="unload_failed",
        )
