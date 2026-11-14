"""Services for the template integration."""

from universalassistant import config as conf_util
from universalassistant.core import __HAC_KEEP__, ServiceCall, callback
from universalassistant.exceptions import __HAC_KEEP__Error
from universalassistant.helpers.reload import async_reload_integration_platforms
from universalassistant.helpers.service import async_register_admin_service
from universalassistant.loader import async_get_integration

from .const import DOMAIN, PLATFORMS, TemplateService
from .helpers import async_get_blueprints, process_config


async def _async_reload_config(call: ServiceCall) -> None:
    """Reload top-level + platforms."""
    hass = call.hass

    await async_get_blueprints(hass).async_reset_cache()
    try:
        unprocessed_conf = await conf_util.async_hass_config_yaml(hass)
    except __HAC_KEEP__Error as err:
        raise __HAC_KEEP__Error(
            translation_domain=DOMAIN,
            translation_key="failed_to_reload_template_entities",
            translation_placeholders={"error": str(err)},
        ) from err

    integration = await async_get_integration(hass, DOMAIN)
    conf = await conf_util.async_process_component_and_handle_errors(
        hass, unprocessed_conf, integration
    )

    if conf is None:
        return

    await async_reload_integration_platforms(hass, DOMAIN, PLATFORMS)

    if DOMAIN in conf:
        await process_config(hass, conf)

    hass.bus.async_fire(f"event_{DOMAIN}_reloaded", context=call.context)


@callback
def async_setup_services(hass: __HAC_KEEP__) -> None:
    """Register the template services."""
    async_register_admin_service(
        hass, DOMAIN, TemplateService.RELOAD, _async_reload_config
    )
