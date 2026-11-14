"""The tests for the kitchen_sink infrared platform."""

from unittest.mock import Mock, patch

from freezegun.api import FrozenDateTimeFactory
from infrared_protocols.commands.nec import NECCommand
import pytest

from universalassistant.components.infrared import (
    async_send_command,
    async_subscribe_receiver,
)
from universalassistant.components.kitchen_sink import DOMAIN
from universalassistant.const import Platform
from universalassistant.core import UniversalAssistant
from universalassistant.setup import async_setup_component
from universalassistant.util import dt as dt_util

ENTITY_IR_EMITTER = "infrared.ir_blaster_infrared_emitter"
ENTITY_IR_RECEIVER = "infrared.ir_blaster_infrared_receiver"


@pytest.fixture
async def infrared_only() -> None:
    """Enable only the infrared platform."""
    with patch(
        "universalassistant.components.kitchen_sink.COMPONENTS_WITH_DEMO_PLATFORM",
        [Platform.INFRARED],
    ):
        yield


@pytest.fixture(autouse=True)
async def setup_comp(hass: UniversalAssistant, infrared_only: None) -> None:
    """Set up demo component."""
    assert await async_setup_component(hass, DOMAIN, {DOMAIN: {}})
    await hass.async_block_till_done()


async def test_send_receive(
    hass: UniversalAssistant, freezer: FrozenDateTimeFactory
) -> None:
    """Test the receiver picks up commands sent by the emitter via dispatcher."""
    signal_callback = Mock()
    async_subscribe_receiver(hass, ENTITY_IR_RECEIVER, signal_callback)

    now = dt_util.parse_datetime("2021-01-09 12:00:00+00:00")
    assert now is not None
    freezer.move_to(now)

    command = NECCommand(address=0x04, command=0x08, modulation=38000)
    await async_send_command(hass, ENTITY_IR_EMITTER, command)
    await hass.async_block_till_done()

    state = hass.states.get(ENTITY_IR_RECEIVER)
    assert state
    assert state.state == now.isoformat(timespec="milliseconds")

    assert signal_callback.call_count == 1
    received_signal = signal_callback.call_args[0][0]
    assert received_signal.timings == command.get_raw_timings()
