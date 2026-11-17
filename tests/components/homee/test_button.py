"""Test Homee buttons."""

from collections.abc import AsyncGenerator
from unittest.mock import MagicMock, patch

import pytest
from pytest_universalassistant.common import MockConfigEntry, snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.button import DOMAIN as BUTTON_DOMAIN, ButtonService
from universalassistant.const import Platform, TargetKey
from universalassistant.core import UniversalAssistant
from universalassistant.helpers import entity_registry as er

from . import build_mock_node, setup_integration


@pytest.fixture(autouse=True)
async def platforms() -> AsyncGenerator[None]:
    """Return the platforms to be loaded for this test."""
    with patch("universalassistant.components.homee.PLATFORMS", [Platform.BUTTON]):
        yield


async def test_button_press(
    hass: UniversalAssistant,
    mock_homee: MagicMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test press button service."""
    mock_homee.nodes = [build_mock_node("buttons.json")]
    mock_homee.get_node_by_id.return_value = mock_homee.nodes[0]
    await setup_integration(hass, mock_config_entry)

    await hass.services.async_call(
        BUTTON_DOMAIN,
        ButtonService.PRESS,
        {TargetKey.ENTITY_ID: "button.test_button_impulse_1"},
        blocking=True,
    )

    mock_homee.set_value.assert_called_once_with(1, 5, 1)


async def test_button_snapshot(
    hass: UniversalAssistant,
    mock_homee: MagicMock,
    mock_config_entry: MockConfigEntry,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test the multisensor snapshot."""
    mock_homee.nodes = [build_mock_node("buttons.json")]
    mock_homee.get_node_by_id.return_value = mock_homee.nodes[0]
    await setup_integration(hass, mock_config_entry)

    await snapshot_platform(hass, entity_registry, snapshot, mock_config_entry.entry_id)
