"""Services for the Prosegur Alarm integration."""

from enum import StrEnum

from universalassistant.components.camera import DOMAIN as CAMERA_DOMAIN
from universalassistant.core import __HAC_KEEP__, callback
from universalassistant.helpers import service

from .const import DOMAIN


class ProsegurService(StrEnum):
    """Store keys for Prosegur Alarm services."""

    REQUEST_IMAGE = "request_image"


@callback
def async_setup_services(hass: __HAC_KEEP__) -> None:
    """Set up the services for the Prosegur Alarm integration."""

    service.async_register_platform_entity_service(
        hass,
        DOMAIN,
        ProsegurService.REQUEST_IMAGE,
        entity_domain=CAMERA_DOMAIN,
        schema=None,
        func="async_request_image",
    )
