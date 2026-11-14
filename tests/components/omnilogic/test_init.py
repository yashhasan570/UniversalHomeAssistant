"""Tests for the Omnilogic integration setup."""

from unittest.mock import patch

from omnilogic import LoginException
from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.omnilogic.const import DOMAIN
from universalassistant.config_entries import ConfigEntryState
from universalassistant.const import CONF_PASSWORD, CONF_USERNAME
from universalassistant.core import __HAC_KEEP__


async def test_setup_login_failed(hass: __HAC_KEEP__) -> None:
    """Test setup fails when logging in fails."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={CONF_USERNAME: "test-username", CONF_PASSWORD: "test-password"},
    )
    entry.add_to_hass(hass)

    with patch(
        "universalassistant.components.omnilogic.OmniLogic.connect",
        side_effect=LoginException("Invalid credentials"),
    ):
        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    assert entry.state is ConfigEntryState.SETUP_ERROR
    assert entry.reason == "Login to OmniLogic failed"
