"""Tests for the Roon integration setup."""

from unittest.mock import patch

from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.roon.const import CONF_ROON_NAME, DOMAIN
from universalassistant.config_entries import ConfigEntryState
from universalassistant.const import CONF_HOST
from universalassistant.core import __HAC_KEEP__


async def test_setup_failed(hass: __HAC_KEEP__) -> None:
    """Test setup fails when the Roon server can't be set up."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={CONF_HOST: "1.1.1.1", CONF_ROON_NAME: "Roon Core"},
    )
    entry.add_to_hass(hass)

    with patch(
        "universalassistant.components.roon.RoonServer.async_setup", return_value=False
    ):
        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    assert entry.state is ConfigEntryState.SETUP_ERROR
    assert entry.reason == "Failed to set up the Roon server Roon Core"
