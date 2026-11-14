"""Provides conditions for power."""

from universalassistant.components.sensor import DOMAIN as SENSOR_DOMAIN, SensorDeviceClass
from universalassistant.const import UnitOfPower
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers.automation import DomainSpec
from universalassistant.helpers.condition import (
    Condition,
    make_entity_numerical_condition_with_unit,
)
from universalassistant.util.unit_conversion import PowerConverter

POWER_DOMAIN_SPECS: dict[str, DomainSpec] = {
    SENSOR_DOMAIN: DomainSpec(device_class=SensorDeviceClass.POWER),
}


CONDITIONS: dict[str, type[Condition]] = {
    "is_value": make_entity_numerical_condition_with_unit(
        POWER_DOMAIN_SPECS, UnitOfPower.WATT, PowerConverter
    ),
}


async def async_get_conditions(hass: __HAC_KEEP__) -> dict[str, type[Condition]]:
    """Return the power conditions."""
    return CONDITIONS
