"""Tests for the intent LLM tools platform (generic intents)."""

from unittest.mock import patch

import probatio
import pytest
from pytest_universalassistant.common import async_mock_service

from universalassistant.components import llm as llm_component
from universalassistant.components.button import ButtonDeviceClass
from universalassistant.components.cover import CoverDeviceClass
from universalassistant.components.universalassistant.exposed_entities import async_expose_entity
from universalassistant.components.intent import llm as intent_llm
from universalassistant.components.intent.timers import async_register_timer_handler
from universalassistant.components.media_player import MediaPlayerDeviceClass
from universalassistant.components.switch import SwitchDeviceClass
from universalassistant.components.timer_list import DOMAIN as TIMER_LIST_DOMAIN
from universalassistant.components.valve import ValveDeviceClass
from universalassistant.const import SERVICE_TURN_ON
from universalassistant.core import Context, UniversalAssistant, callback
from universalassistant.helpers import intent, llm
from universalassistant.setup import async_setup_component

COVER_ENTITY_ID = "cover.test"
LLM_AGENT_ID = "conversation.test_llm_agent"


@pytest.fixture(autouse=True)
async def setup_integrations(hass: UniversalAssistant) -> None:
    """Set up the integrations and expose a cover."""
    assert await async_setup_component(hass, "universalassistant", {})
    assert await async_setup_component(hass, TIMER_LIST_DOMAIN, {})
    assert await async_setup_component(hass, "intent", {})
    assert await async_setup_component(hass, "llm", {})
    hass.states.async_set(COVER_ENTITY_ID, "open", {"friendly_name": "Test Cover"})
    async_expose_entity(hass, "conversation", COVER_ENTITY_ID, True)
    await hass.async_block_till_done()


def _llm_context(device_id: str | None = None) -> llm.LLMContext:
    """Return an LLM context for the conversation assistant."""
    return llm.LLMContext(
        platform="test_platform",
        context=Context(),
        language="*",
        assistant="conversation",
        device_id=device_id,
    )


async def _tool_names(hass: UniversalAssistant) -> set[str]:
    """Return the names of the tools offered by the intent platform."""
    result = await llm_component.async_get_tools(hass, _llm_context(), "assist")
    return {tool.name for tool in result.tools}


async def test_generic_intents_exposed(hass: UniversalAssistant) -> None:
    """Test the always-on generic intents are exposed."""
    names = await _tool_names(hass)
    assert "intent__HassTurnOn" in names
    assert "intent__HassTurnOff" in names


async def test_device_class_enum_has_a_stable_order(hass: UniversalAssistant) -> None:
    """Test the device class enum has a stable order."""
    result = await llm_component.async_get_tools(hass, _llm_context(), "assist")
    tool = next(tool for tool in result.tools if tool.name == "intent__HassTurnOn")
    schema = probatio.to_openapi(tool.parameters)
    assert schema["properties"]["device_class"]["items"]["enum"] == [
        device_class.value
        for device_class_enum in (
            ButtonDeviceClass,
            CoverDeviceClass,
            MediaPlayerDeviceClass,
            SwitchDeviceClass,
            ValveDeviceClass,
        )
        for device_class in device_class_enum
    ]


async def test_turn_on_uses_domain_when_name_blank(hass: UniversalAssistant) -> None:
    """Test HassTurnOn treats a blank name as omitted and uses the domain."""
    hass.states.async_set("light.test_light", "off", {"friendly_name": "Test Light"})
    async_expose_entity(hass, "conversation", "light.test_light", True)
    calls = async_mock_service(hass, "light", SERVICE_TURN_ON)
    api = await llm.async_get_api(hass, "assist", _llm_context())

    await api.async_call_tool(
        llm.ToolInput(
            "intent__HassTurnOn",
            {
                "area": "",
                "domain": "light",
                "floor": " ",
                "name": "",
            },
        )
    )
    await hass.async_block_till_done()

    assert len(calls) == 1
    assert calls[0].data == {"entity_id": ["light.test_light"]}


async def test_turn_on_rejects_all_blank_targets(hass: UniversalAssistant) -> None:
    """Test HassTurnOn still requires a target after omitting blank values."""
    api = await llm.async_get_api(hass, "assist", _llm_context())

    with pytest.raises(
        intent.IntentHandleError, match="^Service handler cannot target all devices$"
    ):
        await api.async_call_tool(
            llm.ToolInput(
                "intent__HassTurnOn", {"area": "", "floor": " ", "name": None}
            )
        )


async def test_timer_intents_require_timer_device(hass: UniversalAssistant) -> None:
    """Test timer intents are not exposed without a timer-capable device."""
    assert "intent__HassStartTimer" not in await _tool_names(hass)


async def test_timer_intents_offered_for_timer_device(hass: UniversalAssistant) -> None:
    """Test timer intents are exposed for a timer-capable device."""

    @callback
    def handle_timer(*args: object) -> None:
        pass

    async_register_timer_handler(hass, "test_device", handle_timer)

    result = await llm_component.async_get_tools(
        hass, _llm_context(device_id="test_device"), "assist"
    )
    names = {tool.name for tool in result.tools}
    assert "intent__HassStartTimer" in names
    assert "intent__HassTimerStatus" in names


