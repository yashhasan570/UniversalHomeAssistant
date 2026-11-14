"""Provides functionality to interact with fans."""

from datetime import timedelta
import logging

from universalassistant.config_entries import ConfigEntry
from universalassistant.const import (
    SERVICE_TOGGLE,
    SERVICE_TURN_OFF,
    SERVICE_TURN_ON,
    STATE_OFF,
    STATE_ON,
)
from universalassistant.core import DOMAIN as HOMEASSISTANT_DOMAIN, __HAC_KEEP__
from universalassistant.exceptions import ConfigEntryError
from universalassistant.helpers import config_validation as cv
from universalassistant.helpers.entity_component import EntityComponent
from universalassistant.helpers.typing import ConfigType

from .const import (
    ATTR_DIRECTION,
    ATTR_OSCILLATING,
    ATTR_PERCENTAGE,
    ATTR_PERCENTAGE_STEP,
    ATTR_PRESET_MODE,
    ATTR_PRESET_MODES,
    DATA_COMPONENT,
    DIRECTION_FORWARD,
    DIRECTION_REVERSE,
    DOMAIN,
    SERVICE_DECREASE_SPEED,
    SERVICE_INCREASE_SPEED,
    SERVICE_OSCILLATE,
    SERVICE_SET_DIRECTION,
    SERVICE_SET_PERCENTAGE,
    SERVICE_SET_PRESET_MODE,
    FanEntityCapabilityAttribute,
    FanEntityFeature,
    FanEntityStateAttribute,
    FanService,
    FanServiceArgument,
)
from .entity import FanEntity, FanEntityDescription, NotValidPresetModeError
from .services import async_setup_services

_LOGGER = logging.getLogger(__name__)

ENTITY_ID_FORMAT = DOMAIN + ".{}"
PLATFORM_SCHEMA = cv.PLATFORM_SCHEMA
PLATFORM_SCHEMA_BASE = cv.PLATFORM_SCHEMA_BASE
SCAN_INTERVAL = timedelta(seconds=30)

__all__ = [
    "ATTR_DIRECTION",
    "ATTR_OSCILLATING",
    "ATTR_PERCENTAGE",
    "ATTR_PERCENTAGE_STEP",
    "ATTR_PRESET_MODE",
    "ATTR_PRESET_MODES",
    "DIRECTION_FORWARD",
    "DIRECTION_REVERSE",
    "DOMAIN",
    "ENTITY_ID_FORMAT",
    "PLATFORM_SCHEMA",
    "PLATFORM_SCHEMA_BASE",
    "SERVICE_DECREASE_SPEED",
    "SERVICE_INCREASE_SPEED",
    "SERVICE_OSCILLATE",
    "SERVICE_SET_DIRECTION",
    "SERVICE_SET_PERCENTAGE",
    "SERVICE_SET_PRESET_MODE",
    "SERVICE_TOGGLE",
    "SERVICE_TURN_OFF",
    "SERVICE_TURN_ON",
    "STATE_OFF",
    "STATE_ON",
    "FanEntity",
    "FanEntityCapabilityAttribute",
    "FanEntityDescription",
    "FanEntityFeature",
    "FanEntityStateAttribute",
    "FanService",
    "FanServiceArgument",
    "NotValidPresetModeError",
]

# mypy: disallow-any-generics


def is_on(hass: __HAC_KEEP__, entity_id: str) -> bool:
    """Return if the fans are on based on the statemachine."""
    entity = hass.states.get(entity_id)
    assert entity
    return entity.state == STATE_ON


async def async_setup(hass: __HAC_KEEP__, config: ConfigType) -> bool:
    """Expose fan control via statemachine and services."""
    component = hass.data[DATA_COMPONENT] = EntityComponent[FanEntity](
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
