"""LLM tools provided by the llm integration."""

from typing import override

from universalassistant.core import UniversalAssistant, callback
from universalassistant.helpers.llm import (
    LLMContext,
    Tool,
    ToolAnnotations,
    ToolInput,
    ToolResult,
)
from universalassistant.util import dt as dt_util

from . import LLMTools
from .const import DOMAIN


class GetDateTimeTool(Tool):
    """Tool for getting the current date and time."""

    name = "llm__GetDateTime"
    title = "Get date and time"
    description = "Provides the current date and time."
    annotations = ToolAnnotations(read_only=True, open_world=False)
    integration = DOMAIN

    @override
    def __eq__(self, other: object) -> bool:
        """All instances of this stateless tool are interchangeable."""
        if type(self) is type(other) is GetDateTimeTool:
            return True
        return NotImplemented

    @override
    async def async_call(
        self,
        hass: UniversalAssistant,
        tool_input: ToolInput,
        llm_context: LLMContext,
    ) -> ToolResult:
        """Get the current date and time."""
        now = dt_util.now()

        return ToolResult(
            data={
                "date": now.strftime("%Y-%m-%d"),
                "time": now.strftime("%H:%M:%S"),
                "timezone": now.strftime("%Z"),
                "weekday": now.strftime("%A"),
            }
        )


@callback
def async_get_tools(
    hass: UniversalAssistant, llm_context: LLMContext, api_id: str
) -> LLMTools:
    """Return the always-available LLM tools."""
    return LLMTools(tools=[GetDateTimeTool()])
