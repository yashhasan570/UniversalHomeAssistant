"""Test 1-Wire diagnostics."""

from collections.abc import Generator
from unittest.mock import MagicMock, patch

import pytest
from pytest_universalassistant.common import MockConfigEntry
from pytest_universalassistant.components.diagnostics import (
    get_diagnostics_for_config_entry,
    get_diagnostics_for_device,
)
from pytest_universalassistant.typing import ClientSessionGenerator
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.onewire import DOMAIN
from universalassistant.const import Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import device_registry as dr

from . import setup_owproxy_mock_devices


@pytest.fixture(autouse=True)
def override_platforms() -> Generator[None]:
    """Override PLATFORMS."""
    with patch("universalassistant.components.onewire._PLATFORMS", [Platform.SWITCH]):
        yield


@pytest.mark.parametrize("device_id", ["EF.111111111113"], indirect=True)
async def test_entry_diagnostics(
    hass: __HAC_KEEP__,
    config_entry: MockConfigEntry,
    hass_client: ClientSessionGenerator,
    owproxy: MagicMock,
    device_id: str,
    snapshot: SnapshotAssertion,
) -> None:
    """Test config entry diagnostics."""
    setup_owproxy_mock_devices(owproxy, [device_id])
    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    assert (
        await get_diagnostics_for_config_entry(hass, hass_client, config_entry)
        == snapshot
    )


@pytest.mark.parametrize("device_id", ["EF.111111111113"], indirect=True)
async def test_device_diagnostics(
    hass: __HAC_KEEP__,
    config_entry: MockConfigEntry,
    device_registry: dr.DeviceRegistry,
    hass_client: ClientSessionGenerator,
    owproxy: MagicMock,
    device_id: str,
    snapshot: SnapshotAssertion,
) -> None:
    """Test device diagnostics."""
    setup_owproxy_mock_devices(owproxy, [device_id])
    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    device = device_registry.async_get_device_by_identifier(
        (DOMAIN, "EF.111111111113"), config_entry.entry_id
    )
    assert device is not None

    assert (
        await get_diagnostics_for_device(hass, hass_client, config_entry, device)
        == snapshot
    )
