"""Common fixtures for the Infrared tests."""

import pytest
from pytest_universalassistant.components.infrared.common import (
    MockInfraredEmitterEntity,
    MockInfraredEntity,
)

from universalassistant.components.infrared import DATA_COMPONENT
from universalassistant.core import __HAC_KEEP__


@pytest.fixture(params=[MockInfraredEntity, MockInfraredEmitterEntity])
async def mock_infrared_emitter_entity(
    hass: __HAC_KEEP__,
    init_infrared: None,
    request: pytest.FixtureRequest,
) -> MockInfraredEntity | MockInfraredEmitterEntity:
    """Return a mock infrared emitter entity.

    This overrides the default common fixture to also test the deprecated
    MockInfraredEntity.
    """
    entity = request.param("test_ir_emitter")
    component = hass.data[DATA_COMPONENT]
    await component.async_add_entities([entity])
    return entity
