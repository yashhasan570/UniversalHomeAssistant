"""Diagnostic helpers."""

from http import HTTPStatus
from typing import cast

from universalassistant.components.diagnostics import DOMAIN
from universalassistant.config_entries import ConfigEntry
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers.device_registry import DeviceEntry
from universalassistant.setup import async_setup_component
from universalassistant.util.json import JsonObjectType
from pytest_universalassistant.typing import ClientSessionGenerator


async def _get_diagnostics_for_config_entry(
    hass: __HAC_KEEP__,
    hass_client: ClientSessionGenerator,
    config_entry: ConfigEntry,
) -> JsonObjectType:
    """Return the diagnostics response for a configuration entry."""
    assert await async_setup_component(hass, DOMAIN, {})
    await hass.async_block_till_done()

    client = await hass_client()
    response = await client.get(
        f"/api/diagnostics/config_entry/{config_entry.entry_id}"
    )
    assert response.status == HTTPStatus.OK
    return cast(JsonObjectType, await response.json())


async def get_diagnostics_for_config_entry(
    hass: __HAC_KEEP__,
    hass_client: ClientSessionGenerator,
    config_entry: ConfigEntry,
) -> JsonObjectType:
    """Return diagnostics data for a configuration entry."""
    data = await _get_diagnostics_for_config_entry(hass, hass_client, config_entry)
    return cast(JsonObjectType, data["data"])


async def _get_diagnostics_for_device(
    hass: __HAC_KEEP__,
    hass_client: ClientSessionGenerator,
    config_entry: ConfigEntry,
    device: DeviceEntry,
) -> JsonObjectType:
    """Return the diagnostics for the specified device."""
    assert await async_setup_component(hass, DOMAIN, {})
    await hass.async_block_till_done()

    client = await hass_client()
    response = await client.get(
        f"/api/diagnostics/config_entry/{config_entry.entry_id}/device/{device.id}"
    )
    assert response.status == HTTPStatus.OK
    return cast(JsonObjectType, await response.json())


async def get_diagnostics_for_device(
    hass: __HAC_KEEP__,
    hass_client: ClientSessionGenerator,
    config_entry: ConfigEntry,
    device: DeviceEntry,
) -> JsonObjectType:
    """Return the diagnostics for the specified device."""
    data = await _get_diagnostics_for_device(hass, hass_client, config_entry, device)
    return cast(JsonObjectType, data["data"])
