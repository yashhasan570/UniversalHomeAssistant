"""Tests for the yolink integration."""

from unittest.mock import patch

import pytest
from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.yolink import DOMAIN
from universalassistant.config_entries import ConfigEntryState
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import device_registry as dr
from universalassistant.helpers.config_entry_oauth2_flow import (
    ImplementationUnavailableError,
)
from universalassistant.setup import async_setup_component


@pytest.mark.usefixtures("setup_credentials", "mock_auth_manager", "mock_yolink_home")
async def test_device_remove_devices(
    hass: __HAC_KEEP__,
    device_registry: dr.DeviceRegistry,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test we can only remove a device that no longer exists."""

    device_registry.async_get_or_create(
        config_entry_id=mock_config_entry.entry_id,
        identifiers={(DOMAIN, "stale_device_id")},
    )
    device_entries = dr.async_entries_for_config_entry(
        device_registry, mock_config_entry.entry_id
    )

    assert len(device_entries) == 1
    device_entry = device_entries[0]
    assert device_entry.identifiers == {(DOMAIN, "stale_device_id")}

    assert await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    device_entries = dr.async_entries_for_config_entry(
        device_registry, mock_config_entry.entry_id
    )
    assert len(device_entries) == 0


@pytest.mark.usefixtures("setup_credentials", "mock_auth_manager", "mock_yolink_home")
async def test_oauth_implementation_not_available(
    hass: __HAC_KEEP__, mock_config_entry: MockConfigEntry
) -> None:
    """Test that an unavailable OAuth implementation raises ConfigEntryNotReady."""
    assert await async_setup_component(hass, "cloud", {})

    with patch(
        "universalassistant.components.yolink.async_get_config_entry_implementation",
        side_effect=ImplementationUnavailableError,
    ):
        await hass.config_entries.async_setup(mock_config_entry.entry_id)
        await hass.async_block_till_done()

    assert mock_config_entry.state is ConfigEntryState.SETUP_RETRY
