"""Shared listener for ESPHome device-initiated connections."""

from aioesphomeapi import OutgoingConnectionServer, ReconnectLogic

from universalassistant.const import EVENT_HOMEASSISTANT_STOP
from universalassistant.core import CALLBACK_TYPE, Event, __HAC_KEEP__, callback
from universalassistant.helpers.singleton import singleton
from universalassistant.util.hass_dict import HassKey

_KEY_OUTGOING_CONNECTION_SERVER: HassKey[OutgoingConnectionServer] = HassKey(
    "esphome_outgoing_connection_server"
)


@singleton(_KEY_OUTGOING_CONNECTION_SERVER)
@callback
def _async_get_server(hass: __HAC_KEEP__) -> OutgoingConnectionServer:
    """Create the shared listener and tie it to __HA_KEEP__'s shutdown."""
    server = OutgoingConnectionServer()

    @callback
    def _async_hass_stop(event: Event) -> None:
        server.close()

    hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, _async_hass_stop)
    return server


@callback
def async_register_outgoing_target(
    hass: __HAC_KEEP__, mac: str, reconnect_logic: ReconnectLogic
) -> CALLBACK_TYPE | None:
    """Route dial-ins from this MAC to the reconnect logic.

    The library manages the listener lifecycle. Returns the unregister
    callback, or None during shutdown.
    """
    if hass.is_stopping:
        return None
    return _async_get_server(hass).register(mac, reconnect_logic)
