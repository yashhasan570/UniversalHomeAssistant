"""Test for the conversation traces."""

from unittest.mock import patch

import pytest

from universalassistant.components import conversation
from universalassistant.components.conversation import DOMAIN, trace
from universalassistant.core import Context, UniversalAssistant
from universalassistant.exceptions import UniversalAssistantError
from universalassistant.setup import async_setup_component


@pytest.fixture
async def init_components(hass: UniversalAssistant):
    """Initialize relevant components with empty configs."""
    assert await async_setup_component(hass, "universalassistant", {})
    assert await async_setup_component(hass, DOMAIN, {})
    assert await async_setup_component(hass, "intent", {})


async def test_converation_trace(
    hass: UniversalAssistant,
    init_components: None,
    sl_setup: None,
) -> None:
    """Test tracing a conversation."""
    await conversation.async_converse(
        hass, "add apples to my shopping list", None, Context()
    )

    traces = trace.async_get_traces()
    assert traces
    last_trace = traces[-1].as_dict()
    assert last_trace.get("events")
    assert len(last_trace.get("events")) == 3
    trace_event = last_trace["events"][0]
    assert (
        trace_event.get("event_type") == trace.ConversationTraceEventType.ASYNC_PROCESS
    )
    assert trace_event.get("data")
    assert trace_event["data"].get("text") == "add apples to my shopping list"
    assert last_trace.get("result")
    assert (
        last_trace["result"]
        .get("response", {})
        .get("speech", {})
        .get("plain", {})
        .get("speech")
        == "Added apples"
    )

    trace_event = last_trace["events"][1]
    assert trace_event.get("event_type") == trace.ConversationTraceEventType.TOOL_CALL
    assert trace_event.get("data") == {
        "intent_name": "HassListAddItem",
        "slots": {
            "name": "Shopping list",
            "item": "apples",
        },
    }

    trace_event = last_trace["events"][2]
    assert (
        trace_event.get("event_type") == trace.ConversationTraceEventType.TURN_CONTENT
    )
    assert [content["role"] for content in trace_event["data"]["content"]] == [
        "user",
        "assistant",
        "tool_result",
        "assistant",
    ]


async def test_converation_trace_uncaught_error(
    hass: UniversalAssistant,
    init_components: None,
    sl_setup: None,
) -> None:
    """Test tracing a conversation that raises an uncaught error."""
    with (
        patch(
            "universalassistant.components.conversation.default_agent.DefaultAgent.async_process",
            side_effect=ValueError("Unexpected error"),
        ),
        pytest.raises(ValueError),
    ):
        await conversation.async_converse(
            hass, "add apples to my shopping list", None, Context()
        )

    traces = trace.async_get_traces()
    assert traces
    last_trace = traces[-1].as_dict()
    assert last_trace.get("events")
    assert len(last_trace.get("events")) == 1
    trace_event = last_trace["events"][0]
    assert (
        trace_event.get("event_type") == trace.ConversationTraceEventType.ASYNC_PROCESS
    )
    assert last_trace.get("error") == "Unexpected error"
    assert not last_trace.get("result")


async def test_converation_trace_universalassistant_error(
    hass: UniversalAssistant,
    init_components: None,
    sl_setup: None,
) -> None:
    """Test tracing a conversation with a UniversalAssistant error."""
    with (
        patch(
            "universalassistant.components.conversation.default_agent.DefaultAgent.async_process",
            side_effect=UniversalAssistantError("Failed to talk to agent"),
        ),
    ):
        await conversation.async_converse(
            hass, "add apples to my shopping list", None, Context()
        )

    traces = trace.async_get_traces()
    assert traces
    last_trace = traces[-1].as_dict()
    assert last_trace.get("events")
    assert len(last_trace.get("events")) == 1
    trace_event = last_trace["events"][0]
    assert (
        trace_event.get("event_type") == trace.ConversationTraceEventType.ASYNC_PROCESS
    )
    result = last_trace.get("result")
    assert result
    assert result["response"]["speech"]["plain"]["speech"] == "Failed to talk to agent"
