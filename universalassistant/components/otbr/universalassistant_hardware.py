"""Universal Home Assistant Hardware firmware utilities."""

import logging

from yarl import URL

from universalassistant.components.hassio import AddonManager
from universalassistant.components.universalassistant_hardware.util import (
    ApplicationType,
    FirmwareInfo,
    OwningAddon,
    OwningIntegration,
    get_otbr_addon_firmware_info,
)
from universalassistant.config_entries import ConfigEntryState
from universalassistant.core import UniversalAssistant
from universalassistant.exceptions import UniversalAssistantError
from universalassistant.helpers.hassio import is_hassio

from .const import DOMAIN
from .types import OTBRConfigEntry

_LOGGER = logging.getLogger(__name__)


async def async_get_firmware_info(
    hass: UniversalAssistant, config_entry: OTBRConfigEntry
) -> FirmwareInfo | None:
    """Return firmware information for the OpenThread Border Router."""
    owners: list[OwningIntegration | OwningAddon] = [
        OwningIntegration(config_entry_id=config_entry.entry_id)
    ]

    device = None

    if is_hassio(hass) and (host := URL(config_entry.data["url"]).host) is not None:
        otbr_addon_manager = AddonManager(
            hass=hass,
            logger=_LOGGER,
            addon_name="OpenThread Border Router",
            addon_slug=host.replace("-", "_"),
        )

        if (
            addon_fw_info := await get_otbr_addon_firmware_info(
                hass, otbr_addon_manager
            )
        ) is not None:
            device = addon_fw_info.device
            owners.extend(addon_fw_info.owners)

    firmware_version = None

    if config_entry.state in (
        # This function is called during OTBR config entry setup so we need to account
        # for both config entry states
        ConfigEntryState.LOADED,
        ConfigEntryState.SETUP_IN_PROGRESS,
    ):
        try:
            firmware_version = await config_entry.runtime_data.get_coprocessor_version()
        except UniversalAssistantError:
            firmware_version = None

    if device is None:
        return None

    return FirmwareInfo(
        device=device,
        firmware_type=ApplicationType.SPINEL,
        firmware_version=firmware_version,
        source=DOMAIN,
        owners=owners,
    )
