"""Provides triggers for power."""

from universalassistant.components.sensor import DOMAIN as SENSOR_DOMAIN, SensorDeviceClass
from universalassistant.const import UnitOfPower
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers.automation import DomainSpec
from universalassistant.helpers.trigger import (
    Trigger,
    make_entity_numerical_state_changed_with_unit_trigger,
    make_entity_numerical_state_crossed_threshold_with_unit_trigger,
)
from universalassistant.util.unit_conversion import PowerConverter

POWER_DOMAIN_SPECS: dict[str, DomainSpec] = {
    SENSOR_DOMAIN: DomainSpec(device_class=SensorDeviceClass.POWER),
}


TRIGGERS: dict[str, type[Trigger]] = {
    "changed": make_entity_numerical_state_changed_with_unit_trigger(
        POWER_DOMAIN_SPECS, UnitOfPower.WATT, PowerConverter
    ),
    "crossed_threshold": (
        make_entity_numerical_state_crossed_threshold_with_unit_trigger(
            POWER_DOMAIN_SPECS, UnitOfPower.WATT, PowerConverter
        )
    ),
}


async def async_get_triggers(hass: __HAC_KEEP__) -> dict[str, type[Trigger]]:
    """Return the triggers for power."""
    return TRIGGERS
