"""Helpers for OpenEVSE."""

from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any

from aiohttp import ContentTypeError, ServerTimeoutError
from openevsehttp.exceptions import (
    AuthenticationError,
    ParseJSONError,
    UnknownError,
    UnsupportedFeature,
)

from universalassistant.exceptions import (
    ConfigEntryAuthFailed,
    UniversalAssistantError,
    ServiceValidationError,
)

from .const import DOMAIN


@contextmanager
def openevse_exception_handler(value: Any = None) -> Iterator[None]:
    """Context manager to handle and translate OpenEVSE exceptions."""
    try:
        yield
    except ValueError as err:
        raise ServiceValidationError(
            translation_domain=DOMAIN,
            translation_key="invalid_value",
            translation_placeholders={"value": str(value)},
        ) from err
    except AuthenticationError as err:
        raise ConfigEntryAuthFailed(
            translation_domain=DOMAIN,
            translation_key="authentication_error",
        ) from err
    except UnsupportedFeature as err:
        raise UniversalAssistantError(
            translation_domain=DOMAIN,
            translation_key="unsupported_feature",
        ) from err
    except (
        TimeoutError,
        ServerTimeoutError,
        ContentTypeError,
        ParseJSONError,
        UnknownError,
        RuntimeError,
    ) as err:
        raise UniversalAssistantError(
            translation_domain=DOMAIN,
            translation_key="communication_error",
        ) from err
