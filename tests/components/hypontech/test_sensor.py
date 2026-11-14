"""Tests for Hypontech sensors."""

from unittest.mock import AsyncMock, patch

from pytest_universalassistant.common import MockConfigEntry, snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.hypontech.const import CONF_OEM, DOMAIN
from universalassistant.const import CONF_PASSWORD, CONF_USERNAME, Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import device_registry as dr, entity_registry as er

from . import setup_integration


async def test_sensors(
    hass: __HAC_KEEP__,
    mock_hyponcloud: AsyncMock,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test the Hypontech sensors."""
    with patch("universalassistant.components.hypontech._PLATFORMS", [Platform.SENSOR]):
        await setup_integration(hass, mock_config_entry)

    await snapshot_platform(hass, entity_registry, snapshot, mock_config_entry.entry_id)


async def test_device_manufacturer_uses_oem(
    hass: __HAC_KEEP__,
    device_registry: dr.DeviceRegistry,
    mock_hyponcloud: AsyncMock,
) -> None:
    """Test device manufacturer uses the selected OEM."""
    mock_config_entry = MockConfigEntry(
        domain=DOMAIN,
        data={
            CONF_USERNAME: "test@example.com",
            CONF_PASSWORD: "test-password",
            CONF_OEM: 4,
        },
        unique_id="4:2123456789123456789",
    )

    with patch("universalassistant.components.hypontech._PLATFORMS", [Platform.SENSOR]):
        await setup_integration(hass, mock_config_entry)

    overview_device = device_registry.async_get_device_by_identifier(
        (DOMAIN, mock_config_entry.unique_id), mock_config_entry.entry_id
    )
    assert overview_device
    assert overview_device.manufacturer == "Nexen"

    plant = mock_hyponcloud.get_list.return_value[0]
    plant_device = device_registry.async_get_device_by_identifier(
        (DOMAIN, plant.plant_id), mock_config_entry.entry_id
    )
    assert plant_device
    assert plant_device.manufacturer == "Nexen"
