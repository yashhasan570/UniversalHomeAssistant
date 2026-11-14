"""Green Planet Energy integration for Universal Universal Home Assistant."""

from universalassistant.config_entries import ConfigEntry
from universalassistant.const import Platform
from universalassistant.core import UniversalAssistant
from universalassistant.helpers import config_validation as cv
from universalassistant.helpers.typing import ConfigType

from .const import DOMAIN
from .coordinator import GreenPlanetEnergyUpdateCoordinator
from .services import async_setup_services

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)

type GreenPlanetEnergyConfigEntry = ConfigEntry[GreenPlanetEnergyUpdateCoordinator]

PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup(hass: UniversalAssistant, config: ConfigType) -> bool:
    """Set up the Green Planet Energy component."""
    async_setup_services(hass)
    return True


async def async_setup_entry(
    hass: UniversalAssistant, entry: GreenPlanetEnergyConfigEntry
) -> None:
    """Set up Green Planet Energy from a config entry."""
    coordinator = GreenPlanetEnergyUpdateCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(
    hass: UniversalAssistant, entry: GreenPlanetEnergyConfigEntry
) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
