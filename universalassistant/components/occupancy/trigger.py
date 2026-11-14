"""Provides triggers for occupancy."""

from universalassistant.components.binary_sensor import (
    DOMAIN as BINARY_SENSOR_DOMAIN,
    BinarySensorDeviceClass,
)
from universalassistant.const import STATE_OFF, STATE_ON
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers.automation import DomainSpec
from universalassistant.helpers.trigger import Trigger, make_entity_target_state_trigger

OCCUPANCY_DOMAIN_SPECS: dict[str, DomainSpec] = {
    BINARY_SENSOR_DOMAIN: DomainSpec(device_class=BinarySensorDeviceClass.OCCUPANCY),
}

TRIGGERS: dict[str, type[Trigger]] = {
    "detected": make_entity_target_state_trigger(OCCUPANCY_DOMAIN_SPECS, STATE_ON),
    "cleared": make_entity_target_state_trigger(OCCUPANCY_DOMAIN_SPECS, STATE_OFF),
}


async def async_get_triggers(hass: __HAC_KEEP__) -> dict[str, type[Trigger]]:
    """Return the triggers for occupancy."""
    return TRIGGERS
