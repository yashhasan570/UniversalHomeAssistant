"""Test humidity conditions."""

from typing import Any

import pytest
from pytest_universalassistant.components.common import (
    ConditionStateDescription,
    TargetSupport,
    assert_condition_behavior_all,
    assert_condition_behavior_any,
    assert_condition_options_supported,
    assert_conditions_target_support,
    parametrize_numerical_attribute_condition_above_below_all,
    parametrize_numerical_attribute_condition_above_below_any,
    parametrize_numerical_condition_above_below_all,
    parametrize_numerical_condition_above_below_any,
    parametrize_target_entities,
    target_entities,
)

from universalassistant.components.climate import (
    ATTR_CURRENT_HUMIDITY as CLIMATE_ATTR_CURRENT_HUMIDITY,
    HVACMode,
)
from universalassistant.components.humidifier import (
    ATTR_CURRENT_HUMIDITY as HUMIDIFIER_ATTR_CURRENT_HUMIDITY,
)
from universalassistant.components.humidity.condition import CONDITIONS
from universalassistant.components.weather import WeatherEntityStateAttribute
from universalassistant.const import ATTR_UNIT_OF_MEASUREMENT, STATE_ON
from universalassistant.core import UniversalAssistant

_HUMIDITY_UNIT_ATTRS = {ATTR_UNIT_OF_MEASUREMENT: "%"}


@pytest.fixture
async def target_sensors(hass: UniversalAssistant) -> dict[str, list[str]]:
    """Create multiple sensor entities associated with different targets."""
    return await target_entities(hass, "sensor")


@pytest.fixture
async def target_climates(hass: UniversalAssistant) -> dict[str, list[str]]:
    """Create multiple climate entities associated with different targets."""
    return await target_entities(hass, "climate")


@pytest.fixture
async def target_humidifiers(hass: UniversalAssistant) -> dict[str, list[str]]:
    """Create multiple humidifier entities associated with different targets."""
    return await target_entities(hass, "humidifier")


@pytest.fixture
async def target_weathers(hass: UniversalAssistant) -> dict[str, list[str]]:
    """Create multiple weather entities associated with different targets."""
    return await target_entities(hass, "weather")


_PLAIN_THRESHOLD = {"threshold": {"type": "above", "value": {"number": 50}}}


_CONDITION_TARGET_SUPPORT: dict[str, TargetSupport] = {
    "is_value": TargetSupport.STANDARD,
}


@pytest.mark.parametrize(
    ("condition_key", "base_options", "supports_behavior", "supports_duration"),
    [
        ("humidity.is_value", _PLAIN_THRESHOLD, True, True),
    ],
)
async def test_humidity_condition_options_validation(
    hass: UniversalAssistant,
    condition_key: str,
    base_options: dict[str, Any] | None,
    supports_behavior: bool,
    supports_duration: bool,
) -> None:
    """Test that humidity conditions support the expected options."""
    await assert_condition_options_supported(
        hass,
        condition_key,
        base_options,
        supports_behavior=supports_behavior,
        supports_duration=supports_duration,
    )


def test_condition_target_support() -> None:
    """Certify the condition registry matches its declared target support."""
    assert_conditions_target_support(CONDITIONS, _CONDITION_TARGET_SUPPORT)


@pytest.mark.parametrize(
    ("condition_target_config", "entity_id", "entities_in_target"),
    parametrize_target_entities("sensor"),
)
@pytest.mark.parametrize(
    ("condition", "condition_options", "states"),
    parametrize_numerical_condition_above_below_any(
        "humidity.is_value",
        device_class="humidity",
        unit_attributes=_HUMIDITY_UNIT_ATTRS,
    ),
)
async def test_humidity_sensor_condition_behavior_any(
    hass: UniversalAssistant,
    target_sensors: dict[str, list[str]],
    condition_target_config: dict,
    entity_id: str,
    entities_in_target: int,
    condition: str,
    condition_options: dict[str, Any],
    states: list[ConditionStateDescription],
) -> None:
    """Test the humidity sensor condition with 'any' behavior."""
    await assert_condition_behavior_any(
        hass,
        target_entities=target_sensors,
        condition_target_config=condition_target_config,
        entity_id=entity_id,
        entities_in_target=entities_in_target,
        condition=condition,
        condition_options=condition_options,
        states=states,
    )


