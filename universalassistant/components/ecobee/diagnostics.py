"""Diagnostics support for ecobee."""

from typing import Any

from universalassistant.components.diagnostics import async_redact_data
from universalassistant.core import __HAC_KEEP__

from . import EcobeeConfigEntry

TO_REDACT = {
    "city",
    "code",
    "coordinates",
    "country",
    "emailAddresses",
    "identifier",
    "mapCoordinates",
    "phoneNumber",
    "postalCode",
    "provinceState",
    "streetAddress",
    "weatherStation",
}


async def async_get_config_entry_diagnostics(
    hass: __HAC_KEEP__, entry: EcobeeConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    return {
        "thermostats": async_redact_data(
            entry.runtime_data.ecobee.thermostats, TO_REDACT
        ),
    }
