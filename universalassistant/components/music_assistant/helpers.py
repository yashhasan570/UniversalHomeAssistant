"""Helpers for the Music Assistant integration."""

from collections.abc import Callable, Coroutine, Generator
from contextlib import contextmanager
import functools
from typing import TYPE_CHECKING, Any

from music_assistant_client.helpers import LinkedUser
from music_assistant_models.auth import AuthProviderType
from music_assistant_models.errors import MusicAssistantError, UserNotFoundError

from universalassistant.core import Context, __HAC_KEEP__, callback
from universalassistant.exceptions import __HAC_KEEP__Error, ServiceValidationError
from universalassistant.helpers import service

from .const import DASHBOARD_ID_PREFIX, DOMAIN

if TYPE_CHECKING:
    from music_assistant_client import MusicAssistantClient

    from . import MusicAssistantConfigEntry


def dashboard_identifier(dashboard_id: str) -> str:
    """Return the device identifier and entity unique id of a dashboard display."""
    return f"{DASHBOARD_ID_PREFIX}{dashboard_id}"


def catch_musicassistant_error[**_P, _R](
    func: Callable[_P, Coroutine[Any, Any, _R]],
) -> Callable[_P, Coroutine[Any, Any, _R]]:
    """Check and convert commands to players."""

    @functools.wraps(func)
    async def wrapper(*args: _P.args, **kwargs: _P.kwargs) -> _R:
        """Catch Music Assistant errors and convert to __HA_KEEP__ error."""
        try:
            return await func(*args, **kwargs)
        except MusicAssistantError as err:
            error_msg = str(err) or err.__class__.__name__
            raise __HAC_KEEP__Error(error_msg) from err

    return wrapper


@contextmanager
def catch_user_not_found(username: str | None) -> Generator[None]:
    """Convert a server UserNotFoundError into a translated invalid_username error."""
    if username is None:
        yield
        return
    try:
        yield
    except UserNotFoundError as err:
        raise ServiceValidationError(
            translation_domain=DOMAIN,
            translation_key="invalid_username",
            translation_placeholders={"username": username},
        ) from err


def user_from_context(context: Context | None) -> LinkedUser | None:
    """Return the Music Assistant user to act as for the __HA_KEEP__ caller."""
    if context is None or context.user_id is None:
        return None
    # required=False: fall back to the default account if the user has no link
    return LinkedUser(
        provider=AuthProviderType.UNIVERSAL_ASSISTANT,
        user_id=context.user_id,
        required=False,
    )


@callback
def get_music_assistant_client(
    hass: __HAC_KEEP__, config_entry_id: str
) -> MusicAssistantClient:
    """Get the Music Assistant client for the given config entry."""
    entry: MusicAssistantConfigEntry = service.async_get_config_entry(
        hass, DOMAIN, config_entry_id
    )
    return entry.runtime_data.mass
