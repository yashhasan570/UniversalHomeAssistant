"""Test the Read Your Meter Pro integration setup."""

from unittest.mock import patch

from pyrympro import CannotConnectError, OperationError, UnauthorizedError
import pytest
from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.rympro.const import DOMAIN
from universalassistant.config_entries import ConfigEntryState
from universalassistant.const import CONF_EMAIL, CONF_PASSWORD, CONF_TOKEN, CONF_UNIQUE_ID
from universalassistant.core import UniversalAssistant

TEST_DATA = {
    CONF_EMAIL: "test-email",
    CONF_PASSWORD: "test-password",
    CONF_TOKEN: "test-token",
    CONF_UNIQUE_ID: "test-account-number",
}


@pytest.fixture
def config_entry(hass: UniversalAssistant) -> MockConfigEntry:
    """Create a mock config entry."""
    config_entry = MockConfigEntry(
        domain=DOMAIN,
        data=TEST_DATA,
        unique_id=TEST_DATA[CONF_UNIQUE_ID],
    )
    config_entry.add_to_hass(hass)
    return config_entry


@pytest.mark.parametrize("exception", [CannotConnectError, OperationError])
async def test_account_info_error_retries_setup(
    hass: UniversalAssistant,
    config_entry: MockConfigEntry,
    exception: type[Exception],
) -> None:
    """Test that a transient account_info error schedules a setup retry."""
    with patch(
        "universalassistant.components.rympro.RymPro.account_info",
        side_effect=exception,
    ):
        await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()

    assert config_entry.state is ConfigEntryState.SETUP_RETRY


async def test_relogin_cannot_connect_error_retries_setup(
    hass: UniversalAssistant, config_entry: MockConfigEntry
) -> None:
    """Test that a connection error while re-authenticating retries setup."""
    with (
        patch(
            "universalassistant.components.rympro.RymPro.account_info",
            side_effect=UnauthorizedError,
        ),
        patch(
            "universalassistant.components.rympro.RymPro.login",
            side_effect=CannotConnectError,
        ),
    ):
        await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()

    assert config_entry.state is ConfigEntryState.SETUP_RETRY
