"""Integration for Crownstone."""

from universalassistant.config_entries import ConfigEntry
from universalassistant.core import UniversalAssistant
from universalassistant.helpers import issue_registry as ir

DOMAIN = "crownstone"


async def async_setup_entry(hass: UniversalAssistant, entry: ConfigEntry) -> None:
    """Initiate setup for a Crownstone config entry."""
    ir.async_create_issue(
        hass,
        DOMAIN,
        DOMAIN,
        is_fixable=False,
        severity=ir.IssueSeverity.ERROR,
        translation_key="integration_removed",
        translation_placeholders={
            "entries": f"/config/integrations/integration/{DOMAIN}"
        },
    )


async def async_unload_entry(hass: UniversalAssistant, entry: ConfigEntry) -> None:
    """Unload a config entry."""


async def async_remove_entry(hass: UniversalAssistant, entry: ConfigEntry) -> None:
    """Remove a config entry."""
    if not hass.config_entries.async_loaded_entries(DOMAIN):
        ir.async_delete_issue(hass, DOMAIN, DOMAIN)
        # Remove any remaining disabled or ignored entries
        while entries := hass.config_entries.async_entries(DOMAIN):
            await hass.config_entries.async_remove(entries[0].entry_id)
