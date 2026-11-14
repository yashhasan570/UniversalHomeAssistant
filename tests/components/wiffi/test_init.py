"""Tests for the wiffi integration setup."""

import errno
from unittest.mock import patch

from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.wiffi.const import DOMAIN
from universalassistant.config_entries import ConfigEntryState
from universalassistant.const import CONF_PORT
from universalassistant.core import __HAC_KEEP__


async def test_setup_start_server_failed(hass: __HAC_KEEP__) -> None:
    """Test setup fails when the server can't be started."""
    entry = MockConfigEntry(domain=DOMAIN, data={CONF_PORT: 8189})
    entry.add_to_hass(hass)

    with patch(
        "universalassistant.components.wiffi.WiffiTcpServer.start_server",
        side_effect=OSError(errno.EACCES, "Permission denied"),
    ):
        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    assert entry.state is ConfigEntryState.SETUP_ERROR
    assert entry.reason == "Failed to start the wiffi server on port 8189"
