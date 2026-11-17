"""Tests for the Kaku RC switch platform."""

from pytest_universalassistant.common import MockConfigEntry
from pytest_universalassistant.components.radio_frequency.common import (
    MockRadioFrequencyEntity,
)
from rf_protocols.commands.kaku import _DEFAULT_REPEATS

from universalassistant.components.switch import DOMAIN as SWITCH_DOMAIN, SwitchService
from universalassistant.const import STATE_OFF, STATE_ON, TargetKey
from universalassistant.core import UniversalAssistant

SWITCH_ENTITY_ID = "switch.kaku_id_123456_ch_1_output"


async def test_turn_on_off_sends_kaku_commands(
    hass: UniversalAssistant,
    mock_rf_entity: MockRadioFrequencyEntity,
    init_klik_aan_klik_uit: MockConfigEntry,
) -> None:
    """Test non-dim switch on/off behavior."""
    await hass.services.async_call(
        SWITCH_DOMAIN,
        SwitchService.TURN_ON,
        {TargetKey.ENTITY_ID: SWITCH_ENTITY_ID},
        blocking=True,
    )

    state = hass.states.get(SWITCH_ENTITY_ID)
    assert state is not None
    assert state.state == STATE_ON
    assert len(mock_rf_entity.send_command_calls) == 1

    first_command = mock_rf_entity.send_command_calls[0].command
    assert first_command.on is True
    assert first_command.dimlevel is None
    assert first_command.repeat_count == _DEFAULT_REPEATS

    await hass.services.async_call(
        SWITCH_DOMAIN,
        SwitchService.TURN_OFF,
        {TargetKey.ENTITY_ID: SWITCH_ENTITY_ID},
        blocking=True,
    )

    state = hass.states.get(SWITCH_ENTITY_ID)
    assert state is not None
    assert state.state == STATE_OFF
    assert len(mock_rf_entity.send_command_calls) == 2

    second_command = mock_rf_entity.send_command_calls[1].command
    assert second_command.on is False
    assert second_command.dimlevel is None
    assert second_command.repeat_count == _DEFAULT_REPEATS
