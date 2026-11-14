"""Support for Geolocation."""

from datetime import timedelta
import logging

from universalassistant.config_entries import ConfigEntry
from universalassistant.const import ATTR_LATITUDE, ATTR_LONGITUDE
from universalassistant.core import DOMAIN as HOMEASSISTANT_DOMAIN, __HAC_KEEP__
from universalassistant.exceptions import ConfigEntryError
from universalassistant.helpers import config_validation as cv
from universalassistant.helpers.entity_component import EntityComponent
from universalassistant.helpers.typing import ConfigType
from universalassistant.util.hass_dict import HassKey

from .const import DOMAIN, GeolocationEntityStateAttribute
from .entity import GeolocationEvent

_LOGGER = logging.getLogger(__name__)

DATA_COMPONENT: HassKey[EntityComponent[GeolocationEvent]] = HassKey(DOMAIN)
ENTITY_ID_FORMAT = DOMAIN + ".{}"
PLATFORM_SCHEMA = cv.PLATFORM_SCHEMA
PLATFORM_SCHEMA_BASE = cv.PLATFORM_SCHEMA_BASE
SCAN_INTERVAL = timedelta(seconds=60)

ATTR_DISTANCE = "distance"
ATTR_SOURCE = "source"


__all__ = [
    "ATTR_DISTANCE",
    "ATTR_LATITUDE",
    "ATTR_LONGITUDE",
    "ATTR_SOURCE",
    "DOMAIN",
    "ENTITY_ID_FORMAT",
    "PLATFORM_SCHEMA",
    "PLATFORM_SCHEMA_BASE",
    "GeolocationEntityStateAttribute",
    "GeolocationEvent",
]

# mypy: disallow-any-generics


async def async_setup(hass: __HAC_KEEP__, config: ConfigType) -> bool:
    """Set up the Geolocation component."""
    component = hass.data[DATA_COMPONENT] = EntityComponent[GeolocationEvent](
        _LOGGER, DOMAIN, hass, SCAN_INTERVAL
    )
    await component.async_setup(config)
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
