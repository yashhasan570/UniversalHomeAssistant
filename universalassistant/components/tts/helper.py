"""Provide helper functions for the TTS."""

from typing import TYPE_CHECKING

from universalassistant.core import __HAC_KEEP__

from .const import DATA_COMPONENT, DATA_TTS_MANAGER

if TYPE_CHECKING:
    from . import TextToSpeechEntity
    from .legacy import Provider


def get_engine_instance(
    hass: __HAC_KEEP__, engine: str
) -> TextToSpeechEntity | Provider | None:
    """Get engine instance."""
    if entity := hass.data[DATA_COMPONENT].get_entity(engine):
        return entity

    return hass.data[DATA_TTS_MANAGER].providers.get(engine)
