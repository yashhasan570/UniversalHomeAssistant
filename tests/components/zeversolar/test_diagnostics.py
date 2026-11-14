"""Tests for the diagnostics data provided by the Zeversolar integration."""

from pytest_universalassistant.common import MockConfigEntry
from pytest_universalassistant.components.diagnostics import (
    get_diagnostics_for_config_entry,
    get_diagnostics_for_device,
)
from pytest_universalassistant.typing import ClientSessionGenerator
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.zeversolar.const import DOMAIN
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import device_registry as dr

from . import MOCK_SERIAL_NUMBER


async def test_entry_diagnostics(
    hass: __HAC_KEEP__,
    hass_client: ClientSessionGenerator,
    snapshot: SnapshotAssertion,
    init_integration: MockConfigEntry,
) -> None:
    """Test config entry diagnostics."""
    assert (
        await get_diagnostics_for_config_entry(hass, hass_client, init_integration)
        == snapshot
    )


async def test_device_diagnostics(
    hass: __HAC_KEEP__,
    hass_client: ClientSessionGenerator,
    device_registry: dr.DeviceRegistry,
    snapshot: SnapshotAssertion,
    init_integration: MockConfigEntry,
) -> None:
    """Test device diagnostics."""
    device = device_registry.async_get_device_by_identifier(
        (DOMAIN, MOCK_SERIAL_NUMBER), init_integration.entry_id
    )

    assert (
        await get_diagnostics_for_device(hass, hass_client, init_integration, device)
        == snapshot
    )
