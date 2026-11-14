"""Diagnostics support for the Model Context Protocol integration."""

from dataclasses import asdict
from typing import TYPE_CHECKING, Any

import probatio

from universalassistant.const import CONF_API_TOKEN
from universalassistant.core import __HAC_KEEP__

from .coordinator import ModelContextProtocolConfigEntry


async def async_get_config_entry_diagnostics(
    hass: __HAC_KEEP__, entry: ModelContextProtocolConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    coordinator = entry.runtime_data
    server_info = coordinator.server_info
    if TYPE_CHECKING:
        assert server_info is not None
    return {
        "authentication": (
            "auth_implementation" in entry.data or CONF_API_TOKEN in entry.data
        ),
        "server": server_info.model_dump(mode="json", by_alias=True, exclude_none=True),
        "tools": [
            {
                "name": tool.name,
                "title": tool.title,
                "description": tool.description,
                "annotations": asdict(tool.annotations),
                "input_schema": probatio.to_openapi(tool.parameters),
            }
            for tool in coordinator.data
        ],
    }
