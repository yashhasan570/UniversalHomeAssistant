"""The Elvia integration."""

from datetime import datetime, timedelta
from typing import TYPE_CHECKING

from elvia import error as ElviaError

from universalassistant.const import CONF_API_TOKEN
from universalassistant.core import UniversalAssistant
from universalassistant.exceptions import ConfigEntryError
from universalassistant.helpers.event import async_track_time_interval

from .const import CONF_METERING_POINT_ID, DOMAIN, LOGGER
from .importer import ElviaImporter

if TYPE_CHECKING:
    from universalassistant.config_entries import ConfigEntry


async def async_setup_entry(hass: UniversalAssistant, entry: ConfigEntry) -> None:
    """Set up Elvia from a config entry."""
    importer = ElviaImporter(
        hass=hass,
        api_token=entry.data[CONF_API_TOKEN],
        metering_point_id=entry.data[CONF_METERING_POINT_ID],
    )

    async def _import_meter_values(_: datetime | None = None) -> None:
        """Import meter values."""
        try:
            await importer.import_meter_values()
        except ElviaError.ElviaException as exception:
            LOGGER.exception("Unknown error %s", exception)

    try:
        await importer.import_meter_values()
    except ElviaError.ElviaException as exception:
        raise ConfigEntryError(
            translation_domain=DOMAIN,
            translation_key="import_failed",
        ) from exception

    entry.async_on_unload(
        async_track_time_interval(
            hass,
            _import_meter_values,
            timedelta(minutes=60),
        )
    )
