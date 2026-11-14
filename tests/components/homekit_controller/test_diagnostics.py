"""Test homekit_controller diagnostics."""

from pytest_universalassistant.components.diagnostics import (
    get_diagnostics_for_config_entry,
    get_diagnostics_for_device,
)
from pytest_universalassistant.typing import ClientSessionGenerator
from syrupy.assertion import SnapshotAssertion
from syrupy.filters import props

from universalassistant.components.homekit_controller.const import KNOWN_DEVICES
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import device_registry as dr

from .common import setup_accessories_from_file, setup_test_accessories

IP_CONNECTION_DATA = {
    "AccessoryIP": "192.168.1.10",
    "AccessoryIPs": ["192.168.1.10", "2001:db8::10", "fd00::10"],
    "AccessoryPort": 51826,
}


async def test_config_entry(
    hass: __HAC_KEEP__,
    hass_client: ClientSessionGenerator,
    snapshot: SnapshotAssertion,
) -> None:
    """Test generating diagnostics for a config entry."""
    accessories = await setup_accessories_from_file(hass, "koogeek_ls1.json")
    config_entry, _ = await setup_test_accessories(hass, accessories)
    hass.config_entries.async_update_entry(
        config_entry, data={**config_entry.data, **IP_CONNECTION_DATA}
    )

    diag = await get_diagnostics_for_config_entry(hass, hass_client, config_entry)

    assert diag == snapshot(
        exclude=props("last_changed", "last_reported", "last_updated")
    )


async def test_device(
    hass: __HAC_KEEP__,
    hass_client: ClientSessionGenerator,
    device_registry: dr.DeviceRegistry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test generating diagnostics for a device entry."""
    accessories = await setup_accessories_from_file(hass, "koogeek_ls1.json")
    config_entry, _ = await setup_test_accessories(hass, accessories)
    hass.config_entries.async_update_entry(
        config_entry, data={**config_entry.data, **IP_CONNECTION_DATA}
    )

    connection = hass.data[KNOWN_DEVICES]["00:00:00:00:00:00"]
    device = device_registry.async_get(connection.devices[1])

    diag = await get_diagnostics_for_device(hass, hass_client, config_entry, device)

    assert diag == snapshot(
        exclude=props("last_changed", "last_reported", "last_updated")
    )
