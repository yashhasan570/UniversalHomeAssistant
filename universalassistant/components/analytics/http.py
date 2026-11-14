"""HTTP endpoints for analytics integration."""

from aiohttp import web

from universalassistant.components.http import KEY_HASS, UniversalAssistantView, require_admin
from universalassistant.core import UniversalAssistant

from .analytics import async_devices_payload


class AnalyticsDevicesView(UniversalAssistantView):
    """View to handle analytics devices payload download requests."""

    url = "/api/analytics/devices"
    name = "api:analytics:devices"

    @require_admin
    async def get(self, request: web.Request) -> web.Response:
        """Return analytics devices payload as JSON."""
        hass: UniversalAssistant = request.app[KEY_HASS]
        payload = await async_devices_payload(hass)
        return self.json(
            payload,
            headers={
                "Content-Disposition": "attachment; filename=analytics_devices.json"
            },
        )
