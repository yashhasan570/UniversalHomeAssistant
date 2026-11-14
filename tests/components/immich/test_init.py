"""Test the Immich integration setup."""

from dataclasses import replace
from datetime import timedelta
from unittest.mock import Mock

from freezegun.api import FrozenDateTimeFactory
import pytest
from pytest_universalassistant.common import MockConfigEntry, async_fire_time_changed

from universalassistant.config_entries import ConfigEntryState
from universalassistant.core import __HAC_KEEP__

from . import setup_integration


@pytest.mark.parametrize(
    ("new_version", "setup_calls"),
    [
        pytest.param("v1.134.0", 1, id="unchanged"),
        pytest.param("v3.1.0", 2, id="changed"),
    ],
)
async def test_reload_on_server_version_change(
    hass: __HAC_KEEP__,
    freezer: FrozenDateTimeFactory,
    mock_immich: Mock,
    mock_config_entry: MockConfigEntry,
    new_version: str,
    setup_calls: int,
) -> None:
    """Test the integration reloads only when the server version changes."""
    await setup_integration(hass, mock_config_entry)
    assert mock_immich.async_setup.call_count == 1

    server_about = mock_immich.server.async_get_about_info.return_value
    mock_immich.server.async_get_about_info.return_value = replace(
        server_about, version=new_version
    )

    freezer.tick(timedelta(seconds=60))
    async_fire_time_changed(hass)
    await hass.async_block_till_done()

    assert mock_config_entry.state is ConfigEntryState.LOADED
    assert mock_immich.async_setup.call_count == setup_calls
