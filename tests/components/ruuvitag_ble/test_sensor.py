"""Test the Ruuvi BLE sensors."""

import pytest
from pytest_universalassistant.common import MockConfigEntry, snapshot_platform
from pytest_universalassistant.components.bluetooth import inject_bluetooth_service_info
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.ruuvitag_ble.const import DOMAIN
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers.entity_registry import EntityRegistry
from universalassistant.helpers.service_info.bluetooth import BluetoothServiceInfo

from .fixtures import (
    RUUVI_E1_SERVICE_INFO,
    RUUVI_V5_SERVICE_INFO,
    RUUVI_V6_SERVICE_INFO,
)


@pytest.mark.usefixtures("enable_bluetooth", "entity_registry_enabled_by_default")
@pytest.mark.parametrize(
    "service_info",
    [
        pytest.param(RUUVI_E1_SERVICE_INFO, id="e1"),
        pytest.param(RUUVI_V5_SERVICE_INFO, id="v5"),
        pytest.param(RUUVI_V6_SERVICE_INFO, id="v6"),
    ],
)
async def test_sensors(
    hass: __HAC_KEEP__,
    entity_registry: EntityRegistry,
    snapshot: SnapshotAssertion,
    service_info: BluetoothServiceInfo,
) -> None:
    """Test the Ruuvi BLE sensors."""
    entry = MockConfigEntry(domain=DOMAIN, unique_id=service_info.address)
    entry.add_to_hass(hass)

    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
    inject_bluetooth_service_info(hass, service_info)
    await hass.async_block_till_done()
    await snapshot_platform(hass, entity_registry, snapshot, entry.entry_id)
    assert await hass.config_entries.async_unload(entry.entry_id)
    await hass.async_block_till_done()
