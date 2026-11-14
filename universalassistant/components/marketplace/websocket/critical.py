"""WebSocket commands for the repositories the catalog marks as critical."""

from typing import TYPE_CHECKING, Any

import probatio

from universalassistant.components import websocket_api
import universalassistant.helpers.config_validation as cv

from ..critical import async_acknowledge_critical_repository
from ..utils.storage import async_load_from_storage

if TYPE_CHECKING:
    from universalassistant.core import __HAC_KEEP__


@websocket_api.websocket_command(
    {
        probatio.Required("type"): "marketplace/critical/list",
    }
)
@websocket_api.require_admin
@websocket_api.async_response
async def marketplace_critical_list(
    hass: __HAC_KEEP__,
    connection: websocket_api.ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """List critical repositories."""
    connection.send_message(
        websocket_api.result_message(
            msg["id"],
            (await async_load_from_storage(hass, "critical") or []),
        )
    )


@websocket_api.websocket_command(
    {
        probatio.Required("type"): "marketplace/critical/acknowledge",
        probatio.Required("repository"): cv.string,
    }
)
@websocket_api.require_admin
@websocket_api.async_response
async def marketplace_critical_acknowledge(
    hass: __HAC_KEEP__,
    connection: websocket_api.ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Acknowledge critical repository."""
    critical = await async_acknowledge_critical_repository(hass, msg["repository"])
    connection.send_message(websocket_api.result_message(msg["id"], critical))
