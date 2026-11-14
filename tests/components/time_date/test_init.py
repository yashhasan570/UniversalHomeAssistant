"""The tests for the Time & Date component."""

from universalassistant.core import __HAC_KEEP__

from . import load_int


async def test_setup_and_remove_config_entry(hass: __HAC_KEEP__) -> None:
    """Test setting up and removing a config entry."""
    entry = await load_int(hass)

    state = hass.states.get("sensor.time")
    assert state is not None

    assert await hass.config_entries.async_remove(entry.entry_id)
    await hass.async_block_till_done()

    assert hass.states.get("sensor.time") is None
