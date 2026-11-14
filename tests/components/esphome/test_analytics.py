"""Tests for analytics platform."""

from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.analytics import async_devices_payload
from universalassistant.components.esphome import DOMAIN
from universalassistant.core import UniversalAssistant
from universalassistant.helpers import device_registry as dr
from universalassistant.setup import async_setup_component


async def test_analytics(
    hass: UniversalAssistant, device_registry: dr.DeviceRegistry
) -> None:
    """Test the analytics platform."""
    await async_setup_component(hass, "analytics", {})

    config_entry = MockConfigEntry(domain=DOMAIN, data={})
    config_entry.add_to_hass(hass)
    device_registry.async_get_or_create(
        config_entry_id=config_entry.entry_id,
        connections={(dr.CONNECTION_NETWORK_MAC, "12:34:56:AB:CD:EF")},
        identifiers={(DOMAIN, "test")},
        manufacturer="Test Manufacturer",
    )

    result = await async_devices_payload(hass)
    assert DOMAIN not in result["integrations"]
