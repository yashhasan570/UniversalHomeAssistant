"""Provides conditions for humidity."""

from typing import override

from universalassistant.components.climate import (
    DOMAIN as CLIMATE_DOMAIN,
    ClimateEntityStateAttribute,
)
from universalassistant.components.humidifier import (
    DOMAIN as HUMIDIFIER_DOMAIN,
    HumidifierEntityStateAttribute,
)
from universalassistant.components.sensor import DOMAIN as SENSOR_DOMAIN, SensorDeviceClass
from universalassistant.components.weather import (
    DOMAIN as WEATHER_DOMAIN,
    WeatherEntityStateAttribute,
)
from universalassistant.const import PERCENTAGE
from universalassistant.core import __HAC_KEEP__, State
from universalassistant.helpers.automation import DomainSpec
from universalassistant.helpers.condition import Condition, EntityNumericalConditionBase

HUMIDITY_DOMAIN_SPECS: dict[str, DomainSpec] = {
    CLIMATE_DOMAIN: DomainSpec(
        value_source=ClimateEntityStateAttribute.CURRENT_HUMIDITY,
    ),
    HUMIDIFIER_DOMAIN: DomainSpec(
        value_source=HumidifierEntityStateAttribute.CURRENT_HUMIDITY,
    ),
    SENSOR_DOMAIN: DomainSpec(device_class=SensorDeviceClass.HUMIDITY),
    WEATHER_DOMAIN: DomainSpec(
        value_source=WeatherEntityStateAttribute.HUMIDITY,
    ),
}


class HumidityCondition(EntityNumericalConditionBase):
    """Condition for humidity value across multiple domains."""

    _domain_specs = HUMIDITY_DOMAIN_SPECS
    _valid_unit = PERCENTAGE

    @override
    def _should_include(self, state: State) -> bool:
        """Skip attribute-source entities that lack the humidity attribute.

        Mirrors the humidity trigger: for climate / humidifier / weather
        (attribute-based), the entity is filtered when the source attribute
        is absent; sensor entities (state-value-based) fall through to the
        base impl.
        """
        if not super()._should_include(state):
            return False
        domain_spec = self._domain_specs[state.domain]
        if domain_spec.value_source is None:
            return True
        return state.attributes.get(domain_spec.value_source) is not None


CONDITIONS: dict[str, type[Condition]] = {
    "is_value": HumidityCondition,
}


async def async_get_conditions(hass: __HAC_KEEP__) -> dict[str, type[Condition]]:
    """Return the conditions for humidity."""
    return CONDITIONS
