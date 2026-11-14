"""Test the LED BLE integration init."""

from unittest.mock import patch

import pytest
from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.led_ble.const import DOMAIN
from universalassistant.config_entries import ConfigEntryState
from universalassistant.const import CONF_ADDRESS
from universalassistant.core import UniversalAssistant

from . import LED_BLE_DISCOVERY_INFO


async def test_setup_retries_when_device_not_found(
    hass: UniversalAssistant,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test setup is retried with a diagnostic reason when the device is missing."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        unique_id=LED_BLE_DISCOVERY_INFO.address,
        data={CONF_ADDRESS: LED_BLE_DISCOVERY_INFO.address},
    )
    entry.add_to_hass(hass)

    with patch(
        "universalassistant.components.led_ble.bluetooth."
        "async_address_reachability_diagnostics",
        return_value="mock reachability reason",
    ):
        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    assert entry.state is ConfigEntryState.SETUP_RETRY
    assert (
        "Could not find LED BLE device with address "
        f"{LED_BLE_DISCOVERY_INFO.address}: mock reachability reason" in caplog.text
    )
