"""Test Wallbox Switch component."""

from pytest_universalassistant.common import MockConfigEntry

from universalassistant.const import CONF_UNIT_OF_MEASUREMENT, UnitOfPower
from universalassistant.core import UniversalAssistant

from .conftest import setup_integration
from .const import (
    MOCK_SENSOR_CHARGING_POWER_ID,
    MOCK_SENSOR_CHARGING_SPEED_ID,
    MOCK_SENSOR_MAX_AVAILABLE_POWER,
)


async def test_wallbox_sensor_class(
    hass: UniversalAssistant, entry: MockConfigEntry, mock_wallbox
) -> None:
    """Test wallbox sensor class."""

    await setup_integration(hass, entry)

    state = hass.states.get(MOCK_SENSOR_CHARGING_POWER_ID)
    assert state.attributes[CONF_UNIT_OF_MEASUREMENT] == UnitOfPower.KILO_WATT
    assert state.name == "Wallbox WallboxName Charging power"

    state = hass.states.get(MOCK_SENSOR_CHARGING_SPEED_ID)
    assert state.name == "Wallbox WallboxName Charging speed"

    # Test round with precision '0' works
    state = hass.states.get(MOCK_SENSOR_MAX_AVAILABLE_POWER)
    assert state.state == "25.0"
