"""Tests for wiz integration."""

import datetime as dt
from unittest.mock import AsyncMock, patch

from pytest_universalassistant.common import MockConfigEntry, async_fire_time_changed

from universalassistant.components.wiz.const import DOMAIN
from universalassistant.config_entries import ConfigEntryState
from universalassistant.const import ATTR_FRIENDLY_NAME, CONF_HOST, EVENT_HOMEASSISTANT_STOP
from universalassistant.core import UniversalAssistant
from universalassistant.setup import async_setup_component
from universalassistant.util.dt import utcnow

from . import (
    FAKE_IP,
    FAKE_MAC,
    FAKE_SOCKET,
    _mocked_wizlight,
    _patch_discovery,
    _patch_wizlight,
    async_setup_integration,
)


async def test_setup_retry(hass: UniversalAssistant) -> None:
    """Test setup is retried on error."""
    bulb = _mocked_wizlight(None, None, FAKE_SOCKET)
    bulb.getMac = AsyncMock(side_effect=OSError)
    _, entry = await async_setup_integration(hass, wizlight=bulb)
    assert entry.state is ConfigEntryState.SETUP_RETRY
    bulb.getMac = AsyncMock(return_value=FAKE_MAC)

    with _patch_discovery(), _patch_wizlight(device=bulb):
        await hass.async_block_till_done(wait_background_tasks=True)
        async_fire_time_changed(hass, utcnow() + dt.timedelta(minutes=15))
        await hass.async_block_till_done(wait_background_tasks=True)
    assert entry.state is ConfigEntryState.LOADED


async def test_cleanup_on_shutdown(hass: UniversalAssistant) -> None:
    """Test the socket is cleaned up on shutdown."""
    bulb = _mocked_wizlight(None, None, FAKE_SOCKET)
    _, entry = await async_setup_integration(hass, wizlight=bulb)
    assert entry.state is ConfigEntryState.LOADED
    hass.bus.async_fire(EVENT_HOMEASSISTANT_STOP)
    await hass.async_block_till_done(wait_background_tasks=True)
    bulb.async_close.assert_called_once()


async def test_cleanup_on_failed_first_update(hass: UniversalAssistant) -> None:
    """Test the socket is cleaned up on failed first update."""
    bulb = _mocked_wizlight(None, None, FAKE_SOCKET)
    bulb.updateState = AsyncMock(side_effect=OSError)
    entry = MockConfigEntry(
        domain=DOMAIN,
        unique_id=FAKE_MAC,
        data={CONF_HOST: FAKE_IP},
    )
    entry.add_to_hass(hass)
    with (
        patch("universalassistant.components.wiz.discovery.find_wizlights", return_value=[]),
        _patch_wizlight(device=bulb),
    ):
        await async_setup_component(hass, DOMAIN, {DOMAIN: {}})
        await hass.async_block_till_done(wait_background_tasks=True)
    assert entry.state is ConfigEntryState.SETUP_RETRY
    bulb.async_close.assert_called_once()


async def test_wrong_device_now_has_our_ip(hass: UniversalAssistant) -> None:
    """Test setup is retried when the wrong device is found."""
    bulb = _mocked_wizlight(None, None, FAKE_SOCKET)
    bulb.mac = "dddddddddddd"
    _, entry = await async_setup_integration(hass, wizlight=bulb)
    assert entry.state is ConfigEntryState.SETUP_RETRY
    # Each retry creates a new bulb, so every attempt must close its socket
    assert bulb.async_close.call_count == bulb.getMac.call_count

    with _patch_wizlight():
        await hass.async_block_till_done(wait_background_tasks=True)


async def test_reload_on_title_change(hass: UniversalAssistant) -> None:
    """Test the integration gets reloaded when the title is updated."""
    bulb = _mocked_wizlight(None, None, FAKE_SOCKET)
    _, entry = await async_setup_integration(hass, wizlight=bulb)
    assert entry.state is ConfigEntryState.LOADED
    await hass.async_block_till_done(wait_background_tasks=True)

    with _patch_discovery(), _patch_wizlight(device=bulb):
        hass.config_entries.async_update_entry(entry, title="Shop Switch")
        assert entry.title == "Shop Switch"
        await hass.async_block_till_done(wait_background_tasks=True)

    assert (
        hass.states.get("switch.mock_title").attributes[ATTR_FRIENDLY_NAME]
        == "Shop Switch"
    )
