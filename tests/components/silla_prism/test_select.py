"""Test the Silla Prism selects."""

import pytest
from pytest_universalassistant.common import (
    MockConfigEntry,
    async_fire_mqtt_message,
    snapshot_platform,
)
from pytest_universalassistant.typing import MqttMockHAClient
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.select import (
    DOMAIN as SELECT_DOMAIN,
    SelectService,
    SelectServiceArgument,
)
from universalassistant.const import STATE_UNKNOWN, Platform, TargetKey
from universalassistant.core import UniversalAssistant
from universalassistant.helpers import entity_registry as er

from . import fire_burst, setup_integration

CHARGING_MODE_ENTITY_ID = "select.silla_prism_charging_mode"
MODE_TOPIC = "prism/1/mode"
SET_MODE_TOPIC = "prism/1/command/set_mode"


async def test_selects(
    hass: UniversalAssistant,
    mqtt_mock: MqttMockHAClient,
    mock_config_entry: MockConfigEntry,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test the selects."""
    await setup_integration(hass, mock_config_entry, [Platform.SELECT])
    await fire_burst(hass)

    await snapshot_platform(hass, entity_registry, snapshot, mock_config_entry.entry_id)


@pytest.mark.parametrize(
    ("option", "payload"),
    [("solar", "1"), ("normal", "2"), ("pause", "3")],
)
async def test_select_option(
    hass: UniversalAssistant,
    mqtt_mock: MqttMockHAClient,
    mock_config_entry: MockConfigEntry,
    option: str,
    payload: str,
) -> None:
    """Test that selecting a mode publishes the matching command."""
    await setup_integration(hass, mock_config_entry)
    await fire_burst(hass)

    await hass.services.async_call(
        SELECT_DOMAIN,
        SelectService.SELECT_OPTION,
        {
            TargetKey.ENTITY_ID: CHARGING_MODE_ENTITY_ID,
            SelectServiceArgument.OPTION: option,
        },
        blocking=True,
    )

    mqtt_mock.async_publish.assert_called_once_with(
        SET_MODE_TOPIC, payload, 0, False, message_expiry_interval=None
    )


@pytest.mark.usefixtures("mqtt_mock")
async def test_mode_updates(
    hass: UniversalAssistant,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test that the selected mode follows the reported one."""
    await setup_integration(hass, mock_config_entry)
    await fire_burst(hass)

    assert hass.states.get(CHARGING_MODE_ENTITY_ID).state == "normal"

    async_fire_mqtt_message(hass, MODE_TOPIC, "1")
    await hass.async_block_till_done()

    assert hass.states.get(CHARGING_MODE_ENTITY_ID).state == "solar"


@pytest.mark.usefixtures("mqtt_mock")
async def test_mode_not_selectable(
    hass: UniversalAssistant,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test that a mode Prism cannot be put back into reads as unknown."""
    await setup_integration(hass, mock_config_entry)
    await fire_burst(hass)

    # Load balancing suspended the session: reported, but not user-settable.
    async_fire_mqtt_message(hass, MODE_TOPIC, "7")
    await hass.async_block_till_done()

    assert hass.states.get(CHARGING_MODE_ENTITY_ID).state == STATE_UNKNOWN
