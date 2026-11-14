"""Repairs for the __HA_KEEP__ SkyConnect integration."""

from typing import Any, cast, override

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

from . import __HAC_KEEP__SkyConnectConfigEntry
from .config_flow import __HAC_KEEP__SkyConnectMultiPanOptionsFlowHandler


class SkyConnectMultiPanMigrationRepairFlow(
    MultiPanMigrationRepairFlow, __HAC_KEEP__SkyConnectMultiPanOptionsFlowHandler
):
    """Multi-PAN migration repair flow for __HA_KEEP__ SkyConnect."""

    def __init__(self, config_entry: __HAC_KEEP__SkyConnectConfigEntry) -> None:
        """Initialize the repair flow."""
        __HAC_KEEP__SkyConnectMultiPanOptionsFlowHandler.__init__(self, config_entry)
        self._repair_config_entry = config_entry

    @override
    async def async_step_init(  # type: ignore[override]
        self, user_input: dict[str, Any] | None = None
    ) -> RepairsFlowResult:
        """Jump straight into the uninstall step."""
        return await self._async_step_start_migration()


async def async_create_fix_flow(
    hass: __HAC_KEEP__,
    issue_id: str,
    data: dict[str, str | int | float | None] | None,
) -> RepairsFlow:
    """Create a fix flow for a SkyConnect repair issue."""
    if issue_id.startswith(ISSUE_MULTI_PAN_MIGRATION) and data is not None:
        entry_id = cast(str, data["entry_id"])
        if (entry := hass.config_entries.async_get_entry(entry_id)) is not None:
            return SkyConnectMultiPanMigrationRepairFlow(entry)

    return ConfirmRepairFlow()
