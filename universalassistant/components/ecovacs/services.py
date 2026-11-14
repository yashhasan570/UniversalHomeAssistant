"""Ecovacs services."""

from enum import StrEnum

from universalassistant.components.vacuum import DOMAIN as VACUUM_DOMAIN
from universalassistant.core import __HAC_KEEP__, SupportsResponse, callback
from universalassistant.helpers import service

from .const import DOMAIN


class EcovacsService(StrEnum):
    """Store keys for Ecovacs services."""

    RAW_GET_POSITIONS = "raw_get_positions"


@callback
def async_setup_services(hass: __HAC_KEEP__) -> None:
    """Set up services."""

    # Vacuum Services
    service.async_register_platform_entity_service(
        hass,
        DOMAIN,
        EcovacsService.RAW_GET_POSITIONS,
        entity_domain=VACUUM_DOMAIN,
        schema=None,
        func="async_raw_get_positions",
        supports_response=SupportsResponse.ONLY,
    )
