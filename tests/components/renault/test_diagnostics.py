"""Test Renault diagnostics."""

import pytest
from pytest_universalassistant.components.diagnostics import (
    get_diagnostics_for_config_entry,
    get_diagnostics_for_device,
)
from pytest_universalassistant.typing import ClientSessionGenerator
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.renault import DOMAIN
from universalassistant.config_entries import ConfigEntry
from universalassistant.core import UniversalAssistant
from universalassistant.helpers import device_registry as dr

pytestmark = pytest.mark.usefixtures("patch_renault_account", "patch_get_vehicles")


@pytest.mark.usefixtures("fixtures_with_data")
@pytest.mark.parametrize("vehicle_type", ["zoe_40"], indirect=True)
async def test_entry_diagnostics(
    hass: UniversalAssistant,
    config_entry: ConfigEntry,
    hass_client: ClientSessionGenerator,
    snapshot: SnapshotAssertion,
) -> None:
    """Test config entry diagnostics."""
    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    assert (
        await get_diagnostics_for_config_entry(hass, hass_client, config_entry)
        == snapshot
    )


@pytest.mark.usefixtures("fixtures_with_data")
@pytest.mark.parametrize("vehicle_type", ["zoe_40"], indirect=True)
async def test_device_diagnostics(
    hass: UniversalAssistant,
    config_entry: ConfigEntry,
    device_registry: dr.DeviceRegistry,
    hass_client: ClientSessionGenerator,
    snapshot: SnapshotAssertion,
) -> None:
    """Test device diagnostics."""
    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    device = device_registry.async_get_device_by_identifier(
        (DOMAIN, "VF1ZOE40VIN"), config_entry.entry_id
    )
    assert device is not None

    assert (
        await get_diagnostics_for_device(hass, hass_client, config_entry, device)
        == snapshot
    )


@pytest.mark.usefixtures("fixtures_with_invalid_upstream_exception")
@pytest.mark.parametrize("vehicle_type", ["zoe_40"], indirect=True)
async def test_device_diagnostics_invalid_upstream_exception(
    hass: UniversalAssistant,
    config_entry: ConfigEntry,
    device_registry: dr.DeviceRegistry,
    hass_client: ClientSessionGenerator,
    snapshot: SnapshotAssertion,
) -> None:
    """Test device diagnostics with invalid upstream exception."""
    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    device = device_registry.async_get_device_by_identifier(
        (DOMAIN, "VF1ZOE40VIN"), config_entry.entry_id
    )
    assert device is not None

    data = await get_diagnostics_for_device(hass, hass_client, config_entry, device)
    assert data["data"] == {
        "battery": None,
        "battery_soc": None,
        "charge_mode": None,
        "charging_settings": None,
        "cockpit": None,
        "hvac_status": None,
    }
