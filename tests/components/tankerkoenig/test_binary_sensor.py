"""Tests for the Tankerkoening integration."""

import pytest
from pytest_universalassistant.common import MockConfigEntry
from syrupy.assertion import SnapshotAssertion

from universalassistant.const import STATE_ON
from universalassistant.core import UniversalAssistant


@pytest.mark.usefixtures("setup_integration")
async def test_binary_sensor(
    hass: UniversalAssistant,
    config_entry: MockConfigEntry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test the tankerkoenig binary sensors."""

    state = hass.states.get("binary_sensor.station_somewhere_street_1_status")
    assert state
    assert state.state == STATE_ON
    assert state.attributes == snapshot
