"""Tests for the Webmin integration."""

from universalassistant.components.webmin.const import DOMAIN
from universalassistant.config_entries import ConfigEntryState
from universalassistant.core import UniversalAssistant

from .conftest import async_init_integration


async def test_unload_entry(hass: UniversalAssistant) -> None:
    """Test successful unload of entry."""

    entry = await async_init_integration(hass)

    assert entry.state is ConfigEntryState.LOADED

    assert await hass.config_entries.async_unload(entry.entry_id)
    await hass.async_block_till_done()

    assert entry.state is ConfigEntryState.NOT_LOADED
    assert not hass.data.get(DOMAIN)


async def test_entry_without_mac_address(hass: UniversalAssistant) -> None:
    """Test an entry without MAC address."""

    entry = await async_init_integration(hass, False)

    assert entry.runtime_data.unique_id == entry.entry_id
