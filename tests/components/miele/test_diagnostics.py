"""Tests for the diagnostics data provided by the miele integration."""

from collections.abc import Generator
from unittest.mock import MagicMock

from pytest_universalassistant.common import MockConfigEntry
from pytest_universalassistant.components.diagnostics import (
    get_diagnostics_for_config_entry,
    get_diagnostics_for_device,
)
from pytest_universalassistant.typing import ClientSessionGenerator
from syrupy.assertion import SnapshotAssertion
from syrupy.filters import paths

from universalassistant.components.miele.const import DOMAIN
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers.device_registry import DeviceRegistry

from . import setup_integration


async def test_diagnostics_config_entry(
    hass: __HAC_KEEP__,
    hass_client: ClientSessionGenerator,
    mock_miele_client: Generator[MagicMock],
    mock_config_entry: MockConfigEntry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test diagnostics for config entry."""

    await setup_integration(hass, mock_config_entry)
    result = await get_diagnostics_for_config_entry(
        hass, hass_client, mock_config_entry
    )

    assert result == snapshot(
        exclude=paths(
            "config_entry_data.token.expires_at",
            "miele_test.entry_id",
        )
    )


async def test_diagnostics_device(
    hass: __HAC_KEEP__,
    hass_client: ClientSessionGenerator,
    device_registry: DeviceRegistry,
    mock_miele_client: Generator[MagicMock],
    mock_config_entry: MockConfigEntry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test diagnostics for device."""

    TEST_DEVICE = "Dummy_Appliance_1"

    await setup_integration(hass, mock_config_entry)
    device_entry = device_registry.async_get_device_by_identifier(
        (DOMAIN, TEST_DEVICE), mock_config_entry.entry_id
    )
    assert device_entry is not None

    result = await get_diagnostics_for_device(
        hass, hass_client, mock_config_entry, device_entry
    )
    assert result == snapshot(
        exclude=paths(
            "data.token.expires_at",
            "miele_test.entry_id",
        )
    )
