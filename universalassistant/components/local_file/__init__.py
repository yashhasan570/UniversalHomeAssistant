"""The local_file component."""

from universalassistant.config_entries import ConfigEntry
from universalassistant.const import CONF_FILE_PATH, Platform
from universalassistant.core import UniversalAssistant
from universalassistant.exceptions import ConfigEntryError
from universalassistant.helpers import config_validation as cv
from universalassistant.helpers.typing import ConfigType

from .const import DOMAIN
from .services import async_setup_services
from .util import check_file_path_access

PLATFORMS = [Platform.CAMERA]


CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)


async def async_setup(hass: UniversalAssistant, config: ConfigType) -> bool:
    """Set up the Local file integration."""
    async_setup_services(hass)
    return True


async def async_setup_entry(hass: UniversalAssistant, entry: ConfigEntry) -> None:
    """Set up Local file from a config entry."""
    file_path: str = entry.options[CONF_FILE_PATH]
    if not await hass.async_add_executor_job(check_file_path_access, file_path):
        raise ConfigEntryError(
            translation_domain=DOMAIN,
            translation_key="not_readable_path",
            translation_placeholders={"file_path": file_path},
        )

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(hass: UniversalAssistant, entry: ConfigEntry) -> None:
    """Unload Local file config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
