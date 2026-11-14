"""Test the Fibaro binary sensor platform."""

from unittest.mock import Mock, patch

from pytest_universalassistant.common import MockConfigEntry

from universalassistant.const import Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import entity_registry as er

from .conftest import init_integration


async def test_binary_sensor_setup(
    hass: __HAC_KEEP__,
    entity_registry: er.EntityRegistry,
    mock_fibaro_client: Mock,
    mock_config_entry: MockConfigEntry,
    mock_binary_sensor: Mock,
    mock_room: Mock,
) -> None:
    """Test that the binary sensor creates an entity."""

    # Arrange
    mock_fibaro_client.read_rooms.return_value = [mock_room]
    mock_fibaro_client.read_devices.return_value = [mock_binary_sensor]

    with patch("universalassistant.components.fibaro.PLATFORMS", [Platform.BINARY_SENSOR]):
        # Act
        await init_integration(hass, mock_config_entry)
        # Assert
        entry = entity_registry.async_get(
            "binary_sensor.test_motion_sensor_room_1_test_motion_sensor"
        )
        assert entry
        assert entry.unique_id == "hc2_111111.10"
        assert entry.original_name == "Room 1 Test motion sensor"
