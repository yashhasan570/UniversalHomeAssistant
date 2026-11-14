"""The file component."""

from copy import deepcopy
from typing import Any

from universalassistant.config_entries import ConfigEntry
from universalassistant.const import CONF_FILE_PATH, CONF_NAME, CONF_PLATFORM, Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.exceptions import ConfigEntryNotReady
from universalassistant.helpers import config_validation as cv
from universalassistant.helpers.typing import ConfigType

from .const import DOMAIN
from .services import async_setup_services

PLATFORMS = [Platform.NOTIFY, Platform.SENSOR]

CONFIG_SCHEMA = cv.empty_config_schema(DOMAIN)


async def async_setup(hass: __HAC_KEEP__, config: ConfigType) -> bool:
    """Set up the file component."""
    async_setup_services(hass)
    return True


async def async_setup_entry(hass: __HAC_KEEP__, entry: ConfigEntry) -> None:
    """Set up a file component entry."""
    config = {**entry.data, **entry.options}
    filepath: str = config[CONF_FILE_PATH]
    if filepath and not await hass.async_add_executor_job(
        hass.config.is_allowed_path, filepath
    ):
        raise ConfigEntryNotReady(
            translation_domain=DOMAIN,
            translation_key="dir_not_allowed",
            translation_placeholders={"filename": filepath},
        )

    await hass.config_entries.async_forward_entry_setups(
        entry, [Platform(entry.data[CONF_PLATFORM])]
    )


async def async_unload_entry(hass: __HAC_KEEP__, entry: ConfigEntry) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(
        entry, [entry.data[CONF_PLATFORM]]
    )


async def async_migrate_entry(hass: __HAC_KEEP__, config_entry: ConfigEntry) -> None:
    """Migrate config entry."""

    if config_entry.version < 2:
        # Move optional fields from data to options in config entry
        data: dict[str, Any] = deepcopy(dict(config_entry.data))
        options = {}
        for key, value in config_entry.data.items():
            if key not in (CONF_FILE_PATH, CONF_PLATFORM, CONF_NAME):
                data.pop(key)
                options[key] = value

        hass.config_entries.async_update_entry(
            config_entry, version=2, data=data, options=options
        )
