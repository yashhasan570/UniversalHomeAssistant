"""The EnergyZero integration."""

from universalassistant.const import Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.exceptions import ConfigEntryNotReady
from universalassistant.helpers import config_validation as cv
from universalassistant.helpers.typing import ConfigType

from .const import DOMAIN
from .coordinator import EnergyZeroConfigEntry, EnergyZeroDataUpdateCoordinator
from .services import async_setup_services

PLATFORMS: list[Platform] = [Platform.SENSOR]
CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)


async def async_setup(hass: __HAC_KEEP__, config: ConfigType) -> bool:
    """Set up EnergyZero services."""

    async_setup_services(hass)

    return True


async def async_setup_entry(hass: __HAC_KEEP__, entry: EnergyZeroConfigEntry) -> None:
    """Set up EnergyZero from a config entry."""

    coordinator = EnergyZeroDataUpdateCoordinator(hass, entry)
    try:
        await coordinator.async_config_entry_first_refresh()
    except ConfigEntryNotReady:
        await coordinator.energyzero.close()
        raise

    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(hass: __HAC_KEEP__, entry: EnergyZeroConfigEntry) -> None:
    """Unload EnergyZero config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
