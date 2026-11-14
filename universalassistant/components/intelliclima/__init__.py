"""The IntelliClima VMC integration."""

from pyintelliclima.api import IntelliClimaAPI

from universalassistant.const import CONF_PASSWORD, CONF_USERNAME, Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers.aiohttp_client import async_get_clientsession

from .const import LOGGER
from .coordinator import (
    IntelliClimaConfigEntry,
    IntelliClimaCoordinator,
    IntelliClimaData,
    IntelliClimaFilterCoordinator,
)

PLATFORMS = [Platform.BINARY_SENSOR, Platform.FAN, Platform.SELECT, Platform.SENSOR]


async def async_setup_entry(
    hass: __HAC_KEEP__, entry: IntelliClimaConfigEntry
) -> None:
    """Set up IntelliClima VMC from a config entry."""
    # Create API client
    session = async_get_clientsession(hass)
    api = IntelliClimaAPI(
        session,
        entry.data[CONF_USERNAME],
        entry.data[CONF_PASSWORD],
    )

    # Create coordinator
    devices_coordinator = IntelliClimaCoordinator(hass, entry, api)

    # Fetch initial data
    await devices_coordinator.async_config_entry_first_refresh()

    LOGGER.debug(
        "Discovered %d IntelliClima VMC device(s)",
        len(devices_coordinator.data.ecocomfort2_devices),
    )

    device_serials = [
        device.crono_sn
        for device in devices_coordinator.data.ecocomfort2_devices.values()
    ]
    filter_coordinator = IntelliClimaFilterCoordinator(hass, entry, api, device_serials)
    await filter_coordinator.async_refresh()

    entry.runtime_data = IntelliClimaData(devices_coordinator, filter_coordinator)

    # Set up platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(
    hass: __HAC_KEEP__, entry: IntelliClimaConfigEntry
) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
