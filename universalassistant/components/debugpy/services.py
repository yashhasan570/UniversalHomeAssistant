"""Services for the Remote Python Debugger integration."""

from enum import StrEnum

import probatio

from universalassistant.core import __HAC_KEEP__, ServiceCall, callback
from universalassistant.helpers.service import async_register_admin_service

from .const import DOMAIN
from .helpers import async_start_debugger


class DebugpyService(StrEnum):
    """Store keys for Remote Python Debugger services."""

    START = "start"


async def _debug_start(call: ServiceCall) -> None:
    """Enable asyncio debugging and start the debugger."""
    await async_start_debugger(call.hass)


@callback
def async_setup_services(hass: __HAC_KEEP__) -> None:
    """Set up the services for the Remote Python Debugger integration."""
    async_register_admin_service(
        hass, DOMAIN, DebugpyService.START, _debug_start, schema=probatio.Schema({})
    )
