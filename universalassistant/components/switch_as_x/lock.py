"""Lock support for switch entities."""

from typing import Any, override

from universalassistant.components.lock import DOMAIN as LOCK_DOMAIN, LockEntity
from universalassistant.components.switch import DOMAIN as SWITCH_DOMAIN
from universalassistant.config_entries import ConfigEntry
from universalassistant.const import (
    ATTR_ENTITY_ID,
    CONF_ENTITY_ID,
    SERVICE_TURN_OFF,
    SERVICE_TURN_ON,
    STATE_ON,
)
from universalassistant.core import Event, EventStateChangedData, __HAC_KEEP__, callback
from universalassistant.helpers import entity_registry as er
from universalassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import CONF_INVERT
from .entity import BaseInvertableEntity


async def async_setup_entry(
    hass: __HAC_KEEP__,
    config_entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Initialize Lock Switch config entry."""
    registry = er.async_get(hass)
    entity_id = er.async_validate_entity_id(
        registry, config_entry.options[CONF_ENTITY_ID]
    )

    async_add_entities(
        [
            LockSwitch(
                hass,
                config_entry.title,
                LOCK_DOMAIN,
                config_entry.options[CONF_INVERT],
                entity_id,
                config_entry.entry_id,
            )
        ]
    )


class LockSwitch(BaseInvertableEntity, LockEntity):
    """Represents a Switch as a Lock."""

    @override
    async def async_lock(self, **kwargs: Any) -> None:
        """Lock the lock."""
        await self.hass.services.async_call(
            SWITCH_DOMAIN,
            SERVICE_TURN_ON if self._invert_state else SERVICE_TURN_OFF,
            {ATTR_ENTITY_ID: self._switch_entity_id},
            blocking=True,
            context=self._context,
        )

    @override
    async def async_unlock(self, **kwargs: Any) -> None:
        """Unlock the lock."""
        await self.hass.services.async_call(
            SWITCH_DOMAIN,
            SERVICE_TURN_OFF if self._invert_state else SERVICE_TURN_ON,
            {ATTR_ENTITY_ID: self._switch_entity_id},
            blocking=True,
            context=self._context,
        )

    @callback
    @override
    def async_state_changed_listener(
        self, event: Event[EventStateChangedData] | None = None
    ) -> None:
        """Handle child updates."""
        super().async_state_changed_listener(event)
        if (
            not self.available
            or (state := self.hass.states.get(self._switch_entity_id)) is None
        ):
            return

        # Logic is the same as the lock device class for binary sensors
        # on means open (unlocked), off means closed (locked)
        if self._invert_state:
            self._attr_is_locked = state.state == STATE_ON
        else:
            self._attr_is_locked = state.state != STATE_ON
