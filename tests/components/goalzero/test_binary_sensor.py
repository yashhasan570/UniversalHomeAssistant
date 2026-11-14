"""Binary sensor tests for the Goalzero integration."""

from pytest_universalassistant.test_util.aiohttp import AiohttpClientMocker

from universalassistant.components.binary_sensor import BinarySensorDeviceClass
from universalassistant.components.goalzero.const import DEFAULT_NAME
from universalassistant.const import ATTR_DEVICE_CLASS, STATE_OFF, STATE_ON
from universalassistant.core import __HAC_KEEP__

from . import async_init_integration


async def test_binary_sensors(
    hass: __HAC_KEEP__, aioclient_mock: AiohttpClientMocker
) -> None:
    """Test we get sensor data."""
    await async_init_integration(hass, aioclient_mock)

    state = hass.states.get(f"binary_sensor.{DEFAULT_NAME}_backlight")
    assert state.state == STATE_ON
    assert state.attributes.get(ATTR_DEVICE_CLASS) is None
    state = hass.states.get(f"binary_sensor.{DEFAULT_NAME}_app_online")
    assert state.state == STATE_OFF
    assert (
        state.attributes.get(ATTR_DEVICE_CLASS) == BinarySensorDeviceClass.CONNECTIVITY
    )
    state = hass.states.get(f"binary_sensor.{DEFAULT_NAME}_charging")
    assert state.state == STATE_OFF
    assert (
        state.attributes.get(ATTR_DEVICE_CLASS)
        == BinarySensorDeviceClass.BATTERY_CHARGING
    )
    state = hass.states.get(f"binary_sensor.{DEFAULT_NAME}_input_detected")
    assert state.state == STATE_OFF
    assert state.attributes.get(ATTR_DEVICE_CLASS) == BinarySensorDeviceClass.POWER
