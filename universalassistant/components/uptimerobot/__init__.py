"""The UptimeRobot integration."""

from pyuptimerobot import UptimeRobot

from universalassistant.const import CONF_API_KEY
from universalassistant.core import UniversalAssistant
from universalassistant.exceptions import ConfigEntryAuthFailed
from universalassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN, PLATFORMS
from .coordinator import UptimeRobotConfigEntry, UptimeRobotDataUpdateCoordinator


async def async_setup_entry(hass: UniversalAssistant, entry: UptimeRobotConfigEntry) -> None:
    """Set up UptimeRobot from a config entry."""
    key: str = entry.data[CONF_API_KEY]
    if key.startswith(("ur", "m")):
        raise ConfigEntryAuthFailed(
            translation_domain=DOMAIN,
            translation_key="api_key_wrong_type",
        )
    uptime_robot_api = UptimeRobot(key, async_get_clientsession(hass))

    coordinator = UptimeRobotDataUpdateCoordinator(
        hass,
        entry,
        api=uptime_robot_api,
    )

    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(
    hass: UniversalAssistant, entry: UptimeRobotConfigEntry
) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
