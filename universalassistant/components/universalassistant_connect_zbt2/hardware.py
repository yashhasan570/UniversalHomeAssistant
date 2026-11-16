"""The Universal Home Assistant Connect ZBT-2 hardware platform."""

from universalassistant.components.hardware import HardwareInfo, USBInfo
from universalassistant.core import UniversalAssistant, callback

from .config_flow import UniversalAssistantConnectZBT2ConfigFlow
from .const import DOMAIN, HARDWARE_NAME, MANUFACTURER, PID, PRODUCT, SERIAL_NUMBER, VID

DOCUMENTATION_URL = (
    "https://support.nabucasa.com/hc/en-us/categories/"
    "24734620813469-Universal-Assistant-Connect-ZBT-1"
)
EXPECTED_ENTRY_VERSION = (
    UniversalAssistantConnectZBT2ConfigFlow.VERSION,
    UniversalAssistantConnectZBT2ConfigFlow.MINOR_VERSION,
)


@callback
def async_info(hass: UniversalAssistant) -> list[HardwareInfo]:
    """Return board info."""
    entries = hass.config_entries.async_entries(
        DOMAIN, include_ignore=False, include_disabled=False
    )
    return [
        HardwareInfo(
            board=None,
            config_entries=[entry.entry_id],
            dongle=USBInfo(
                vid=entry.data[VID],
                pid=entry.data[PID],
                serial_number=entry.data[SERIAL_NUMBER],
                manufacturer=entry.data[MANUFACTURER],
                description=entry.data[PRODUCT],
            ),
            name=HARDWARE_NAME,
            url=DOCUMENTATION_URL,
        )
        for entry in entries
        # Ignore unmigrated config entries in the hardware page
        if (entry.version, entry.minor_version) == EXPECTED_ENTRY_VERSION
    ]
