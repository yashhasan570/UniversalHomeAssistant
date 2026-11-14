"""Test UptimeRobot switch."""

from unittest.mock import patch

import pytest
from pytest_universalassistant.common import MockConfigEntry, async_fire_time_changed
from pyuptimerobot import UptimeRobotAuthenticationException, UptimeRobotException
from pyuptimerobot.const import API_PATH_MONITOR_DETAIL

from universalassistant.components.switch import DOMAIN as SWITCH_DOMAIN, SwitchService
from universalassistant.components.uptimerobot.const import COORDINATOR_UPDATE_INTERVAL
from universalassistant.const import STATE_OFF, STATE_ON, CommonServiceArgument
from universalassistant.core import __HAC_KEEP__
from universalassistant.exceptions import __HAC_KEEP__Error
from universalassistant.util import dt as dt_util

from .common import (
    MOCK_UPTIMEROBOT_CONFIG_ENTRY_DATA,
    MOCK_UPTIMEROBOT_MONITOR,
    MOCK_UPTIMEROBOT_MONITOR_2,
    MOCK_UPTIMEROBOT_MONITOR_PAUSED,
    UPTIMEROBOT_SWITCH_TEST_ENTITY,
    mock_uptimerobot_api_response,
    setup_uptimerobot_integration,
)


async def test_presentation(hass: __HAC_KEEP__) -> None:
    """Test the presentation of UptimeRobot switches."""
    await setup_uptimerobot_integration(hass)

    assert (entity := hass.states.get(UPTIMEROBOT_SWITCH_TEST_ENTITY)) is not None
    assert entity.state == STATE_ON
    assert entity.attributes["target"] == MOCK_UPTIMEROBOT_MONITOR["url"]


async def test_switch_off(hass: __HAC_KEEP__) -> None:
    """Test entity unavailable on update failure."""

    mock_entry = MockConfigEntry(**MOCK_UPTIMEROBOT_CONFIG_ENTRY_DATA)
    mock_entry.add_to_hass(hass)

    with (
        patch(
            "pyuptimerobot.UptimeRobot.async_get_monitors",
            return_value=mock_uptimerobot_api_response(
                data=[MOCK_UPTIMEROBOT_MONITOR_PAUSED]
            ),
        ),
        patch(
            "pyuptimerobot.UptimeRobot.async_pause_monitor",
            return_value=mock_uptimerobot_api_response(
                api_path=API_PATH_MONITOR_DETAIL, data=MOCK_UPTIMEROBOT_MONITOR_PAUSED
            ),
        ),
    ):
        assert await hass.config_entries.async_setup(mock_entry.entry_id)
        await hass.async_block_till_done()

        await hass.services.async_call(
            SWITCH_DOMAIN,
            SwitchService.TURN_OFF,
            {CommonServiceArgument.ENTITY_ID: UPTIMEROBOT_SWITCH_TEST_ENTITY},
            blocking=True,
        )

    assert (entity := hass.states.get(UPTIMEROBOT_SWITCH_TEST_ENTITY)) is not None
    assert entity.state == STATE_OFF


async def test_switch_on(hass: __HAC_KEEP__) -> None:
    """Test entity unavailable on update failure."""

    mock_entry = MockConfigEntry(**MOCK_UPTIMEROBOT_CONFIG_ENTRY_DATA)
    mock_entry.add_to_hass(hass)

    with (
        patch(
            "pyuptimerobot.UptimeRobot.async_get_monitors",
            return_value=mock_uptimerobot_api_response(data=[MOCK_UPTIMEROBOT_MONITOR]),
        ),
        patch(
            "pyuptimerobot.UptimeRobot.async_start_monitor",
            return_value=mock_uptimerobot_api_response(
                api_path=API_PATH_MONITOR_DETAIL,
                data=MOCK_UPTIMEROBOT_MONITOR,
            ),
        ),
    ):
        assert await hass.config_entries.async_setup(mock_entry.entry_id)
        await hass.async_block_till_done()

        await hass.services.async_call(
            SWITCH_DOMAIN,
            SwitchService.TURN_ON,
            {CommonServiceArgument.ENTITY_ID: UPTIMEROBOT_SWITCH_TEST_ENTITY},
            blocking=True,
        )

        assert (entity := hass.states.get(UPTIMEROBOT_SWITCH_TEST_ENTITY)) is not None
        assert entity.state == STATE_ON


