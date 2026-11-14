"""Helpers for the vizio integration."""

from collections.abc import Coroutine
from typing import Any

from vizaio import VizioError

from universalassistant.exceptions import __HAC_KEEP__Error

from .const import DOMAIN


async def async_device_command[T](coro: Coroutine[Any, Any, T]) -> T:
    """Run a device command, raising __HAC_KEEP__Error on API failure."""
    try:
        return await coro
    except VizioError as err:
        raise __HAC_KEEP__Error(
            translation_domain=DOMAIN,
            translation_key="command_error",
            translation_placeholders={"error": str(err)},
        ) from err
