"""Test evil genius labs init."""

import pytest

from universalassistant.components.evil_genius_labs import PLATFORMS
from universalassistant.config_entries import ConfigEntryState
from universalassistant.core import __HAC_KEEP__


@pytest.mark.parametrize("platforms", [PLATFORMS])
async def test_setup_unload_entry(
    hass: __HAC_KEEP__, setup_evil_genius_labs, config_entry
) -> None:
    """Test setting up and unloading a config entry."""
    assert len(hass.states.async_entity_ids()) == 1
    assert await hass.config_entries.async_unload(config_entry.entry_id)
    assert config_entry.state is ConfigEntryState.NOT_LOADED
