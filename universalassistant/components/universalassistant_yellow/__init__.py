"""The __HA_KEEP__ Yellow integration."""

from dataclasses import dataclass
import logging

from universalassistant.components.hassio import HassioNotReadyError, get_os_info
from universalassistant.components.universalassistant_hardware.coordinator import (
    FirmwareUpdateCoordinator,
)
from universalassistant.components.universalassistant_hardware.repair_helpers import (
    async_create_multi_pan_migration_issue,
    async_delete_multi_pan_migration_issue,
)
from universalassistant.components.universalassistant_hardware.silabs_multiprotocol_addon import (
    check_multi_pan_addon,
    multi_pan_addon_using_device,
)
from universalassistant.components.universalassistant_hardware.util import (
    ApplicationType,
    guess_firmware_info,
)
from universalassistant.components.usb import (
    SerialDevice,
    USBDevice,
    async_register_serial_port_scanner,
)
from universalassistant.config_entries import SOURCE_HARDWARE, ConfigEntry
from universalassistant.core import __HAC_KEEP__, callback
from universalassistant.exceptions import (
    ConfigEntryError,
    ConfigEntryNotReady,
    __HAC_KEEP__Error,
)
from universalassistant.helpers import discovery_flow
from universalassistant.helpers.aiohttp_client import async_get_clientsession
from universalassistant.helpers.hassio import is_hassio

from .const import (
    DOMAIN,
    FIRMWARE,
    FIRMWARE_VERSION,
    MANUFACTURER,
    NABU_CASA_FIRMWARE_RELEASES_URL,
    RADIO_DEVICE,
    ZHA_HW_DISCOVERY_DATA,
)

_LOGGER = logging.getLogger(__name__)

type __HAC_KEEP__YellowConfigEntry = ConfigEntry[__HAC_KEEP__YellowData]

__all__ = [
    "DOMAIN",
    "RADIO_DEVICE",
]


@dataclass
class __HAC_KEEP__YellowData:
    """Runtime data definition."""

    coordinator: (
        FirmwareUpdateCoordinator  # Type from universalassistant_hardware.coordinator
    )


async def async_setup_entry(
    hass: __HAC_KEEP__, entry: __HAC_KEEP__YellowConfigEntry
) -> None:
    """Set up a __HA_KEEP__ Yellow config entry."""
    if not is_hassio(hass):
        # Not running under supervisor, __HA_KEEP__ may have been migrated
        hass.async_create_task(hass.config_entries.async_remove(entry.entry_id))
        raise ConfigEntryError(
            translation_domain=DOMAIN,
            translation_key="not_hassio",
        )

    try:
        os_info = get_os_info(hass)
    except HassioNotReadyError as err:
        raise ConfigEntryNotReady from err

    if os_info.get("board") != "yellow":
        # Not running on a __HA_KEEP__ Yellow, __HA_KEEP__ may have been migrated
        hass.async_create_task(hass.config_entries.async_remove(entry.entry_id))
        raise ConfigEntryError(
            translation_domain=DOMAIN,
            translation_key="unsupported_board",
            translation_placeholders={"board": str(os_info.get("board"))},
        )

    firmware = ApplicationType(entry.data[FIRMWARE])

    # Auto start the multiprotocol addon if it is in use
    if firmware is ApplicationType.CPC:
        try:
            await check_multi_pan_addon(hass)
        except __HAC_KEEP__Error as err:
            raise ConfigEntryNotReady from err

    try:
        multipan_using_device = await multi_pan_addon_using_device(hass, RADIO_DEVICE)
    except __HAC_KEEP__Error as err:
        raise ConfigEntryNotReady from err

    if multipan_using_device:
        async_create_multi_pan_migration_issue(hass, DOMAIN, entry)
    else:
        async_delete_multi_pan_migration_issue(hass, DOMAIN, entry)

    if firmware is ApplicationType.EZSP:
        discovery_flow.async_create_flow(
            hass,
            "zha",
            context={"source": SOURCE_HARDWARE},
            data=ZHA_HW_DISCOVERY_DATA,
        )

    @callback
    def _scan_serial_ports(hass: __HAC_KEEP__) -> list[USBDevice | SerialDevice]:
        """Contribute the Yellow's built-in Zigbee radio port."""
        return [
            SerialDevice(
                device=RADIO_DEVICE,
                serial_number=None,
                manufacturer=MANUFACTURER,
                description="Yellow Zigbee Radio",
            )
        ]

    entry.async_on_unload(async_register_serial_port_scanner(hass, _scan_serial_ports))

    # Create and store the firmware update coordinator in runtime_data
    session = async_get_clientsession(hass)
    coordinator = FirmwareUpdateCoordinator(
        hass,
        entry,
        session,
        NABU_CASA_FIRMWARE_RELEASES_URL,
    )
    entry.runtime_data = __HAC_KEEP__YellowData(coordinator)

    await hass.config_entries.async_forward_entry_setups(entry, ["switch", "update"])


async def async_unload_entry(
    hass: __HAC_KEEP__, entry: __HAC_KEEP__YellowConfigEntry
) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(
        entry, ["switch", "update"]
    )


async def async_migrate_entry(
    hass: __HAC_KEEP__, config_entry: __HAC_KEEP__YellowConfigEntry
) -> None:
    """Migrate old entry."""

    _LOGGER.debug(
        "Migrating from version %s.%s", config_entry.version, config_entry.minor_version
    )

    if config_entry.version == 1:
        if config_entry.minor_version == 1:
            # Add-on startup with type service get started before
            # Core, always (e.g. the Multi-Protocol add-on).
            # Probing the firmware would interfere with the
            # add-on, so we can't safely probe here. Instead,
            # we must make an educated guess!
            firmware_guess = await guess_firmware_info(hass, RADIO_DEVICE)

            new_data = {**config_entry.data}
            new_data[FIRMWARE] = firmware_guess.firmware_type.value

            hass.config_entries.async_update_entry(
                config_entry,
                data=new_data,
                version=1,
                minor_version=2,
            )

        if config_entry.minor_version <= 3:
            # Add a `firmware_version` key if it doesn't exist to handle entries created
            # with minor version 1.3 where the firmware version was not set.
            hass.config_entries.async_update_entry(
                config_entry,
                data={
                    **config_entry.data,
                    FIRMWARE_VERSION: config_entry.data.get(FIRMWARE_VERSION),
                },
                version=1,
                minor_version=4,
            )

    _LOGGER.debug(
        "Migration to version %s.%s successful",
        config_entry.version,
        config_entry.minor_version,
    )
