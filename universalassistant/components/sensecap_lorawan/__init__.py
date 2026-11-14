"""Support SenseCAP devices over LoRaWAN."""

from lorawan_connection import ConnectionUnavailable
from sensecap_lorawan import SenseCapDevice, SenseCapDeviceCollection

from universalassistant.components.lorawan import DeviceManager
from universalassistant.config_entries import ConfigEntry
from universalassistant.const import Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.exceptions import ConfigEntryNotReady
from universalassistant.helpers import config_validation as cv

from .const import DOMAIN
from .coordinator import SenseCapCoordinator

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)
type SenseCapConfigEntry = ConfigEntry[
    DeviceManager[SenseCapDevice, SenseCapCoordinator]
]
PLATFORMS = [Platform.SENSOR]


async def async_setup_entry(hass: __HAC_KEEP__, entry: SenseCapConfigEntry) -> None:
    """Set up SenseCAP devices across the available LoRaWAN connections."""
    manager = entry.runtime_data = DeviceManager(
        hass,
        entry,
        create_collection=SenseCapDeviceCollection,
        create_coordinator=SenseCapCoordinator,
    )
    entry.async_on_unload(manager.close)
    try:
        await manager.async_setup()
    except ConnectionUnavailable as err:
        raise ConfigEntryNotReady(str(err)) from err
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(hass: __HAC_KEEP__, entry: SenseCapConfigEntry) -> None:
    """Unload entities; the manager releases the collection and coordinators."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
