"""The test for the sensibo sensor."""

from unittest.mock import Mock

from pytest_universalassistant.common import MockConfigEntry
from yalesmartalarmclient import YaleSmartAlarmData

from universalassistant.core import UniversalAssistant


async def test_coordinator_setup_and_update_errors(
    hass: UniversalAssistant,
    load_config_entry: tuple[MockConfigEntry, Mock],
    get_data: YaleSmartAlarmData,
) -> None:
    """Test the Yale Smart Living coordinator with errors."""

    state = hass.states.get("sensor.smoke_alarm_temperature")
    assert state.state == "21"
