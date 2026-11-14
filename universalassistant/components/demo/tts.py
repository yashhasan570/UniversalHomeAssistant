"""Support for the demo for text-to-speech service."""

import os
from typing import Any, override

from universalassistant.components.tts import TextToSpeechEntity, TtsAudioType
from universalassistant.config_entries import ConfigEntry
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

SUPPORT_LANGUAGES = ["en", "de"]

DEFAULT_LANG = "en"


async def async_setup_entry(
    hass: __HAC_KEEP__,
    config_entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up Demo speech platform via config entry."""
    async_add_entities([DemoProviderEntity()])


class DemoProviderEntity(TextToSpeechEntity):
    """Demo speech API provider entity."""

    _attr_name = "Demo TTS"
    _attr_default_language = DEFAULT_LANG
    _attr_supported_languages = SUPPORT_LANGUAGES
    _attr_supported_options = ["voice", "age"]

    @override
    def get_tts_audio(
        self, message: str, language: str, options: dict[str, Any]
    ) -> TtsAudioType:
        """Load TTS from demo."""
        filename = os.path.join(os.path.dirname(__file__), "tts.mp3")
        try:
            with open(filename, "rb") as voice:
                data = voice.read()
        except OSError:
            return (None, None)

        return ("mp3", data)
