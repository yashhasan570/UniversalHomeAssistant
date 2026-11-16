"""Test recorder system health."""

from unittest.mock import ANY, Mock, patch

import pytest
from pytest_universalassistant.common import get_system_health_info
from pytest_universalassistant.components.recorder.common import async_wait_recording_done
from pytest_universalassistant.typing import RecorderInstanceGenerator

from universalassistant.components.recorder import get_instance
from universalassistant.components.recorder.const import SupportedDialect
from universalassistant.core import UniversalAssistant
from universalassistant.setup import async_setup_component


@pytest.mark.skip_on_db_engine(["mysql", "postgresql"])
@pytest.mark.usefixtures("skip_by_db_engine", "recorder_mock")
async def test_recorder_system_health(
    hass: UniversalAssistant, recorder_db_url: str
) -> None:
    """Test recorder system health.

    This test is specific for SQLite.
    """

    assert await async_setup_component(hass, "system_health", {})
    await async_wait_recording_done(hass)
    info = await get_system_health_info(hass, "recorder")
    instance = get_instance(hass)
    assert info == {
        "current_recorder_run": instance.recorder_runs_manager.current.start,
        "oldest_recorder_run": instance.recorder_runs_manager.first.start,
        "estimated_db_size": ANY,
        "database_engine": SupportedDialect.SQLITE.value,
        "database_version": ANY,
    }


@pytest.mark.parametrize(
    "db_engine", [SupportedDialect.MYSQL, SupportedDialect.POSTGRESQL]
)
@pytest.mark.usefixtures("recorder_mock")
async def test_recorder_system_health_alternate_dbms(
    hass: UniversalAssistant,
    db_engine: SupportedDialect,
    recorder_dialect_name: None,
) -> None:
    """Test recorder system health."""
    assert await async_setup_component(hass, "system_health", {})
    await async_wait_recording_done(hass)
    with (
        patch(
            "sqlalchemy.orm.session.Session.execute",
            return_value=Mock(scalar=Mock(return_value=("1048576"))),
        ),
    ):
        info = await get_system_health_info(hass, "recorder")
    instance = get_instance(hass)
    assert info == {
        "current_recorder_run": instance.recorder_runs_manager.current.start,
        "oldest_recorder_run": instance.recorder_runs_manager.first.start,
        "estimated_db_size": "1.00 MiB",
        "database_engine": db_engine.value,
        "database_version": ANY,
    }


@pytest.mark.parametrize(
    "db_engine", [SupportedDialect.MYSQL, SupportedDialect.POSTGRESQL]
)
@pytest.mark.usefixtures("recorder_mock")
async def test_recorder_system_health_db_url_missing_host(
    hass: UniversalAssistant,
    db_engine: SupportedDialect,
    recorder_dialect_name: None,
) -> None:
    """Test recorder system health with a db_url without a hostname."""
    assert await async_setup_component(hass, "system_health", {})
    await async_wait_recording_done(hass)

    instance = get_instance(hass)
    with (
        patch.object(
            instance,
            "db_url",
            "postgresql://universalassistant:blabla@/universal_assistant?host=/config/socket",
        ),
        patch(
            "sqlalchemy.orm.session.Session.execute",
            return_value=Mock(scalar=Mock(return_value=("1048576"))),
        ),
    ):
        info = await get_system_health_info(hass, "recorder")
    assert info == {
        "current_recorder_run": instance.recorder_runs_manager.current.start,
        "oldest_recorder_run": instance.recorder_runs_manager.first.start,
        "estimated_db_size": "1.00 MiB",
        "database_engine": db_engine.value,
        "database_version": ANY,
    }


@pytest.mark.skip_on_db_engine(["mysql", "postgresql"])
@pytest.mark.usefixtures("skip_by_db_engine")
async def test_recorder_system_health_crashed_recorder_runs_table(
    async_setup_recorder_instance: RecorderInstanceGenerator,
    hass: UniversalAssistant,
    recorder_db_url: str,
) -> None:
    """Test recorder system health with crashed recorder runs table.

    This test is specific for SQLite.
    """

    with patch(
        "universalassistant.components.recorder.table_managers.recorder_runs.RecorderRunsManager.load_from_db"
    ):
        assert await async_setup_component(hass, "system_health", {})
        instance = await async_setup_recorder_instance(hass)
        await async_wait_recording_done(hass)
    info = await get_system_health_info(hass, "recorder")
    assert info == {
        "current_recorder_run": instance.recorder_runs_manager.current.start,
        "oldest_recorder_run": instance.recorder_runs_manager.current.start,
        "estimated_db_size": ANY,
        "database_engine": SupportedDialect.SQLITE.value,
        "database_version": ANY,
    }


@pytest.mark.parametrize("db_engine", [SupportedDialect.POSTGRESQL])
@pytest.mark.parametrize(
    "db_url",
    [
        "postgresql://universalassistant:secret@192.168.0.2:5432/universal_assistant",
        "postgresql://universalassistant:pa#ss@192.168.0.2:5432/universal_assistant",
        "postgresql://universalassistant:pa?ss@192.168.0.2:5432/universal_assistant",
        "postgresql://universalassistant:pa/ss@192.168.0.2:5432/universal_assistant",
    ],
    ids=["plain", "hash", "question_mark", "slash"],
)
@pytest.mark.usefixtures("recorder_mock")
async def test_recorder_system_health_db_name_with_special_characters(
    hass: UniversalAssistant,
    db_engine: SupportedDialect,
    db_url: str,
    recorder_dialect_name: None,
) -> None:
    """Test the database name is read correctly when the password needs escaping.

    Characters that are structural in a generic URL, such as ``#`` and ``?``,
    must not be allowed to swallow the database name that follows them.
    """
    assert await async_setup_component(hass, "system_health", {})
    await async_wait_recording_done(hass)

    instance = get_instance(hass)
    with (
        patch.object(instance, "db_url", db_url),
        patch(
            "sqlalchemy.orm.session.Session.execute",
            return_value=Mock(scalar=Mock(return_value=("1048576"))),
        ) as execute_mock,
    ):
        await get_system_health_info(hass, "recorder")

    assert execute_mock.call_args.args[1] == {"database_name": "universal_assistant"}
