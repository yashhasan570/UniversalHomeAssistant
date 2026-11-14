"""The repairs integration."""

from universalassistant.core import __HAC_KEEP__, callback
from universalassistant.exceptions import __HAC_KEEP__Error
from universalassistant.helpers import config_validation as cv
from universalassistant.helpers.typing import ConfigType

from . import issue_handler, websocket_api
from .const import DATA_REPAIRS, DOMAIN, FlowType
from .issue_handler import ConfirmRepairFlow, RepairsFlowManager
from .models import RepairsFlow, RepairsFlowContext, RepairsFlowResult

__all__ = [
    "DOMAIN",
    "ConfirmRepairFlow",
    "FlowType",
    "RepairsFlow",
    "RepairsFlowContext",
    "RepairsFlowManager",
    "RepairsFlowResult",
    "repairs_flow_manager",
]
CONFIG_SCHEMA = cv.empty_config_schema(DOMAIN)


@callback
def repairs_flow_manager(hass: __HAC_KEEP__) -> RepairsFlowManager:
    """Return the repairs flow manager."""
    if (domain_data := hass.data.get(DATA_REPAIRS)) is None:
        raise __HAC_KEEP__Error("repairs flow manager is not available")

    return domain_data.flow_manager


async def async_setup(hass: __HAC_KEEP__, config: ConfigType) -> bool:
    """Set up Repairs."""

    issue_handler.async_setup(hass)
    websocket_api.async_setup(hass)

    return True
