"""Support for VeSync Services."""

from enum import StrEnum

from pyvesync.base_devices import VeSyncBaseDevice
from pyvesync.utils.errors import VeSyncError

from universalassistant.config_entries import ConfigEntryState
from universalassistant.core import UniversalAssistant, ServiceCall, callback
from universalassistant.exceptions import UniversalAssistantError, ServiceValidationError
from universalassistant.helpers.dispatcher import async_dispatcher_send

from .const import DOMAIN, VS_DEVICES, VS_DISCOVERY
from .coordinator import VesyncConfigEntry


class VeSyncService(StrEnum):
    """Store keys for VeSync services."""

    UPDATE_DEVICES = "update_devices"


@callback
def async_setup_services(hass: UniversalAssistant) -> None:
    """Handle for services."""

    hass.services.async_register(
        DOMAIN, VeSyncService.UPDATE_DEVICES, async_new_device_discovery
    )


async def async_new_device_discovery(call: ServiceCall) -> None:
    """Discover and add new devices."""

    entries = call.hass.config_entries.async_entries(DOMAIN)
    config_entry: VesyncConfigEntry | None = entries[0] if entries else None

    if not config_entry:
        raise ServiceValidationError("Entry not found")
    if config_entry.state is not ConfigEntryState.LOADED:
        raise ServiceValidationError("Entry not loaded")
    manager = config_entry.runtime_data.manager
    known_devices = list(manager.devices)
    new_devices: list[VeSyncBaseDevice] = []
    try:
        await manager.get_devices()
        new_devices = [
            device for device in manager.devices if device not in known_devices
        ]
        update_error: VeSyncError | None = None
        for device in new_devices:
            try:
                await device.update()
            except VeSyncError as err:
                if update_error is None:
                    update_error = err
        if update_error is not None:
            raise update_error
    except VeSyncError as err:
        raise UniversalAssistantError(
            translation_domain=DOMAIN, translation_key="api_response_error"
        ) from err
    finally:
        # Devices get_devices added count as known on the next call
        if new_devices:
            async_dispatcher_send(
                call.hass, VS_DISCOVERY.format(VS_DEVICES), new_devices
            )
