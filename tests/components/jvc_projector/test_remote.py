"""Tests for JVC Projector remote platform."""

from unittest.mock import MagicMock, patch

import pytest
from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.remote import (
    ATTR_COMMAND,
    DOMAIN as REMOTE_DOMAIN,
    SERVICE_SEND_COMMAND,
)
from universalassistant.const import ATTR_ENTITY_ID, SERVICE_TURN_OFF, SERVICE_TURN_ON
from universalassistant.core import UniversalAssistant
from universalassistant.exceptions import UniversalAssistantError
from universalassistant.helpers import entity_registry as er

ENTITY_ID = "remote.jvc_projector"


async def test_entity_state(
    hass: UniversalAssistant,
    entity_registry: er.EntityRegistry,
    mock_device: MagicMock,
    mock_integration: MockConfigEntry,
) -> None:
    """Tests entity state is registered."""
    entity = hass.states.get(ENTITY_ID)
    assert entity
    assert entity_registry.async_get(entity.entity_id)


@patch("universalassistant.components.jvc_projector.remote.POWER_SLEEP", 0)
async def test_commands(
    hass: UniversalAssistant,
    mock_device: MagicMock,
    mock_integration: MockConfigEntry,
) -> None:
    """Test service call are called."""
    await hass.services.async_call(
        REMOTE_DOMAIN,
        SERVICE_TURN_ON,
        {ATTR_ENTITY_ID: ENTITY_ID},
        blocking=True,
    )

    await hass.services.async_call(
        REMOTE_DOMAIN,
        SERVICE_TURN_OFF,
        {ATTR_ENTITY_ID: ENTITY_ID},
        blocking=True,
    )

    await hass.services.async_call(
        REMOTE_DOMAIN,
        SERVICE_SEND_COMMAND,
        {ATTR_ENTITY_ID: ENTITY_ID, ATTR_COMMAND: ["ok"]},
        blocking=True,
    )

    await hass.services.async_call(
        REMOTE_DOMAIN,
        SERVICE_SEND_COMMAND,
        {ATTR_ENTITY_ID: ENTITY_ID, ATTR_COMMAND: ["hdmi1"]},
        blocking=True,
    )

    await hass.services.async_call(
        REMOTE_DOMAIN,
        SERVICE_SEND_COMMAND,
        {ATTR_ENTITY_ID: ENTITY_ID, ATTR_COMMAND: ["anamo"]},
        blocking=True,
    )

    await hass.services.async_call(
        REMOTE_DOMAIN,
        SERVICE_SEND_COMMAND,
        {ATTR_ENTITY_ID: ENTITY_ID, ATTR_COMMAND: ["picture_mode"]},
        blocking=True,
    )
    assert mock_device.remote.call_count == 4


async def test_unknown_command(
    hass: UniversalAssistant,
    mock_device: MagicMock,
    mock_integration: MockConfigEntry,
) -> None:
    """Test unknown service call errors."""
    with pytest.raises(UniversalAssistantError) as err:
        await hass.services.async_call(
            REMOTE_DOMAIN,
            SERVICE_SEND_COMMAND,
            {ATTR_ENTITY_ID: ENTITY_ID, ATTR_COMMAND: ["bad"]},
            blocking=True,
        )
    assert str(err.value) == "bad is not a known command"
