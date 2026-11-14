"""Test for diagnostics platform of the LED Infrared integration."""

import pytest
from pytest_universalassistant.common import MockConfigEntry
from pytest_universalassistant.components.diagnostics import get_diagnostics_for_config_entry
from pytest_universalassistant.typing import ClientSessionGenerator
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.led_infrared.const import LEDIrDeviceType
from universalassistant.config_entries import ConfigEntryState
from universalassistant.core import __HAC_KEEP__


@pytest.mark.parametrize(
    "config_entry",
    [
        LEDIrDeviceType.GENERIC_10_KEY,
        LEDIrDeviceType.GENERIC_10_KEY_B708,
        LEDIrDeviceType.GENERIC_13_KEY,
        LEDIrDeviceType.GENERIC_21_KEY,
        LEDIrDeviceType.GENERIC_24_KEY,
        LEDIrDeviceType.GENERIC_40_KEY,
        LEDIrDeviceType.GENERIC_44_KEY,
    ],
    indirect=True,
)
async def test_diagnostics(
    hass: __HAC_KEEP__,
    hass_client: ClientSessionGenerator,
    config_entry: MockConfigEntry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test diagnostics."""

    config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    assert config_entry.state is ConfigEntryState.LOADED

    assert (
        await get_diagnostics_for_config_entry(hass, hass_client, config_entry)
        == snapshot
    )
