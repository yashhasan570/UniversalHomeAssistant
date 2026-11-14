"""Tests for the LIFX integration."""

from contextlib import contextmanager
from datetime import timedelta
from typing import Any
from unittest.mock import AsyncMock, patch

from lifx import Device, DiscoveredDevice
from pytest_universalassistant.common import MockConfigEntry, async_fire_time_changed

from universalassistant.components.lifx.const import DOMAIN
from universalassistant.const import CONF_HOST, Platform
from universalassistant.core import UniversalAssistant
from universalassistant.helpers import entity_registry as er
from universalassistant.setup import async_setup_component
from universalassistant.util import dt as dt_util

from .helpers import GROUP, IP_ADDRESS, LABEL, SERIAL, create_mock_light

__all__ = ["GROUP", "IP_ADDRESS", "LABEL", "SERIAL"]

MODULE = "universalassistant.components.lifx"
MODULE_CONFIG_FLOW = "universalassistant.components.lifx.config_flow"
# Firmware 3.70 and earlier report a MAC address one greater than the serial
LEGACY_MAC_ADDRESS = "d0:73:d5:dd:ee:cd"
DHCP_FORMATTED_MAC = "d073d5ddeecd"
DEFAULT_ENTRY_TITLE = LABEL
# Comfortably past the coordinator's own update interval
UPDATE_INTERVAL = timedelta(seconds=15)


async def async_setup_lifx_entry(
    hass: UniversalAssistant, device: Device
) -> MockConfigEntry:
    """Set up a config entry for one typed LIFX device."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        title=DEFAULT_ENTRY_TITLE,
        data={CONF_HOST: IP_ADDRESS},
        unique_id=SERIAL,
    )
    entry.add_to_hass(hass)
    with patch("universalassistant.components.lifx.Device.connect", return_value=device):
        assert await async_setup_component(hass, DOMAIN, {DOMAIN: {}})
        await hass.async_block_till_done()
    return entry


async def async_setup_lifx_entries(
    hass: UniversalAssistant, devices: list[Device]
) -> list[MockConfigEntry]:
    """Set up one config entry per typed LIFX device."""
    entries = [
        MockConfigEntry(
            domain=DOMAIN,
            title=device.state.label,
            data={CONF_HOST: device.ip},
            unique_id=device.serial,
        )
        for device in devices
    ]
    for entry in entries:
        entry.add_to_hass(hass)

    devices_by_host = {device.ip: device for device in devices}
    with patch(
        "universalassistant.components.lifx.Device.connect",
        side_effect=lambda **kwargs: devices_by_host[kwargs["ip"]],
    ):
        assert await async_setup_component(hass, DOMAIN, {DOMAIN: {}})
        await hass.async_block_till_done()
    return entries


async def async_enable_components(
    hass: UniversalAssistant,
    entry: MockConfigEntry,
    entity_registry: er.EntityRegistry,
    device: Device,
    keys: tuple[str, ...],
) -> None:
    """Enable a device's component entities and reload so they are added."""
    for key in keys:
        entity_id = entity_registry.async_get_entity_id(
            Platform.LIGHT, DOMAIN, f"{SERIAL}_{key}"
        )
        assert entity_id
        entity_registry.async_update_entity(entity_id, disabled_by=None)
    with patch("universalassistant.components.lifx.Device.connect", return_value=device):
        await hass.config_entries.async_reload(entry.entry_id)
        await hass.async_block_till_done()


async def async_trigger_update(hass: UniversalAssistant) -> None:
    """Advance time so the coordinator polls the device again."""
    # Advancing the clock also fires the periodic discovery this helper does not want
    with patch(
        "universalassistant.components.lifx.discovery.async_discover_devices",
        AsyncMock(return_value={}),
    ):
        async_fire_time_changed(hass, dt_util.utcnow() + UPDATE_INTERVAL)
        await hass.async_block_till_done()


@contextmanager
def _patch_device(device: Device | None = None):
    """Patch the public connection boundary."""
    with patch(
        "universalassistant.components.lifx.Device.connect",
        AsyncMock(return_value=device or create_mock_light()),
    ):
        yield


@contextmanager
def _patch_discovery(device: Device | None = None):
    """Patch the public broadcast discovery boundary."""
    discovered = device or create_mock_light()

    async def mock_discover_devices(**kwargs: Any):
        """Yield deterministic metadata-only discovery results."""
        yield DiscoveredDevice(serial=discovered.serial, ip=discovered.ip)

    with patch(
        "universalassistant.components.lifx.discovery.discover_devices",
        mock_discover_devices,
    ):
        yield


@contextmanager
def _patch_config_flow_try_connect(device: Device | None = None):
    """Patch public config-flow connection functions."""
    flow_device = device or create_mock_light()
    with (
        patch(
            "universalassistant.components.lifx.config_flow.Device.connect",
            AsyncMock(return_value=flow_device),
        ),
        patch(
            "universalassistant.components.lifx.config_flow.find_by_ip",
            AsyncMock(return_value=flow_device),
        ),
        patch(
            "universalassistant.components.lifx.config_flow.find_by_serial",
            AsyncMock(return_value=flow_device),
        ),
    ):
        yield
