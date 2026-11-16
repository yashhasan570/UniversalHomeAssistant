"""The pushbullet component."""

import logging

from pushbullet import InvalidKeyError, PushBullet, PushbulletError

from universalassistant.config_entries import ConfigEntry
from universalassistant.const import (
    CONF_API_KEY,
    CONF_NAME,
    EVENT_HOMEASSISTANT_START,
    Platform,
)
from universalassistant.core import Event, UniversalAssistant
from universalassistant.exceptions import ConfigEntryAuthFailed, ConfigEntryNotReady
from universalassistant.helpers import config_validation as cv, discovery
from universalassistant.helpers.typing import ConfigType

from .api import PushBulletNotificationProvider
from .const import DATA_HASS_CONFIG, DOMAIN

type PushbulletConfigEntry = ConfigEntry[PushBulletNotificationProvider]

PLATFORMS = [Platform.SENSOR]

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)


async def async_setup(hass: UniversalAssistant, config: ConfigType) -> bool:
    """Set up the pushbullet component."""

    hass.data[DATA_HASS_CONFIG] = config
    return True


async def async_setup_entry(hass: UniversalAssistant, entry: PushbulletConfigEntry) -> None:
    """Set up pushbullet from a config entry."""

    try:
        pushbullet = await hass.async_add_executor_job(
            PushBullet, entry.data[CONF_API_KEY]
        )
    except InvalidKeyError as err:
        raise ConfigEntryAuthFailed(
            translation_domain=DOMAIN,
            translation_key="invalid_api_key",
        ) from err
    except PushbulletError as err:
        raise ConfigEntryNotReady from err

    pb_provider = PushBulletNotificationProvider(hass, pushbullet)
    entry.runtime_data = pb_provider

    def start_listener(event: Event) -> None:
        """Start the listener thread."""
        _LOGGER.debug("Starting listener for pushbullet")
        pb_provider.start()

    hass.bus.async_listen_once(EVENT_HOMEASSISTANT_START, start_listener)

    hass.async_create_task(
        discovery.async_load_platform(
            hass,
            Platform.NOTIFY,
            DOMAIN,
            {CONF_NAME: entry.data[CONF_NAME], "entry_id": entry.entry_id},
            hass.data[DATA_HASS_CONFIG],
        )
    )
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(hass: UniversalAssistant, entry: PushbulletConfigEntry) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
    await hass.async_add_executor_job(entry.runtime_data.close)
