"""Test the Fibaro lock platform."""

from unittest.mock import Mock, patch

from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.lock import DOMAIN as LOCK_DOMAIN, LockService
from universalassistant.const import Platform, TargetKey
from universalassistant.core import UniversalAssistant
from universalassistant.helpers import entity_registry as er

from .conftest import init_integration


async def test_lock_setup(
    hass: UniversalAssistant,
    entity_registry: er.EntityRegistry,
    mock_fibaro_client: Mock,
    mock_config_entry: MockConfigEntry,
    mock_lock: Mock,
    mock_room: Mock,
) -> None:
    """Test that the lock creates an entity."""

    # Arrange
    mock_fibaro_client.read_rooms.return_value = [mock_room]
    mock_fibaro_client.read_devices.return_value = [mock_lock]

    with patch("universalassistant.components.fibaro.PLATFORMS", [Platform.LOCK]):
        # Act
        await init_integration(hass, mock_config_entry)
        # Assert
        entry = entity_registry.async_get("lock.test_lock_room_1_test_lock")
        assert entry
        assert entry.unique_id == "hc2_111111.11"
        assert entry.original_name == "Room 1 Test lock"


async def test_execute_lock_action(
    hass: UniversalAssistant,
    mock_fibaro_client: Mock,
    mock_config_entry: MockConfigEntry,
    mock_lock: Mock,
    mock_room: Mock,
) -> None:
    """Test activate scene is called."""
    # Arrange
    mock_fibaro_client.read_rooms.return_value = [mock_room]
    mock_fibaro_client.read_devices.return_value = [mock_lock]

    with patch("universalassistant.components.fibaro.PLATFORMS", [Platform.LOCK]):
        await init_integration(hass, mock_config_entry)
        # Act
        await hass.services.async_call(
            LOCK_DOMAIN,
            LockService.LOCK,
            {TargetKey.ENTITY_ID: "lock.test_lock_room_1_test_lock"},
            blocking=True,
        )
        # Assert
        assert mock_lock.execute_action.call_count == 1


async def test_execute_unlock_action(
    hass: UniversalAssistant,
    mock_fibaro_client: Mock,
    mock_config_entry: MockConfigEntry,
    mock_lock: Mock,
    mock_room: Mock,
) -> None:
    """Test activate scene is called."""
    # Arrange
    mock_fibaro_client.read_rooms.return_value = [mock_room]
    mock_fibaro_client.read_devices.return_value = [mock_lock]

    with patch("universalassistant.components.fibaro.PLATFORMS", [Platform.LOCK]):
        await init_integration(hass, mock_config_entry)
        # Act
        await hass.services.async_call(
            LOCK_DOMAIN,
            LockService.UNLOCK,
            {TargetKey.ENTITY_ID: "lock.test_lock_room_1_test_lock"},
            blocking=True,
        )
        # Assert
        assert mock_lock.execute_action.call_count == 1
