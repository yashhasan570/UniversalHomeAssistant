"""Universal Universal Home Assistant pytest fixtures and test helpers."""

import pytest

# Install Universal Universal Home Assistant's httpx and voluptuous aliases before test dependencies.
import universalassistant  # noqa: F401

# Preserve assertion introspection when helpers are imported through compatibility modules.
pytest.register_assert_rewrite(
    "pytest_universalassistant.common",
    "pytest_universalassistant.plugins",
    "pytest_universalassistant.components.common",
    "pytest_universalassistant.components.diagnostics",
    "pytest_universalassistant.components.infrared.common",
    "pytest_universalassistant.components.mqtt.common",
    "pytest_universalassistant.components.radio_frequency.common",
    "pytest_universalassistant.components.recorder.common",
    "pytest_universalassistant.components.repairs",
)
