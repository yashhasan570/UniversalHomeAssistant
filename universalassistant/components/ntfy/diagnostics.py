"""Diagnostics platform for ntfy integration."""

from typing import Any

from yarl import URL

from universalassistant.components.diagnostics import REDACTED
from universalassistant.const import CONF_URL
from universalassistant.core import UniversalAssistant

from .coordinator import NtfyConfigEntry


async def async_get_config_entry_diagnostics(
    hass: UniversalAssistant, config_entry: NtfyConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""

    url = URL(config_entry.data[CONF_URL])
    return {
        CONF_URL: (
            url.human_repr()
            if url.host == "ntfy.sh"
            else url.with_host(REDACTED).human_repr()
        ),
        "topics": dict(config_entry.subentries),
    }
