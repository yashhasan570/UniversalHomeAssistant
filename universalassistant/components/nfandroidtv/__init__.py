"""The NFAndroidTV integration."""

import logging

from notifications_android_tv.notifications import ConnectError, Notifications

from universalassistant.config_entries import ConfigEntry
from universalassistant.const import CONF_HOST, CONF_NAME, Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.exceptions import ConfigEntryNotReady
from universalassistant.helpers import config_validation as cv, discovery
from universalassistant.helpers.typing import ConfigType

from .const import DATA_HASS_CONFIG, DOMAIN
from .services import async_setup_services

_LOGGER = logging.getLogger(__name__)
PLATFORMS = [Platform.NOTIFY]

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)
type NFAndroidTVConfigEntry = ConfigEntry[Notifications]


async def async_setup(hass: __HAC_KEEP__, config: ConfigType) -> bool:
    """Set up the NFAndroidTV component."""

    hass.data[DATA_HASS_CONFIG] = config

    async_setup_services(hass)
    return True


async def async_setup_entry(hass: __HAC_KEEP__, entry: NFAndroidTVConfigEntry) -> None:
    """Set up NFAndroidTV from a config entry."""

    hass.async_create_task(
        discovery.async_load_platform(
            hass,
            Platform.NOTIFY,
            DOMAIN,
            {CONF_NAME: entry.title, **entry.data},
            hass.data[DATA_HASS_CONFIG],
        )
    )

    try:
        client = await hass.async_add_executor_job(Notifications, entry.data[CONF_HOST])
    except ConnectError as e:
        _LOGGER.debug("Full exception:", exc_info=True)
        raise ConfigEntryNotReady(
            translation_domain=DOMAIN,
            translation_key="setup_connection_error",
            translation_placeholders={"name": entry.title},
        ) from e

    entry.runtime_data = client

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(
    hass: __HAC_KEEP__, entry: NFAndroidTVConfigEntry
) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
