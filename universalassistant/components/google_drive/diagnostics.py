"""Diagnostics support for Google Drive."""

import dataclasses
from typing import Any

from universalassistant.components.backup import async_get_manager
from universalassistant.components.diagnostics import async_redact_data
from universalassistant.const import CONF_ACCESS_TOKEN
from universalassistant.core import UniversalAssistant

from .const import DOMAIN
from .coordinator import GoogleDriveConfigEntry

TO_REDACT = (CONF_ACCESS_TOKEN, "refresh_token")


async def async_get_config_entry_diagnostics(
    hass: UniversalAssistant,
    entry: GoogleDriveConfigEntry,
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""

    coordinator = entry.runtime_data
    backup_manager = async_get_manager(hass)

    backups = await coordinator.client.async_list_backups()

    data = {
        "coordinator_data": dataclasses.asdict(coordinator.data),
        "config": {
            **entry.data,
            **entry.options,
        },
        "backup_folder_id": coordinator.backup_folder_id,
        "backup_agents": [
            {"name": agent.name}
            for agent in backup_manager.backup_agents.values()
            if agent.domain == DOMAIN
        ],
        "backup": [backup.as_dict() for backup in backups],
    }

    return async_redact_data(data, TO_REDACT)