@pytest.mark.parametrize(
    ("condition_target_config", "entity_id", "entities_in_target"),
    parametrize_target_entities("sensor"),
)
@pytest.mark.parametrize(
    ("condition", "condition_options", "states"),
    parametrize_numerical_condition_above_below_all(
        "humidity.is_value",
        device_class="humidity",
        unit_attributes=_HUMIDITY_UNIT_ATTRS,
    ),
)
async def test_humidity_sensor_condition_behavior_all(
    hass: UniversalAssistant,
    target_sensors: dict[str, list[str]],
    condition_target_config: dict,
    entity_id: str,
    entities_in_target: int,
    condition: str,
    condition_options: dict[str, Any],
    states: list[ConditionStateDescription],
) -> None:
    """Test the humidity sensor condition with 'all' behavior."""
    await assert_condition_behavior_all(
        hass,
        target_entities=target_sensors,
        condition_target_config=condition_target_config,
        entity_id=entity_id,
        entities_in_target=entities_in_target,
        condition=condition,
        condition_options=condition_options,
        states=states,
    )


@pytest.mark.parametrize(
    ("condition_target_config", "entity_id", "entities_in_target"),
    parametrize_target_entities("climate"),
)
@pytest.mark.parametrize(
    ("condition", "condition_options", "states"),
    parametrize_numerical_attribute_condition_above_below_any(
        "humidity.is_value",
        HVACMode.AUTO,
        CLIMATE_ATTR_CURRENT_HUMIDITY,
        attribute_required=True,
    ),
)
async def test_humidity_climate_condition_behavior_any(
    hass: UniversalAssistant,
    target_climates: dict[str, list[str]],
    condition_target_config: dict,
    entity_id: str,
    entities_in_target: int,
    condition: str,
    condition_options: dict[str, Any],
    states: list[ConditionStateDescription],
) -> None:
    """Test the humidity climate condition with 'any' behavior."""
    await assert_condition_behavior_any(
        hass,
        target_entities=target_climates,
        condition_target_config=condition_target_config,
        entity_id=entity_id,
        entities_in_target=entities_in_target,
        condition=condition,
        condition_options=condition_options,
        states=states,
    )


@pytest.mark.parametrize(
    ("condition_target_config", "entity_id", "entities_in_target"),
    parametrize_target_entities("climate"),
)
@pytest.mark.parametrize(
    ("condition", "condition_options", "states"),
    parametrize_numerical_attribute_condition_above_below_all(
        "humidity.is_value",
        HVACMode.AUTO,
        CLIMATE_ATTR_CURRENT_HUMIDITY,
        attribute_required=True,
    ),
)
async def test_humidity_climate_condition_behavior_all(
    hass: UniversalAssistant,
    target_climates: dict[str, list[str]],
    condition_target_config: dict,
    entity_id: str,
    entities_in_target: int,
    condition: str,
    condition_options: dict[str, Any],
    states: list[ConditionStateDescription],
) -> None:
    """Test the humidity climate condition with 'all' behavior."""
    await assert_condition_behavior_all(
        hass,
        target_entities=target_climates,
        condition_target_config=condition_target_config,
        entity_id=entity_id,
        entities_in_target=entities_in_target,
        condition=condition,
        condition_options=condition_options,
        states=states,
    )


