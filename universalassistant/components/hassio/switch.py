"""Switch platform for Hass.io addons."""

from typing import Any, override

from aiohasupervisor import SupervisorError
from aiohasupervisor.models import AddonState

from universalassistant.components.switch import SwitchEntity, SwitchEntityDescription
from universalassistant.config_entries import ConfigEntry
from universalassistant.core import __HAC_KEEP__
from universalassistant.exceptions import __HAC_KEEP__Error
from universalassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import ADDONS_COORDINATOR
from .entity import HassioAddonEntity
from .handler import get_supervisor_client

ENTITY_DESCRIPTION = SwitchEntityDescription(
    key="state",
    name=None,
    icon="mdi:puzzle",
    entity_registry_enabled_default=False,
)


async def async_setup_entry(
    hass: __HAC_KEEP__,
    config_entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Switch set up for Hass.io config entry."""
    coordinator = hass.data[ADDONS_COORDINATOR]

    async_add_entities(
        HassioAddonSwitch(
            addon=addon,
            coordinator=coordinator,
            entity_description=ENTITY_DESCRIPTION,
        )
        for addon in coordinator.data.addons.values()
    )


class HassioAddonSwitch(HassioAddonEntity, SwitchEntity):
    """Switch for Hass.io add-ons."""

    @property
    @override
    def is_on(self) -> bool:
        """Return true if the add-on is on."""
        return (
            self.coordinator.data.addons[self._addon_slug].addon.state
            == AddonState.STARTED
        )

    @property
    @override
    def entity_picture(self) -> str | None:
        """Return the icon of the add-on if any."""
        if not self.available:
            return None
        if self.coordinator.data.addons[self._addon_slug].addon.icon:
            return f"/api/hassio/addons/{self._addon_slug}/icon"
        return None

    @override
    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the entity on."""
        supervisor_client = get_supervisor_client(self.hass)
        try:
            await supervisor_client.addons.start_addon(self._addon_slug)
        except SupervisorError as err:
            raise __HAC_KEEP__Error(err) from err

        await self.coordinator.force_addon_info_data_refresh(self._addon_slug)

    @override
    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the entity off."""
        supervisor_client = get_supervisor_client(self.hass)
        try:
            await supervisor_client.addons.stop_addon(self._addon_slug)
        except SupervisorError as err:
            raise __HAC_KEEP__Error(err) from err

        await self.coordinator.force_addon_info_data_refresh(self._addon_slug)
