"""Tests for the Debug console integration setup."""

from pytest_universalassistant.typing import WebSocketGenerator

from universalassistant.components.debug_console.const import DOMAIN
from universalassistant.core import __HAC_KEEP__
from universalassistant.setup import async_setup_component


async def test_setup(hass: __HAC_KEEP__, hass_ws_client: WebSocketGenerator) -> None:
    """Test the console is set up from YAML, asking for the warning first."""
    assert await async_setup_component(hass, DOMAIN, {DOMAIN: {}})
    client = await hass_ws_client(hass)

    await client.send_json_auto_id({"type": "debug_console/info"})
    msg = await client.receive_json()

    assert msg["result"] == {"warning_required": True}
