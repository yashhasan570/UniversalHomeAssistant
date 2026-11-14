"""Helpers for automation integration."""

from universalassistant.components.blueprint import BLUEPRINT_SCHEMA, DomainBlueprints
from universalassistant.core import __HAC_KEEP__, callback
from universalassistant.helpers.singleton import singleton

from .const import DOMAIN, LOGGER, ScriptService

DATA_BLUEPRINTS = "script_blueprints"


def _blueprint_in_use(hass: __HAC_KEEP__, blueprint_path: str) -> bool:
    """Return True if any script references the blueprint."""
    from . import scripts_with_blueprint  # noqa: PLC0415

    return len(scripts_with_blueprint(hass, blueprint_path)) > 0


async def _reload_blueprint_scripts(hass: __HAC_KEEP__, blueprint_path: str) -> None:
    """Reload all script that rely on a specific blueprint."""
    await hass.services.async_call(DOMAIN, ScriptService.RELOAD)


@singleton(DATA_BLUEPRINTS)
@callback
def async_get_blueprints(hass: __HAC_KEEP__) -> DomainBlueprints:
    """Get script blueprints."""
    return DomainBlueprints(
        hass,
        DOMAIN,
        LOGGER,
        _blueprint_in_use,
        _reload_blueprint_scripts,
        BLUEPRINT_SCHEMA,
    )
