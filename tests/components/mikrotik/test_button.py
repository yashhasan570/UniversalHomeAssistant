"""Tests for the Mikrotik button platform."""

from unittest.mock import MagicMock, patch

from pytest_universalassistant.common import snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.button import DOMAIN as BUTTON_DOMAIN, ButtonService
from universalassistant.const import CommonServiceArgument, Platform
from universalassistant.core import UniversalAssistant
from universalassistant.helpers import entity_registry as er

from . import setup_mikrotik_entry
from .conftest import MockConfigEntryFactory


async def test_button_entities_created(
    hass: UniversalAssistant,
    snapshot: SnapshotAssertion,
    entity_registry: er.EntityRegistry,
) -> None:
    """Test Mikrotik button entities are created with expected values."""
    with patch("universalassistant.components.mikrotik.PLATFORMS", [Platform.BUTTON]):
        config_entry = await setup_mikrotik_entry(hass)

    await snapshot_platform(hass, entity_registry, snapshot, config_entry.entry_id)


async def test_button_press(
    hass: UniversalAssistant,
    mock_api: MagicMock,
    mock_config_entry: MockConfigEntryFactory,
) -> None:
    """Test Mikrotik button entities press."""
    await setup_mikrotik_entry(
        hass,
        health_data=[
            {"name": "voltage", "value": 24.2},
        ],
        system_data=[
            {
                "cpu-load": 15,
                "total-memory": 0,
                "free-memory": 200,
                "total-hdd-space": 0,
                "free-hdd-space": 25,
                "uptime": None,
            }
        ],
    )

    await hass.services.async_call(
        BUTTON_DOMAIN,
        ButtonService.PRESS,
        {CommonServiceArgument.ENTITY_ID: "button.mikrotik_restart"},
        blocking=True,
    )

    mock_api.assert_called_with("/system/reboot")
