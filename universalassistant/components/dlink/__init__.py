"""The D-Link Power Plug integration."""

from pyW215.pyW215 import SmartPlug

from universalassistant.config_entries import ConfigEntry
from universalassistant.const import CONF_HOST, CONF_PASSWORD, CONF_USERNAME, Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.exceptions import ConfigEntryNotReady

from .const import CONF_USE_LEGACY_PROTOCOL
from .data import SmartPlugData

type DLinkConfigEntry = ConfigEntry[SmartPlugData]

PLATFORMS = [Platform.SWITCH]


async def async_setup_entry(hass: __HAC_KEEP__, entry: DLinkConfigEntry) -> None:
    """Set up D-Link Power Plug from a config entry."""
    smartplug = await hass.async_add_executor_job(
        SmartPlug,
        entry.data[CONF_HOST],
        entry.data[CONF_PASSWORD],
        entry.data[CONF_USERNAME],
        entry.data[CONF_USE_LEGACY_PROTOCOL],
    )
    if not smartplug.authenticated and smartplug.use_legacy_protocol:
        raise ConfigEntryNotReady("Cannot connect/authenticate")

    entry.runtime_data = SmartPlugData(smartplug)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(hass: __HAC_KEEP__, entry: DLinkConfigEntry) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
