"""Provides conditions for illuminance."""

from universalassistant.components.binary_sensor import (
    DOMAIN as BINARY_SENSOR_DOMAIN,
    BinarySensorDeviceClass,
)
from universalassistant.components.sensor import DOMAIN as SENSOR_DOMAIN, SensorDeviceClass
from universalassistant.const import LIGHT_LUX, STATE_OFF, STATE_ON
from universalassistant.core import UniversalAssistant
from universalassistant.helpers.automation import DomainSpec
from universalassistant.helpers.condition import (
    Condition,
    make_entity_numerical_condition,
    make_entity_state_condition,
)

ILLUMINANCE_DETECTED_DOMAIN_SPECS: dict[str, DomainSpec] = {
    BINARY_SENSOR_DOMAIN: DomainSpec(device_class=BinarySensorDeviceClass.LIGHT),
}
ILLUMINANCE_VALUE_DOMAIN_SPECS: dict[str, DomainSpec] = {
    SENSOR_DOMAIN: DomainSpec(device_class=SensorDeviceClass.ILLUMINANCE),
}

CONDITIONS: dict[str, type[Condition]] = {
    "is_detected": make_entity_state_condition(
        ILLUMINANCE_DETECTED_DOMAIN_SPECS, STATE_ON
    ),
    "is_not_detected": make_entity_state_condition(
        ILLUMINANCE_DETECTED_DOMAIN_SPECS, STATE_OFF
    ),
    "is_value": make_entity_numerical_condition(
        ILLUMINANCE_VALUE_DOMAIN_SPECS, LIGHT_LUX
    ),
}


async def async_get_conditions(hass: UniversalAssistant) -> dict[str, type[Condition]]:
    """Return the conditions for illuminance."""
    return CONDITIONS
