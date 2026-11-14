"""Tests for the Kodi notify platform."""

from unittest.mock import AsyncMock, patch

import jsonrpc_async
import pytest

from universalassistant.components.kodi.const import DOMAIN
from universalassistant.components.notify import DOMAIN as NOTIFY_DOMAIN
from universalassistant.core import UniversalAssistant
from universalassistant.exceptions import UniversalAssistantError
from universalassistant.setup import async_setup_component

NOTIFY_CONFIG = {
    NOTIFY_DOMAIN: {
        "platform": "kodi",
        "name": "kodi",
        "host": "1.1.1.1",
        "port": 8080,
    }
}


async def setup_notify(hass: UniversalAssistant, server: AsyncMock) -> None:
    """Set up the Kodi notify platform with a mocked server."""
    with patch("jsonrpc_async.Server", return_value=server):
        assert await async_setup_component(hass, NOTIFY_DOMAIN, NOTIFY_CONFIG)
        await hass.async_block_till_done()


async def test_send_message(hass: UniversalAssistant) -> None:
    """Test sending a notification to Kodi."""
    server = AsyncMock()
    await setup_notify(hass, server)

    await hass.services.async_call(
        NOTIFY_DOMAIN, "kodi", {"message": "Hello", "title": "Test"}, blocking=True
    )

    server.GUI.ShowNotification.assert_called_once_with("Test", "Hello", "info", 10000)


async def test_send_message_transport_error(hass: UniversalAssistant) -> None:
    """Test an unreachable Kodi raises an error instead of only logging."""
    server = AsyncMock()
    server.GUI.ShowNotification.side_effect = jsonrpc_async.TransportError(
        "Unable to connect"
    )
    await setup_notify(hass, server)

    with pytest.raises(UniversalAssistantError) as err:
        await hass.services.async_call(
            NOTIFY_DOMAIN, "kodi", {"message": "Hello"}, blocking=True
        )

    assert err.value.translation_domain == DOMAIN
    assert err.value.translation_key == "notify_failed"
