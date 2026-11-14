"""Tests for the UpCloud integration setup."""

from unittest.mock import patch

from pytest_universalassistant.common import MockConfigEntry
from upcloud_api import UpCloudAPIError

from universalassistant.components.upcloud.const import DOMAIN
from universalassistant.config_entries import ConfigEntryState
from universalassistant.const import CONF_PASSWORD, CONF_USERNAME
from universalassistant.core import __HAC_KEEP__


async def test_setup_authentication_failed(hass: __HAC_KEEP__) -> None:
    """Test setup fails when authentication fails."""
    entry = MockConfigEntry(
        domain=DOMAIN, data={CONF_USERNAME: "user", CONF_PASSWORD: "pass"}
    )
    entry.add_to_hass(hass)

    with patch(
        "upcloud_api.CloudManager.authenticate",
        side_effect=UpCloudAPIError(
            error_code="AUTHENTICATION_FAILED",
            error_message="Authentication failed using the given username and password.",
        ),
    ):
        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    assert entry.state is ConfigEntryState.SETUP_ERROR
    assert entry.reason == "Authentication with UpCloud failed"
