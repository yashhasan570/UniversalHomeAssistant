"""Velbus button platform tests."""

from unittest.mock import AsyncMock, patch

import pytest
from pytest_universalassistant.common import MockConfigEntry, snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.button import DOMAIN as BUTTON_DOMAIN, ButtonService
from universalassistant.const import CommonServiceArgument, Platform
from universalassistant.core import UniversalAssistant
from universalassistant.helpers import entity_registry as er

from . import init_integration


@pytest.mark.usefixtures("entity_registry_enabled_by_default")
async def test_entities(
    hass: UniversalAssistant,
    snapshot: SnapshotAssertion,
    config_entry: MockConfigEntry,
    entity_registry: er.EntityRegistry,
) -> None:
    """Test all entities."""
    with patch("universalassistant.components.velbus.PLATFORMS", [Platform.BUTTON]):
        await init_integration(hass, config_entry)

    await snapshot_platform(hass, entity_registry, snapshot, config_entry.entry_id)


@pytest.mark.usefixtures("entity_registry_enabled_by_default")
async def test_button_press(
    hass: UniversalAssistant,
    mock_button: AsyncMock,
    config_entry: MockConfigEntry,
) -> None:
    """Test button press."""
    await init_integration(hass, config_entry)
    await hass.services.async_call(
        BUTTON_DOMAIN,
        ButtonService.PRESS,
        {CommonServiceArgument.ENTITY_ID: "button.bedroom_kid_1_buttonon"},
        blocking=True,
    )
    mock_button.press.assert_called_once_with()
