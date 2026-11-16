"""Tests for the Abode alarm control panel device."""

from unittest.mock import PropertyMock, patch

from pytest_universalassistant.common import snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.alarm_control_panel import (
    DOMAIN as ALARM_DOMAIN,
    AlarmControlPanelState,
)
from universalassistant.const import (
    ATTR_ENTITY_ID,
    SERVICE_ALARM_ARM_AWAY,
    SERVICE_ALARM_ARM_HOME,
    SERVICE_ALARM_DISARM,
)
from universalassistant.core import UniversalAssistant
from universalassistant.helpers import entity_registry as er

from .common import setup_platform

DEVICE_ID = "alarm_control_panel.abode_alarm"


async def test_all_entities(
    hass: UniversalAssistant,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test all entities."""
    config_entry = await setup_platform(hass, ALARM_DOMAIN)

    await snapshot_platform(hass, entity_registry, snapshot, config_entry.entry_id)


async def test_set_alarm_away(hass: UniversalAssistant) -> None:
    """Test alarm state updates immediately after arming away."""
    with (
        patch("jaraco.abode.event_controller.EventController.add_device_callback"),
        patch(
            "jaraco.abode.devices.alarm.Alarm.mode", new_callable=PropertyMock
        ) as mock_mode,
    ):
        mock_mode.return_value = "standby"
        await setup_platform(hass, ALARM_DOMAIN)

        def set_away() -> None:
            mock_mode.return_value = "away"

        with patch(
            "jaraco.abode.devices.alarm.Alarm.set_away",
            side_effect=set_away,
        ) as mock_set_away:
            await hass.services.async_call(
                ALARM_DOMAIN,
                SERVICE_ALARM_ARM_AWAY,
                {ATTR_ENTITY_ID: DEVICE_ID},
                blocking=True,
            )
            await hass.async_block_till_done()

            mock_set_away.assert_called_once()
            assert hass.states.get(DEVICE_ID).state == AlarmControlPanelState.ARMED_AWAY


async def test_set_alarm_home(hass: UniversalAssistant) -> None:
    """Test alarm state updates immediately after arming home."""
    with (
        patch("jaraco.abode.event_controller.EventController.add_device_callback"),
        patch(
            "jaraco.abode.devices.alarm.Alarm.mode", new_callable=PropertyMock
        ) as mock_mode,
    ):
        mock_mode.return_value = "standby"
        await setup_platform(hass, ALARM_DOMAIN)

        def set_home() -> None:
            mock_mode.return_value = "home"

        with patch(
            "jaraco.abode.devices.alarm.Alarm.set_home",
            side_effect=set_home,
        ) as mock_set_home:
            await hass.services.async_call(
                ALARM_DOMAIN,
                SERVICE_ALARM_ARM_HOME,
                {ATTR_ENTITY_ID: DEVICE_ID},
                blocking=True,
            )
            await hass.async_block_till_done()

            mock_set_home.assert_called_once()
            assert hass.states.get(DEVICE_ID).state == AlarmControlPanelState.ARMED_HOME


async def test_set_alarm_standby(hass: UniversalAssistant) -> None:
    """Test alarm state updates immediately after disarming."""
    with (
        patch("jaraco.abode.event_controller.EventController.add_device_callback"),
        patch(
            "jaraco.abode.devices.alarm.Alarm.mode", new_callable=PropertyMock
        ) as mock_mode,
    ):
        mock_mode.return_value = "away"
        await setup_platform(hass, ALARM_DOMAIN)

        def set_standby() -> None:
            mock_mode.return_value = "standby"

        with patch(
            "jaraco.abode.devices.alarm.Alarm.set_standby",
            side_effect=set_standby,
        ) as mock_set_standby:
            await hass.services.async_call(
                ALARM_DOMAIN,
                SERVICE_ALARM_DISARM,
                {ATTR_ENTITY_ID: DEVICE_ID},
                blocking=True,
            )
            await hass.async_block_till_done()

            mock_set_standby.assert_called_once()
            assert hass.states.get(DEVICE_ID).state == AlarmControlPanelState.DISARMED


async def test_state_unknown(hass: UniversalAssistant) -> None:
    """Test an unknown alarm control panel state."""
    with patch(
        "jaraco.abode.devices.alarm.Alarm.mode", new_callable=PropertyMock
    ) as mock_mode:
        await setup_platform(hass, ALARM_DOMAIN)
        await hass.async_block_till_done()

        mock_mode.return_value = None

        state = hass.states.get(DEVICE_ID)
        assert state.state == "unknown"
