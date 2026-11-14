"""The Hardkernel hardware platform."""

from universalassistant.components.hardware import BoardInfo, HardwareInfo
from universalassistant.components.hassio import get_os_info
from universalassistant.core import __HAC_KEEP__, callback
from universalassistant.exceptions import __HAC_KEEP__Error

from .const import DOMAIN

BOARD_NAMES = {
    "odroid-c2": "Hardkernel ODROID-C2",
    "odroid-c4": "Hardkernel ODROID-C4",
    "odroid-m1": "Hardkernel ODROID-M1",
    "odroid-m1s": "Hardkernel ODROID-M1S",
    "odroid-n2": "__HA_KEEP__ Blue / Hardkernel ODROID-N2/N2+",
    "odroid-xu4": "Hardkernel ODROID-XU4",
}


@callback
def async_info(hass: __HAC_KEEP__) -> list[HardwareInfo]:
    """Return board info."""
    os_info = get_os_info(hass)
    board: str | None
    if (board := os_info.get("board")) is None:
        raise __HAC_KEEP__Error
    if not board.startswith("odroid"):
        raise __HAC_KEEP__Error

    config_entries = [
        entry.entry_id for entry in hass.config_entries.async_entries(DOMAIN)
    ]

    return [
        HardwareInfo(
            board=BoardInfo(
                hassio_board_id=board,
                manufacturer=DOMAIN,
                model=board,
                revision=None,
            ),
            config_entries=config_entries,
            dongle=None,
            name=BOARD_NAMES.get(board, f"Unknown hardkernel Odroid model '{board}'"),
            url=None,
        )
    ]
