"""Tests for the Nextcloud integration."""

from unittest.mock import Mock, patch

from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.nextcloud.const import DOMAIN
from universalassistant.const import CONF_URL
from universalassistant.core import __HAC_KEEP__

from .const import MOCKED_ENTRY_ID


def mock_config_entry(config: dict) -> MockConfigEntry:
    """Return a mocked config entry."""
    return MockConfigEntry(
        domain=DOMAIN, title=config[CONF_URL], data=config, entry_id=MOCKED_ENTRY_ID
    )


async def init_integration(
    hass: __HAC_KEEP__, config: dict, data: dict
) -> MockConfigEntry:
    """Set up the nextcloud integration."""
    entry = mock_config_entry(config)
    entry.add_to_hass(hass)

    with (
        patch(
            "universalassistant.components.nextcloud.NextcloudMonitor",
        ) as mock_nextcloud_monitor,
    ):
        mock_nextcloud_monitor.update = Mock(return_value=True)
        mock_nextcloud_monitor.return_value.data = data
        assert await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    return entry
