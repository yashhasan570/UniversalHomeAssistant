"""Tests for the Aseko Pool Live integration."""

from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.aseko_pool_live.const import DOMAIN
from universalassistant.config_entries import ConfigEntryState
from universalassistant.const import CONF_EMAIL, CONF_PASSWORD
from universalassistant.core import UniversalAssistant


async def test_migrate_entry_unknown_version(hass: UniversalAssistant) -> None:
    """Test migration from an unknown version raises an error."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={CONF_EMAIL: "aseko@example.com", CONF_PASSWORD: "passw0rd"},
        version=2,
        minor_version=2,
    )
    entry.add_to_hass(hass)

    await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    assert entry.state is ConfigEntryState.MIGRATION_ERROR
    assert entry.reason == "Cannot migrate configuration entry from unknown version 2"
