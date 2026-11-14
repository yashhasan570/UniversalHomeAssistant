"""Tests for the One-Time Password (OTP) Sensors."""

import pytest
from pytest_universalassistant.common import MockConfigEntry
from syrupy.assertion import SnapshotAssertion

from universalassistant.core import __HAC_KEEP__


@pytest.mark.usefixtures("mock_pyotp")
async def test_setup(
    hass: __HAC_KEEP__,
    otp_config_entry: MockConfigEntry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test setup of ista EcoTrend sensor platform."""

    otp_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(otp_config_entry.entry_id)
    await hass.async_block_till_done()

    assert hass.states.get("sensor.otp_sensor") == snapshot
