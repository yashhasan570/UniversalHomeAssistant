"""Test Wallbox Lock component."""

from unittest.mock import patch

import pytest
from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.switch import SwitchService
from universalassistant.const import TargetKey
from universalassistant.core import UniversalAssistant
from universalassistant.exceptions import UniversalAssistantError

from .conftest import http_404_error, http_429_error, setup_integration
from .const import MOCK_SWITCH_ENTITY_ID


async def test_wallbox_switch_class(
    hass: UniversalAssistant, entry: MockConfigEntry, mock_wallbox
) -> None:
    """Test wallbox switch class."""

    await setup_integration(hass, entry)

    state = hass.states.get(MOCK_SWITCH_ENTITY_ID)
    assert state
    assert state.state == "on"

    await hass.services.async_call(
        "switch",
        SwitchService.TURN_ON,
        {
            TargetKey.ENTITY_ID: MOCK_SWITCH_ENTITY_ID,
        },
        blocking=True,
    )

    await hass.services.async_call(
        "switch",
        SwitchService.TURN_OFF,
        {
            TargetKey.ENTITY_ID: MOCK_SWITCH_ENTITY_ID,
        },
        blocking=True,
    )


async def test_wallbox_switch_class_error_handling(
    hass: UniversalAssistant, entry: MockConfigEntry, mock_wallbox
) -> None:
    """Test wallbox switch class connection error."""

    await setup_integration(hass, entry)

    with (
        patch.object(mock_wallbox, "resumeChargingSession", side_effect=http_404_error),
        pytest.raises(UniversalAssistantError),
    ):
        # Test behavior when a connection error occurs
        await hass.services.async_call(
            "switch",
            SwitchService.TURN_ON,
            {
                TargetKey.ENTITY_ID: MOCK_SWITCH_ENTITY_ID,
            },
            blocking=True,
        )

    with (
        patch.object(mock_wallbox, "resumeChargingSession", side_effect=http_429_error),
        pytest.raises(UniversalAssistantError),
    ):
        # Test behavior when a connection error occurs
        await hass.services.async_call(
            "switch",
            SwitchService.TURN_ON,
            {
                TargetKey.ENTITY_ID: MOCK_SWITCH_ENTITY_ID,
            },
            blocking=True,
        )
