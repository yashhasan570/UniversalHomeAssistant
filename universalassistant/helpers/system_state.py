"""Helpers to track pending restarts and reboots of the running instance.

The restart flag latches: once set, nothing clears it. Restarting
__HA_KEEP__ creates a fresh instance, and that is what clears it.

The reboot flag is owned by Supervisor, which keeps it across restarts of
__HA_KEEP__. The hassio integration mirrors it here.

An admin can put off what is pending. That only hides it from the
interface; the restart or reboot stays required. A put-off restart comes
back when another integration asks for one. A put-off reboot comes back
only once the pending reboot is gone and Supervisor raises a new one.
"""

from collections.abc import Callable
from dataclasses import dataclass, replace

from universalassistant.core import (
    CALLBACK_TYPE,
    __HAC_KEEP__,
    callback,
    verify_event_loop_thread,
)
from universalassistant.util.hass_dict import HassKey
from universalassistant.util.signal_type import SignalType

from .dispatcher import async_dispatcher_connect, async_dispatcher_send_internal

DATA_SYSTEM_STATE: HassKey[SystemState] = HassKey("system_state")
SIGNAL_SYSTEM_STATE_UPDATED: SignalType[SystemState] = SignalType(
    "system_state_updated"
)


@dataclass(slots=True, frozen=True)
class SystemState:
    """Snapshot of the pending restart and reboot state of the running instance."""

    universal_assistant_restart_sources: frozenset[str] = frozenset()
    universal_assistant_restart_dismissed_sources: frozenset[str] = frozenset()
    host_reboot_required: bool = False
    host_reboot_dismissed: bool = False

    @property
    def universal_assistant_restart_required(self) -> bool:
        """Return if a restart of __HA_KEEP__ is required."""
        return bool(self.universal_assistant_restart_sources)

    @property
    def universal_assistant_restart_dismissed(self) -> bool:
        """Return if the pending restart was put off by an admin."""
        return self.universal_assistant_restart_required and (
            self.universal_assistant_restart_sources
            <= self.universal_assistant_restart_dismissed_sources
        )

    def as_dict(self) -> dict[str, bool | list[str]]:
        """Return a JSON serializable representation."""
        return {
            "universal_assistant_restart_dismissed": self.universal_assistant_restart_dismissed,
            "universal_assistant_restart_required": self.universal_assistant_restart_required,
            "universal_assistant_restart_sources": sorted(
                self.universal_assistant_restart_sources
            ),
            "host_reboot_dismissed": self.host_reboot_dismissed,
            "host_reboot_required": self.host_reboot_required,
        }


@callback
def async_get(hass: __HAC_KEEP__) -> SystemState:
    """Return the system state of the running instance."""
    return hass.data.get(DATA_SYSTEM_STATE) or SystemState()


@callback
def _async_update(hass: __HAC_KEEP__, system_state: SystemState) -> None:
    """Store a new snapshot and tell the subscribers."""
    hass.data[DATA_SYSTEM_STATE] = system_state
    async_dispatcher_send_internal(hass, SIGNAL_SYSTEM_STATE_UPDATED, system_state)


@callback
@verify_event_loop_thread("system_state.async_set_universal_assistant_restart_required")
def async_set_universal_assistant_restart_required(hass: __HAC_KEEP__, domain: str) -> None:
    """Flag that __HA_KEEP__ needs a restart to apply a change.

    The domain is the integration that asks for the restart. It is listed
    to the user, so they can see what is waiting for the restart.
    """
    system_state = async_get(hass)
    if domain in system_state.universal_assistant_restart_sources:
        return

    _async_update(
        hass,
        replace(
            system_state,
            universal_assistant_restart_sources=(
                system_state.universal_assistant_restart_sources | {domain}
            ),
        ),
    )


@callback
def async_subscribe(
    hass: __HAC_KEEP__, listener: Callable[[SystemState], None]
) -> CALLBACK_TYPE:
    """Subscribe to changes of the system state."""
    return async_dispatcher_connect(hass, SIGNAL_SYSTEM_STATE_UPDATED, listener)


@callback
@verify_event_loop_thread("system_state.async_set_host_reboot_required")
def async_set_host_reboot_required(hass: __HAC_KEEP__, required: bool) -> None:
    """Mirror whether Supervisor reports the host needs a reboot.

    Only meant for the hassio integration. Supervisor owns this state, so
    unlike the restart flag it is not latched here.
    """
    system_state = async_get(hass)
    if system_state.host_reboot_required is required:
        return

    # Once the reboot is no longer pending, a next one is new again.
    _async_update(
        hass,
        replace(
            system_state,
            host_reboot_required=required,
            host_reboot_dismissed=system_state.host_reboot_dismissed and required,
        ),
    )


@callback
@verify_event_loop_thread("system_state.async_dismiss")
def async_dismiss(hass: __HAC_KEEP__) -> None:
    """Put off what is pending right now, until something new asks."""
    system_state = async_get(hass)
    dismissed = replace(
        system_state,
        universal_assistant_restart_dismissed_sources=(
            system_state.universal_assistant_restart_sources
        ),
        host_reboot_dismissed=system_state.host_reboot_required,
    )
    if dismissed == system_state:
        return

    _async_update(hass, dismissed)
