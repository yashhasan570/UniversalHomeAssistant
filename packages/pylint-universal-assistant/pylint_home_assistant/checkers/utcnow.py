"""Checker that enforces ``universalassistant.util.dt.utcnow`` over ``datetime.now(UTC)``.

__HA_KEEP__ exposes ``universalassistant.util.dt.utcnow`` -- a thin wrapper around
``datetime.datetime.now(UTC)`` implemented as a ``functools.partial``. Using the
helper avoids the per-call global lookup of ``UTC`` and keeps the codebase
consistent in how the current UTC time is obtained.
"""

from pylint.lint import PyLinter

from pylint_universal_assistant.helpers.datetime_now import (
    CASE_UTC,
    HassEnforceDatetimeNowChecker,
)


class HassEnforceUtcnowChecker(HassEnforceDatetimeNowChecker):
    """Checker that flags ``datetime.now(UTC)`` calls."""

    name = "universal_assistant_enforce_utcnow"
    msgs = {
        "C7414": (
            "Use `universalassistant.util.dt.utcnow()` instead of `datetime.now(UTC)`",
            "universal-assistant-enforce-utcnow",
            "Used when ``datetime.datetime.now(UTC)`` is called. Use the "
            "``universalassistant.util.dt.utcnow`` helper instead -- it is "
            "implemented as ``functools.partial(datetime.datetime.now, UTC)`` "
            "and avoids the global lookup of ``UTC`` on every call.",
        ),
    }

    message = "universal-assistant-enforce-utcnow"
    flagged_case = CASE_UTC


def register(linter: PyLinter) -> None:
    """Register the checker."""
    linter.register_checker(HassEnforceUtcnowChecker(linter))
