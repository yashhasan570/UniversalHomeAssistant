"""Send instance and usage analytics."""

from typing import Any

import probatio

from universalassistant.components import labs, websocket_api
from universalassistant.components.hassio import HassioNotReadyError
from universalassistant.config_entries import SOURCE_SYSTEM, ConfigEntry
from universalassistant.core import __HAC_KEEP__, callback
from universalassistant.exceptions import ConfigEntryNotReady
from universalassistant.helpers import discovery_flow
from universalassistant.helpers.start import async_at_started
from universalassistant.helpers.typing import ConfigType
from universalassistant.util.hass_dict import HassKey

from .analytics import (
    Analytics,
    AnalyticsInput,
    AnalyticsModifications,
    DeviceAnalyticsModifications,
    EntityAnalyticsModifications,
    async_devices_payload,
)
from .const import (
    ATTR_ONBOARDED,
    ATTR_PREFERENCES,
    ATTR_SNAPSHOTS,
    DOMAIN,
    PREFERENCE_SCHEMA,
)
from .http import AnalyticsDevicesView

__all__ = [
    "AnalyticsInput",
    "AnalyticsModifications",
    "DeviceAnalyticsModifications",
    "EntityAnalyticsModifications",
    "async_devices_payload",
]

CONF_SNAPSHOTS_URL = "snapshots_url"

CONFIG_SCHEMA = probatio.Schema(
    {
        DOMAIN: probatio.Schema(
            {
                probatio.Optional(CONF_SNAPSHOTS_URL): probatio.Any(str, None),
            }
        )
    },
    extra=probatio.ALLOW_EXTRA,
)

DATA_COMPONENT: HassKey[Analytics] = HassKey(DOMAIN)
_DATA_SNAPSHOTS_URL: HassKey[str | None] = HassKey(f"{DOMAIN}_snapshots_url")

LABS_SNAPSHOT_FEATURE = "snapshots"


async def async_setup(hass: __HAC_KEEP__, config: ConfigType) -> bool:
    """Set up the analytics integration."""
    analytics_config = config.get(DOMAIN, {})

    snapshots_url: str | None = None
    if CONF_SNAPSHOTS_URL in analytics_config:
        await labs.async_update_preview_feature(
            hass, DOMAIN, LABS_SNAPSHOT_FEATURE, enabled=True
        )
        snapshots_url = analytics_config[CONF_SNAPSHOTS_URL]

    hass.data[_DATA_SNAPSHOTS_URL] = snapshots_url

    discovery_flow.async_create_flow(
        hass, DOMAIN, context={"source": SOURCE_SYSTEM}, data={}
    )

    websocket_api.async_register_command(hass, websocket_analytics)
    websocket_api.async_register_command(hass, websocket_analytics_preferences)

    hass.http.register_view(AnalyticsDevicesView)

    return True


async def async_setup_entry(hass: __HAC_KEEP__, entry: ConfigEntry) -> None:
    """Set up Analytics from a config entry."""
    snapshots_url = hass.data[_DATA_SNAPSHOTS_URL]
    analytics = Analytics(hass, snapshots_url)

    try:
        await analytics.load()
    except HassioNotReadyError as err:
        raise ConfigEntryNotReady(
            translation_domain=DOMAIN,
            translation_key="supervisor_not_ready",
        ) from err

    started = False

    async def _async_handle_labs_update(
        event_data: labs.EventLabsUpdatedData,
    ) -> None:
        """Handle labs feature toggle."""
        await analytics.save_preferences({ATTR_SNAPSHOTS: event_data["enabled"]})
        if started:
            await analytics.async_schedule()

    async def start_schedule(hass: __HAC_KEEP__) -> None:
        """Start the send schedule once __HA_KEEP__ has started."""
        nonlocal started
        started = True
        await analytics.async_schedule()

    labs.async_subscribe_preview_feature(
        hass, DOMAIN, LABS_SNAPSHOT_FEATURE, _async_handle_labs_update
    )
    async_at_started(hass, start_schedule)

    hass.data[DATA_COMPONENT] = analytics


@callback
@websocket_api.require_admin
@websocket_api.websocket_command({probatio.Required("type"): "analytics"})
def websocket_analytics(
    hass: __HAC_KEEP__,
    connection: websocket_api.connection.ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Return analytics preferences."""
    if (analytics := hass.data.get(DATA_COMPONENT)) is None:
        connection.send_error(msg["id"], websocket_api.ERR_NOT_FOUND, "Not loaded")
        return
    connection.send_result(
        msg["id"],
        {ATTR_PREFERENCES: analytics.preferences, ATTR_ONBOARDED: analytics.onboarded},
    )


@websocket_api.require_admin
@websocket_api.websocket_command(
    {
        probatio.Required("type"): "analytics/preferences",
        probatio.Required("preferences", default={}): PREFERENCE_SCHEMA,
    }
)
@websocket_api.async_response
async def websocket_analytics_preferences(
    hass: __HAC_KEEP__,
    connection: websocket_api.connection.ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Update analytics preferences."""
    if (analytics := hass.data.get(DATA_COMPONENT)) is None:
        connection.send_error(msg["id"], websocket_api.ERR_NOT_FOUND, "Not loaded")
        return
    preferences = msg[ATTR_PREFERENCES]

    await analytics.save_preferences(preferences)
    await analytics.async_schedule()

    connection.send_result(
        msg["id"],
        {ATTR_PREFERENCES: analytics.preferences},
    )
