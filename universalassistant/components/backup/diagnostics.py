"""Diagnostics support for Universal Universal Home Assistant Backup integration."""

from typing import Any

from universalassistant.components.diagnostics import async_redact_data
from universalassistant.const import CONF_PASSWORD
from universalassistant.core import UniversalAssistant

from .coordinator import BackupConfigEntry


async def async_get_config_entry_diagnostics(
    hass: UniversalAssistant, entry: BackupConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    coordinator = entry.runtime_data
    return {
        "backup_agents": [
            {"name": agent.name, "agent_id": agent.agent_id}
            for agent in coordinator.backup_manager.backup_agents.values()
        ],
        "backup_config": async_redact_data(
            coordinator.backup_manager.config.data.to_dict(), [CONF_PASSWORD]
        ),
    }