@pytest.mark.parametrize(
    ("condition_target_config", "entity_id", "entities_in_target"),
    parametrize_target_entities("humidifier"),
)
@pytest.mark.parametrize(
    ("condition", "condition_options", "states"),
    parametrize_numerical_attribute_condition_above_below_any(
        "humidity.is_value",
        STATE_ON,
        HUMIDIFIER_ATTR_CURRENT_HUMIDITY,
        attribute_required=True,
    ),
)
async def test_humidity_humidifier_condition_behavior_any(
    hass: UniversalAssistant,
    target_humidifiers: dict[str, list[str]],
    condition_target_config: dict,
    entity_id: str,
    entities_in_target: int,
    condition: str,
    condition_options: dict[str, Any],
    states: list[ConditionStateDescription],
) -> None:
    """Test the humidity humidifier condition with 'any' behavior."""
    await assert_condition_behavior_any(
        hass,
        target_entities=target_humidifiers,
        condition_target_config=condition_target_config,
        entity_id=entity_id,
        entities_in_target=entities_in_target,
        condition=condition,
        condition_options=condition_options,
        states=states,
    )


@pytest.mark.parametrize(
    ("condition_target_config", "entity_id", "entities_in_target"),
    parametrize_target_entities("humidifier"),
)
@pytest.mark.parametrize(
    ("condition", "condition_options", "states"),
    parametrize_numerical_attribute_condition_above_below_all(
        "humidity.is_value",
        STATE_ON,
        HUMIDIFIER_ATTR_CURRENT_HUMIDITY,
        attribute_required=True,
    ),
)
async def test_humidity_humidifier_condition_behavior_all(
    hass: UniversalAssistant,
    target_humidifiers: dict[str, list[str]],
    condition_target_config: dict,
    entity_id: str,
    entities_in_target: int,
    condition: str,
    condition_options: dict[str, Any],
    states: list[ConditionStateDescription],
) -> None:
    """Test the humidity humidifier condition with 'all' behavior."""
    await assert_condition_behavior_all(
        hass,
        target_entities=target_humidifiers,
        condition_target_config=condition_target_config,
        entity_id=entity_id,
        entities_in_target=entities_in_target,
        condition=condition,
        condition_options=condition_options,
        states=states,
    )


@pytest.mark.parametrize(
    ("condition_target_config", "entity_id", "entities_in_target"),
    parametrize_target_entities("weather"),
)
@pytest.mark.parametrize(
    ("condition", "condition_options", "states"),
    parametrize_numerical_attribute_condition_above_below_any(
        "humidity.is_value",
        "sunny",
        WeatherEntityStateAttribute.HUMIDITY,
        attribute_required=True,
    ),
)
async def test_humidity_weather_condition_behavior_any(
    hass: UniversalAssistant,
    target_weathers: dict[str, list[str]],
    condition_target_config: dict,
    entity_id: str,
    entities_in_target: int,
    condition: str,
    condition_options: dict[str, Any],
    states: list[ConditionStateDescription],
) -> None:
    """Test the humidity weather condition with 'any' behavior."""
    await assert_condition_behavior_any(
        hass,
        target_entities=target_weathers,
        condition_target_config=condition_target_config,
        entity_id=entity_id,
        entities_in_target=entities_in_target,
        condition=condition,
        condition_options=condition_options,
        states=states,
    )


@pytest.mark.parametrize(
    ("condition_target_config", "entity_id", "entities_in_target"),
    parametrize_target_entities("weather"),
)
@pytest.mark.parametrize(
    ("condition", "condition_options", "states"),
    parametrize_numerical_attribute_condition_above_below_all(
        "humidity.is_value",
        "sunny",
        WeatherEntityStateAttribute.HUMIDITY,
        attribute_required=True,
    ),
)
async def test_humidity_weather_condition_behavior_all(
    hass: UniversalAssistant,
    target_weathers: dict[str, list[str]],
    condition_target_config: dict,
    entity_id: str,
    entities_in_target: int,
    condition: str,
    condition_options: dict[str, Any],
    states: list[ConditionStateDescription],
) -> None:
    """Test the humidity weather condition with 'all' behavior."""
    await assert_condition_behavior_all(
        hass,
        target_entities=target_weathers,
        condition_target_config=condition_target_config,
        entity_id=entity_id,
        entities_in_target=entities_in_target,
        condition=condition,
        condition_options=condition_options,
        states=states,
    )
