"""Test DROP select entities."""

from pytest_universalassistant.common import async_fire_mqtt_message
from pytest_universalassistant.typing import MqttMockHAClient

from universalassistant.components.select import (
    ATTR_OPTIONS,
    DOMAIN as SELECT_DOMAIN,
    SelectService,
    SelectServiceArgument,
)
from universalassistant.const import CommonServiceArgument
from universalassistant.core import UniversalAssistant

from .common import (
    TEST_DATA_HUB,
    TEST_DATA_HUB_RESET,
    TEST_DATA_HUB_TOPIC,
    config_entry_hub,
)


async def test_selects_hub(hass: UniversalAssistant, mqtt_mock: MqttMockHAClient) -> None:
    """Test DROP binary sensors for hubs."""
    entry = config_entry_hub()
    entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(entry.entry_id)

    protect_mode_select_name = "select.hub_drop_1_c0ffee_protect_mode"
    protect_mode_select = hass.states.get(protect_mode_select_name)
    assert protect_mode_select
    assert protect_mode_select.attributes.get(ATTR_OPTIONS) == [
        "away",
        "home",
        "schedule",
    ]

    async_fire_mqtt_message(hass, TEST_DATA_HUB_TOPIC, TEST_DATA_HUB_RESET)
    await hass.async_block_till_done()
    protect_mode_select = hass.states.get(protect_mode_select_name)
    assert protect_mode_select
    assert protect_mode_select.attributes.get(ATTR_OPTIONS) == [
        "away",
        "home",
        "schedule",
    ]

    async_fire_mqtt_message(hass, TEST_DATA_HUB_TOPIC, TEST_DATA_HUB)
    await hass.async_block_till_done()

    protect_mode_select = hass.states.get(protect_mode_select_name)
    assert protect_mode_select
    assert protect_mode_select.state == "home"

    mqtt_mock.async_publish.reset_mock()
    await hass.services.async_call(
        SELECT_DOMAIN,
        SelectService.SELECT_OPTION,
        {
            SelectServiceArgument.OPTION: "away",
            CommonServiceArgument.ENTITY_ID: protect_mode_select_name,
        },
        blocking=True,
    )
    await hass.async_block_till_done()
    assert len(mqtt_mock.async_publish.mock_calls) == 1

    # Simulate response of the device
    async_fire_mqtt_message(hass, TEST_DATA_HUB_TOPIC, TEST_DATA_HUB_RESET)
    await hass.async_block_till_done()

    protect_mode_select = hass.states.get(protect_mode_select_name)
    assert protect_mode_select
    assert protect_mode_select.state == "away"
