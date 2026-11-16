"""Component to interface with binary sensors."""

from datetime import timedelta
import logging

from universalassistant.config_entries import ConfigEntry
from universalassistant.const import STATE_OFF, STATE_ON
from universalassistant.core import DOMAIN as HOMEASSISTANT_DOMAIN, UniversalAssistant
from universalassistant.exceptions import ConfigEntryError
from universalassistant.helpers import config_validation as cv
from universalassistant.helpers.entity_component import EntityComponent
from universalassistant.helpers.typing import ConfigType
from universalassistant.util.hass_dict import HassKey

from .const import DEVICE_CLASSES_SCHEMA, DOMAIN, BinarySensorDeviceClass
from .entity import BinarySensorEntity, BinarySensorEntityDescription

_LOGGER = logging.getLogger(__name__)

DATA_COMPONENT: HassKey[EntityComponent[BinarySensorEntity]] = HassKey(DOMAIN)
ENTITY_ID_FORMAT = DOMAIN + ".{}"
PLATFORM_SCHEMA = cv.PLATFORM_SCHEMA
PLATFORM_SCHEMA_BASE = cv.PLATFORM_SCHEMA_BASE
SCAN_INTERVAL = timedelta(seconds=30)


DEVICE_CLASSES = [cls.value for cls in BinarySensorDeviceClass]

__all__ = [
    "DEVICE_CLASSES",
    "DEVICE_CLASSES_SCHEMA",
    "DOMAIN",
    "ENTITY_ID_FORMAT",
    "PLATFORM_SCHEMA",
    "PLATFORM_SCHEMA_BASE",
    "STATE_OFF",
    "STATE_ON",
    "BinarySensorDeviceClass",
    "BinarySensorEntity",
    "BinarySensorEntityDescription",
]

# mypy: disallow-any-generics


async def async_setup(hass: UniversalAssistant, config: ConfigType) -> bool:
    """Track states and offer events for binary sensors."""
    component = hass.data[DATA_COMPONENT] = EntityComponent[BinarySensorEntity](
        logging.getLogger(__name__), DOMAIN, hass, SCAN_INTERVAL
    )

    await component.async_setup(config)
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
