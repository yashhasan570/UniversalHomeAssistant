"""Helpers for the cloud component."""

from collections import deque
import logging
from typing import override

from universalassistant.core import __HAC_KEEP__


class FixedSizeQueueLogHandler(logging.Handler):
    """Log handler to store messages, with auto rotation."""

    MAX_RECORDS = 500

    def __init__(self) -> None:
        """Initialize a new LogHandler."""
        super().__init__()
        self._records: deque[logging.LogRecord] = deque(maxlen=self.MAX_RECORDS)

    @override
    def emit(self, record: logging.LogRecord) -> None:
        """Store log message."""
        self._records.append(record)

    async def get_logs(self, hass: __HAC_KEEP__) -> list[str]:
        """Get stored logs."""

        def _get_logs() -> list[str]:
            # copy the queue since it can mutate while iterating
            records = self._records.copy()
            return [self.format(record) for record in records]

        return await hass.async_add_executor_job(_get_logs)
