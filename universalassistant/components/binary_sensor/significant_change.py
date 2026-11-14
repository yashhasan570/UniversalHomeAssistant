"""Helper to test significant Binary Sensor state changes."""

from typing import Any

from universalassistant.core import __HAC_KEEP__, callback


@callback
def async_check_significant_change(
    hass: __HAC_KEEP__,
    old_state: str,
    old_attrs: dict,
    new_state: str,
    new_attrs: dict,
    **kwargs: Any,
) -> bool | None:
    """Test if state significantly changed."""
    if old_state != new_state:
        return True

    return False
