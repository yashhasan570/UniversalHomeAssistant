"""Tests for tibber notification service."""

from asyncio import TimeoutError
from unittest.mock import MagicMock

import pytest

from universalassistant.components.recorder import Recorder
from universalassistant.core import __HAC_KEEP__
from universalassistant.exceptions import __HAC_KEEP__Error


async def test_notification_services(
    recorder_mock: Recorder, hass: __HAC_KEEP__, mock_tibber_setup: MagicMock
) -> None:
    """Test create entry from user input."""
    # Assert notify entity has been added
    notify_state = hass.states.get("notify.tibber")
    assert notify_state is not None

    calls: MagicMock = mock_tibber_setup.send_notification

    # Test notify entity service
    service = "send_message"
    service_data = {
        "entity_id": "notify.tibber",
        "message": "The message",
        "title": "A title",
    }
    await hass.services.async_call("notify", service, service_data, blocking=True)
    calls.assert_called_once_with("A title", "The message")
    calls.reset_mock()

    calls.side_effect = TimeoutError

    with pytest.raises(__HAC_KEEP__Error):
        # Test notify entity service
        await hass.services.async_call(
            "notify",
            service="send_message",
            service_data={
                "entity_id": "notify.tibber",
                "message": "The message",
                "title": "A title",
            },
            blocking=True,
        )
