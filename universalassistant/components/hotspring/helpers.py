"""Helpers for Hot Spring."""

from collections.abc import Callable, Coroutine
from typing import Any, Concatenate

from hotspring import (
    HotSpringConnectionError,
    HotSpringConnectionTimeoutError,
    HotSpringError,
    HotSpringNotReadyError,
)

from universalassistant.exceptions import __HAC_KEEP__Error

from .const import DOMAIN
from .entity import HotSpringEntity


def hotspring_exception_handler[_HotSpringEntityT: HotSpringEntity, **_P](
    func: Callable[Concatenate[_HotSpringEntityT, _P], Coroutine[Any, Any, Any]],
) -> Callable[Concatenate[_HotSpringEntityT, _P], Coroutine[Any, Any, None]]:
    """Decorate Hot Spring calls to handle Hot Spring exceptions.

    A decorator that wraps the passed in function, catches Hot Spring errors,
    and raises a translated __HAC_KEEP__Error.
    """

    async def handler(
        self: _HotSpringEntityT, *args: _P.args, **kwargs: _P.kwargs
    ) -> None:
        try:
            await func(self, *args, **kwargs)
        except HotSpringConnectionTimeoutError as error:
            raise __HAC_KEEP__Error(
                translation_domain=DOMAIN,
                translation_key="timeout",
            ) from error
        except HotSpringConnectionError as error:
            raise __HAC_KEEP__Error(
                translation_domain=DOMAIN,
                translation_key="cannot_connect",
            ) from error
        except HotSpringNotReadyError as error:
            raise __HAC_KEEP__Error(
                translation_domain=DOMAIN,
                translation_key="spa_not_connected",
            ) from error
        except HotSpringError as error:
            raise __HAC_KEEP__Error(
                translation_domain=DOMAIN,
                translation_key="invalid_response",
            ) from error

    return handler
