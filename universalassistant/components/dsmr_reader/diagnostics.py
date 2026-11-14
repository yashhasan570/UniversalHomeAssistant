"""Diagnostics support for DSMR Reader."""

from typing import Any

from universalassistant.config_entries import ConfigEntry
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import entity_registry as er


async def async_get_config_entry_diagnostics(
    hass: __HAC_KEEP__, entry: ConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for the config entry."""
    ent_reg = er.async_get(hass)
    entities = [
        entity.entity_id
        for entity in er.async_entries_for_config_entry(ent_reg, entry.entry_id)
    ]

    entity_states = {entity: hass.states.get(entity) for entity in entities}

    return {
        "entry": entry.as_dict(),
        "entities": entity_states,
    }
