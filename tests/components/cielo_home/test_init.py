"""Common tests for the Cielo Home."""

from unittest.mock import MagicMock

from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.cielo_home.const import DOMAIN
from universalassistant.config_entries import ConfigEntryState
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import entity_registry as er


async def test_async_setup_and_unload_entry(
    hass: __HAC_KEEP__,
    entity_registry: er.EntityRegistry,
    mock_cielo_client: MagicMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test setting up and unloading the integration."""
    mock_config_entry.add_to_hass(hass)

    assert await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    assert mock_config_entry.state is ConfigEntryState.LOADED
    assert mock_config_entry.runtime_data is not None

    entities = [
        e
        for e in entity_registry.entities.values()
        if e.platform == DOMAIN and e.domain == "climate"
    ]
    assert len(entities) == 1

    # Unload
    assert await hass.config_entries.async_unload(mock_config_entry.entry_id)
    await hass.async_block_till_done()
    assert mock_config_entry.state is ConfigEntryState.NOT_LOADED
