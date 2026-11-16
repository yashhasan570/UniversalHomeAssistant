"""Support for vacuum cleaner robots (botvacs)."""

from datetime import timedelta
import logging

from universalassistant.config_entries import ConfigEntry
from universalassistant.const import (
    ATTR_COMMAND,
    SERVICE_TOGGLE,
    SERVICE_TURN_OFF,
    SERVICE_TURN_ON,
    STATE_ON,
)
from universalassistant.core import DOMAIN as HOMEASSISTANT_DOMAIN, UniversalAssistant
from universalassistant.exceptions import ConfigEntryError
from universalassistant.helpers import config_validation as cv
from universalassistant.helpers.entity_component import EntityComponent
from universalassistant.helpers.typing import ConfigType

from .const import (
    ATTR_FAN_SPEED,
    ATTR_PARAMS,
    DATA_COMPONENT,
    DOMAIN,
    SERVICE_CLEAN_AREA,
    SERVICE_CLEAN_SPOT,
    SERVICE_LOCATE,
    SERVICE_PAUSE,
    SERVICE_RETURN_TO_BASE,
    SERVICE_SEND_COMMAND,
    SERVICE_SET_FAN_SPEED,
    SERVICE_START,
    SERVICE_STOP,
    VacuumActivity,
    VacuumEntityCapabilityAttribute,
    VacuumEntityFeature,
    VacuumEntityStateAttribute,
    VacuumService,
    VacuumServiceArgument,
)
from .entity import Segment, StateVacuumEntity, StateVacuumEntityDescription
from .services import async_setup_services
from .websocket import async_register_websocket_handlers

_LOGGER = logging.getLogger(__name__)

ENTITY_ID_FORMAT = DOMAIN + ".{}"
PLATFORM_SCHEMA = cv.PLATFORM_SCHEMA
PLATFORM_SCHEMA_BASE = cv.PLATFORM_SCHEMA_BASE
SCAN_INTERVAL = timedelta(seconds=20)

ATTR_CLEANED_AREA = "cleaned_area"
ATTR_FAN_SPEED_LIST = "fan_speed_list"
ATTR_STATUS = "status"

DEFAULT_NAME = "Vacuum cleaner robot"


__all__ = [
    "ATTR_CLEANED_AREA",
    "ATTR_COMMAND",
    "ATTR_FAN_SPEED",
    "ATTR_FAN_SPEED_LIST",
    "ATTR_PARAMS",
    "ATTR_STATUS",
    "DOMAIN",
    "ENTITY_ID_FORMAT",
    "PLATFORM_SCHEMA",
    "PLATFORM_SCHEMA_BASE",
    "SERVICE_CLEAN_AREA",
    "SERVICE_CLEAN_SPOT",
    "SERVICE_LOCATE",
    "SERVICE_PAUSE",
    "SERVICE_RETURN_TO_BASE",
    "SERVICE_SEND_COMMAND",
    "SERVICE_SET_FAN_SPEED",
    "SERVICE_START",
    "SERVICE_STOP",
    "SERVICE_TOGGLE",
    "SERVICE_TURN_OFF",
    "SERVICE_TURN_ON",
    "Segment",
    "StateVacuumEntity",
    "StateVacuumEntityDescription",
    "VacuumActivity",
    "VacuumEntityCapabilityAttribute",
    "VacuumEntityFeature",
    "VacuumEntityStateAttribute",
    "VacuumService",
    "VacuumServiceArgument",
]

# mypy: disallow-any-generics


def is_on(hass: UniversalAssistant, entity_id: str) -> bool:
    """Return if the vacuum is on based on the statemachine."""
    return hass.states.is_state(entity_id, STATE_ON)


async def async_setup(hass: UniversalAssistant, config: ConfigType) -> bool:
    """Set up the vacuum component."""
    component = hass.data[DATA_COMPONENT] = EntityComponent[StateVacuumEntity](
        _LOGGER, DOMAIN, hass, SCAN_INTERVAL
    )

    await component.async_setup(config)

    async_register_websocket_handlers(hass)

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
