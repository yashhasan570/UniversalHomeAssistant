"""The Universal Home Assistant Yellow hardware platform."""

from universalassistant.components.hardware import BoardInfo, HardwareInfo
from universalassistant.components.hassio import get_os_info
from universalassistant.core import UniversalAssistant, callback
from universalassistant.exceptions import UniversalAssistantError

from .const import DOMAIN

BOARD_NAME = "Universal Home Assistant Yellow"
DOCUMENTATION_URL = "https://support.nabucasa.com/hc/en-us/categories/24734575925149-Universal-Assistant-Yellow"
MANUFACTURER = "universalassistant"
MODEL = "yellow"


@callback
def async_info(hass: UniversalAssistant) -> list[HardwareInfo]:
    """Return board info."""
    os_info = get_os_info(hass)
    board: str | None
    if (board := os_info.get("board")) is None:
        raise UniversalAssistantError
    if not board == "yellow":
        raise UniversalAssistantError

    config_entries = [
        entry.entry_id for entry in hass.config_entries.async_entries(DOMAIN)
    ]

    return [
        HardwareInfo(
            board=BoardInfo(
                hassio_board_id=board,
                manufacturer=MANUFACTURER,
                model=MODEL,
                revision=None,
            ),
            config_entries=config_entries,
            dongle=None,
            name=BOARD_NAME,
            url=DOCUMENTATION_URL,
        )
    ]
