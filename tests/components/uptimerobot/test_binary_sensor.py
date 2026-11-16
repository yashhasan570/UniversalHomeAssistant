"""Test UptimeRobot binary_sensor."""

from unittest.mock import patch

from pytest_universalassistant.common import async_fire_time_changed
from pyuptimerobot import UptimeRobotAuthenticationException

from universalassistant.components.binary_sensor import BinarySensorDeviceClass
from universalassistant.components.uptimerobot.const import (
    ATTRIBUTION,
    COORDINATOR_UPDATE_INTERVAL,
)
from universalassistant.const import STATE_ON, STATE_UNAVAILABLE
from universalassistant.core import UniversalAssistant
from universalassistant.util import dt as dt_util

from .common import (
    MOCK_UPTIMEROBOT_MONITOR,
    MOCK_UPTIMEROBOT_MONITOR_2,
    UPTIMEROBOT_BINARY_SENSOR_TEST_ENTITY,
    mock_uptimerobot_api_response,
    setup_uptimerobot_integration,
)


async def test_presentation(hass: UniversalAssistant) -> None:
    """Test the presenstation of UptimeRobot binary_sensors."""
    await setup_uptimerobot_integration(hass)

    assert (entity := hass.states.get(UPTIMEROBOT_BINARY_SENSOR_TEST_ENTITY))
    assert entity.state == STATE_ON
    assert entity.attributes["device_class"] == BinarySensorDeviceClass.CONNECTIVITY
    assert entity.attributes["attribution"] == ATTRIBUTION
    assert entity.attributes["target"] == MOCK_UPTIMEROBOT_MONITOR["url"]


async def test_unavailable_on_update_failure(hass: UniversalAssistant) -> None:
    """Test entity unavailable on update failure."""
    await setup_uptimerobot_integration(hass)

    assert (entity := hass.states.get(UPTIMEROBOT_BINARY_SENSOR_TEST_ENTITY))
    assert entity.state == STATE_ON

    with patch(
        "pyuptimerobot.UptimeRobot.async_get_monitors",
        side_effect=UptimeRobotAuthenticationException,
    ):
        async_fire_time_changed(hass, dt_util.utcnow() + COORDINATOR_UPDATE_INTERVAL)
        await hass.async_block_till_done()

    assert (entity := hass.states.get(UPTIMEROBOT_BINARY_SENSOR_TEST_ENTITY))
    assert entity.state == STATE_UNAVAILABLE


async def test_binary_sensor_dynamic(hass: UniversalAssistant) -> None:
    """Test binary_sensor dynamically added."""
    await setup_uptimerobot_integration(hass)

    assert (entity := hass.states.get(UPTIMEROBOT_BINARY_SENSOR_TEST_ENTITY))
    assert entity.state == STATE_ON

    entity_id_2 = "binary_sensor.test_monitor_2"

    with patch(
        "pyuptimerobot.UptimeRobot.async_get_monitors",
        return_value=mock_uptimerobot_api_response(
            data=[
                MOCK_UPTIMEROBOT_MONITOR,
                MOCK_UPTIMEROBOT_MONITOR_2,
            ]
        ),
    ):
        async_fire_time_changed(hass, dt_util.utcnow() + COORDINATOR_UPDATE_INTERVAL)
        await hass.async_block_till_done()

        assert (entity := hass.states.get(UPTIMEROBOT_BINARY_SENSOR_TEST_ENTITY))
        assert entity.state == STATE_ON

        assert (entity := hass.states.get(entity_id_2))
        assert entity.state == STATE_ON
