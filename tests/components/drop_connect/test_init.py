"""Test DROP initialisation."""

from pytest_universalassistant.common import async_fire_mqtt_message
from pytest_universalassistant.typing import MqttMockHAClient

from universalassistant.config_entries import ConfigEntryState
from universalassistant.const import STATE_UNAVAILABLE, STATE_UNKNOWN
from universalassistant.core import __HAC_KEEP__

from .common import (
    TEST_DATA_HUB,
    TEST_DATA_HUB_RESET,
    TEST_DATA_HUB_TOPIC,
    config_entry_hub,
)


async def test_bad_json(hass: __HAC_KEEP__, mqtt_mock: MqttMockHAClient) -> None:
    """Test bad JSON."""
    entry = config_entry_hub()
    entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(entry.entry_id)

    current_flow_sensor_name = "sensor.hub_drop_1_c0ffee_water_flow_rate"
    assert hass.states.get(current_flow_sensor_name).state == STATE_UNKNOWN

    async_fire_mqtt_message(hass, TEST_DATA_HUB_TOPIC, "{BAD JSON}")
    await hass.async_block_till_done()
    assert hass.states.get(current_flow_sensor_name).state == STATE_UNKNOWN


async def test_unload(hass: __HAC_KEEP__, mqtt_mock: MqttMockHAClient) -> None:
    """Test entity unload."""
    # Load the hub device
    entry = config_entry_hub()
    entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(entry.entry_id)

    current_flow_sensor_name = "sensor.hub_drop_1_c0ffee_water_flow_rate"
    assert hass.states.get(current_flow_sensor_name).state == STATE_UNKNOWN

    async_fire_mqtt_message(hass, TEST_DATA_HUB_TOPIC, TEST_DATA_HUB_RESET)
    await hass.async_block_till_done()
    assert hass.states.get(current_flow_sensor_name).state == "0.0"

    async_fire_mqtt_message(hass, TEST_DATA_HUB_TOPIC, TEST_DATA_HUB)
    await hass.async_block_till_done()

    assert hass.states.get(current_flow_sensor_name).state == "21.84182599368"

    # Unload the device
    await hass.config_entries.async_unload(entry.entry_id)
    assert entry.state is ConfigEntryState.NOT_LOADED

    # Verify sensor is unavailable
    assert hass.states.get(current_flow_sensor_name).state == STATE_UNAVAILABLE


async def test_no_mqtt(hass: __HAC_KEEP__) -> None:
    """Test no MQTT."""
    entry = config_entry_hub()
    entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(entry.entry_id) is False
    assert entry.state is ConfigEntryState.SETUP_ERROR
    assert entry.reason == "MQTT integration is not available"

    protect_mode_select_name = "select.hub_drop_1_c0ffee_protect_mode"
    assert hass.states.get(protect_mode_select_name) is None
