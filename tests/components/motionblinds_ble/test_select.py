"""Tests for Motionblinds BLE selects."""

from collections.abc import Callable
from enum import Enum
from typing import Any
from unittest.mock import Mock

from motionblindsble.const import MotionSpeedLevel
from motionblindsble.device import MotionDevice
import pytest
from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.motionblinds_ble.const import ATTR_SPEED
from universalassistant.components.select import (
    DOMAIN as SELECT_DOMAIN,
    SelectService,
    SelectServiceArgument,
)
from universalassistant.const import CommonServiceArgument
from universalassistant.core import __HAC_KEEP__

from . import setup_integration


@pytest.mark.parametrize(("select", "args"), [(ATTR_SPEED, MotionSpeedLevel.HIGH)])
async def test_select(
    hass: __HAC_KEEP__,
    mock_config_entry: MockConfigEntry,
    mock_motion_device: Mock,
    name: str,
    select: str,
    args: Any,
) -> None:
    """Test select."""

    await setup_integration(hass, mock_config_entry)

    await hass.services.async_call(
        SELECT_DOMAIN,
        SelectService.SELECT_OPTION,
        {
            CommonServiceArgument.ENTITY_ID: f"select.{name}_{select}",
            SelectServiceArgument.OPTION: MotionSpeedLevel.HIGH.value,
        },
        blocking=True,
    )
    getattr(mock_motion_device, select).assert_called_once_with(args)


@pytest.mark.parametrize(
    ("select", "register_callback", "value"),
    [
        (
            ATTR_SPEED,
            lambda device: device.register_speed_callback,
            MotionSpeedLevel.HIGH,
        )
    ],
)
async def test_select_update(
    hass: __HAC_KEEP__,
    mock_config_entry: MockConfigEntry,
    mock_motion_device: Mock,
    name: str,
    select: str,
    register_callback: Callable[[MotionDevice], Callable[..., None]],
    value: type[Enum],
) -> None:
    """Test select state update."""

    await setup_integration(hass, mock_config_entry)

    update_func = register_callback(mock_motion_device).call_args[0][0]

    update_func(value)
    assert hass.states.get(f"select.{name}_{select}").state == str(value.value)
