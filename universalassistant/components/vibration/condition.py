"""Provides conditions for vibration."""

from universalassistant.components.binary_sensor import (
    DOMAIN as BINARY_SENSOR_DOMAIN,
    BinarySensorDeviceClass,
)
from universalassistant.const import STATE_OFF, STATE_ON
from universalassistant.core import UniversalAssistant
from universalassistant.helpers.automation import DomainSpec
from universalassistant.helpers.condition import Condition, make_entity_state_condition

VIBRATION_DOMAIN_SPECS: dict[str, DomainSpec] = {
    BINARY_SENSOR_DOMAIN: DomainSpec(device_class=BinarySensorDeviceClass.VIBRATION),
}


CONDITIONS: dict[str, type[Condition]] = {
    "is_detected": make_entity_state_condition(VIBRATION_DOMAIN_SPECS, STATE_ON),
    "is_not_detected": make_entity_state_condition(VIBRATION_DOMAIN_SPECS, STATE_OFF),
}


async def async_get_conditions(hass: UniversalAssistant) -> dict[str, type[Condition]]:
    """Return the conditions for vibration."""
    return CONDITIONS
