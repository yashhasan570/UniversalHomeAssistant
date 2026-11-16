"""Tests for the light LLM tools platform."""

import pytest

from universalassistant.components import llm as llm_component
from universalassistant.components.universalassistant.exposed_entities import async_expose_entity
from universalassistant.components.light import llm as light_llm
from universalassistant.core import Context, UniversalAssistant
from universalassistant.helpers import llm
from universalassistant.setup import async_setup_component

ENTITY_ID = "light.test"


@pytest.fixture(autouse=True)
async def setup_integrations(hass: UniversalAssistant) -> None:
    """Set up the integrations and expose a light entity."""
    assert await async_setup_component(hass, "universalassistant", {})
    assert await async_setup_component(hass, "intent", {})
    assert await async_setup_component(hass, "light", {})
    assert await async_setup_component(hass, "llm", {})
    hass.states.async_set(ENTITY_ID, "on", {"friendly_name": "Test light"})
    async_expose_entity(hass, "conversation", ENTITY_ID, True)
    await hass.async_block_till_done()


def _llm_context() -> llm.LLMContext:
    """Return an LLM context for the conversation assistant."""
    return llm.LLMContext(
        platform="test_platform",
        context=Context(),
        language="*",
        assistant="conversation",
        device_id=None,
    )


async def _tool_names(hass: UniversalAssistant) -> set[str]:
    """Return the names of the tools offered by the light platform."""
    result = await llm_component.async_get_tools(hass, _llm_context(), "assist")
    return {tool.name for tool in result.tools}


async def test_intent_tool_exposed(hass: UniversalAssistant) -> None:
    """Test the intent tool is offered for an exposed light entity."""
    result = await llm_component.async_get_tools(hass, _llm_context(), "assist")
    tools = {tool.name: tool for tool in result.tools}
    assert "light__HassLightSet" in tools

    tool = tools["light__HassLightSet"]
    assert tool.title == "Set light"
    assert tool.integration == "light"
    assert tool.annotations == llm.ToolAnnotations(idempotent=True, open_world=False)


async def test_intent_tool_not_exposed(hass: UniversalAssistant) -> None:
    """Test the intent tool is hidden when no light entity is exposed."""
    async_expose_entity(hass, "conversation", ENTITY_ID, False)
    assert "light__HassLightSet" not in await _tool_names(hass)
    assert light_llm.async_get_tools(hass, _llm_context(), "assist") is None


async def test_no_tools_for_other_api(hass: UniversalAssistant) -> None:
    """Test the platform returns None for an unsupported API."""
    assert light_llm.async_get_tools(hass, _llm_context(), "other") is None
