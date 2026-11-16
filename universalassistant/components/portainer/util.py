"""Utility functions for the Portainer integration."""

from collections import defaultdict
from collections.abc import Callable, Iterable

from universalassistant.helpers.entity import Entity
from universalassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback


def sanitize_container_name(container_name: str) -> str:
    """Sanitize to get a proper container name."""
    return container_name.replace("/", " ").strip()


def async_add_entities_by_subentry(
    async_add_entities: AddConfigEntryEntitiesCallback,
    subentry_id_for_endpoint: Callable[[int], str | None],
    entities: Iterable[tuple[Entity, int]],
) -> None:
    """Add entities to Universal Home Assistant, grouped by their endpoint's subentry."""
    grouped: dict[str, list[Entity]] = defaultdict(list)
    for entity, endpoint_id in entities:
        if (subentry_id := subentry_id_for_endpoint(endpoint_id)) is not None:
            grouped[subentry_id].append(entity)

    for subentry_id, group in grouped.items():
        async_add_entities(group, config_subentry_id=subentry_id)
