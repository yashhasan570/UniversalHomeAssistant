"""Test util for the homekit integration."""

from unittest.mock import patch

from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.homekit.const import DOMAIN
from universalassistant.const import CONF_NAME, CONF_PORT
from universalassistant.core import UniversalAssistant

PATH_HOMEKIT = "universalassistant.components.homekit"


async def async_init_integration(hass: UniversalAssistant) -> MockConfigEntry:
    """Set up the homekit integration in Universal Universal Home Assistant."""

    with patch(f"{PATH_HOMEKIT}.HomeKit.async_start"):
        entry = MockConfigEntry(
            domain=DOMAIN, data={CONF_NAME: "mock_name", CONF_PORT: 12345}
        )
        entry.add_to_hass(hass)
        assert await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()
        return entry


async def async_init_entry(hass: UniversalAssistant, entry: MockConfigEntry):
    """Set up the homekit integration in Universal Universal Home Assistant."""

    with patch(f"{PATH_HOMEKIT}.HomeKit.async_start"):
        entry.add_to_hass(hass)
        assert await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()
        return entry
