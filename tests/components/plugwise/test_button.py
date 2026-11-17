"""Tests for Plugwise button entities."""

from unittest.mock import MagicMock

import pytest
from pytest_universalassistant.common import MockConfigEntry, snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.button import DOMAIN as BUTTON_DOMAIN, ButtonService
from universalassistant.const import TargetKey
from universalassistant.core import UniversalAssistant
from universalassistant.helpers import entity_registry as er


@pytest.mark.usefixtures("mock_smile_adam")
@pytest.mark.parametrize("platforms", [(BUTTON_DOMAIN,)])
@pytest.mark.usefixtures("entity_registry_enabled_by_default")
async def test_adam_button_snapshot(
    hass: UniversalAssistant,
    snapshot: SnapshotAssertion,
    entity_registry: er.EntityRegistry,
    setup_platform: MockConfigEntry,
) -> None:
    """Test Adam button snapshot."""
    await snapshot_platform(hass, entity_registry, snapshot, setup_platform.entry_id)


async def test_adam_press_reboot_button(
    hass: UniversalAssistant, mock_smile_adam: MagicMock, init_integration: MockConfigEntry
) -> None:
    """Test pressing of button entity."""
    await hass.services.async_call(
        BUTTON_DOMAIN,
        ButtonService.PRESS,
        {TargetKey.ENTITY_ID: "button.adam_reboot"},
        blocking=True,
    )

    assert mock_smile_adam.reboot_gateway.call_count == 1
    mock_smile_adam.reboot_gateway.assert_called_with()
