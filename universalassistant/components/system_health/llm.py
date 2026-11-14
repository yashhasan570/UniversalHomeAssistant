"""LLM tools for the system_health integration."""

from typing import override

from universalassistant.components.frontend import async_get_version
from universalassistant.components.llm import LLMTools
from universalassistant.core import UniversalAssistant, callback
from universalassistant.helpers.llm import (
    LLM_API_UNIVERSAL_ASSISTANT,
    LLMContext,
    Tool,
    ToolAnnotations,
    ToolInput,
    ToolResult,
)
from universalassistant.helpers.system_info import async_get_system_info
from universalassistant.util.json import JsonObjectType

from . import DOMAIN


class GetSystemInfoTool(Tool):
    """LLM Tool to get information about the system Universal Universal Home Assistant runs on."""

    name = "system_health__get_system_info"
    title = "Get system info"
    description = (
        "Get the installation type of Universal Universal Home Assistant, the time zone, and the "
        "versions of Universal Universal Home Assistant Core, the frontend, Python, the operating "
        "system, and the Supervisor. Use this for example to fill in a bug report."
    )
    annotations = ToolAnnotations(
        read_only=True, destructive=False, idempotent=True, open_world=False
    )
    integration = DOMAIN

    @override
    async def async_call(
        self, hass: UniversalAssistant, tool_input: ToolInput, llm_context: LLMContext
    ) -> ToolResult:
        """Return the system info."""
        info = await async_get_system_info(hass)
        result: JsonObjectType = {
            "installation_type": info["installation_type"],
            "core_version": info["version"],
            "frontend_version": await async_get_version(hass),
            "python_version": info["python_version"],
            "os_name": info["os_name"],
            "os_version": info["os_version"],
            "arch": info["arch"],
            "timezone": info["timezone"],
        }
        # Only set on installations with a Supervisor
        if supervisor_version := info.get("supervisor"):
            result["supervisor_version"] = supervisor_version
        if host_os := info.get("host_os"):
            result["host_os"] = host_os
        return ToolResult(data={"result": result})


@callback
def async_get_tools(
    hass: UniversalAssistant, llm_context: LLMContext, api_id: str
) -> LLMTools | None:
    """Return the system_health LLM tools for the Universal Universal Home Assistant API."""
    if api_id != LLM_API_UNIVERSAL_ASSISTANT:
        return None

    return LLMTools(tools=[GetSystemInfoTool()])
