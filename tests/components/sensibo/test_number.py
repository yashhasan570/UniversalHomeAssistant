"""The test for the sensibo number platform."""

from datetime import timedelta
from unittest.mock import MagicMock

from freezegun.api import FrozenDateTimeFactory
import pytest
from pytest_universalassistant.common import async_fire_time_changed, snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.number import (
    DOMAIN as NUMBER_DOMAIN,
    NumberService,
    NumberServiceArgument,
)
from universalassistant.config_entries import ConfigEntry
from universalassistant.const import Platform, TargetKey
from universalassistant.core import UniversalAssistant
from universalassistant.exceptions import UniversalAssistantError
from universalassistant.helpers import entity_registry as er


@pytest.mark.parametrize(
    "load_platforms",
    [[Platform.NUMBER]],
)
@pytest.mark.usefixtures("entity_registry_enabled_by_default")
async def test_number(
    hass: UniversalAssistant,
    load_int: ConfigEntry,
    mock_client: MagicMock,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
    freezer: FrozenDateTimeFactory,
) -> None:
    """Test the Sensibo number."""

    await snapshot_platform(hass, entity_registry, snapshot, load_int.entry_id)

    mock_client.async_get_devices_data.return_value.parsed[
        "ABC999111"
    ].calibration_temp = 0.2

    freezer.tick(timedelta(minutes=5))
    async_fire_time_changed(hass)
    await hass.async_block_till_done()

    state = hass.states.get("number.hallway_hallway_temperature_calibration")
    assert state.state == "0.2"


@pytest.mark.usefixtures("entity_registry_enabled_by_default")
async def test_number_set_value(
    hass: UniversalAssistant, load_int: ConfigEntry, mock_client: MagicMock
) -> None:
    """Test the Sensibo number service."""

    state = hass.states.get("number.hallway_hallway_temperature_calibration")
    assert state.state == "0.1"

    mock_client.async_set_calibration.return_value = {"status": "failure"}

    with pytest.raises(UniversalAssistantError):
        await hass.services.async_call(
            NUMBER_DOMAIN,
            NumberService.SET_VALUE,
            {
                TargetKey.ENTITY_ID: state.entity_id,
                NumberServiceArgument.VALUE: "0.2",
            },
            blocking=True,
        )

    state = hass.states.get("number.hallway_hallway_temperature_calibration")
    assert state.state == "0.1"

    mock_client.async_set_calibration.return_value = {"status": "success"}

    await hass.services.async_call(
        NUMBER_DOMAIN,
        NumberService.SET_VALUE,
        {
            TargetKey.ENTITY_ID: state.entity_id,
            NumberServiceArgument.VALUE: "0.2",
        },
        blocking=True,
    )

    state = hass.states.get("number.hallway_hallway_temperature_calibration")
    assert state.state == "0.2"
