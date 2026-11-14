"""Component to allow setting text as platforms."""

from datetime import timedelta
import logging

from universalassistant.config_entries import ConfigEntry
from universalassistant.const import ATTR_MODE
from universalassistant.core import DOMAIN as HOMEASSISTANT_DOMAIN, __HAC_KEEP__
from universalassistant.exceptions import ConfigEntryError
from universalassistant.helpers import config_validation as cv
from universalassistant.helpers.entity_component import EntityComponent
from universalassistant.helpers.typing import ConfigType

from .const import (
    ATTR_MAX,
    ATTR_MIN,
    ATTR_PATTERN,
    ATTR_VALUE,
    DATA_COMPONENT,
    DOMAIN,
    SERVICE_SET_VALUE,
    TextEntityCapabilityAttribute,
    TextMode,
    TextService,
    TextServiceArgument,
)
from .entity import RestoreText, TextEntity, TextEntityDescription, TextExtraStoredData
from .services import async_setup_services

_LOGGER = logging.getLogger(__name__)

ENTITY_ID_FORMAT = DOMAIN + ".{}"
PLATFORM_SCHEMA = cv.PLATFORM_SCHEMA
PLATFORM_SCHEMA_BASE = cv.PLATFORM_SCHEMA_BASE
SCAN_INTERVAL = timedelta(seconds=30)

MIN_TIME_BETWEEN_SCANS = timedelta(seconds=10)


__all__ = [
    "ATTR_MAX",
    "ATTR_MIN",
    "ATTR_MODE",
    "ATTR_PATTERN",
    "ATTR_VALUE",
    "DOMAIN",
    "SERVICE_SET_VALUE",
    "RestoreText",
    "TextEntity",
    "TextEntityCapabilityAttribute",
    "TextEntityDescription",
    "TextExtraStoredData",
    "TextMode",
    "TextService",
    "TextServiceArgument",
]


async def async_setup(hass: __HAC_KEEP__, config: ConfigType) -> bool:
    """Set up Text entities."""
    component = hass.data[DATA_COMPONENT] = EntityComponent[TextEntity](
        _LOGGER, DOMAIN, hass, SCAN_INTERVAL
    )
    await component.async_setup(config)

    async_setup_services(hass)

    return True


async def async_setup_entry(hass: __HAC_KEEP__, entry: ConfigEntry) -> None:
    """Set up a config entry."""
    if not await hass.data[DATA_COMPONENT].async_setup_entry(entry):
        raise ConfigEntryError(
            translation_domain=HOMEASSISTANT_DOMAIN,
            translation_key="platform_setup_failed",
            translation_placeholders={"platform": entry.domain, "domain": DOMAIN},
        )


async def async_unload_entry(hass: __HAC_KEEP__, entry: ConfigEntry) -> None:
    """Unload a config entry."""
    await hass.data[DATA_COMPONENT].async_unload_entry(entry)
