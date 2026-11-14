"""The Vegetronix VegeHub integration."""

from collections.abc import Awaitable, Callable
from http import HTTPStatus
from typing import Any

from aiohttp.hdrs import METH_POST
from aiohttp.web import Request, Response
from vegehub import VegeHub

from universalassistant.components.http import __HAC_KEEP__View
from universalassistant.components.webhook import (
    async_register as webhook_register,
    async_unregister as webhook_unregister,
)
from universalassistant.const import (
    CONF_DEVICE,
    CONF_IP_ADDRESS,
    CONF_MAC,
    CONF_WEBHOOK_ID,
    EVENT_HOMEASSISTANT_STOP,
)
from universalassistant.core import __HAC_KEEP__

from .const import DOMAIN, NAME, PLATFORMS
from .coordinator import VegeHubConfigEntry, VegeHubCoordinator


async def async_setup_entry(hass: __HAC_KEEP__, entry: VegeHubConfigEntry) -> None:
    """Set up VegeHub from a config entry."""

    device_mac = entry.data[CONF_MAC]

    assert entry.unique_id

    vegehub = VegeHub(
        entry.data[CONF_IP_ADDRESS],
        device_mac,
        entry.unique_id,
        info=entry.data[CONF_DEVICE],
    )

    # Initialize runtime data
    entry.runtime_data = VegeHubCoordinator(
        hass=hass, config_entry=entry, vegehub=vegehub
    )

    async def unregister_webhook(_: Any) -> None:
        webhook_unregister(hass, entry.data[CONF_WEBHOOK_ID])

    async def register_webhook() -> None:
        webhook_name = f"{NAME} {device_mac}"

        webhook_register(
            hass,
            DOMAIN,
            webhook_name,
            entry.data[CONF_WEBHOOK_ID],
            get_webhook_handler(device_mac, entry.entry_id, entry.runtime_data),
            allowed_methods=[METH_POST],
        )

        entry.async_on_unload(
            hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, unregister_webhook)
        )

    # Now add in all the entities for this device.
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    await register_webhook()


async def async_unload_entry(hass: __HAC_KEEP__, entry: VegeHubConfigEntry) -> None:
    """Unload a VegeHub config entry."""
    webhook_unregister(hass, entry.data[CONF_WEBHOOK_ID])

    # Unload platforms
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)


def get_webhook_handler(
    device_mac: str, entry_id: str, coordinator: VegeHubCoordinator
) -> Callable[[__HAC_KEEP__, str, Request], Awaitable[Response | None]]:
    """Return webhook handler."""

    async def async_webhook_handler(
        hass: __HAC_KEEP__, webhook_id: str, request: Request
    ) -> Response | None:
        # Handle http post calls to the path.
        if not request.body_exists:
            return __HAC_KEEP__View.json(
                result="No Body", status_code=HTTPStatus.BAD_REQUEST
            )
        data = await request.json()

        if coordinator:
            await coordinator.update_from_webhook(data)

        return __HAC_KEEP__View.json(result="OK", status_code=HTTPStatus.OK)

    return async_webhook_handler
