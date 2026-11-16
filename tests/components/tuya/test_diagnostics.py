"""Test Tuya diagnostics platform."""

import pytest
from pytest_universalassistant.common import MockConfigEntry
from pytest_universalassistant.components.diagnostics import (
    get_diagnostics_for_config_entry,
    get_diagnostics_for_device,
)
from pytest_universalassistant.typing import ClientSessionGenerator
from syrupy.assertion import SnapshotAssertion
from syrupy.filters import props
from tuya_sharing import CustomerDevice, Manager

from universalassistant.components.tuya.const import DOMAIN
from universalassistant.core import UniversalAssistant
from universalassistant.helpers import device_registry as dr

from . import initialize_entry


@pytest.mark.parametrize("mock_device_code", ["rqbj_4iqe2hsfyd86kwwc"])
async def test_entry_diagnostics(
    hass: UniversalAssistant,
    mock_manager: Manager,
    mock_config_entry: MockConfigEntry,
    mock_device: CustomerDevice,
    hass_client: ClientSessionGenerator,
    snapshot: SnapshotAssertion,
) -> None:
    """Test config entry diagnostics."""
    await initialize_entry(hass, mock_manager, mock_config_entry, mock_device)

    result = await get_diagnostics_for_config_entry(
        hass, hass_client, mock_config_entry
    )

    # Sort the lists of entities by entity_id to ensure consistent ordering
    # for snapshot testing
    for device in result["devices"]:
        device["universal_assistant"]["entities"] = sorted(
            device["universal_assistant"]["entities"], key=lambda x: x["state"]["entity_id"]
        )
    assert result == snapshot(
        exclude=props("last_changed", "last_reported", "last_updated")
    )


@pytest.mark.parametrize(
    "mock_device_code",
    [
        "rqbj_4iqe2hsfyd86kwwc",
        "mal_gyitctrjj1kefxp2",  # with redacted dpcodes
        "tdq_9htyiowaf5rtdhrv",  # with bad enum warnings
    ],
)
async def test_device_diagnostics(
    hass: UniversalAssistant,
    mock_manager: Manager,
    mock_config_entry: MockConfigEntry,
    mock_device: CustomerDevice,
    hass_client: ClientSessionGenerator,
    device_registry: dr.DeviceRegistry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test device diagnostics."""
    await initialize_entry(hass, mock_manager, mock_config_entry, mock_device)

    device = device_registry.async_get_device_by_identifier(
        (DOMAIN, mock_device.id), mock_config_entry.entry_id
    )
    assert device, repr(device_registry._devices)

    result = await get_diagnostics_for_device(
        hass, hass_client, mock_config_entry, device
    )
    # Sort the list of entities by entity_id to ensure consistent ordering
    # for snapshot testing
    result["universal_assistant"]["entities"] = sorted(
        result["universal_assistant"]["entities"], key=lambda x: x["state"]["entity_id"]
    )
    assert result == snapshot(
        exclude=props("last_changed", "last_reported", "last_updated")
    )