async def test_tool_annotations(hass: UniversalAssistant) -> None:
    """Test the intent tools declare how they behave."""

    @callback
    def handle_timer(*args: object) -> None:
        pass

    async_register_timer_handler(hass, "test_device", handle_timer)

    result = await llm_component.async_get_tools(
        hass, _llm_context(device_id="test_device"), "assist"
    )
    tools = {tool.name: tool for tool in result.tools}

    assert tools["intent__HassTurnOn"].title == "Turn on"
    assert tools["intent__HassTurnOn"].integration == "intent"
    # Turning on a button entity presses it, so the call is not idempotent.
    assert tools["intent__HassTurnOn"].annotations == llm.ToolAnnotations(
        open_world=False
    )
    assert tools["intent__HassTurnOff"].annotations == llm.ToolAnnotations(
        idempotent=True, open_world=False
    )
    # Adding time only adds, and has an effect on every call.
    assert tools["intent__HassIncreaseTimer"].annotations == llm.ToolAnnotations(
        destructive=False, open_world=False
    )
    # A started timer can carry a command to run when it finishes.
    assert tools["intent__HassStartTimer"].annotations == llm.ToolAnnotations(
        open_world=False
    )
    assert tools["intent__HassTimerStatus"].annotations == llm.ToolAnnotations(
        read_only=True, open_world=False
    )


async def test_set_position_requires_exposed_cover(hass: UniversalAssistant) -> None:
    """Test intent__HassSetPosition is only exposed when a cover/valve is exposed."""
    assert "intent__HassSetPosition" in await _tool_names(hass)

    async_expose_entity(hass, "conversation", COVER_ENTITY_ID, False)
    assert "intent__HassSetPosition" not in await _tool_names(hass)


async def test_prompt_includes_device_control(hass: UniversalAssistant) -> None:
    """Test the platform contributes device-control guidance when exposed."""
    result = intent_llm.async_get_tools(hass, _llm_context(), "assist")
    assert result is not None
    assert result.prompt is not None
    assert intent_llm.DEVICE_CONTROL_TOOL_USAGE_PROMPT in result.prompt
    assert "This device is not able to start timers." in result.prompt


async def test_no_prompt_without_exposed_entities(hass: UniversalAssistant) -> None:
    """Test the platform contributes no prompt when nothing is exposed."""
    async_expose_entity(hass, "conversation", COVER_ENTITY_ID, False)
    result = intent_llm.async_get_tools(hass, _llm_context(), "assist")
    assert result is not None
    assert result.prompt is None


async def test_no_tools_for_other_api(hass: UniversalAssistant) -> None:
    """Test the platform returns None for an unsupported API."""
    assert intent_llm.async_get_tools(hass, _llm_context(), "other") is None


@pytest.mark.parametrize(
    ("assistant", "agent_id", "offered"),
    [
        pytest.param("conversation", LLM_AGENT_ID, True, id="conversation_agent"),
        pytest.param("conversation", None, False, id="no_agent"),
        pytest.param("ai_task", "ai_task.test", False, id="ai_task"),
    ],
)
async def test_schedule_command_requires_conversation_agent(
    hass: UniversalAssistant, assistant: str, agent_id: str | None, offered: bool
) -> None:
    """Test the schedule command tool needs an agent to run the command later."""
    llm_context = llm.LLMContext(
        platform="test_platform",
        context=Context(),
        language="en",
        assistant=assistant,
        device_id=None,
        agent_id=agent_id,
    )
    result = await llm_component.async_get_tools(hass, llm_context, "assist")
    names = {tool.name for tool in result.tools}
    assert ("intent__schedule_command" in names) is offered


async def test_schedule_command_runs_on_same_agent(hass: UniversalAssistant) -> None:
    """Test a scheduled command runs on the same agent as the same user."""
    request_context = Context(user_id="test_user")
    llm_context = llm.LLMContext(
        platform="test_platform",
        context=request_context,
        language="en",
        assistant="conversation",
        device_id="test_device",
        agent_id=LLM_AGENT_ID,
    )
    api = await llm.async_get_api(hass, "assist", llm_context)

    with patch("universalassistant.components.conversation.async_converse") as mock_converse:
        result = await api.async_call_tool(
            llm.ToolInput(
                "intent__schedule_command",
                {"command": " Turn off the kitchen light ", "seconds": 0},
            )
        )
        await hass.async_block_till_done()

    assert result.data == {"success": True}
    mock_converse.assert_called_once()
    assert mock_converse.call_args.args[1] == "Turn off the kitchen light"
    assert mock_converse.call_args.kwargs["agent_id"] == LLM_AGENT_ID
    assert mock_converse.call_args.kwargs["device_id"] == "test_device"
    command_context = mock_converse.call_args.kwargs["context"]
    assert command_context.user_id == request_context.user_id
    assert command_context.parent_id == request_context.id


async def test_prompt_offers_schedule_command_without_timers(
    hass: UniversalAssistant,
) -> None:
    """Test the prompt points a device without timers to scheduled commands."""
    llm_context = llm.LLMContext(
        platform="test_platform",
        context=Context(),
        language="en",
        assistant="conversation",
        device_id=None,
        agent_id=LLM_AGENT_ID,
    )
    result = await llm_component.async_get_tools(hass, llm_context, "assist")
    assert (
        "This device is not able to start timers. It can still run a command"
        " later with intent__schedule_command."
    ) in result.prompt
