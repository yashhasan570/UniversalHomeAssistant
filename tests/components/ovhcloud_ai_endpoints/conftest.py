"""Fixtures for OVHcloud AI Endpoints integration tests."""

from collections.abc import AsyncGenerator, Generator
import json
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

from openai.types import CompletionUsage, Model
from openai.types.chat import ChatCompletion, ChatCompletionMessage
from openai.types.chat.chat_completion import Choice
import pytest
from pytest_universalassistant.common import MockConfigEntry, async_load_fixture

from universalassistant.components.ovhcloud_ai_endpoints.const import DOMAIN
from universalassistant.config_entries import ConfigSubentryData
from universalassistant.const import CONF_API_KEY, CONF_LLM_HASS_API, CONF_MODEL, CONF_PROMPT
from universalassistant.core import UniversalAssistant
from universalassistant.helpers import llm
from universalassistant.setup import async_setup_component


@pytest.fixture
def mock_setup_entry() -> Generator[AsyncMock]:
    """Override async_setup_entry."""
    with patch(
        "universalassistant.components.ovhcloud_ai_endpoints.async_setup_entry",
        return_value=None,
    ) as mock_setup_entry:
        yield mock_setup_entry


@pytest.fixture
def enable_assist() -> bool:
    """Toggle for whether the conversation subentry exposes the Assist API."""
    return False


@pytest.fixture
def conversation_subentry_data(enable_assist: bool) -> dict[str, Any]:
    """Mock conversation subentry data."""
    res: dict[str, Any] = {
        CONF_MODEL: "Meta-Llama-3_3-70B-Instruct",
        CONF_PROMPT: "You are a helpful assistant.",
    }
    if enable_assist:
        res[CONF_LLM_HASS_API] = [llm.LLM_API_ASSIST]
    return res


@pytest.fixture
def mock_config_entry(
    hass: UniversalAssistant,
    conversation_subentry_data: dict[str, Any],
) -> MockConfigEntry:
    """Mock a config entry."""
    return MockConfigEntry(
        title="OVHcloud AI Endpoints",
        domain=DOMAIN,
        data={
            CONF_API_KEY: "bla",
        },
        subentries_data=[
            ConfigSubentryData(
                data=conversation_subentry_data,
                subentry_id="ABCDEF",
                subentry_type="conversation",
                title="Meta-Llama-3_3-70B-Instruct",
                unique_id=None,
            ),
        ],
    )


async def _build_models(hass: UniversalAssistant) -> list[Model]:
    """Load mocked models from the fixture file."""
    raw = await async_load_fixture(hass, "models.json", DOMAIN)
    return [Model.model_validate(m) for m in json.loads(raw)["data"]]


@pytest.fixture
async def mock_openai_client(hass: UniversalAssistant) -> AsyncGenerator[AsyncMock]:
    """Mock the AsyncOpenAI client used by the integration."""
    models = await _build_models(hass)

    async def _list_models(*args: Any, **kwargs: Any) -> AsyncGenerator[Model]:
        for model in models:
            yield model

    with patch(
        "universalassistant.components.ovhcloud_ai_endpoints.AsyncOpenAI"
    ) as mock_async_openai:
        client = mock_async_openai.return_value
        client.with_options.return_value = client
        client.models.list = MagicMock(side_effect=_list_models)
        client.chat.completions.create = AsyncMock(
            return_value=ChatCompletion(
                id="chatcmpl-1234567890ABCDEFGHIJKLMNOPQRS",
                choices=[
                    Choice(
                        finish_reason="stop",
                        index=0,
                        message=ChatCompletionMessage(
                            content="Hello, how can I help you?",
                            role="assistant",
                            function_call=None,
                            tool_calls=None,
                        ),
                    )
                ],
                created=1700000000,
                model="Meta-Llama-3_3-70B-Instruct",
                object="chat.completion",
                system_fingerprint=None,
                usage=CompletionUsage(
                    completion_tokens=9, prompt_tokens=8, total_tokens=17
                ),
            )
        )
        yield client


@pytest.fixture(autouse=True)
async def setup_ha(hass: UniversalAssistant) -> None:
    """Set up Universal Universal Home Assistant."""
    assert await async_setup_component(hass, "universalassistant", {})
