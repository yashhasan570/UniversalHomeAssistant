"""Component to interface with locks that can be controlled remotely."""

from datetime import timedelta
import logging

from universalassistant.config_entries import ConfigEntry
from universalassistant.const import (
    ATTR_CODE,
    ATTR_CODE_FORMAT,
    SERVICE_LOCK,
    SERVICE_OPEN,
    SERVICE_UNLOCK,
)
from universalassistant.core import DOMAIN as HOMEASSISTANT_DOMAIN, UniversalAssistant
from universalassistant.exceptions import ConfigEntryError
from universalassistant.helpers import config_validation as cv
from universalassistant.helpers.entity_component import EntityComponent
from universalassistant.helpers.typing import ConfigType

from .const import (
    ATTR_CHANGED_BY,
    CONF_DEFAULT_CODE,
    DATA_COMPONENT,
    DOMAIN,
    LockEntityFeature,
    LockEntityStateAttribute,
    LockService,
    LockServiceArgument,
    LockState,
)
from .entity import LockEntity, LockEntityDescription
from .services import async_setup_services

_LOGGER = logging.getLogger(__name__)

ENTITY_ID_FORMAT = DOMAIN + ".{}"
PLATFORM_SCHEMA = cv.PLATFORM_SCHEMA
PLATFORM_SCHEMA_BASE = cv.PLATFORM_SCHEMA_BASE
SCAN_INTERVAL = timedelta(seconds=30)

MIN_TIME_BETWEEN_SCANS = timedelta(seconds=10)


__all__ = [
    "ATTR_CHANGED_BY",
    "ATTR_CODE",
    "ATTR_CODE_FORMAT",
    "CONF_DEFAULT_CODE",
    "DOMAIN",
    "ENTITY_ID_FORMAT",
    "PLATFORM_SCHEMA",
    "PLATFORM_SCHEMA_BASE",
    "SERVICE_LOCK",
    "SERVICE_OPEN",
    "SERVICE_UNLOCK",
    "LockEntity",
    "LockEntityDescription",
    "LockEntityFeature",
    "LockEntityStateAttribute",
    "LockService",
    "LockServiceArgument",
    "LockState",
]

# mypy: disallow-any-generics


async def async_setup(hass: UniversalAssistant, config: ConfigType) -> bool:
    """Track states and offer events for locks."""
    component = hass.data[DATA_COMPONENT] = EntityComponent[LockEntity](
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
