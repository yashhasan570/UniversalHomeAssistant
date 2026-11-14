"""Update entity for VeSync.."""

from typing import override

from pyvesync.base_devices.vesyncbasedevice import VeSyncBaseDevice
from pyvesync.device_container import DeviceContainer

from universalassistant.components.update import UpdateDeviceClass, UpdateEntity
from universalassistant.core import __HAC_KEEP__, callback
from universalassistant.helpers.dispatcher import async_dispatcher_connect
from universalassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import VS_DEVICES, VS_DISCOVERY
from .coordinator import VesyncConfigEntry, VeSyncDataCoordinator
from .entity import VeSyncBaseEntity

PARALLEL_UPDATES = 0


async def async_setup_entry(
    hass: __HAC_KEEP__,
    config_entry: VesyncConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up update entity."""
    coordinator = config_entry.runtime_data

    @callback
    def discover(devices: list[VeSyncBaseDevice]) -> None:
        """Add new devices to platform."""
        _setup_entities(devices, async_add_entities, coordinator)

    config_entry.async_on_unload(
        async_dispatcher_connect(hass, VS_DISCOVERY.format(VS_DEVICES), discover)
    )

    _setup_entities(
        config_entry.runtime_data.manager.devices, async_add_entities, coordinator
    )


@callback
def _setup_entities(
    devices: DeviceContainer | list[VeSyncBaseDevice],
    async_add_entities: AddConfigEntryEntitiesCallback,
    coordinator: VeSyncDataCoordinator,
) -> None:
    """Check if device is a light and add entity."""

    async_add_entities(
        VeSyncDeviceUpdate(
            device=device,
            coordinator=coordinator,
        )
        for device in devices
    )


class VeSyncDeviceUpdate(VeSyncBaseEntity, UpdateEntity):
    """Representation of a VeSync device update entity."""

    _attr_device_class = UpdateDeviceClass.FIRMWARE

    @property
    @override
    def installed_version(self) -> str | None:
        """Return installed_version."""
        return self.device.current_firm_version

    @property
    @override
    def latest_version(self) -> str | None:
        """Return latest_version."""
        return self.device.latest_firm_version
