"""Tests for the acaia buttons."""

from datetime import timedelta
from unittest.mock import MagicMock, patch

from aioacaia.exceptions import AcaiaDeviceNotFound, AcaiaError
from freezegun.api import FrozenDateTimeFactory
import pytest
from pytest_universalassistant.common import (
    MockConfigEntry,
    async_fire_time_changed,
    snapshot_platform,
)
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.button import DOMAIN as BUTTON_DOMAIN, ButtonService
from universalassistant.const import STATE_UNAVAILABLE, STATE_UNKNOWN, Platform, TargetKey
from universalassistant.core import UniversalAssistant
from universalassistant.exceptions import UniversalAssistantError
from universalassistant.helpers import entity_registry as er

from . import setup_integration

BUTTONS = (
    "tare",
    "reset_timer",
    "start_stop_timer",
)


async def test_buttons(
    hass: UniversalAssistant,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
    mock_scale: MagicMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test the acaia buttons."""

    with patch("universalassistant.components.acaia.PLATFORMS", [Platform.BUTTON]):
        await setup_integration(hass, mock_config_entry)
    await snapshot_platform(hass, entity_registry, snapshot, mock_config_entry.entry_id)


async def test_button_presses(
    hass: UniversalAssistant,
    mock_scale: MagicMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test the acaia button presses."""

    await setup_integration(hass, mock_config_entry)

    for button in BUTTONS:
        await hass.services.async_call(
            BUTTON_DOMAIN,
            ButtonService.PRESS,
            {
                TargetKey.ENTITY_ID: f"button.kitchen_lunar_ddeeff_{button}",
            },
            blocking=True,
        )

        function = getattr(mock_scale, button)
        function.assert_called_once()


@pytest.mark.parametrize("button", BUTTONS)
@pytest.mark.parametrize(
    "exception",
    [
        pytest.param(AcaiaError("Error during connecting to device"), id="error"),
        pytest.param(AcaiaDeviceNotFound("Device not found"), id="not_found"),
    ],
)
async def test_button_press_error(
    hass: UniversalAssistant,
    mock_scale: MagicMock,
    mock_config_entry: MockConfigEntry,
    button: str,
    exception: Exception,
) -> None:
    """Test a button press raises when the scale can't be reached."""

    await setup_integration(hass, mock_config_entry)
    getattr(mock_scale, button).side_effect = exception

    with pytest.raises(UniversalAssistantError, match="Could not connect to the scale"):
        await hass.services.async_call(
            BUTTON_DOMAIN,
            ButtonService.PRESS,
            {
                TargetKey.ENTITY_ID: f"button.kitchen_lunar_ddeeff_{button}",
            },
            blocking=True,
        )


async def test_buttons_unavailable_on_disconnected_scale(
    hass: UniversalAssistant,
    mock_scale: MagicMock,
    mock_config_entry: MockConfigEntry,
    freezer: FrozenDateTimeFactory,
) -> None:
    """Test the acaia buttons are unavailable when the scale is disconnected."""

    await setup_integration(hass, mock_config_entry)

    for button in BUTTONS:
        state = hass.states.get(f"button.kitchen_lunar_ddeeff_{button}")
        assert state
        assert state.state == STATE_UNKNOWN

    mock_scale.connected = False
    freezer.tick(timedelta(minutes=10))
    async_fire_time_changed(hass)
    await hass.async_block_till_done()

    for button in BUTTONS:
        state = hass.states.get(f"button.kitchen_lunar_ddeeff_{button}")
        assert state
        assert state.state == STATE_UNAVAILABLE
