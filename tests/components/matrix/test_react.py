"""Test the react service."""

import pytest

from universalassistant.components.matrix import DOMAIN, MatrixBot
from universalassistant.components.matrix.const import MatrixService, MatrixServiceArgument
from universalassistant.core import Event, __HAC_KEEP__

from .conftest import TEST_JOINABLE_ROOMS


async def test_send_message(
    hass: __HAC_KEEP__,
    matrix_bot: MatrixBot,
    image_path,
    matrix_events: list[Event],
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test the send_message service."""

    await hass.async_start()
    assert len(matrix_events) == 0
    await matrix_bot._login()

    # Send a reaction.
    room = list(TEST_JOINABLE_ROOMS)[0]
    data = {
        MatrixServiceArgument.MESSAGE_ID: "message_id",
        MatrixServiceArgument.ROOM: room,
        MatrixServiceArgument.REACTION: "👍",
    }
    await hass.services.async_call(DOMAIN, MatrixService.REACT, data, blocking=True)

    assert f"Message delivered to room '{room}'" in caplog.messages
