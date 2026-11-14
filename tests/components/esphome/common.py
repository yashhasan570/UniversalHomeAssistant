"""ESPHome test common code."""

from datetime import datetime

from pytest_universalassistant.common import async_fire_time_changed

from universalassistant.components import assist_satellite
from universalassistant.components.assist_satellite import AssistSatelliteEntity
from universalassistant.components.esphome import DOMAIN
from universalassistant.components.esphome.assist_satellite import EsphomeAssistSatellite
from universalassistant.components.esphome.coordinator import REFRESH_INTERVAL
from universalassistant.const import Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import entity_registry as er
from universalassistant.helpers.entity_component import EntityComponent
from universalassistant.util import dt as dt_util


class MockDashboardRefresh:
    """Mock dashboard refresh."""

    def __init__(self, hass: __HAC_KEEP__) -> None:
        """Initialize the mock dashboard refresh."""
        self.hass = hass
        self.last_time: datetime | None = None

    async def async_refresh(self) -> None:
        """Refresh the dashboard."""
        if self.last_time is None:
            self.last_time = dt_util.utcnow()
        self.last_time += REFRESH_INTERVAL
        async_fire_time_changed(self.hass, self.last_time)
        await self.hass.async_block_till_done()


def get_satellite_entity(
    hass: __HAC_KEEP__, mac_address: str
) -> EsphomeAssistSatellite | None:
    """Get the satellite entity for a device."""
    ent_reg = er.async_get(hass)
    satellite_entity_id = ent_reg.async_get_entity_id(
        Platform.ASSIST_SATELLITE, DOMAIN, f"{mac_address}-assist_satellite"
    )
    if satellite_entity_id is None:
        return None
    assert satellite_entity_id.endswith("_assist_satellite")

    component: EntityComponent[AssistSatelliteEntity] = hass.data[
        assist_satellite.DOMAIN
    ]
    if (entity := component.get_entity(satellite_entity_id)) is not None:
        assert isinstance(entity, EsphomeAssistSatellite)
        return entity

    return None
