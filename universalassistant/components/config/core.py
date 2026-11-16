"""Component to interact with Hassbian tools."""

from typing import Any

from aiohttp import web
import probatio

from universalassistant.components import websocket_api
from universalassistant.components.http import KEY_HASS, UniversalAssistantView, require_admin
from universalassistant.components.sensor import async_update_suggested_units
from universalassistant.core import UniversalAssistant, callback
from universalassistant.helpers import check_config, config_validation as cv
from universalassistant.helpers.aiohttp_client import async_get_clientsession
from universalassistant.util import location as location_util, unit_system


@callback
def async_setup(hass: UniversalAssistant) -> bool:
    """Set up the Hassbian config."""
    hass.http.register_view(CheckConfigView)
    websocket_api.async_register_command(hass, websocket_update_config)
    websocket_api.async_register_command(hass, websocket_detect_config)
    return True


class CheckConfigView(UniversalAssistantView):
    """Hassbian packages endpoint."""

    url = "/api/config/core/check_config"
    name = "api:config:core:check_config"

    @require_admin
    async def post(self, request: web.Request) -> web.Response:
        """Validate configuration and return results."""

        res = await check_config.async_check_ha_config_file(request.app[KEY_HASS])

        state = "invalid" if res.errors else "valid"

        return self.json(
            {
                "result": state,
                "errors": res.error_str or None,
                "warnings": res.warning_str or None,
            }
        )


@websocket_api.require_admin
@websocket_api.websocket_command(
    {
        "type": "config/core/update",
        probatio.Optional("country"): cv.country,
        probatio.Optional("currency"): cv.currency,
        probatio.Optional("elevation"): probatio.Coerce(int),
        probatio.Optional("external_url"): probatio.Any(cv.url_no_path, None),
        probatio.Optional("internal_url"): probatio.Any(cv.url_no_path, None),
        probatio.Optional("language"): cv.language,
        probatio.Optional("latitude"): cv.latitude,
        probatio.Optional("location_name"): str,
        probatio.Optional("longitude"): cv.longitude,
        probatio.Optional("radius"): cv.positive_int,
        # Validated by async_set_time_zone in the executor to avoid
        # blocking I/O loading zoneinfo data on the event loop.
        probatio.Optional("time_zone"): str,
        probatio.Optional("update_units"): bool,
        probatio.Optional("unit_system"): unit_system.validate_unit_system,
    }
)
@websocket_api.async_response
async def websocket_update_config(
    hass: UniversalAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Handle update core config command."""
    data = dict(msg)
    data.pop("id")
    data.pop("type")

    update_units = data.pop("update_units", False)

    try:
        await hass.config.async_update(**data)
        if update_units:
            async_update_suggested_units(hass)
        connection.send_result(msg["id"])
    except ValueError as err:
        connection.send_error(msg["id"], "invalid_info", str(err))


@websocket_api.require_admin
@websocket_api.websocket_command({"type": "config/core/detect"})
@websocket_api.async_response
async def websocket_detect_config(
    hass: UniversalAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Detect core config."""
    session = async_get_clientsession(hass)
    location_info = await location_util.async_detect_location_info(session)

    info: dict[str, Any] = {}

    if location_info is None:
        connection.send_result(msg["id"], info)
        return

    # We don't want any integrations to use the name of the unit system
    # so we are using the private attribute here
    if location_info.use_metric:
        info["unit_system"] = unit_system._CONF_UNIT_SYSTEM_METRIC  # noqa: SLF001
    else:
        info["unit_system"] = unit_system._CONF_UNIT_SYSTEM_US_CUSTOMARY  # noqa: SLF001

    if location_info.latitude:
        info["latitude"] = location_info.latitude

    if location_info.longitude:
        info["longitude"] = location_info.longitude

    if location_info.time_zone:
        info["time_zone"] = location_info.time_zone

    if location_info.currency:
        info["currency"] = location_info.currency

    if location_info.country_code:
        info["country"] = location_info.country_code

    connection.send_result(msg["id"], info)
