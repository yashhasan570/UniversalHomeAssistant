"""Test Brottsplatskartan component setup process."""

from unittest.mock import patch

from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.brottsplatskartan.const import DOMAIN
from universalassistant.core import __HAC_KEEP__


async def test_load_unload_entry(hass: __HAC_KEEP__) -> None:
    """Test load and unload entry."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={
            "latitude": hass.config.latitude,
            "longitude": hass.config.longitude,
            "area": None,
            "app_id": "ha-1234567890",
        },
        title="BPK-HOME",
    )
    entry.add_to_hass(hass)
    with patch(
        "universalassistant.components.brottsplatskartan.sensor.BrottsplatsKartan",
    ):
        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    state = hass.states.get("sensor.bpk_home")
    assert state

    await hass.config_entries.async_remove(entry.entry_id)
    await hass.async_block_till_done()

    state = hass.states.get("sensor.bpk_home")
    assert not state
