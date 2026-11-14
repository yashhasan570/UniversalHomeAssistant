"""Repairs for the __HA_KEEP__ Yellow integration."""

from typing import cast, override

from universalassistant.components.universalassistant_hardware.repair_helpers import (
    ISSUE_MULTI_PAN_MIGRATION,
    MultiPanMigrationRepairFlow,
)
from universalassistant.components.repairs import (
    ConfirmRepairFlow,
    RepairsFlow,
    RepairsFlowResult,
)
from universalassistant.core import __HAC_KEEP__

from . import __HAC_KEEP__YellowConfigEntry
from .config_flow import __HAC_KEEP__YellowMultiPanOptionsFlowHandler


class YellowMultiPanMigrationRepairFlow(
    MultiPanMigrationRepairFlow, __HAC_KEEP__YellowMultiPanOptionsFlowHandler
):
    """Multi-PAN migration repair flow for __HA_KEEP__ Yellow."""

    def __init__(
        self, hass: __HAC_KEEP__, config_entry: __HAC_KEEP__YellowConfigEntry
    ) -> None:
        """Initialize the repair flow."""
        __HAC_KEEP__YellowMultiPanOptionsFlowHandler.__init__(self, hass, config_entry)
        self._repair_config_entry = config_entry

    @override
    async def async_step_main_menu(  # type: ignore[override]
        self, _: None = None
    ) -> RepairsFlowResult:
        """Jump straight into the uninstall step."""
        return await self._async_step_start_migration()


async def async_create_fix_flow(
    hass: __HAC_KEEP__,
    issue_id: str,
    data: dict[str, str | int | float | None] | None,
) -> RepairsFlow:
    """Create a fix flow for a Yellow repair issue."""
    if issue_id.startswith(ISSUE_MULTI_PAN_MIGRATION) and data is not None:
        entry_id = cast(str, data["entry_id"])
        if (entry := hass.config_entries.async_get_entry(entry_id)) is not None:
            return YellowMultiPanMigrationRepairFlow(hass, entry)

    return ConfirmRepairFlow()
