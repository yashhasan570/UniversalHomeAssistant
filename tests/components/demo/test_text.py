"""The tests for the demo text component."""

from collections.abc import Generator
from unittest.mock import patch

import pytest

from universalassistant.components.text import (
    DOMAIN as TEXT_DOMAIN,
    TextEntityCapabilityAttribute,
    TextService,
    TextServiceArgument,
)
from universalassistant.const import MAX_LENGTH_STATE_STATE, Platform, TargetKey
from universalassistant.core import UniversalAssistant
from universalassistant.setup import async_setup_component

ENTITY_TEXT = "text.text"


@pytest.fixture
def text_only() -> Generator[None]:
    """Enable only the text platform."""
    with patch(
        "universalassistant.components.demo.COMPONENTS_WITH_CONFIG_ENTRY_DEMO_PLATFORM",
        [Platform.TEXT],
    ):
        yield


@pytest.fixture(autouse=True)
async def setup_demo_text(hass: UniversalAssistant, text_only: None) -> None:
    """Initialize setup demo text."""
    assert await async_setup_component(
        hass, TEXT_DOMAIN, {"text": {"platform": "demo"}}
    )
    await hass.async_block_till_done()


def test_setup_params(hass: UniversalAssistant) -> None:
    """Test the initial parameters."""
    state = hass.states.get(ENTITY_TEXT)
    assert state.state == "Hello world"
    assert state.attributes[TextEntityCapabilityAttribute.MIN] == 0
    assert state.attributes[TextEntityCapabilityAttribute.MAX] == MAX_LENGTH_STATE_STATE
    assert state.attributes[TextEntityCapabilityAttribute.PATTERN] is None
    assert state.attributes[TextEntityCapabilityAttribute.MODE] == "text"


async def test_set_value(hass: UniversalAssistant) -> None:
    """Test set value service."""
    await hass.services.async_call(
        TEXT_DOMAIN,
        TextService.SET_VALUE,
        {TargetKey.ENTITY_ID: ENTITY_TEXT, TextServiceArgument.VALUE: "new"},
        blocking=True,
    )
    state = hass.states.get(ENTITY_TEXT)
    assert state.state == "new"
