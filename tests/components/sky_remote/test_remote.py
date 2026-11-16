"""Test sky_remote remote."""

from unittest.mock import MagicMock

import pytest
from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.remote import (
    ATTR_COMMAND,
    DOMAIN as REMOTE_DOMAIN,
    SERVICE_SEND_COMMAND,
)
from universalassistant.components.sky_remote.const import DOMAIN
from universalassistant.const import ATTR_ENTITY_ID, SERVICE_TURN_OFF, SERVICE_TURN_ON
from universalassistant.core import UniversalAssistant
from universalassistant.exceptions import UniversalAssistantError, ServiceValidationError

from . import setup_mock_entry

ENTITY_ID = "remote.example_com"


async def test_send_command(
    hass: UniversalAssistant, mock_config_entry, mock_remote_control
) -> None:
    """Test "send_command" method."""
    await setup_mock_entry(hass, mock_config_entry)
    await hass.services.async_call(
        REMOTE_DOMAIN,
        SERVICE_SEND_COMMAND,
        {ATTR_ENTITY_ID: ENTITY_ID, ATTR_COMMAND: ["sky"]},
        blocking=True,
    )
    mock_remote_control._instance_mock.send_keys.assert_called_once_with(["sky"])


async def test_send_invalid_command(
    hass: UniversalAssistant, mock_config_entry, mock_remote_control
) -> None:
    """Test "send_command" method."""
    await setup_mock_entry(hass, mock_config_entry)

    with pytest.raises(ServiceValidationError):
        await hass.services.async_call(
            REMOTE_DOMAIN,
            SERVICE_SEND_COMMAND,
            {ATTR_ENTITY_ID: ENTITY_ID, ATTR_COMMAND: ["apple"]},
            blocking=True,
        )
    mock_remote_control._instance_mock.send_keys.assert_not_called()


async def test_send_command_failure(
    hass: UniversalAssistant,
    mock_config_entry: MockConfigEntry,
    mock_remote_control: MagicMock,
) -> None:
    """Test "send_command" method when the library rejects a command."""
    await setup_mock_entry(hass, mock_config_entry)
    mock_remote_control._instance_mock.send_keys.side_effect = ValueError("Bad key")

    with pytest.raises(UniversalAssistantError) as err:
        await hass.services.async_call(
            REMOTE_DOMAIN,
            SERVICE_SEND_COMMAND,
            {ATTR_ENTITY_ID: ENTITY_ID, ATTR_COMMAND: ["sky"]},
            blocking=True,
        )
    assert err.value.translation_domain == DOMAIN
    assert err.value.translation_key == "invalid_command"


@pytest.mark.parametrize(
    ("service", "expected_command"),
    [
        pytest.param(SERVICE_TURN_ON, "sky", id="turn_on"),
        pytest.param(SERVICE_TURN_OFF, "power", id="turn_off"),
    ],
)
async def test_turn_on_off(
    hass: UniversalAssistant,
    mock_config_entry: MockConfigEntry,
    mock_remote_control: MagicMock,
    service: str,
    expected_command: str,
) -> None:
    """Test "turn_on" and "turn_off" methods."""
    await setup_mock_entry(hass, mock_config_entry)
    await hass.services.async_call(
        REMOTE_DOMAIN,
        service,
        {ATTR_ENTITY_ID: ENTITY_ID},
        blocking=True,
    )
    mock_remote_control._instance_mock.send_keys.assert_called_once_with(
        [expected_command]
    )
