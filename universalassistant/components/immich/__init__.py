"""The Immich integration."""

from universalassistant.const import Platform
from universalassistant.core import UniversalAssistant
from universalassistant.helpers import config_validation as cv
from universalassistant.helpers.typing import ConfigType

from .const import DOMAIN
from .coordinator import ImmichConfigEntry, ImmichDataUpdateCoordinator
from .services import async_setup_services

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)

PLATFORMS: list[Platform] = [Platform.SENSOR, Platform.UPDATE]


async def async_setup(hass: UniversalAssistant, config: ConfigType) -> bool:
    """Set up immich integration."""
    async_setup_services(hass)
    return True


async def async_setup_entry(hass: UniversalAssistant, entry: ImmichConfigEntry) -> None:
    """Set up Immich from a config entry."""

    coordinator = ImmichDataUpdateCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()
    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(hass: UniversalAssistant, entry: ImmichConfigEntry) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
