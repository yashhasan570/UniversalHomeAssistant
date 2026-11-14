"""Tests for the Edifier Infrared button platform."""

from infrared_protocols.codes.edifier.models import EdifierCommandSet
from infrared_protocols.codes.edifier.r1700bts import EdifierR1700BTsCode
import pytest
from pytest_universalassistant.common import MockConfigEntry, snapshot_platform
from pytest_universalassistant.components.common import (
    assert_availability_follows_source_entity,
)
from pytest_universalassistant.components.infrared import EMITTER_ENTITY_ID
from pytest_universalassistant.components.infrared.common import MockInfraredEmitterEntity
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.button import DOMAIN as BUTTON_DOMAIN, ButtonService
from universalassistant.components.edifier_infrared.button import COMMAND_SET_BUTTONS
from universalassistant.components.edifier_infrared.const import SUPPORTED_COMMAND_SETS
from universalassistant.const import CommonServiceArgument, Platform
from universalassistant.core import UniversalAssistant
from universalassistant.helpers import entity_registry as er

BLUETOOTH_BUTTON_ENTITY_ID = "button.edifier_r1700bts_bluetooth"


@pytest.fixture
def platforms() -> list[Platform]:
    """Return platforms to set up."""
    return [Platform.BUTTON]


@pytest.mark.usefixtures("init_integration")
async def test_entities(
    hass: UniversalAssistant,
    snapshot: SnapshotAssertion,
    entity_registry: er.EntityRegistry,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test the button entities are created with correct attributes."""
    await snapshot_platform(hass, entity_registry, snapshot, mock_config_entry.entry_id)


@pytest.mark.parametrize(
    ("entity_id", "expected_code"),
    [
        ("button.edifier_r1700bts_bluetooth", EdifierR1700BTsCode.BLUETOOTH),
        ("button.edifier_r1700bts_line_1", EdifierR1700BTsCode.LINE_1),
        ("button.edifier_r1700bts_line_2", EdifierR1700BTsCode.LINE_2),
        ("button.edifier_r1700bts_fx_on", EdifierR1700BTsCode.FX_ON),
        ("button.edifier_r1700bts_fx_off", EdifierR1700BTsCode.FX_OFF),
    ],
)
@pytest.mark.usefixtures("init_integration")
async def test_button_press_sends_correct_code(
    hass: UniversalAssistant,
    mock_infrared_emitter_entity: MockInfraredEmitterEntity,
    entity_id: str,
    expected_code: EdifierR1700BTsCode,
) -> None:
    """Test each button press sends the correct IR code."""
    await hass.services.async_call(
        BUTTON_DOMAIN,
        ButtonService.PRESS,
        {CommonServiceArgument.ENTITY_ID: entity_id},
        blocking=True,
    )

    assert len(mock_infrared_emitter_entity.send_command_calls) == 1
    assert mock_infrared_emitter_entity.send_command_calls[0] == expected_code


@pytest.mark.usefixtures("init_integration")
async def test_button_availability_follows_ir_entity(
    hass: UniversalAssistant,
) -> None:
    """Test button becomes unavailable when IR entity is unavailable."""
    await assert_availability_follows_source_entity(
        hass, BLUETOOTH_BUTTON_ENTITY_ID, [EMITTER_ENTITY_ID]
    )


def test_command_sets_match_supported_command_sets() -> None:
    """Test that the button platform implements every supported command set."""
    # R1280T only has volume and mute codes, which are covered by the media player
    assert set(COMMAND_SET_BUTTONS) == set(SUPPORTED_COMMAND_SETS) - {
        EdifierCommandSet.R1280T
    }
