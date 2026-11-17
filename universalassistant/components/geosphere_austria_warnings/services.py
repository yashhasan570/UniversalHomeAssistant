"""Services for the GeoSphere Austria Warnings integration."""

from typing import cast

import probatio

from universalassistant.const import ATTR_CONFIG_ENTRY_ID
from universalassistant.core import (
    UniversalAssistant,
    ServiceCall,
    ServiceResponse,
    SupportsResponse,
    callback,
)
from universalassistant.exceptions import UniversalAssistantError
from universalassistant.helpers import service
from universalassistant.helpers.selector import ConfigEntrySelector

from .const import DOMAIN, GeoSphereService
from .coordinator import GeoSphereConfigEntry
from .warnings import serialize_warnings

SERVICE_GET_WARNINGS_SCHEMA = probatio.Schema(
    {
        probatio.Required(ATTR_CONFIG_ENTRY_ID): ConfigEntrySelector(
            {"integration": DOMAIN}
        )
    }
)


@callback
def async_setup_services(hass: UniversalAssistant) -> None:
    """Set up the GeoSphere Austria Warnings services."""

    async def get_warnings(call: ServiceCall) -> ServiceResponse:
        """Return cached warnings for the selected config entry."""
        entry = cast(
            GeoSphereConfigEntry,
            service.async_get_config_entry(
                hass,
                DOMAIN,
                call.data[ATTR_CONFIG_ENTRY_ID],
            ),
        )
        coordinator = entry.runtime_data

        if not coordinator.last_update_success:
            raise UniversalAssistantError(
                translation_domain=DOMAIN,
                translation_key="warnings_unavailable",
            )

        data = coordinator.data

        return {
            "active_warnings": serialize_warnings(data.active_warnings),
            "advance_warnings": serialize_warnings(data.advance_warnings),
        }

    hass.services.async_register(
        DOMAIN,
        GeoSphereService.GET_WARNINGS,
        get_warnings,
        schema=SERVICE_GET_WARNINGS_SCHEMA,
        supports_response=SupportsResponse.ONLY,
    )
