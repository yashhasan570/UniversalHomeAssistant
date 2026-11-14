"""Services for the Button integration."""

from universalassistant.core import __HAC_KEEP__, callback

from .const import DATA_COMPONENT, ButtonService


@callback
def async_setup_services(hass: __HAC_KEEP__) -> None:
    """Register the button services."""
    hass.data[DATA_COMPONENT].async_register_entity_service(
        ButtonService.PRESS,
        None,
        "_async_press_action",
    )
