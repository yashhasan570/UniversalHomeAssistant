"""Tests for the Qingping integration."""

from datetime import timedelta
import time

from pytest_universalassistant.common import MockConfigEntry, async_fire_time_changed
from pytest_universalassistant.components.bluetooth import (
    inject_bluetooth_service_info,
    patch_all_discovered_devices,
    patch_bluetooth_time,
)

from universalassistant.components.bluetooth import (
    FALLBACK_MAXIMUM_STALE_ADVERTISEMENT_SECONDS,
)
from universalassistant.components.qingping import async_remove_config_entry_device
from universalassistant.components.qingping.const import DOMAIN
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import device_registry as dr
from universalassistant.util import dt as dt_util

from . import LIGHT_SERVICE_INFO


def _device_entry_for(hass: __HAC_KEEP__, entry: MockConfigEntry) -> dr.DeviceEntry:
    """Return the device created for the config entry."""
    device_registry = dr.async_get(hass)
    return next(
        iter(dr.async_entries_for_config_entry(device_registry, entry.entry_id))
    )


async def _setup_entry_and_device(hass: __HAC_KEEP__) -> MockConfigEntry:
    """Set up a config entry and inject an advertisement to create the device."""
    entry = MockConfigEntry(domain=DOMAIN, unique_id="aa:bb:cc:dd:ee:ff")
    entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    inject_bluetooth_service_info(hass, LIGHT_SERVICE_INFO)
    await hass.async_block_till_done()
    return entry


async def test_remove_config_entry_device_available(hass: __HAC_KEEP__) -> None:
    """Test a device that is still available cannot be removed."""
    entry = await _setup_entry_and_device(hass)
    device_entry = _device_entry_for(hass, entry)

    assert not await async_remove_config_entry_device(hass, entry, device_entry)


async def test_remove_config_entry_device_unavailable(hass: __HAC_KEEP__) -> None:
    """Test a device that is no longer available can be removed."""
    start_monotonic = time.monotonic()
    entry = await _setup_entry_and_device(hass)

    # Fastforward time without BLE advertisements
    monotonic_now = start_monotonic + FALLBACK_MAXIMUM_STALE_ADVERTISEMENT_SECONDS + 1

    with (
        patch_bluetooth_time(
            monotonic_now,
        ),
        patch_all_discovered_devices([]),
    ):
        async_fire_time_changed(
            hass,
            dt_util.utcnow()
            + timedelta(seconds=FALLBACK_MAXIMUM_STALE_ADVERTISEMENT_SECONDS + 1),
        )
        await hass.async_block_till_done()

    device_entry = _device_entry_for(hass, entry)

    assert await async_remove_config_entry_device(hass, entry, device_entry)
