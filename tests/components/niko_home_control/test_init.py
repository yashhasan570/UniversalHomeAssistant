"""Test init."""

import pytest
from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.light import DOMAIN as LIGHT_DOMAIN
from universalassistant.components.niko_home_control.const import DOMAIN
from universalassistant.const import CONF_HOST
from universalassistant.core import UniversalAssistant
from universalassistant.helpers import entity_registry as er


@pytest.mark.usefixtures("mock_setup_entry")
async def test_migrate_entry(
    hass: UniversalAssistant, entity_registry: er.EntityRegistry
) -> None:
    """Validate that the unique_id is migrated to the new unique_id."""
    config_entry = MockConfigEntry(
        domain=DOMAIN,
        minor_version=1,
        data={CONF_HOST: "192.168.0.123"},
    )
    config_entry.add_to_hass(hass)
    entity_entry = entity_registry.async_get_or_create(
        LIGHT_DOMAIN, DOMAIN, "light-1", config_entry=config_entry
    )
    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    entity_entry = entity_registry.async_get(entity_entry.entity_id)

    assert config_entry.minor_version == 2
    assert (
        entity_registry.async_get(entity_entry.entity_id).unique_id
        == f"{config_entry.entry_id}-1"
    )
