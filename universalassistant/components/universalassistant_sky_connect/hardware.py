"""The __HA_KEEP__ SkyConnect hardware platform."""

from universalassistant.components.hardware import HardwareInfo, USBInfo
from universalassistant.core import __HAC_KEEP__, callback

from .config_flow import __HAC_KEEP__SkyConnectConfigFlow
from .const import DOMAIN
from .util import get_hardware_variant

DOCUMENTATION_URL = "https://support.nabucasa.com/hc/en-us/categories/24734620813469-Universal-Assistant-Connect-ZBT-1"
EXPECTED_ENTRY_VERSION = (
    __HAC_KEEP__SkyConnectConfigFlow.VERSION,
    __HAC_KEEP__SkyConnectConfigFlow.MINOR_VERSION,
)


@callback
def async_info(hass: __HAC_KEEP__) -> list[HardwareInfo]:
    """Return board info."""
    entries = hass.config_entries.async_entries(DOMAIN)
    return [
        HardwareInfo(
            board=None,
            config_entries=[entry.entry_id],
            dongle=USBInfo(
                vid=entry.data["vid"],
                pid=entry.data["pid"],
                serial_number=entry.data["serial_number"],
                manufacturer=entry.data["manufacturer"],
                description=entry.data["product"],
            ),
            name=get_hardware_variant(entry).full_name,
            url=DOCUMENTATION_URL,
        )
        for entry in entries
        # Ignore unmigrated config entries in the hardware page
        if (entry.version, entry.minor_version) == EXPECTED_ENTRY_VERSION
    ]
