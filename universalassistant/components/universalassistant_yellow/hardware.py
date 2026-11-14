"""The __HA_KEEP__ Yellow hardware platform."""

from universalassistant.components.hardware import BoardInfo, HardwareInfo
from universalassistant.components.hassio import get_os_info
from universalassistant.core import __HAC_KEEP__, callback
from universalassistant.exceptions import __HAC_KEEP__Error

from .const import DOMAIN

BOARD_NAME = "__HA_KEEP__ Yellow"
DOCUMENTATION_URL = "https://support.nabucasa.com/hc/en-us/categories/24734575925149-Universal-Assistant-Yellow"
MANUFACTURER = "universalassistant"
MODEL = "yellow"


@callback
def async_info(hass: __HAC_KEEP__) -> list[HardwareInfo]:
    """Return board info."""
    os_info = get_os_info(hass)
    board: str | None
    if (board := os_info.get("board")) is None:
        raise __HAC_KEEP__Error
    if not board == "yellow":
        raise __HAC_KEEP__Error

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
