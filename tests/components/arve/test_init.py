"""Tests for the Arve component."""

from unittest.mock import patch

from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.arve.const import DOMAIN
from universalassistant.const import CONF_ACCESS_TOKEN, CONF_CLIENT_SECRET
from universalassistant.core import __HAC_KEEP__


async def test_migrate_entry_minor_version_1_2(hass: __HAC_KEEP__) -> None:
    """Test migrating a 1.1 config entry to 1.2."""
    with patch("universalassistant.components.arve.async_setup_entry", return_value=None):
        entry = MockConfigEntry(
            domain=DOMAIN,
            data={CONF_ACCESS_TOKEN: "mock", CONF_CLIENT_SECRET: "mock"},
            version=1,
            minor_version=1,
            unique_id=12345,
        )
        entry.add_to_hass(hass)
        assert await hass.config_entries.async_setup(entry.entry_id)
        assert entry.version == 1
        assert entry.minor_version == 2
        assert entry.unique_id == "12345"
