"""WebSocket API related errors."""

from universalassistant.exceptions import __HAC_KEEP__Error


class Disconnect(__HAC_KEEP__Error):
    """Disconnect the current session."""
