"""Conversation test helpers."""

from collections.abc import Generator
from unittest.mock import Mock, patch

import pytest
from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components import conversation
from universalassistant.components.conversation import DOMAIN, async_get_agent, default_agent
from universalassistant.components.shopping_list import intent as sl_intent
from universalassistant.const import MATCH_ALL
from universalassistant.core import Context, UniversalAssistant
from universalassistant.setup import async_setup_component

from . import MockAgent


@pytest.fixture
def mock_ulid() -> Generator[Mock]:
    """Mock the ulid library."""
    with patch("universalassistant.helpers.chat_session.secure_ulid_now") as mock_ulid_now:
        mock_ulid_now.return_value = "mock-ulid"
        yield mock_ulid_now


@pytest.fixture
def mock_agent_support_all(hass: UniversalAssistant) -> MockAgent:
    """Mock agent that supports all languages."""
    entry = MockConfigEntry(entry_id="mock-entry-support-all")
    entry.add_to_hass(hass)
    agent = MockAgent(entry.entry_id, MATCH_ALL)
    conversation.async_set_agent(hass, entry, agent)
    return agent


@pytest.fixture
def mock_conversation_input(hass: UniversalAssistant) -> conversation.ConversationInput:
    """Return a conversation input instance."""
    return conversation.ConversationInput(
        text="Hello",
        context=Context(),
        conversation_id=None,
        agent_id="mock-agent-id",
        device_id=None,
        satellite_id=None,
        language="en",
    )


@pytest.fixture(autouse=True)
def mock_shopping_list_io():
    """Stub out the persistence."""
    with (
        patch("universalassistant.components.shopping_list.ShoppingData.save"),
        patch("universalassistant.components.shopping_list.ShoppingData.async_load"),
    ):
        yield


@pytest.fixture
async def sl_setup(hass: UniversalAssistant):
    """Set up the shopping list."""

    entry = MockConfigEntry(domain="shopping_list")
    entry.add_to_hass(hass)

    assert await hass.config_entries.async_setup(entry.entry_id)

    await sl_intent.async_setup_intents(hass)


@pytest.fixture
async def init_components(hass: UniversalAssistant):
    """Initialize relevant components with empty configs."""
    assert await async_setup_component(hass, "universalassistant", {})
    assert await async_setup_component(hass, DOMAIN, {conversation.DOMAIN: {}})

    # Disable fuzzy matching by default for tests
    agent = async_get_agent(hass)
    assert isinstance(agent, default_agent.DefaultAgent)
    agent.fuzzy_matching = False
