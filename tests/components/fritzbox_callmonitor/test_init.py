"""Tests for the fritzbox_callmonitor integration setup."""

from unittest.mock import patch

from fritzconnection.core.exceptions import FritzSecurityError
from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.fritzbox_callmonitor.const import CONF_PHONEBOOK, DOMAIN
from universalassistant.config_entries import ConfigEntryState
from universalassistant.const import CONF_HOST, CONF_PASSWORD, CONF_PORT, CONF_USERNAME
from universalassistant.core import UniversalAssistant


async def test_setup_insufficient_permissions(hass: UniversalAssistant) -> None:
    """Test setup fails when the user lacks permissions."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={
            CONF_HOST: "fake_host",
            CONF_PORT: 1234,
            CONF_USERNAME: "fake_username",
            CONF_PASSWORD: "fake_password",
            CONF_PHONEBOOK: 0,
        },
    )
    entry.add_to_hass(hass)

    with patch(
        "universalassistant.components.fritzbox_callmonitor.FritzBoxPhonebook.init_phonebook",
        side_effect=FritzSecurityError,
    ):
        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    assert entry.state is ConfigEntryState.SETUP_ERROR
    assert entry.reason == (
        "User has insufficient permissions to access FRITZ!Box settings and its"
        " phonebooks"
    )
