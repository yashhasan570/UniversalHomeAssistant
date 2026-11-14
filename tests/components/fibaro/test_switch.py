"""Test the Fibaro switch platform."""

from unittest.mock import Mock, patch

from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.switch import DOMAIN as SWITCH_DOMAIN, SwitchService
from universalassistant.const import CommonServiceArgument, Platform
from universalassistant.core import UniversalAssistant
from universalassistant.helpers import entity_registry as er

from .conftest import init_integration


async def test_switch_setup(
    hass: UniversalAssistant,
    entity_registry: er.EntityRegistry,
    mock_fibaro_client: Mock,
    mock_config_entry: MockConfigEntry,
    mock_switch: Mock,
    mock_room: Mock,
) -> None:
    """Test that the switch creates an entity."""

    # Arrange
    mock_fibaro_client.read_rooms.return_value = [mock_room]
    mock_fibaro_client.read_devices.return_value = [mock_switch]

    with patch("universalassistant.components.fibaro.PLATFORMS", [Platform.SWITCH]):
        # Act
        await init_integration(hass, mock_config_entry)
        # Assert
        entry = entity_registry.async_get("switch.test_switch_room_1_test_switch")
        assert entry
        assert entry.unique_id == "hc2_111111.9"
        assert entry.original_name == "Room 1 Test switch"


async def test_switch_turn_on(
    hass: UniversalAssistant,
    mock_fibaro_client: Mock,
    mock_config_entry: MockConfigEntry,
    mock_switch: Mock,
    mock_room: Mock,
) -> None:
    """Test activate scene is called."""
    # Arrange
    mock_fibaro_client.read_rooms.return_value = [mock_room]
    mock_fibaro_client.read_devices.return_value = [mock_switch]

    with patch("universalassistant.components.fibaro.PLATFORMS", [Platform.SWITCH]):
        await init_integration(hass, mock_config_entry)
        # Act
        await hass.services.async_call(
            SWITCH_DOMAIN,
            SwitchService.TURN_ON,
            {CommonServiceArgument.ENTITY_ID: "switch.test_switch_room_1_test_switch"},
            blocking=True,
        )
        # Assert
        assert mock_switch.execute_action.call_count == 1


async def test_switch_turn_off(
    hass: UniversalAssistant,
    mock_fibaro_client: Mock,
    mock_config_entry: MockConfigEntry,
    mock_switch: Mock,
    mock_room: Mock,
) -> None:
    """Test activate scene is called."""
    # Arrange
    mock_fibaro_client.read_rooms.return_value = [mock_room]
    mock_fibaro_client.read_devices.return_value = [mock_switch]

    with patch("universalassistant.components.fibaro.PLATFORMS", [Platform.SWITCH]):
        await init_integration(hass, mock_config_entry)
        # Act
        await hass.services.async_call(
            SWITCH_DOMAIN,
            SwitchService.TURN_OFF,
            {CommonServiceArgument.ENTITY_ID: "switch.test_switch_room_1_test_switch"},
            blocking=True,
        )
        # Assert
        assert mock_switch.execute_action.call_count == 1
