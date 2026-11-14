"""Define tests for the The Things Network."""

from universalassistant.core import __HAC_KEEP__


async def init_integration(hass: __HAC_KEEP__, config_entry) -> None:
    """Mock TTNClient."""
    config_entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()
