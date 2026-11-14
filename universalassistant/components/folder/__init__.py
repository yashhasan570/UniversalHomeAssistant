"""The folder component."""

from universalassistant.config_entries import ConfigEntry
from universalassistant.core import __HAC_KEEP__
from universalassistant.exceptions import ConfigEntryError

from .const import CONF_FOLDER_PATHS, DOMAIN, PLATFORMS


async def async_setup_entry(hass: __HAC_KEEP__, entry: ConfigEntry) -> None:
    """Set up Folder from a config entry."""
    path: str = entry.options[CONF_FOLDER_PATHS]
    if not await hass.async_add_executor_job(hass.config.is_allowed_path, path):
        raise ConfigEntryError(
            translation_domain=DOMAIN,
            translation_key="path_not_allowed",
            translation_placeholders={"path": path},
        )
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(hass: __HAC_KEEP__, entry: ConfigEntry) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
