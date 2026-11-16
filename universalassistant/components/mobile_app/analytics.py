"""Analytics platform."""

from universalassistant.components.analytics import AnalyticsInput, AnalyticsModifications
from universalassistant.core import UniversalAssistant


async def async_modify_analytics(
    hass: UniversalAssistant, analytics_input: AnalyticsInput
) -> AnalyticsModifications:
    """Modify the analytics."""
    return AnalyticsModifications(remove=True)
