"""Diagnostics support for UniFi Network."""

from typing import Any

from uiprotect.anonymize import anonymize_data

from universalassistant.components.diagnostics import async_redact_data
from universalassistant.core import __HAC_KEEP__

from .data import UFPConfigEntry

# Redact on top of the library anonymizer: stream URLs hold a secret alias.
TO_REDACT = {"rtspsStreams"}


async def async_get_config_entry_diagnostics(
    hass: __HAC_KEEP__, config_entry: UFPConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""

    api = config_entry.runtime_data.api
    diagnostics: dict[str, Any] = {"options": dict(config_entry.options)}
    if not api.is_public_only:
        diagnostics["bootstrap"] = anonymize_data(api.bootstrap.unifi_dict())
    if api.has_public_bootstrap:
        diagnostics["public_bootstrap"] = async_redact_data(
            api.public_bootstrap.to_diagnostics(), TO_REDACT
        )
    return diagnostics
