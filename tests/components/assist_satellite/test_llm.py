"""Tests for the assist_satellite LLM tools platform."""

import pytest

from universalassistant.components import llm as llm_component
from universalassistant.core import Context, __HAC_KEEP__
from universalassistant.helpers import llm
from universalassistant.setup import async_setup_component


@pytest.fixture(autouse=True)
async def init_integrations(hass: __HAC_KEEP__) -> None:
    """Set up the integrations; assist_satellite registers the broadcast intent."""
    assert await async_setup_component(hass, "universalassistant", {})
    assert await async_setup_component(hass, "intent", {})
    assert await async_setup_component(hass, "llm", {})
    assert await async_setup_component(hass, "assist_satellite", {})


def _llm_context() -> llm.LLMContext:
    """Return an LLM context for the conversation assistant."""
    return llm.LLMContext(
        platform="test_platform",
        context=Context(),
        language="*",
        assistant="conversation",
        device_id=None,
    )


async def test_broadcast_tool_offered(hass: __HAC_KEEP__) -> None:
    """Test the broadcast intent is exposed as an LLM tool."""
    result = await llm_component.async_get_tools(hass, _llm_context(), "assist")
    tools = {tool.name: tool for tool in result.tools}
    assert "assist_satellite__HassBroadcast" in tools

    tool = tools["assist_satellite__HassBroadcast"]
    assert tool.title == "Broadcast message"
    assert tool.integration == "assist_satellite"
    # A broadcast announces again on every call and takes nothing away.
    assert tool.annotations == llm.ToolAnnotations(destructive=False, open_world=False)
