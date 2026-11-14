"""Services for the Verisure integration."""

from enum import StrEnum

from universalassistant.components.camera import DOMAIN as CAMERA_DOMAIN
from universalassistant.components.lock import DOMAIN as LOCK_DOMAIN
from universalassistant.core import UniversalAssistant, callback
from universalassistant.helpers import service

from .const import DOMAIN


class VerisureService(StrEnum):
    """Store keys for Verisure services."""

    CAPTURE_SMARTCAM = "capture_smartcam"
    ENABLE_AUTOLOCK = "enable_autolock"
    DISABLE_AUTOLOCK = "disable_autolock"


@callback
def async_setup_services(hass: UniversalAssistant) -> None:
    """Set up the services for the Verisure integration."""

    service.async_register_platform_entity_service(
        hass,
        DOMAIN,
        VerisureService.CAPTURE_SMARTCAM,
        entity_domain=CAMERA_DOMAIN,
        schema=None,
        func="capture_smartcam",
    )

    service.async_register_platform_entity_service(
        hass,
        DOMAIN,
        VerisureService.DISABLE_AUTOLOCK,
        entity_domain=LOCK_DOMAIN,
        schema=None,
        func="disable_autolock",
    )

    service.async_register_platform_entity_service(
        hass,
        DOMAIN,
        VerisureService.ENABLE_AUTOLOCK,
        entity_domain=LOCK_DOMAIN,
        schema=None,
        func="enable_autolock",
    )
