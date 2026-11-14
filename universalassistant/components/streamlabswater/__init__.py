"""Support for Streamlabs Water Monitor devices."""

from streamlabswater.streamlabswater import StreamlabsClient

from universalassistant.const import CONF_API_KEY, Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import config_validation as cv
from universalassistant.helpers.typing import ConfigType

from .const import DOMAIN
from .coordinator import StreamlabsConfigEntry, StreamlabsCoordinator
from .services import async_setup_services

ISSUE_PLACEHOLDER = {"url": "/config/integrations/dashboard/add?domain=streamlabswater"}


PLATFORMS: list[Platform] = [Platform.BINARY_SENSOR, Platform.SENSOR]

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)


async def async_setup(hass: __HAC_KEEP__, config: ConfigType) -> bool:
    """Set up the integration."""
    async_setup_services(hass)
    return True


async def async_setup_entry(hass: __HAC_KEEP__, entry: StreamlabsConfigEntry) -> None:
    """Set up StreamLabs from a config entry."""

    api_key = entry.data[CONF_API_KEY]
    client = StreamlabsClient(api_key)
    coordinator = StreamlabsCoordinator(hass, entry, client)

    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(hass: __HAC_KEEP__, entry: StreamlabsConfigEntry) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
