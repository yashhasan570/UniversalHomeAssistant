"""Constants for the Homeassistant integration."""

from enum import StrEnum
from typing import TYPE_CHECKING, Final

from universalassistant import core as ha
from universalassistant.util.hass_dict import HassKey

if TYPE_CHECKING:
    from .exposed_entities import ExposedEntities

DOMAIN = ha.DOMAIN

DATA_EXPOSED_ENTITIES: HassKey[ExposedEntities] = HassKey(f"{DOMAIN}.exposed_entities")
DATA_STOP_HANDLER = f"{DOMAIN}.stop_handler"


class UniversalAssistantService(StrEnum):
    """Store keys for Universal Home Assistant services."""

    CHECK_CONFIG = "check_config"
    RELOAD_ALL = "reload_all"
    RELOAD_CONFIG_ENTRY = "reload_config_entry"
    RELOAD_CORE_CONFIG = "reload_core_config"
    RELOAD_CUSTOM_TEMPLATES = "reload_custom_templates"
    RESTART = "restart"
    SAVE_PERSISTENT_STATES = "save_persistent_states"
    SET_LOCATION = "set_location"
    STOP = "stop"
    TOGGLE = "toggle"
    TURN_OFF = "turn_off"
    TURN_ON = "turn_on"
    UPDATE_ENTITY = "update_entity"


class UniversalAssistantServiceArgument(StrEnum):
    """Store keys for Universal Home Assistant service arguments."""

    ELEVATION = "elevation"
    ENTRY_ID = "entry_id"
    LATITUDE = "latitude"
    LONGITUDE = "longitude"
    SAFE_MODE = "safe_mode"


# To be deprecated at a later stage, replaced by UniversalAssistantService
SERVICE_HOMEASSISTANT_STOP: Final = UniversalAssistantService.STOP.value
SERVICE_HOMEASSISTANT_RESTART: Final = UniversalAssistantService.RESTART.value
