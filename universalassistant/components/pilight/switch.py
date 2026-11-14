"""Support for switching devices via Pilight to on and off."""

import probatio

from universalassistant.components.switch import (
    PLATFORM_SCHEMA as SWITCH_PLATFORM_SCHEMA,
    SwitchEntity,
)
from universalassistant.const import CONF_SWITCHES
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import config_validation as cv
from universalassistant.helpers.entity_platform import AddEntitiesCallback
from universalassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .entity import SWITCHES_SCHEMA, PilightBaseDevice

PLATFORM_SCHEMA = SWITCH_PLATFORM_SCHEMA.extend(
    {probatio.Required(CONF_SWITCHES): probatio.Schema({cv.string: SWITCHES_SCHEMA})}
)


def setup_platform(
    hass: __HAC_KEEP__,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the Pilight platform."""
    switches = config[CONF_SWITCHES]
    devices = []

    for dev_name, dev_config in switches.items():
        devices.append(PilightSwitch(hass, dev_name, dev_config))

    add_entities(devices)


class PilightSwitch(PilightBaseDevice, SwitchEntity):
    """Representation of a Pilight switch."""
