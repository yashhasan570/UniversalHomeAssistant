"""Provide common test tools for wake-word-detection."""

from collections.abc import Callable, Coroutine
from pathlib import Path
from typing import Any

from pytest_universalassistant.common import MockPlatform, mock_platform

from universalassistant.components import wake_word
from universalassistant.config_entries import ConfigEntry
from universalassistant.core import UniversalAssistant
from universalassistant.helpers.entity_platform import AddEntitiesCallback


def mock_wake_word_entity_platform(
    hass: UniversalAssistant,
    tmp_path: Path,
    integration: str,
    async_setup_entry: Callable[
        [UniversalAssistant, ConfigEntry, AddEntitiesCallback],
        Coroutine[Any, Any, None],
    ]
    | None = None,
) -> MockPlatform:
    """Specialize the mock platform for stt."""
    loaded_platform = MockPlatform(async_setup_entry=async_setup_entry)
    mock_platform(hass, f"{integration}.{wake_word.DOMAIN}", loaded_platform)
    return loaded_platform
