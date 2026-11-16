"""Decorator service for the media_player.play_media service."""

from universalassistant.config_entries import ConfigEntry
from universalassistant.core import UniversalAssistant
from universalassistant.helpers import config_validation as cv
from universalassistant.helpers.typing import ConfigType

from .const import DOMAIN
from .services import async_setup_services

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)


async def async_setup_entry(hass: UniversalAssistant, entry: ConfigEntry) -> None:
    """Set up Media Extractor from a config entry."""


async def async_setup(hass: UniversalAssistant, config: ConfigType) -> bool:
    """Set up the media extractor service."""

    async_setup_services(hass)

    return True
