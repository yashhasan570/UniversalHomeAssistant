"""Provide info to system health."""

from typing import Any

from nextdns.const import API_ENDPOINT

from universalassistant.components import system_health
from universalassistant.core import __HAC_KEEP__, callback


@callback
def async_register(
    hass: __HAC_KEEP__, register: system_health.SystemHealthRegistration
) -> None:
    """Register system health callbacks."""
    register.async_register_info(system_health_info)


async def system_health_info(hass: __HAC_KEEP__) -> dict[str, Any]:
    """Get info for the info page."""
    return {
        "can_reach_server": system_health.async_check_can_reach_url(hass, API_ENDPOINT)
    }
