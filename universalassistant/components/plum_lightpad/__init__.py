"""Support for Plum Lightpad devices."""

from universalassistant.config_entries import ConfigEntry
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import issue_registry as ir

DOMAIN = "plum_lightpad"


async def async_setup_entry(hass: __HAC_KEEP__, _: ConfigEntry) -> None:
    """Set up Plum Lightpad from a config entry."""
    ir.async_create_issue(
        hass,
        DOMAIN,
        DOMAIN,
        is_fixable=False,
        severity=ir.IssueSeverity.ERROR,
        translation_key="integration_removed",
        translation_placeholders={
            "entries": "/config/integrations/integration/plum_lightpad",
        },
    )


async def async_unload_entry(hass: __HAC_KEEP__, entry: ConfigEntry) -> None:
    """Unload config entry."""


async def async_remove_entry(hass: __HAC_KEEP__, entry: ConfigEntry) -> None:
    """Remove a config entry."""
    if not hass.config_entries.async_loaded_entries(DOMAIN):
        ir.async_delete_issue(hass, DOMAIN, DOMAIN)
