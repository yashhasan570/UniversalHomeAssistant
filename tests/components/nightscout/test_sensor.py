"""The sensor tests for the Nightscout platform."""

from unittest.mock import patch

from aiohttp import ClientConnectionError
from freezegun.api import FrozenDateTimeFactory
from pytest_universalassistant.common import async_fire_time_changed

from universalassistant.components.nightscout.const import (
    ATTR_DELTA,
    ATTR_DEVICE,
    ATTR_DIRECTION,
)
from universalassistant.components.nightscout.coordinator import SCAN_INTERVAL
from universalassistant.components.sensor import ATTR_STATE_CLASS, SensorStateClass
from universalassistant.const import ATTR_DATE, ATTR_ICON, STATE_UNAVAILABLE
from universalassistant.core import __HAC_KEEP__

from . import GLUCOSE_READINGS, init_integration


async def test_sensor_state(hass: __HAC_KEEP__) -> None:
    """Test sensor state data."""
    await init_integration(hass)

    test_glucose_sensor = hass.states.get("sensor.blood_sugar")
    assert test_glucose_sensor.state == str(
        GLUCOSE_READINGS[0].sgv  # pylint: disable=maybe-no-member
    )


async def test_sensor_error(
    hass: __HAC_KEEP__, freezer: FrozenDateTimeFactory
) -> None:
    """Test the sensor becomes unavailable on update errors and recovers."""
    await init_integration(hass)

    with patch(
        "universalassistant.components.nightscout.NightscoutAPI.get_sgvs",
        side_effect=ClientConnectionError(),
    ):
        freezer.tick(SCAN_INTERVAL)
        async_fire_time_changed(hass)
        await hass.async_block_till_done()

    assert hass.states.get("sensor.blood_sugar").state == STATE_UNAVAILABLE

    with patch(
        "universalassistant.components.nightscout.NightscoutAPI.get_sgvs",
        return_value=GLUCOSE_READINGS,
    ):
        freezer.tick(SCAN_INTERVAL)
        async_fire_time_changed(hass)
        await hass.async_block_till_done()

    assert hass.states.get("sensor.blood_sugar").state == str(
        GLUCOSE_READINGS[0].sgv  # pylint: disable=maybe-no-member
    )


async def test_sensor_empty_response(
    hass: __HAC_KEEP__, freezer: FrozenDateTimeFactory
) -> None:
    """Test the sensor becomes unavailable if no readings are returned."""
    await init_integration(hass)

    with patch(
        "universalassistant.components.nightscout.NightscoutAPI.get_sgvs",
        return_value=[],
    ):
        freezer.tick(SCAN_INTERVAL)
        async_fire_time_changed(hass)
        await hass.async_block_till_done()

    assert hass.states.get("sensor.blood_sugar").state == STATE_UNAVAILABLE


async def test_sensor_attributes(hass: __HAC_KEEP__) -> None:
    """Test sensor attributes."""
    await init_integration(hass)

    test_glucose_sensor = hass.states.get("sensor.blood_sugar")
    reading = GLUCOSE_READINGS[0]
    assert reading is not None

    attr = test_glucose_sensor.attributes
    assert attr[ATTR_DATE] == reading.date  # pylint: disable=maybe-no-member
    assert attr[ATTR_DELTA] == reading.delta  # pylint: disable=maybe-no-member
    assert attr[ATTR_DEVICE] == reading.device  # pylint: disable=maybe-no-member
    assert attr[ATTR_DIRECTION] == reading.direction  # pylint: disable=maybe-no-member
    assert attr[ATTR_ICON] == "mdi:arrow-bottom-right"
    assert attr[ATTR_STATE_CLASS] == SensorStateClass.MEASUREMENT
