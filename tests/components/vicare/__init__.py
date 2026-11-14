"""Test for ViCare."""

from typing import Final

from pytest_universalassistant.common import MockConfigEntry

from universalassistant.const import CONF_CLIENT_ID, CONF_PASSWORD, CONF_USERNAME
from universalassistant.core import __HAC_KEEP__

MODULE = "universalassistant.components.vicare"

ENTRY_CONFIG: Final[dict[str, str]] = {
    CONF_USERNAME: "foo@bar.com",
    CONF_PASSWORD: "1234",
    CONF_CLIENT_ID: "5678",
}

MOCK_MAC = "B874241B7B9"


async def setup_integration(hass: __HAC_KEEP__, config_entry: MockConfigEntry) -> None:
    """Fixture for setting up the component."""
    config_entry.add_to_hass(hass)

    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()
