"""Provide common tests tools for conversation."""

from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components import conversation
from universalassistant.core import __HAC_KEEP__

from . import MockAgent


def mock_conversation_agent_fixture_helper(hass: __HAC_KEEP__) -> MockAgent:
    """Mock agent."""
    entry = MockConfigEntry(entry_id="mock-entry")
    entry.add_to_hass(hass)
    agent = MockAgent(entry.entry_id, ["smurfish"])
    conversation.async_set_agent(hass, entry, agent)
    return agent
