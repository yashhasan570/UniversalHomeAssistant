"""Snapcast Integration."""

from universalassistant.const import CONF_HOST, CONF_PORT
from universalassistant.core import UniversalAssistant
from universalassistant.exceptions import ConfigEntryNotReady
from universalassistant.helpers import config_validation as cv
from universalassistant.helpers.typing import ConfigType

from .const import DOMAIN, PLATFORMS
from .coordinator import SnapcastConfigEntry, SnapcastUpdateCoordinator
from .services import async_setup_services

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)


async def async_setup(hass: UniversalAssistant, config: ConfigType) -> bool:
    """Set up the component."""
    async_setup_services(hass)
    return True


async def async_setup_entry(hass: UniversalAssistant, entry: SnapcastConfigEntry) -> None:
    """Set up Snapcast from a config entry."""
    coordinator = SnapcastUpdateCoordinator(hass, entry)

    try:
        await coordinator.async_config_entry_first_refresh()
    except OSError as ex:
        raise ConfigEntryNotReady(
            "Could not connect to Snapcast server at "
            f"{entry.data[CONF_HOST]}:{entry.data[CONF_PORT]}"
        ) from ex

    entry.runtime_data = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(hass: UniversalAssistant, entry: SnapcastConfigEntry) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
    # disconnect from server
    await entry.runtime_data.disconnect()
