"""Config flow for __HA_KEEP__ Backup integration."""

from typing import Any

from universalassistant.config_entries import ConfigFlow, ConfigFlowResult

from .const import DOMAIN


class BackupConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for __HA_KEEP__ Backup."""

    VERSION = 1

    async def async_step_system(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        return self.async_create_entry(title="Backup", data={})
