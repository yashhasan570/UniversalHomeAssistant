"""Tests for the LG Infrared select platform."""

from unittest.mock import patch

from infrared_protocols.codes.lg.ac import LGACCode
import pytest
from pytest_universalassistant.common import (
    MockConfigEntry,
    mock_restore_cache,
    snapshot_platform,
)
from pytest_universalassistant.components.common import (
    assert_availability_follows_source_entity,
)
from pytest_universalassistant.components.infrared import EMITTER_ENTITY_ID
from pytest_universalassistant.components.infrared.common import MockInfraredEmitterEntity
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.lg_infrared.const import LGDeviceType
from universalassistant.components.select import (
    DOMAIN as SELECT_DOMAIN,
    SelectService,
    SelectServiceArgument,
)
from universalassistant.const import Platform, TargetKey
from universalassistant.core import UniversalAssistant, State
from universalassistant.helpers import entity_registry as er

_ENTITY_ID = "select.lg_ac_energy_limit"


@pytest.fixture
def platforms() -> list[Platform]:
    """Return platforms to set up."""
    return [Platform.SELECT]


@pytest.fixture
def device_type() -> LGDeviceType:
    """Return the device type of the config entry."""
    return LGDeviceType.AC


@pytest.fixture
def has_receiver() -> bool:
    """Return whether the config entry has an infrared receiver configured."""
    return False


@pytest.mark.usefixtures("init_integration")
async def test_entities(
    hass: UniversalAssistant,
    snapshot: SnapshotAssertion,
    entity_registry: er.EntityRegistry,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test the select entity is created with correct attributes."""
    await snapshot_platform(hass, entity_registry, snapshot, mock_config_entry.entry_id)


@pytest.mark.usefixtures("init_integration")
@pytest.mark.parametrize(
    ("previous_option", "option", "expected_button"),
    [
        pytest.param("40", "off", LGACCode.ENERGY_LIMIT_OFF, id="off"),
        pytest.param("off", "40", LGACCode.ENERGY_LIMIT_40, id="40"),
        pytest.param("off", "60", LGACCode.ENERGY_LIMIT_60, id="60"),
        pytest.param("off", "80", LGACCode.ENERGY_LIMIT_80, id="80"),
    ],
)
async def test_select_option_sends_correct_code(
    hass: UniversalAssistant,
    mock_infrared_emitter_entity: MockInfraredEmitterEntity,
    previous_option: str,
    option: str,
    expected_button: LGACCode,
) -> None:
    """Test selecting an energy cap sends the matching IR code."""
    # Start from a different cap, so every case has to change the state rather than
    # land on the one it started in.
    await hass.services.async_call(
        SELECT_DOMAIN,
        SelectService.SELECT_OPTION,
        {
            TargetKey.ENTITY_ID: _ENTITY_ID,
            SelectServiceArgument.OPTION: previous_option,
        },
        blocking=True,
    )

    await hass.services.async_call(
        SELECT_DOMAIN,
        SelectService.SELECT_OPTION,
        {
            TargetKey.ENTITY_ID: _ENTITY_ID,
            SelectServiceArgument.OPTION: option,
        },
        blocking=True,
    )

    assert len(mock_infrared_emitter_entity.send_command_calls) == 2
    timings = mock_infrared_emitter_entity.send_command_calls[1].get_raw_timings()
    assert timings == expected_button.to_command().get_raw_timings()

    state = hass.states.get(_ENTITY_ID)
    assert state is not None
    assert state.state == option


async def test_state_restored_on_restart(
    hass: UniversalAssistant,
    mock_config_entry: MockConfigEntry,
    mock_infrared_emitter_entity: MockInfraredEmitterEntity,
    platforms: list[Platform],
) -> None:
    """Test the assumed selection is restored after a restart."""
    mock_restore_cache(hass, [State(_ENTITY_ID, "60")])
    mock_config_entry.add_to_hass(hass)

    with patch("universalassistant.components.lg_infrared.PLATFORMS", platforms):
        await hass.config_entries.async_setup(mock_config_entry.entry_id)
        await hass.async_block_till_done()

    state = hass.states.get(_ENTITY_ID)
    assert state is not None
    assert state.state == "60"


@pytest.mark.usefixtures("init_integration")
async def test_availability_follows_emitter(hass: UniversalAssistant) -> None:
    """Test select availability follows the infrared emitter."""
    await assert_availability_follows_source_entity(
        hass, _ENTITY_ID, [EMITTER_ENTITY_ID]
    )