async def test_authentication_error(
    hass: __HAC_KEEP__, caplog: pytest.LogCaptureFixture
) -> None:
    """Test authentication error turning switch on/off."""
    await setup_uptimerobot_integration(hass)

    assert (entity := hass.states.get(UPTIMEROBOT_SWITCH_TEST_ENTITY)) is not None
    assert entity.state == STATE_ON

    with (
        patch(
            "pyuptimerobot.UptimeRobot.async_start_monitor",
            side_effect=UptimeRobotAuthenticationException,
        ),
        patch(
            "universalassistant.config_entries.ConfigEntry.async_start_reauth"
        ) as config_entry_reauth,
    ):
        await hass.services.async_call(
            SWITCH_DOMAIN,
            SwitchService.TURN_ON,
            {CommonServiceArgument.ENTITY_ID: UPTIMEROBOT_SWITCH_TEST_ENTITY},
            blocking=True,
        )

        config_entry_reauth.assert_called()


async def test_action_execution_failure(hass: __HAC_KEEP__) -> None:
    """Test turning switch on/off failure."""
    await setup_uptimerobot_integration(hass)

    assert (entity := hass.states.get(UPTIMEROBOT_SWITCH_TEST_ENTITY)) is not None
    assert entity.state == STATE_ON

    with (
        patch(
            "pyuptimerobot.UptimeRobot.async_start_monitor",
            side_effect=UptimeRobotException,
        ),
        pytest.raises(__HAC_KEEP__Error) as exc_info,
    ):
        await hass.services.async_call(
            SWITCH_DOMAIN,
            SwitchService.TURN_ON,
            {CommonServiceArgument.ENTITY_ID: UPTIMEROBOT_SWITCH_TEST_ENTITY},
            blocking=True,
        )

    assert exc_info.value.translation_domain == "uptimerobot"
    assert exc_info.value.translation_key == "api_switch_exception"
    assert exc_info.value.translation_placeholders == {
        "error": "Generic UptimeRobot exception"
    }


async def test_switch_api_failure(hass: __HAC_KEEP__) -> None:
    """Test general exception turning switch on/off."""
    await setup_uptimerobot_integration(hass)

    assert (entity := hass.states.get(UPTIMEROBOT_SWITCH_TEST_ENTITY)) is not None
    assert entity.state == STATE_ON

    with (
        patch(
            "pyuptimerobot.UptimeRobot.async_pause_monitor",
            side_effect=UptimeRobotException,
        ),
        pytest.raises(__HAC_KEEP__Error) as exc_info,
    ):
        await hass.services.async_call(
            SWITCH_DOMAIN,
            SwitchService.TURN_OFF,
            {CommonServiceArgument.ENTITY_ID: UPTIMEROBOT_SWITCH_TEST_ENTITY},
            blocking=True,
        )

    assert exc_info.value.translation_domain == "uptimerobot"
    assert exc_info.value.translation_key == "api_switch_exception"
    assert exc_info.value.translation_placeholders == {
        "error": "Generic UptimeRobot exception"
    }


async def test_switch_dynamic(hass: __HAC_KEEP__) -> None:
    """Test switch dynamically added."""
    await setup_uptimerobot_integration(hass)

    assert (entity := hass.states.get(UPTIMEROBOT_SWITCH_TEST_ENTITY))
    assert entity.state == STATE_ON

    entity_id_2 = "switch.test_monitor_2"

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

        assert (entity := hass.states.get(UPTIMEROBOT_SWITCH_TEST_ENTITY))
        assert entity.state == STATE_ON

        assert (entity := hass.states.get(entity_id_2))
        assert entity.state == STATE_ON
