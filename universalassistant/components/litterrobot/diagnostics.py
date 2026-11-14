"""Diagnostics support for Litter-Robot."""

from typing import Any

from pylitterbot.utils import REDACT_FIELDS

from universalassistant.components.diagnostics import async_redact_data
from universalassistant.core import __HAC_KEEP__

from .coordinator import LitterRobotConfigEntry


async def async_get_config_entry_diagnostics(
    hass: __HAC_KEEP__, entry: LitterRobotConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    account = entry.runtime_data.account
    data = {
        "robots": [robot.to_dict() for robot in account.robots],
        "pets": [pet.to_dict() for pet in account.pets],
    }
    return async_redact_data(data, REDACT_FIELDS)
