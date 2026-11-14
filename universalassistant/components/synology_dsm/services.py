"""The Synology DSM component."""

from enum import StrEnum
import logging
from typing import cast

import probatio
from synology_dsm.exceptions import SynologyDSMException

from universalassistant.config_entries import ConfigEntryState
from universalassistant.core import UniversalAssistant, ServiceCall, callback
from universalassistant.exceptions import UniversalAssistantError, ServiceValidationError
from universalassistant.helpers import issue_registry as ir
from universalassistant.helpers.service import async_register_admin_service

from .const import DOMAIN
from .coordinator import SynologyDSMConfigEntry

LOGGER = logging.getLogger(__name__)


class SynologyDSMService(StrEnum):
    """Store keys for Synology DSM services."""

    REBOOT = "reboot"
    SHUTDOWN = "shutdown"


class SynologyDSMServiceArgument(StrEnum):
    """Store keys for Synology DSM service arguments."""

    SERIAL = "serial"


async def _service_handler(call: ServiceCall) -> None:
    """Handle service call."""
    serial: str | None = call.data.get(SynologyDSMServiceArgument.SERIAL)
    entries: list[SynologyDSMConfigEntry] = (
        call.hass.config_entries.async_loaded_entries(DOMAIN)
    )
    dsm_devices = {cast(str, entry.unique_id): entry.runtime_data for entry in entries}

    if serial:
        entry: SynologyDSMConfigEntry | None = (
            call.hass.config_entries.async_entry_for_domain_unique_id(DOMAIN, serial)
        )
        if not entry:
            raise UniversalAssistantError(
                translation_domain=DOMAIN,
                translation_key="serial_not_found",
                translation_placeholders={"serial": serial},
            )
        if entry.state is not ConfigEntryState.LOADED:
            raise ServiceValidationError(
                translation_domain=DOMAIN,
                translation_key="entry_not_loaded",
                translation_placeholders={"serial": serial},
            )
        dsm_device = entry.runtime_data
    elif len(dsm_devices) == 1:
        dsm_device = next(iter(dsm_devices.values()))
        serial = next(iter(dsm_devices))
    else:
        raise UniversalAssistantError(
            translation_domain=DOMAIN,
            translation_key="missing_serial",
            translation_placeholders={"serials": ", ".join(sorted(dsm_devices))},
        )

    if call.service in [SynologyDSMService.REBOOT, SynologyDSMService.SHUTDOWN]:
        LOGGER.debug("%s DSM with serial %s", call.service, serial)
        ir.async_create_issue(
            call.hass,
            DOMAIN,
            f"deprecated_action_{call.service}",
            breaks_in_ha_version="2027.6.0",
            is_fixable=False,
            severity=ir.IssueSeverity.WARNING,
            translation_key="deprecated_action",
            translation_placeholders={"action": f"{DOMAIN}.{call.service}"},
        )
        dsm_api = dsm_device.api
        try:
            await getattr(dsm_api, f"async_{call.service}")()
        except SynologyDSMException as ex:
            raise UniversalAssistantError(
                translation_domain=DOMAIN,
                translation_key="execution_error",
                translation_placeholders={
                    "action": call.service,
                    "serial": serial,
                    "error": str(ex),
                },
            ) from ex


@callback
def async_setup_services(hass: UniversalAssistant) -> None:
    """Service handler setup."""

    for service in SynologyDSMService:
        # The call data is left as permissive as it has always been here, the
        # helper would otherwise reject the optional serial with its default
        # empty schema.
        async_register_admin_service(
            hass,
            DOMAIN,
            service,
            _service_handler,
            probatio.Schema({}, extra=probatio.ALLOW_EXTRA),
        )
