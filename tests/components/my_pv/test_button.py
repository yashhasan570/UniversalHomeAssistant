"""Test the my-PV button platform."""

from unittest.mock import AsyncMock, patch

from my_pv.exceptions import (
    MyPVAuthenticationError,
    MyPVConnectionError,
    MyPVTooManyRequestsError,
)
import pytest
from pytest_universalassistant.common import MockConfigEntry, snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.button import DOMAIN as BUTTON_DOMAIN, ButtonService
from universalassistant.const import STATE_UNAVAILABLE, Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.exceptions import ConfigEntryAuthFailed, __HAC_KEEP__Error
from universalassistant.helpers import entity_registry as er

from . import setup_integration

pytestmark = pytest.mark.usefixtures("entity_registry_enabled_by_default")


@pytest.mark.usefixtures("mock_my_pv_client")
async def test_button(
    hass: __HAC_KEEP__,
    mock_config_entry: MockConfigEntry,
    snapshot: SnapshotAssertion,
    entity_registry: er.EntityRegistry,
) -> None:
    """Test successful setup of a button platform."""
    with patch("universalassistant.components.my_pv.PLATFORMS", [Platform.BUTTON]):
        await setup_integration(hass, mock_config_entry)

    await snapshot_platform(hass, entity_registry, snapshot, mock_config_entry.entry_id)


async def test_button_unavailable_not_connected(
    hass: __HAC_KEEP__,
    mock_config_entry: MockConfigEntry,
    mock_my_pv_client: AsyncMock,
) -> None:
    """Test if a button is unavailable when not connected."""
    mock_my_pv_client.connected = False

    await setup_integration(hass, mock_config_entry)

    state = hass.states.get("button.my_pv_ac_elwa_2_restart")
    assert state.state == STATE_UNAVAILABLE


async def test_button_press(
    hass: __HAC_KEEP__,
    mock_config_entry: MockConfigEntry,
    mock_my_pv_client: AsyncMock,
) -> None:
    """Test successful press of a button."""
    await setup_integration(hass, mock_config_entry)

    await hass.services.async_call(
        BUTTON_DOMAIN,
        ButtonService.PRESS,
        {"entity_id": "button.my_pv_ac_elwa_2_restart"},
        blocking=True,
    )
    mock_my_pv_client.send_command.assert_awaited_once_with("reboot_device", None)


async def test_button_press_send_command_returns_false(
    hass: __HAC_KEEP__,
    mock_config_entry: MockConfigEntry,
    mock_my_pv_client: AsyncMock,
) -> None:
    """Test for __HAC_KEEP__Error when send_command returns False."""
    await setup_integration(hass, mock_config_entry)

    mock_my_pv_client.send_command.return_value = False
    with pytest.raises(__HAC_KEEP__Error):
        await hass.services.async_call(
            BUTTON_DOMAIN,
            ButtonService.PRESS,
            {"entity_id": "button.my_pv_ac_elwa_2_restart"},
            blocking=True,
        )
    mock_my_pv_client.send_command.assert_awaited_once_with("reboot_device", None)

    mock_my_pv_client.send_command.reset_mock()
    mock_my_pv_client.send_command.return_value = True
    await hass.services.async_call(
        BUTTON_DOMAIN,
        ButtonService.PRESS,
        {"entity_id": "button.my_pv_ac_elwa_2_restart"},
        blocking=True,
    )
    mock_my_pv_client.send_command.assert_awaited_once_with("reboot_device", None)


@pytest.mark.parametrize(
    ("error", "expected_ha_error"),
    [
        (MyPVConnectionError(), __HAC_KEEP__Error),
        (MyPVAuthenticationError(), ConfigEntryAuthFailed),
        (MyPVTooManyRequestsError(), __HAC_KEEP__Error),
    ],
)
async def test_button_press_send_command_raises_error(
    hass: __HAC_KEEP__,
    mock_config_entry: MockConfigEntry,
    mock_my_pv_client: AsyncMock,
    error: MyPVConnectionError | MyPVAuthenticationError,
    expected_ha_error: type[__HAC_KEEP__Error],
) -> None:
    """Test for __HAC_KEEP__Error when send_command raises error."""
    await setup_integration(hass, mock_config_entry)

    mock_my_pv_client.send_command.side_effect = error
    with pytest.raises(expected_ha_error):
        await hass.services.async_call(
            BUTTON_DOMAIN,
            ButtonService.PRESS,
            {"entity_id": "button.my_pv_ac_elwa_2_restart"},
            blocking=True,
        )
    mock_my_pv_client.send_command.assert_awaited_once_with("reboot_device", None)

    mock_my_pv_client.send_command.reset_mock()
    mock_my_pv_client.send_command.side_effect = None
    await hass.services.async_call(
        BUTTON_DOMAIN,
        ButtonService.PRESS,
        {"entity_id": "button.my_pv_ac_elwa_2_restart"},
        blocking=True,
    )
    mock_my_pv_client.send_command.assert_awaited_once_with("reboot_device", None)
