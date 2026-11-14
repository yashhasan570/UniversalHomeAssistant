"""Diagnostics for camera."""

from typing import Any

from universalassistant.config_entries import ConfigEntry
from universalassistant.core import __HAC_KEEP__
from universalassistant.exceptions import __HAC_KEEP__Error
from universalassistant.helpers import entity_registry as er

from .const import DOMAIN
from .helper import get_camera_from_entity_id


async def async_get_config_entry_diagnostics(
    hass: __HAC_KEEP__, config_entry: ConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    entity_registry = er.async_get(hass)
    entities = er.async_entries_for_config_entry(entity_registry, config_entry.entry_id)
    diagnostics = {}
    for entity in entities:
        if entity.domain != DOMAIN:
            continue
        try:
            camera = get_camera_from_entity_id(hass, entity.entity_id)
        except __HAC_KEEP__Error:
            continue
        diagnostics[entity.entity_id] = (
            camera.stream.get_diagnostics() if camera.stream else {}
        )
    return diagnostics
