"""Support for functionality to download files."""

import os

from universalassistant.config_entries import ConfigEntry
from universalassistant.core import __HAC_KEEP__
from universalassistant.exceptions import ConfigEntryError
from universalassistant.helpers import config_validation as cv
from universalassistant.helpers.typing import ConfigType

from .const import CONF_DOWNLOAD_DIR, DOMAIN
from .services import async_setup_services

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)


async def async_setup(hass: __HAC_KEEP__, config: ConfigType) -> bool:
    """Set up the Downloader component."""
    async_setup_services(hass)
    return True


async def async_setup_entry(hass: __HAC_KEEP__, entry: ConfigEntry) -> None:
    """Listen for download events to download files."""
    download_path = entry.data[CONF_DOWNLOAD_DIR]

    # If path is relative, we assume relative to __HA_KEEP__ config dir
    if not os.path.isabs(download_path):
        download_path = hass.config.path(download_path)
        hass.config_entries.async_update_entry(
            entry, data={**entry.data, CONF_DOWNLOAD_DIR: download_path}
        )

    if not await hass.async_add_executor_job(os.path.isdir, download_path):
        raise ConfigEntryError(
            translation_domain=DOMAIN,
            translation_key="download_path_not_found",
            translation_placeholders={"path": download_path},
        )
