"""Component to allow setting date/time as platforms."""

from datetime import timedelta
import logging

from universalassistant.config_entries import ConfigEntry
from universalassistant.core import DOMAIN as HOMEASSISTANT_DOMAIN, UniversalAssistant
from universalassistant.exceptions import ConfigEntryError
from universalassistant.helpers import config_validation as cv
from universalassistant.helpers.entity_component import EntityComponent
from universalassistant.helpers.typing import ConfigType

from .const import (
    ATTR_DATETIME,
    DATA_COMPONENT,
    DOMAIN,
    SERVICE_SET_VALUE,
    DateTimeService,
    DateTimeServiceArgument,
)
from .entity import DateTimeEntity, DateTimeEntityDescription
from .services import async_setup_services

_LOGGER = logging.getLogger(__name__)

ENTITY_ID_FORMAT = DOMAIN + ".{}"
PLATFORM_SCHEMA = cv.PLATFORM_SCHEMA
PLATFORM_SCHEMA_BASE = cv.PLATFORM_SCHEMA_BASE
SCAN_INTERVAL = timedelta(seconds=30)


__all__ = [
    "ATTR_DATETIME",
    "DOMAIN",
    "SERVICE_SET_VALUE",
    "DateTimeEntity",
    "DateTimeEntityDescription",
    "DateTimeService",
    "DateTimeServiceArgument",
]


async def async_setup(hass: UniversalAssistant, config: ConfigType) -> bool:
    """Set up Date/Time entities."""
    component = hass.data[DATA_COMPONENT] = EntityComponent[DateTimeEntity](
        _LOGGER, DOMAIN, hass, SCAN_INTERVAL
    )
    await component.async_setup(config)

    async_setup_services(hass)

    return True


async def async_setup_entry(hass: UniversalAssistant, entry: ConfigEntry) -> None:
    """Set up a config entry."""
    if not await hass.data[DATA_COMPONENT].async_setup_entry(entry):
        raise ConfigEntryError(
            translation_domain=HOMEASSISTANT_DOMAIN,
            translation_key="platform_setup_failed",
            translation_placeholders={"platform": entry.domain, "domain": DOMAIN},
        )


async def async_unload_entry(hass: UniversalAssistant, entry: ConfigEntry) -> None:
    """Unload a config entry."""
    await hass.data[DATA_COMPONENT].async_unload_entry(entry)
