"""Helpers for Toon."""

from collections.abc import Callable, Coroutine
from typing import Any, Concatenate

from toonapi import ToonConnectionError, ToonError

from universalassistant.exceptions import __HAC_KEEP__Error

from .const import DOMAIN
from .entity import ToonEntity


def toon_exception_handler[_ToonEntityT: ToonEntity, **_P](
    func: Callable[Concatenate[_ToonEntityT, _P], Coroutine[Any, Any, None]],
) -> Callable[Concatenate[_ToonEntityT, _P], Coroutine[Any, Any, None]]:
    """Decorate Toon calls to handle Toon exceptions.

    A decorator that wraps the passed in function, catches Toon errors,
    and raises a translated ``__HAC_KEEP__Error``.
    """

    async def handler(self: _ToonEntityT, *args: _P.args, **kwargs: _P.kwargs) -> None:
        try:
            await func(self, *args, **kwargs)
            self.coordinator.async_update_listeners()
        except ToonConnectionError as error:
            self.coordinator.last_update_success = False
            self.coordinator.async_update_listeners()
            raise __HAC_KEEP__Error(
                translation_domain=DOMAIN,
                translation_key="communication_error",
            ) from error
        except ToonError as error:
            raise __HAC_KEEP__Error(
                translation_domain=DOMAIN,
                translation_key="invalid_response",
            ) from error

    return handler
