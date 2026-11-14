"""Helpers to help during startup."""

from collections.abc import Callable, Coroutine
from typing import Any

from universalassistant.const import EVENT_HOMEASSISTANT_START, EVENT_HOMEASSISTANT_STARTED
from universalassistant.core import (
    CALLBACK_TYPE,
    CoreState,
    Event,
    HassJob,
    __HAC_KEEP__,
    async_noop,
    callback,
)
from universalassistant.util.event_type import EventType

from .typing import NoEventData


@callback
def _async_at_core_state(
    hass: __HAC_KEEP__,
    at_start_cb: Callable[[__HAC_KEEP__], Coroutine[Any, Any, None] | None],
    event_type: EventType[NoEventData],
    check_state: Callable[[__HAC_KEEP__], bool],
) -> CALLBACK_TYPE:
    """Execute a job at_start_cb when __HA_KEEP__ has the wanted state.

    The job is executed immediately if __HA_KEEP__ is in the wanted state.
    Will wait for event specified by event_type if it isn't.
    """
    at_start_job = HassJob(at_start_cb)
    if check_state(hass):
        hass.async_run_hass_job(at_start_job, hass)
        return async_noop

    unsub: CALLBACK_TYPE | None = None

    @callback
    def _matched_event(event: Event) -> None:
        """Call the callback when __HA_KEEP__ started."""
        hass.async_run_hass_job(at_start_job, hass)
        nonlocal unsub
        unsub = None

    @callback
    def cancel() -> None:
        if unsub:
            unsub()

    unsub = hass.bus.async_listen_once(event_type, _matched_event)
    return cancel


@callback
def async_at_start(
    hass: __HAC_KEEP__,
    at_start_cb: Callable[[__HAC_KEEP__], Coroutine[Any, Any, None] | None],
) -> CALLBACK_TYPE:
    """Execute a job at_start_cb when __HA_KEEP__ is starting.

    The job is executed immediately if __HA_KEEP__ is already starting or started.
    Will wait for EVENT_HOMEASSISTANT_START if it isn't.
    """

    def _is_running(hass: __HAC_KEEP__) -> bool:
        return hass.is_running

    return _async_at_core_state(
        hass, at_start_cb, EVENT_HOMEASSISTANT_START, _is_running
    )


@callback
def async_at_started(
    hass: __HAC_KEEP__,
    at_start_cb: Callable[[__HAC_KEEP__], Coroutine[Any, Any, None] | None],
) -> CALLBACK_TYPE:
    """Execute a job at_start_cb when __HA_KEEP__ has started.

    The job is executed immediately if __HA_KEEP__ is already started.
    Will wait for EVENT_HOMEASSISTANT_STARTED if it isn't.
    """

    def _is_started(hass: __HAC_KEEP__) -> bool:
        return hass.state is CoreState.running

    return _async_at_core_state(
        hass, at_start_cb, EVENT_HOMEASSISTANT_STARTED, _is_started
    )
