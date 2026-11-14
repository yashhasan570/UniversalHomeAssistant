"""The Kiosker integration."""

from universalassistant.const import Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import config_validation as cv
from universalassistant.helpers.typing import ConfigType

from .const import DOMAIN
from .coordinator import KioskerConfigEntry, KioskerDataUpdateCoordinator
from .services import async_setup_services

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)

_PLATFORMS: list[Platform] = [
    Platform.BINARY_SENSOR,
    Platform.BUTTON,
    Platform.SENSOR,
    Platform.SWITCH,
]


async def async_setup(hass: __HAC_KEEP__, config: ConfigType) -> bool:
    """Set up the Kiosker integration."""
    async_setup_services(hass)
    return True


async def async_setup_entry(hass: __HAC_KEEP__, entry: KioskerConfigEntry) -> None:
    """Set up Kiosker from a config entry."""

    coordinator = KioskerDataUpdateCoordinator(hass, entry)

    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, _PLATFORMS)


async def async_unload_entry(hass: __HAC_KEEP__, entry: KioskerConfigEntry) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, _PLATFORMS)
