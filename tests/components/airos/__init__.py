"""Tests for the Ubiquity airOS integration."""

from airos.airos6 import AirOS6Data
from airos.airos8 import AirOS8Data
from pytest_universalassistant.common import MockConfigEntry, patch

from universalassistant.const import Platform
from universalassistant.core import UniversalAssistant

AirOSData = AirOS8Data | AirOS6Data


async def setup_integration(
    hass: UniversalAssistant,
    mock_config_entry: MockConfigEntry,
    platforms: list[Platform] | None = None,
) -> None:
    """Fixture for setting up the component."""
    mock_config_entry.add_to_hass(hass)

    with patch("universalassistant.components.airos._PLATFORMS", platforms):
        await hass.config_entries.async_setup(mock_config_entry.entry_id)
        await hass.async_block_till_done()
