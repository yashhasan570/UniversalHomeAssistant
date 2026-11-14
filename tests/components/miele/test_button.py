"""Tests for Miele button module."""

from unittest.mock import MagicMock, Mock

from aiohttp import ClientResponseError
import pytest
from pytest_universalassistant.common import MockConfigEntry, snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.button import DOMAIN as BUTTON_DOMAIN, ButtonService
from universalassistant.const import CommonServiceArgument, Platform
from universalassistant.core import UniversalAssistant
from universalassistant.exceptions import UniversalAssistantError
from universalassistant.helpers import entity_registry as er

pytestmark = pytest.mark.parametrize("platforms", [(Platform.BUTTON,)])

ENTITY_ID = "button.washing_machine_start"


@pytest.mark.usefixtures("entity_registry_enabled_by_default")
async def test_button_states(
    hass: UniversalAssistant,
    mock_miele_client: MagicMock,
    snapshot: SnapshotAssertion,
    entity_registry: er.EntityRegistry,
    setup_platform: MockConfigEntry,
) -> None:
    """Test button entity state."""

    await snapshot_platform(hass, entity_registry, snapshot, setup_platform.entry_id)


@pytest.mark.usefixtures("entity_registry_enabled_by_default")
async def test_button_states_api_push(
    hass: UniversalAssistant,
    mock_miele_client: MagicMock,
    snapshot: SnapshotAssertion,
    entity_registry: er.EntityRegistry,
    setup_platform: MockConfigEntry,
    push_data_and_actions: None,
) -> None:
    """Test binary sensor state when the API pushes data via SSE."""

    await snapshot_platform(hass, entity_registry, snapshot, setup_platform.entry_id)


@pytest.mark.usefixtures("entity_registry_enabled_by_default")
async def test_button_press(
    hass: UniversalAssistant,
    mock_miele_client: MagicMock,
    setup_platform: MockConfigEntry,
) -> None:
    """Test button press."""

    await hass.services.async_call(
        BUTTON_DOMAIN,
        ButtonService.PRESS,
        {CommonServiceArgument.ENTITY_ID: ENTITY_ID},
        blocking=True,
    )
    mock_miele_client.send_action.assert_called_once_with(
        "Dummy_Appliance_3", {"processAction": 1}
    )


@pytest.mark.usefixtures("entity_registry_enabled_by_default")
async def test_api_failure(
    hass: UniversalAssistant,
    mock_miele_client: MagicMock,
    setup_platform: MockConfigEntry,
) -> None:
    """Test handling of exception from API."""
    mock_miele_client.send_action.side_effect = ClientResponseError(Mock(), Mock())

    with pytest.raises(
        UniversalAssistantError, match=f"Failed to set state for {ENTITY_ID}"
    ):
        await hass.services.async_call(
            BUTTON_DOMAIN,
            ButtonService.PRESS,
            {CommonServiceArgument.ENTITY_ID: ENTITY_ID},
            blocking=True,
        )
    mock_miele_client.send_action.assert_called_once()
