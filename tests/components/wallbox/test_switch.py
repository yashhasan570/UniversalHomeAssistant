"""Test Wallbox Lock component."""

from unittest.mock import patch

import pytest
from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.switch import SwitchService
from universalassistant.const import CommonServiceArgument
from universalassistant.core import __HAC_KEEP__
from universalassistant.exceptions import __HAC_KEEP__Error

from .conftest import http_404_error, http_429_error, setup_integration
from .const import MOCK_SWITCH_ENTITY_ID


async def test_wallbox_switch_class(
    hass: __HAC_KEEP__, entry: MockConfigEntry, mock_wallbox
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
            CommonServiceArgument.ENTITY_ID: MOCK_SWITCH_ENTITY_ID,
        },
        blocking=True,
    )

    await hass.services.async_call(
        "switch",
        SwitchService.TURN_OFF,
        {
            CommonServiceArgument.ENTITY_ID: MOCK_SWITCH_ENTITY_ID,
        },
        blocking=True,
    )


async def test_wallbox_switch_class_error_handling(
    hass: __HAC_KEEP__, entry: MockConfigEntry, mock_wallbox
) -> None:
    """Test wallbox switch class connection error."""

    await setup_integration(hass, entry)

    with (
        patch.object(mock_wallbox, "resumeChargingSession", side_effect=http_404_error),
        pytest.raises(__HAC_KEEP__Error),
    ):
        # Test behavior when a connection error occurs
        await hass.services.async_call(
            "switch",
            SwitchService.TURN_ON,
            {
                CommonServiceArgument.ENTITY_ID: MOCK_SWITCH_ENTITY_ID,
            },
            blocking=True,
        )

    with (
        patch.object(mock_wallbox, "resumeChargingSession", side_effect=http_429_error),
        pytest.raises(__HAC_KEEP__Error),
    ):
        # Test behavior when a connection error occurs
        await hass.services.async_call(
            "switch",
            SwitchService.TURN_ON,
            {
                CommonServiceArgument.ENTITY_ID: MOCK_SWITCH_ENTITY_ID,
            },
            blocking=True,
        )
