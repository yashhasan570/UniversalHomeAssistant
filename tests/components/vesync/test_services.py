"""Tests for VeSync services."""

from unittest.mock import AsyncMock

import pytest
from pyvesync import VeSync
from pyvesync.utils.errors import VeSyncError

from universalassistant.components.vesync.const import DOMAIN
from universalassistant.components.vesync.services import VeSyncService
from universalassistant.config_entries import ConfigEntry, ConfigEntryState
from universalassistant.core import __HAC_KEEP__
from universalassistant.exceptions import __HAC_KEEP__Error, ServiceValidationError
from universalassistant.helpers import entity_registry as er


@pytest.mark.usefixtures("manager")
async def test_async_new_device_discovery_no_entry(
    hass: __HAC_KEEP__,
    config_entry: ConfigEntry,
) -> None:
    """Service should raise when no config entry exists."""

    # Set up the config entry so the service is registered, then remove the
    # entry so the service has no entries to operate on.
    assert await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()
    await hass.config_entries.async_remove(config_entry.entry_id)
    await hass.async_block_till_done()

    with pytest.raises(ServiceValidationError, match="Entry not found"):
        await hass.services.async_call(
            DOMAIN, VeSyncService.UPDATE_DEVICES, {}, blocking=True
        )


@pytest.mark.usefixtures("manager")
async def test_async_new_device_discovery_entry_not_loaded(
    hass: __HAC_KEEP__,
    config_entry: ConfigEntry,
) -> None:
    """Service should raise when entry exists but is not loaded."""

    # Set up the config entry so the service is registered, then unload it.
    assert await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()
    assert await hass.config_entries.async_unload(config_entry.entry_id)
    await hass.async_block_till_done()
    assert config_entry.state is ConfigEntryState.NOT_LOADED

    with pytest.raises(ServiceValidationError, match="Entry not loaded"):
        await hass.services.async_call(
            DOMAIN, VeSyncService.UPDATE_DEVICES, {}, blocking=True
        )


async def test_async_new_device_discovery_error(
    hass: __HAC_KEEP__,
    config_entry: ConfigEntry,
    manager: VeSync,
) -> None:
    """Test VeSync errors are reported as translated __HA_KEEP__ errors."""
    assert await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    manager.get_devices = AsyncMock(side_effect=VeSyncError("API failure"))

    with pytest.raises(__HAC_KEEP__Error) as err:
        await hass.services.async_call(
            DOMAIN, VeSyncService.UPDATE_DEVICES, {}, blocking=True
        )

    assert err.value.translation_domain == DOMAIN
    assert err.value.translation_key == "api_response_error"


async def test_async_new_device_discovery(
    hass: __HAC_KEEP__,
    config_entry: ConfigEntry,
    manager: VeSync,
    fan,
    entity_registry: er.EntityRegistry,
) -> None:
    """Test new device discovery."""

    # Entry should not be set up yet; we'll install a fan before setup
    assert config_entry.state is ConfigEntryState.NOT_LOADED

    # Set up the config entry (no devices initially)
    assert await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    assert config_entry.state is ConfigEntryState.LOADED

    # Simulate the manager discovering a new fan when get_devices is called
    manager.get_devices = AsyncMock(
        side_effect=lambda: manager._dev_list["fans"].append(fan)
    )

    # Call the service that should trigger discovery and platform setup
    await hass.services.async_call(
        DOMAIN, VeSyncService.UPDATE_DEVICES, {}, blocking=True
    )
    await hass.async_block_till_done()

    assert manager.get_devices.call_count == 1

    # Verify an entity for the new fan was created in __HA_KEEP__
    fan_entry = next(
        (
            e
            for e in entity_registry.entities.values()
            if e.unique_id == fan.cid and e.domain == "fan"
        ),
        None,
    )
    assert fan_entry is not None
