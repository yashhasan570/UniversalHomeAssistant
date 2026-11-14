"""Tests for the devolo Home Control integration."""

from unittest.mock import MagicMock, patch

from devolo_home_control_api.exceptions.gateway import GatewayOfflineError
from pytest_universalassistant.typing import WebSocketGenerator

from universalassistant.components.binary_sensor import DOMAIN as BINARY_SENSOR_DOMAIN
from universalassistant.components.devolo_home_control.const import DOMAIN
from universalassistant.config_entries import ConfigEntryState
from universalassistant.const import EVENT_HOMEASSISTANT_STOP
from universalassistant.core import UniversalAssistant
from universalassistant.helpers import device_registry as dr
from universalassistant.setup import async_setup_component

from . import configure_integration
from .mocks import HomeControlMock, HomeControlMockBinarySensor


async def test_setup_entry(hass: UniversalAssistant) -> None:
    """Test setup entry."""
    entry = configure_integration(hass)
    with patch("universalassistant.components.devolo_home_control.HomeControl"):
        await hass.config_entries.async_setup(entry.entry_id)
        assert entry.state is ConfigEntryState.LOADED


async def test_setup_entry_credentials_invalid(
    hass: UniversalAssistant, mydevolo: MagicMock
) -> None:
    """Test setup entry fails if credentials are invalid."""
    mydevolo.credentials_valid.return_value = False
    entry = configure_integration(hass)
    await hass.config_entries.async_setup(entry.entry_id)
    assert entry.state is ConfigEntryState.SETUP_ERROR


async def test_setup_entry_maintenance(
    hass: UniversalAssistant, mydevolo: MagicMock
) -> None:
    """Test setup entry fails if mydevolo is in maintenance mode."""
    mydevolo.maintenance.return_value = True
    entry = configure_integration(hass)
    await hass.config_entries.async_setup(entry.entry_id)
    assert entry.state is ConfigEntryState.SETUP_RETRY


async def test_setup_gateway_offline(hass: UniversalAssistant) -> None:
    """Test setup entry with one gateway online and one gateway offline."""
    entry = configure_integration(hass)
    test_gateway = HomeControlMock()
    with patch(
        "universalassistant.components.devolo_home_control.HomeControl",
        side_effect=[test_gateway, GatewayOfflineError],
    ):
        await hass.config_entries.async_setup(entry.entry_id)
        assert entry.state is ConfigEntryState.LOADED


async def test_setup_all_gateways_offline(hass: UniversalAssistant) -> None:
    """Test setup entry fails on all gateways offline."""
    entry = configure_integration(hass)
    with patch(
        "universalassistant.components.devolo_home_control.HomeControl",
        side_effect=GatewayOfflineError,
    ):
        await hass.config_entries.async_setup(entry.entry_id)
        assert entry.state is ConfigEntryState.SETUP_RETRY


async def test_unload_entry(hass: UniversalAssistant) -> None:
    """Test unload entry."""
    entry = configure_integration(hass)
    with patch("universalassistant.components.devolo_home_control.HomeControl"):
        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()
        await hass.config_entries.async_unload(entry.entry_id)
        assert entry.state is ConfigEntryState.NOT_LOADED


async def test_universal_assistant_stop(hass: UniversalAssistant) -> None:
    """Test universal assistant stop."""
    entry = configure_integration(hass)
    test_gateway = HomeControlMock()
    test_gateway2 = HomeControlMock()
    with patch(
        "universalassistant.components.devolo_home_control.HomeControl",
        side_effect=[test_gateway, test_gateway2],
    ):
        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()
        hass.bus.async_fire(EVENT_HOMEASSISTANT_STOP)
        await hass.async_block_till_done()
        assert test_gateway.websocket_disconnect.called
        assert test_gateway2.websocket_disconnect.called


async def test_remove_device(
    hass: UniversalAssistant,
    hass_ws_client: WebSocketGenerator,
    device_registry: dr.DeviceRegistry,
) -> None:
    """Test removing a device."""
    assert await async_setup_component(hass, "config", {})
    entry = configure_integration(hass)
    test_gateway = HomeControlMockBinarySensor()
    with patch(
        "universalassistant.components.devolo_home_control.HomeControl",
        side_effect=[test_gateway, HomeControlMock()],
    ):
        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

        device_entry = device_registry.async_get_device_by_identifier(
            (DOMAIN, "Test"), entry.entry_id
        )
        assert device_entry

        client = await hass_ws_client(hass)
        response = await client.remove_device(device_entry.id)
        assert response["success"]
        assert (
            device_registry.async_get_device_by_identifier(
                (DOMAIN, "Test"), entry.entry_id
            )
            is None
        )
        assert hass.states.get(f"{BINARY_SENSOR_DOMAIN}.test") is None
