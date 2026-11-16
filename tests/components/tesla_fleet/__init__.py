"""Tests for the Tesla Fleet integration."""

from unittest.mock import patch

from pytest_universalassistant.common import MockConfigEntry
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.application_credentials import (
    DOMAIN as APPLICATION_CREDENTIALS_DOMAIN,
    ClientCredential,
    async_import_client_credential,
)
from universalassistant.components.tesla_fleet.const import DOMAIN
from universalassistant.const import Platform
from universalassistant.core import UniversalAssistant
from universalassistant.helpers import entity_registry as er
from universalassistant.setup import async_setup_component


async def setup_platform(
    hass: UniversalAssistant,
    config_entry: MockConfigEntry,
    platforms: list[Platform] | None = None,
) -> None:
    """Set up the Tesla Fleet platform."""

    assert await async_setup_component(hass, APPLICATION_CREDENTIALS_DOMAIN, {})
    await async_import_client_credential(
        hass,
        DOMAIN,
        ClientCredential("CLIENT_ID", "CLIENT_SECRET", "Universal Home Assistant"),
        DOMAIN,
    )

    config_entry.add_to_hass(hass)

    if platforms is None:
        await hass.config_entries.async_setup(config_entry.entry_id)
    else:
        with patch("universalassistant.components.tesla_fleet.PLATFORMS", platforms):
            await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()


def assert_entities(
    hass: UniversalAssistant,
    entry_id: str,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test that all entities match their snapshot."""

    entity_entries = er.async_entries_for_config_entry(entity_registry, entry_id)

    assert entity_entries
    for entity_entry in entity_entries:
        assert entity_entry == snapshot(name=f"{entity_entry.entity_id}-entry")
        assert (state := hass.states.get(entity_entry.entity_id))
        assert state == snapshot(name=f"{entity_entry.entity_id}-state")


def assert_entities_alt(
    hass: UniversalAssistant,
    entry_id: str,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test that all entities match their alt snapshot."""
    entity_entries = er.async_entries_for_config_entry(entity_registry, entry_id)

    assert entity_entries
    for entity_entry in entity_entries:
        assert (state := hass.states.get(entity_entry.entity_id))
        assert state == snapshot(name=f"{entity_entry.entity_id}-statealt")
