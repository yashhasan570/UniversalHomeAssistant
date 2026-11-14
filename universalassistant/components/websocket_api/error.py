"""WebSocket API related errors."""

from universalassistant.exceptions import UniversalAssistantError


class Disconnect(UniversalAssistantError):
    """Disconnect the current session."""
