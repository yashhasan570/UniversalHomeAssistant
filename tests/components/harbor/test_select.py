"""Test the Harbor selects."""

from typing import Any
from unittest.mock import AsyncMock, patch

from harbor import HarborCommandError
import pytest
from pytest_universalassistant.common import MockConfigEntry, snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.select import (
    DOMAIN as SELECT_DOMAIN,
    SelectService,
    SelectServiceArgument,
)
from universalassistant.config_entries import ConfigEntryState
from universalassistant.const import STATE_UNKNOWN, CommonServiceArgument, Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.exceptions import __HAC_KEEP__Error
from universalassistant.helpers import entity_registry as er

from . import setup_integration
from .conftest import SETTINGS_TOPIC, emit_message

NIGHT_MODE_ENTITY = "select.harbor_camera_1234567890_night_mode"

SELECT_SETTINGS_PAYLOAD: dict[str, Any] = {
    "settings": {"preference_video_night_mode": "auto"},
}


@pytest.mark.usefixtures("entity_registry_enabled_by_default")
async def test_selects(
    hass: __HAC_KEEP__,
    entity_registry: er.EntityRegistry,
    mock_config_entry: MockConfigEntry,
    mock_mqtt_client: AsyncMock,
    snapshot: SnapshotAssertion,
) -> None:
    """Test the Harbor selects report their current option."""
    with patch("universalassistant.components.harbor.PLATFORMS", [Platform.SELECT]):
        await setup_integration(hass, mock_config_entry)
    assert mock_config_entry.state is ConfigEntryState.LOADED

    await emit_message(mock_mqtt_client, SETTINGS_TOPIC, SELECT_SETTINGS_PAYLOAD)
    await hass.async_block_till_done()

    await snapshot_platform(hass, entity_registry, snapshot, mock_config_entry.entry_id)


@pytest.mark.parametrize(
    "option",
    [
        pytest.param("auto", id="auto"),
        pytest.param("on", id="on"),
        pytest.param("off", id="off"),
    ],
)
async def test_select_option(
    hass: __HAC_KEEP__,
    mock_config_entry: MockConfigEntry,
    mock_mqtt_client: AsyncMock,
    option: str,
) -> None:
    """Test selecting an option passes the device value to the library."""
    await setup_integration(hass, mock_config_entry)

    await hass.services.async_call(
        SELECT_DOMAIN,
        SelectService.SELECT_OPTION,
        {
            CommonServiceArgument.ENTITY_ID: NIGHT_MODE_ENTITY,
            SelectServiceArgument.OPTION: option,
        },
        blocking=True,
    )

    mock_mqtt_client.return_value.set_night_mode.assert_awaited_once_with(option)


@pytest.mark.parametrize(
    "error",
    [
        pytest.param(
            HarborCommandError("command", {"error": "rejected"}), id="command"
        ),
        pytest.param(TimeoutError, id="timeout"),
        pytest.param(ConnectionError, id="connection"),
    ],
)
async def test_select_option_failure_raises(
    hass: __HAC_KEEP__,
    mock_config_entry: MockConfigEntry,
    mock_mqtt_client: AsyncMock,
    error: Exception | type[Exception],
) -> None:
    """Test a failed camera command surfaces as a __HAC_KEEP__Error."""
    await setup_integration(hass, mock_config_entry)

    mock_mqtt_client.return_value.set_night_mode.side_effect = error

    with pytest.raises(__HAC_KEEP__Error):
        await hass.services.async_call(
            SELECT_DOMAIN,
            SelectService.SELECT_OPTION,
            {
                CommonServiceArgument.ENTITY_ID: NIGHT_MODE_ENTITY,
                SelectServiceArgument.OPTION: "off",
            },
            blocking=True,
        )


async def test_unexpected_option_stays_valid(
    hass: __HAC_KEEP__,
    mock_config_entry: MockConfigEntry,
    mock_mqtt_client: AsyncMock,
) -> None:
    """Test a night mode outside the declared options surfaces as unknown.

    The library maps unrecognized enum values onto its own "unknown" member;
    the select treats that as no selection rather than exposing "unknown" as a
    literal option.
    """
    await setup_integration(hass, mock_config_entry)

    await emit_message(mock_mqtt_client, SETTINGS_TOPIC, SELECT_SETTINGS_PAYLOAD)
    await hass.async_block_till_done()
    assert hass.states.get(NIGHT_MODE_ENTITY).state == "auto"

    await emit_message(
        mock_mqtt_client,
        SETTINGS_TOPIC,
        {"settings": {"preference_video_night_mode": "sunset"}},
    )
    await hass.async_block_till_done()
    assert hass.states.get(NIGHT_MODE_ENTITY).state == STATE_UNKNOWN
