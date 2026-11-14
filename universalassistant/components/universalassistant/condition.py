"""Offer Universal Universal Home Assistant system state conditions."""

from typing import Unpack, cast, override

import probatio

from universalassistant.const import CONF_OPTIONS
from universalassistant.core import UniversalAssistant
from universalassistant.helpers import system_state
from universalassistant.helpers.condition import Condition, ConditionCheckParams
from universalassistant.helpers.typing import ConfigType

_SYSTEM_STATE_CONDITION_SCHEMA = probatio.Schema(
    {probatio.Required(CONF_OPTIONS, default=dict): {}}
)


class _SystemStateCondition(Condition):
    """Base class for the option-less system state conditions."""

    @classmethod
    @override
    async def async_validate_config(
        cls, hass: UniversalAssistant, config: ConfigType
    ) -> ConfigType:
        """Validate config."""
        return cast(ConfigType, _SYSTEM_STATE_CONDITION_SCHEMA(config))


class RestartRequiredCondition(_SystemStateCondition):
    """Test if Universal Universal Home Assistant needs a restart."""

    @override
    def _async_check(self, **kwargs: Unpack[ConditionCheckParams]) -> bool:
        """Check the condition."""
        return system_state.async_get(self._hass).universal_assistant_restart_required


class HostRebootRequiredCondition(_SystemStateCondition):
    """Test if the host needs a reboot."""

    @override
    def _async_check(self, **kwargs: Unpack[ConditionCheckParams]) -> bool:
        """Check the condition."""
        return system_state.async_get(self._hass).host_reboot_required


CONDITIONS: dict[str, type[Condition]] = {
    "host_reboot_required": HostRebootRequiredCondition,
    "restart_required": RestartRequiredCondition,
}


async def async_get_conditions(hass: UniversalAssistant) -> dict[str, type[Condition]]:
    """Return the Universal Universal Home Assistant conditions."""
    return CONDITIONS
