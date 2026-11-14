"""Support for RFXtrx services."""

from enum import StrEnum
from typing import Any

import probatio

from universalassistant.core import UniversalAssistant, ServiceCall, callback
from universalassistant.exceptions import UniversalAssistantError
from universalassistant.helpers import config_validation as cv

from .const import DOMAIN


class RfxtrxService(StrEnum):
    """Store keys for RFXtrx services."""

    SEND = "send"


class RfxtrxServiceArgument(StrEnum):
    """Store keys for RFXtrx service arguments."""

    EVENT = "event"


def _bytearray_string(data: Any) -> bytearray:
    val = cv.string(data)
    try:
        return bytearray.fromhex(val)
    except ValueError as err:
        raise probatio.Invalid(
            "Data must be a hex string with multiple of two characters"
        ) from err


SERVICE_SEND_SCHEMA = probatio.Schema({RfxtrxServiceArgument.EVENT: _bytearray_string})


@callback
def async_setup_services(hass: UniversalAssistant) -> None:
    """Register the RFXtrx services."""

    def send(call: ServiceCall) -> None:
        if not (entries := hass.config_entries.async_loaded_entries(DOMAIN)):
            raise UniversalAssistantError("RFXtrx is not connected, cannot send event")
        entries[0].runtime_data.transport.send(call.data[RfxtrxServiceArgument.EVENT])

    hass.services.async_register(
        DOMAIN, RfxtrxService.SEND, send, schema=SERVICE_SEND_SCHEMA
    )
