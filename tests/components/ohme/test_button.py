"""Tests for sensors."""

from datetime import timedelta
from unittest.mock import MagicMock, patch

from freezegun.api import FrozenDateTimeFactory
from ohme import ChargerStatus
from pytest_universalassistant.common import (
    MockConfigEntry,
    async_fire_time_changed,
    snapshot_platform,
)
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.button import DOMAIN as BUTTON_DOMAIN, ButtonService
from universalassistant.const import (
    STATE_UNAVAILABLE,
    STATE_UNKNOWN,
    CommonServiceArgument,
    Platform,
)
from universalassistant.core import UniversalAssistant
from universalassistant.helpers import entity_registry as er

from . import setup_integration


async def test_buttons(
    hass: UniversalAssistant,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
    mock_config_entry: MockConfigEntry,
    mock_client: MagicMock,
) -> None:
    """Test the Ohme buttons."""
    with patch("universalassistant.components.ohme.PLATFORMS", [Platform.BUTTON]):
        await setup_integration(hass, mock_config_entry)

    await snapshot_platform(hass, entity_registry, snapshot, mock_config_entry.entry_id)


async def test_button_available(
    hass: UniversalAssistant,
    freezer: FrozenDateTimeFactory,
    mock_config_entry: MockConfigEntry,
    mock_client: MagicMock,
) -> None:
    """Test that button shows as unavailable when a charge is not pending approval."""
    mock_client.status = ChargerStatus.PENDING_APPROVAL
    await setup_integration(hass, mock_config_entry)

    state = hass.states.get("button.ohme_home_pro_approve_charge")
    assert state.state == STATE_UNKNOWN

    mock_client.status = ChargerStatus.PLUGGED_IN
    freezer.tick(timedelta(seconds=60))
    async_fire_time_changed(hass)
    await hass.async_block_till_done(wait_background_tasks=True)

    state = hass.states.get("button.ohme_home_pro_approve_charge")
    assert state.state == STATE_UNAVAILABLE


async def test_button_press(
    hass: UniversalAssistant,
    mock_config_entry: MockConfigEntry,
    mock_client: MagicMock,
) -> None:
    """Test the button press action."""
    mock_client.status = ChargerStatus.PENDING_APPROVAL
    await setup_integration(hass, mock_config_entry)

    await hass.services.async_call(
        BUTTON_DOMAIN,
        ButtonService.PRESS,
        {
            CommonServiceArgument.ENTITY_ID: "button.ohme_home_pro_approve_charge",
        },
        blocking=True,
    )

    assert len(mock_client.async_approve_charge.mock_calls) == 1
