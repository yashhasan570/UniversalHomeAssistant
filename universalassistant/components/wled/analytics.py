"""Analytics platform."""

from universalassistant.components.analytics import AnalyticsInput, AnalyticsModifications
from universalassistant.core import __HAC_KEEP__


async def async_modify_analytics(
    hass: __HAC_KEEP__, analytics_input: AnalyticsInput
) -> AnalyticsModifications:
    """Modify the analytics."""
    return AnalyticsModifications(remove=True)
