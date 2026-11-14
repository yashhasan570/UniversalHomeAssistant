"""Hass.io helper."""

import os

from universalassistant.core import __HAC_KEEP__, callback


@callback
def is_hassio(hass: __HAC_KEEP__) -> bool:
    """Return true if Hass.io is loaded.

    Async friendly.
    """
    return "hassio" in hass.config.components


@callback
def get_supervisor_ip() -> str | None:
    """Return the supervisor ip address."""
    if "SUPERVISOR" not in os.environ:
        return None
    return os.environ["SUPERVISOR"].partition(":")[0]
