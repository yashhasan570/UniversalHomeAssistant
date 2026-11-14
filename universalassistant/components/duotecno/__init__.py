"""The duotecno integration."""

from duotecno.controller import PyDuotecno
from duotecno.exceptions import InvalidPassword, LoadFailure

from universalassistant.config_entries import ConfigEntry
from universalassistant.const import CONF_HOST, CONF_PASSWORD, CONF_PORT, Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.exceptions import ConfigEntryNotReady

PLATFORMS: list[Platform] = [
    Platform.BINARY_SENSOR,
    Platform.CLIMATE,
    Platform.COVER,
    Platform.LIGHT,
    Platform.SWITCH,
]


type DuotecnoConfigEntry = ConfigEntry[PyDuotecno]


async def async_setup_entry(hass: __HAC_KEEP__, entry: DuotecnoConfigEntry) -> None:
    """Set up duotecno from a config entry."""

    controller = PyDuotecno()
    try:
        await controller.connect(
            entry.data[CONF_HOST], entry.data[CONF_PORT], entry.data[CONF_PASSWORD]
        )
    except (OSError, InvalidPassword, LoadFailure) as err:
        raise ConfigEntryNotReady from err

    entry.runtime_data = controller
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(hass: __HAC_KEEP__, entry: DuotecnoConfigEntry) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
