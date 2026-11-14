"""Diagnostics support for Collection Image."""

from typing import Any

from yarl import URL

from universalassistant.components.image import DOMAIN as IMAGE_DOMAIN
from universalassistant.components.media_player import BrowseError, MediaClass
from universalassistant.components.media_source import (
    Unresolvable,
    async_browse_media,
    async_resolve_media,
)
from universalassistant.config_entries import ConfigEntry
from universalassistant.core import UniversalAssistant
from universalassistant.helpers import entity_registry as er

from .const import CONF_MEDIA, DOMAIN


async def _async_browse_source(
    hass: UniversalAssistant, media_content_id: str
) -> dict[str, Any]:
    """Browse a configured media source and describe its contents."""
    try:
        media = await async_browse_media(hass, media_content_id)
    except BrowseError as err:
        return {"media_content_id": media_content_id, "error": str(err)}

    children = media.children or []
    return {
        "media_content_id": media_content_id,
        "title": media.title,
        "media_class": media.media_class,
        "children_count": len(children),
        "image_count": sum(
            1 for child in children if child.media_class == MediaClass.IMAGE
        ),
        "children": [
            {
                "title": child.title,
                "media_content_id": child.media_content_id,
                "media_content_type": child.media_content_type,
                "media_class": child.media_class,
                "can_play": child.can_play,
                "can_expand": child.can_expand,
            }
            for child in children
        ],
    }


async def _async_resolve_image(
    hass: UniversalAssistant, media_content_id: str, entity_id: str
) -> dict[str, Any]:
    """Resolve the current image and describe the result."""
    try:
        resolved = await async_resolve_media(hass, media_content_id, entity_id)
    except Unresolvable as err:
        return {"error": str(err)}

    return {
        # Some media sources put access tokens in the query string.
        "url": str(URL(resolved.url).with_query(None)) if resolved.url else None,
        "mime_type": resolved.mime_type,
        "path": str(resolved.path) if resolved.path else None,
    }


async def async_get_config_entry_diagnostics(
    hass: UniversalAssistant, entry: ConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    media = entry.data[CONF_MEDIA]
    items = [media] if isinstance(media, dict) else media

    current_image: dict[str, Any] | None = None
    entity_registry = er.async_get(hass)
    if (
        entity_id := entity_registry.async_get_entity_id(
            IMAGE_DOMAIN, DOMAIN, entry.entry_id
        )
    ) and (state := hass.states.get(entity_id)):
        media_content_id = state.attributes.get("current_media_id")
        current_image = {
            "entity_id": entity_id,
            "state": state.state,
            "media_content_id": media_content_id,
            "resolved": (
                await _async_resolve_image(hass, media_content_id, entity_id)
                if media_content_id
                else None
            ),
        }

    return {
        "entry": {"title": entry.title, "data": dict(entry.data)},
        "current_image": current_image,
        "media_sources": [
            await _async_browse_source(hass, item["media_content_id"]) for item in items
        ],
    }
