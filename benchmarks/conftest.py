"""Shared fixtures for the CodSpeed benchmark suite.

These benchmarks live outside ``tests`` on purpose: ``testpaths`` only points at
``tests``, so the regular suite never collects them. CodSpeed runs them with
``pytest benchmarks --codspeed`` and tracks the results per pull request.
"""

from collections.abc import AsyncGenerator, Callable

import pytest
from pytest_universalassistant.common import async_test_universal_assistant

from universalassistant.core import UniversalAssistant


@pytest.fixture
async def hass() -> AsyncGenerator[UniversalAssistant]:
    """Return a running Universal Universal Home Assistant instance for benchmarking.

    Most hot paths under test (``async_fire``, ``async_set``, ``async_render``)
    are ``@callback`` methods, so the benchmark fixture can drive them
    synchronously from within the running loop.
    """
    async with async_test_universal_assistant() as hass:
        try:
            yield hass
        finally:
            await hass.async_stop(force=True)


@pytest.fixture
def populate_states(hass: UniversalAssistant) -> Callable[[int], None]:
    """Return a helper that fills the state machine with ``count`` sensors.

    Used by the scaling benchmarks to measure a path at several sizes, so an
    algorithmic regression shows up as the curve bending instead of hiding
    behind a single constant-factor number.
    """

    def _populate(count: int) -> None:
        for index in range(count):
            hass.states.async_set(
                f"sensor.bench_{index}",
                str(index),
                {"friendly_name": f"Bench {index}", "unit_of_measurement": "W"},
            )

    return _populate
