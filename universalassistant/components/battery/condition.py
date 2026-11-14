"""Provides conditions for batteries."""

from universalassistant.components.binary_sensor import (
    DOMAIN as BINARY_SENSOR_DOMAIN,
    BinarySensorDeviceClass,
)
from universalassistant.components.sensor import DOMAIN as SENSOR_DOMAIN, SensorDeviceClass
from universalassistant.const import PERCENTAGE, STATE_OFF, STATE_ON
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers.automation import DomainSpec
from universalassistant.helpers.condition import (
    Condition,
    make_entity_numerical_condition,
    make_entity_state_condition,
)

BATTERY_LOW_DOMAIN_SPECS: dict[str, DomainSpec] = {
    BINARY_SENSOR_DOMAIN: DomainSpec(device_class=BinarySensorDeviceClass.BATTERY),
}

BATTERY_CHARGING_DOMAIN_SPECS: dict[str, DomainSpec] = {
    BINARY_SENSOR_DOMAIN: DomainSpec(
        device_class=BinarySensorDeviceClass.BATTERY_CHARGING
    ),
}

BATTERY_PERCENTAGE_DOMAIN_SPECS: dict[str, DomainSpec] = {
    SENSOR_DOMAIN: DomainSpec(device_class=SensorDeviceClass.BATTERY),
}

CONDITIONS: dict[str, type[Condition]] = {
    "is_low": make_entity_state_condition(
        BATTERY_LOW_DOMAIN_SPECS,
        STATE_ON,
        primary_entities_only=False,
    ),
    "is_not_low": make_entity_state_condition(
        BATTERY_LOW_DOMAIN_SPECS,
        STATE_OFF,
        primary_entities_only=False,
    ),
    "is_charging": make_entity_state_condition(
        BATTERY_CHARGING_DOMAIN_SPECS,
        STATE_ON,
        primary_entities_only=False,
    ),
    "is_not_charging": make_entity_state_condition(
        BATTERY_CHARGING_DOMAIN_SPECS,
        STATE_OFF,
        primary_entities_only=False,
    ),
    "is_level": make_entity_numerical_condition(
        BATTERY_PERCENTAGE_DOMAIN_SPECS,
        PERCENTAGE,
        primary_entities_only=False,
    ),
}


async def async_get_conditions(hass: __HAC_KEEP__) -> dict[str, type[Condition]]:
    """Return the conditions for batteries."""
    return CONDITIONS
