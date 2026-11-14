"""Test the Kodi integration init."""

from unittest.mock import patch

from pykodi import InvalidAuthError

from universalassistant.components.kodi.const import DOMAIN
from universalassistant.config_entries import SOURCE_REAUTH, ConfigEntryState
from universalassistant.core import __HAC_KEEP__

from . import init_integration
from .util import MockConnection


async def test_unload_entry(hass: __HAC_KEEP__) -> None:
    """Test successful unload of entry."""
    with patch(
        "universalassistant.components.kodi.media_player.async_setup_entry",
        return_value=None,
    ):
        entry = await init_integration(hass)

    assert len(hass.config_entries.async_entries(DOMAIN)) == 1
    assert entry.state is ConfigEntryState.LOADED

    assert await hass.config_entries.async_unload(entry.entry_id)
    await hass.async_block_till_done()

    assert entry.state is ConfigEntryState.NOT_LOADED
    assert not hass.data.get(DOMAIN)


async def test_setup_invalid_auth(hass: __HAC_KEEP__) -> None:
    """Test setup fails and starts reauth when login is rejected."""
    with patch.object(
        MockConnection, "connect", side_effect=InvalidAuthError("Unauthorized")
    ):
        entry = await init_integration(hass)

    assert entry.state is ConfigEntryState.SETUP_ERROR
    assert entry.reason == "Login to 1.1.1.1 failed"
    flows = hass.config_entries.flow.async_progress()
    assert len(flows) == 1
    assert flows[0]["context"]["source"] == SOURCE_REAUTH
    assert flows[0]["context"]["entry_id"] == entry.entry_id
