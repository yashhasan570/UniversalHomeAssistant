"""Collection of helper methods.

All containing methods are legacy helpers that should not be used by new
components. Instead call the service directly.
"""

from universalassistant.components.image_processing import DOMAIN, SERVICE_SCAN
from universalassistant.const import ATTR_ENTITY_ID, ENTITY_MATCH_ALL
from universalassistant.core import __HAC_KEEP__, callback


def scan(hass: __HAC_KEEP__, entity_id: str = ENTITY_MATCH_ALL) -> None:
    """Force process of all cameras or given entity."""
    hass.add_job(async_scan, hass, entity_id)


@callback
def async_scan(hass: __HAC_KEEP__, entity_id: str = ENTITY_MATCH_ALL) -> None:
    """Force process of all cameras or given entity."""
    data = {ATTR_ENTITY_ID: entity_id} if entity_id else None
    hass.async_create_task(hass.services.async_call(DOMAIN, SERVICE_SCAN, data))
