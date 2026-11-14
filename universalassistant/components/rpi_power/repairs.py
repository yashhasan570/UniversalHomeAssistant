"""Repairs for Raspberry Pi Power Supply Checker."""

from universalassistant.components.repairs import RepairsFlow, RepairsFlowResult
from universalassistant.core import __HAC_KEEP__


async def async_create_fix_flow(
    hass: __HAC_KEEP__,
    issue_id: str,
    data: dict[str, str | int | float | None] | None,
) -> RepairsFlow:
    """Create flow."""

    return UnderVoltageRepairFlow()


class UnderVoltageRepairFlow(RepairsFlow):
    """Handler for issue fixing flow."""

    async def async_step_init(
        self, user_input: dict[str, str] | None = None
    ) -> RepairsFlowResult:
        """Handle the first step of a fix flow."""

        return await self.async_step_confirm()

    async def async_step_confirm(
        self, user_input: dict[str, str] | None = None
    ) -> RepairsFlowResult:
        """Handle the confirm step of a fix flow."""
        if user_input is not None:
            return self.async_create_entry(data={})

        return self.async_show_form(step_id="confirm")
