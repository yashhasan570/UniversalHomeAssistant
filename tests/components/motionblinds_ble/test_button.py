"""Tests for Motionblinds BLE buttons."""

from unittest.mock import Mock

import pytest
from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.button import DOMAIN as BUTTON_DOMAIN, ButtonService
from universalassistant.components.motionblinds_ble.const import (
    ATTR_CONNECT,
    ATTR_DISCONNECT,
    ATTR_FAVORITE,
)
from universalassistant.const import TargetKey
from universalassistant.core import UniversalAssistant

from . import setup_integration


@pytest.mark.usefixtures("motionblinds_ble_connect")
@pytest.mark.parametrize(
    ("button"),
    [
        ATTR_CONNECT,
        ATTR_DISCONNECT,
        ATTR_FAVORITE,
    ],
)
async def test_button(
    hass: UniversalAssistant,
    mock_config_entry: MockConfigEntry,
    mock_motion_device: Mock,
    name: str,
    button: str,
) -> None:
    """Test states of the button."""

    await setup_integration(hass, mock_config_entry)

    await hass.services.async_call(
        BUTTON_DOMAIN,
        ButtonService.PRESS,
        {TargetKey.ENTITY_ID: f"button.{name}_{button}"},
        blocking=True,
    )
    getattr(mock_motion_device, button).assert_called_once()
