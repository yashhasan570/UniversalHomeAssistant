"""Tests for pylint hass_imports plugin."""

from pathlib import Path
import textwrap

import astroid
from pylint.checkers import BaseChecker
import pylint.testutils
from pylint.testutils.unittest_linter import UnittestLinter
import pytest

from . import assert_adds_messages, assert_no_messages


@pytest.mark.parametrize(
    ("module_name", "import_from", "import_what"),
    [
        (
            "universalassistant.components.pylint_test.sensor",
            "universalassistant.const",
            "CONSTANT",
        ),
        (
            "universalassistant.components.pylint_test.sensor",
            "universalassistant.components.pylint_testing",
            "CONSTANT",
        ),
        ("universalassistant.components.pylint_test.sensor", ".const", "CONSTANT"),
        ("universalassistant.components.pylint_test.sensor", ".", "CONSTANT"),
        ("universalassistant.components.pylint_test.sensor", "..", "pylint_test"),
        (
            "universalassistant.components.pylint_test.api.hub",
            "universalassistant.const",
            "CONSTANT",
        ),
        ("universalassistant.components.pylint_test.api.hub", "..const", "CONSTANT"),
        ("universalassistant.components.pylint_test.api.hub", "..", "CONSTANT"),
        ("universalassistant.components.pylint_test.api.hub", "...", "pylint_test"),
        ("tests.components.pylint_test.api.hub", "..const", "CONSTANT"),
    ],
)
def test_good_import(
    linter: UnittestLinter,
    imports_checker: BaseChecker,
    module_name: str,
    import_from: str,
    import_what: str,
) -> None:
    """Ensure good imports pass through ok."""

    import_node = astroid.extract_node(
        f"from {import_from} import {import_what} #@",
        module_name,
    )
    imports_checker.visit_module(import_node.parent)

    with assert_no_messages(linter):
        imports_checker.visit_importfrom(import_node)


@pytest.mark.parametrize(
    ("module_name", "import_from", "import_what", "error_code"),
    [
        (
            "universalassistant.components.pylint_test.sensor",
            "universalassistant.components.pylint_test.const",
            "CONSTANT",
            "universal-assistant-relative-import",
        ),
        (
            "universalassistant.components.pylint_test.sensor",
            "..const",
            "CONSTANT",
            "universal-assistant-absolute-import",
        ),
        (
            "universalassistant.components.pylint_test.sensor",
            "...const",
            "CONSTANT",
            "universal-assistant-absolute-import",
        ),
        (
            "universalassistant.components.pylint_test.api.hub",
            "universalassistant.components.pylint_test.api.const",
            "CONSTANT",
            "universal-assistant-relative-import",
        ),
        (
            "universalassistant.components.pylint_test.api.hub",
            "...const",
            "CONSTANT",
            "universal-assistant-absolute-import",
        ),
        (
            "universalassistant.components.pylint_test.api.hub",
            "universalassistant.components",
            "pylint_test",
            "universal-assistant-relative-import",
        ),
        (
            "universalassistant.components.pylint_test.api.hub",
            "universalassistant.components.pylint_test.const",
            "CONSTANT",
            "universal-assistant-relative-import",
        ),
        (
            "tests.components.pylint_test.api.hub",
            "tests.components.pylint_test.const",
            "CONSTANT",
            "universal-assistant-relative-import",
        ),
        (
            "tests.components.pylint_test.api.hub",
            "...const",
            "CONSTANT",
            "universal-assistant-absolute-import",
        ),
    ],
)
def test_bad_import(
    linter: UnittestLinter,
    imports_checker: BaseChecker,
    module_name: str,
    import_from: str,
    import_what: str,
    error_code: str,
) -> None:
    """Ensure bad imports are rejected."""

    import_node = astroid.extract_node(
        f"from {import_from} import {import_what} #@",
        module_name,
    )
    imports_checker.visit_module(import_node.parent)

    with assert_adds_messages(
        linter,
        pylint.testutils.MessageTest(
            msg_id=error_code,
            node=import_node,
            args=None,
            line=1,
            col_offset=0,
            end_line=1,
            end_col_offset=len(import_from) + len(import_what) + 13,
        ),
    ):
        imports_checker.visit_importfrom(import_node)


@pytest.mark.parametrize(
    ("import_node", "module_name"),
    [
        (
            "from universalassistant.components import climate",
            "universalassistant.components.pylint_test.climate",
        ),
        (
            "from universalassistant.components.climate import ClimateEntityFeature",
            "universalassistant.components.pylint_test.climate",
        ),
        (
            "from universalassistant.components.pylint_test import const",
            "tests.components.pylint_test.climate",
        ),
        (
            "from universalassistant.components.pylint_test.const import CONSTANT",
            "tests.components.pylint_test.climate",
        ),
        (
            "import universalassistant.components.pylint_test.const as climate",
            "tests.components.pylint_test.climate",
        ),
    ],
)
def test_good_root_import(
    linter: UnittestLinter,
    imports_checker: BaseChecker,
    import_node: str,
    module_name: str,
) -> None:
    """Ensure bad root imports are rejected."""

    node = astroid.extract_node(
        f"{import_node} #@",
        module_name,
    )
    imports_checker.visit_module(node.parent)

    with assert_no_messages(linter):
        if import_node.startswith("import"):
            imports_checker.visit_import(node)
        if import_node.startswith("from"):
            imports_checker.visit_importfrom(node)


@pytest.mark.parametrize(
    ("import_node", "module_name"),
    [
        (
            "import universalassistant.components.climate.const as climate",
            "universalassistant.components.pylint_test.climate",
        ),
        (
            "from universalassistant.components.climate import const",
            "universalassistant.components.pylint_test.climate",
        ),
        (
            "from universalassistant.components.climate.const import ClimateEntityFeature",
            "universalassistant.components.pylint_test.climate",
        ),
        (
            "from universalassistant.components.climate.entity import ClimateEntityFeature",
            "universalassistant.components.pylint_test.climate",
        ),
        (
            "from universalassistant.components.climate import const",
            "tests.components.pylint_test.climate",
        ),
        (
            "from universalassistant.components.climate.const import CONSTANT",
            "tests.components.pylint_test.climate",
        ),
        (
            "import universalassistant.components.climate.const as climate",
            "tests.components.pylint_test.climate",
        ),
        (
            "import universalassistant.components.climate.entity as climate",
            "tests.components.pylint_test.climate",
        ),
    ],
)
def test_bad_root_import(
    linter: UnittestLinter,
    imports_checker: BaseChecker,
    import_node: str,
    module_name: str,
) -> None:
    """Ensure bad root imports are rejected."""

    node = astroid.extract_node(
        f"{import_node} #@",
        module_name,
    )
    imports_checker.visit_module(node.parent)

    with assert_adds_messages(
        linter,
        pylint.testutils.MessageTest(
            msg_id="universal-assistant-component-root-import",
            node=node,
            args=None,
            line=1,
            col_offset=0,
            end_line=1,
            end_col_offset=len(import_node),
        ),
    ):
        if import_node.startswith("import"):
            imports_checker.visit_import(node)
        if import_node.startswith("from"):
            imports_checker.visit_importfrom(node)


@pytest.mark.parametrize(
    ("import_node", "module_name", "expected_args"),
    [
        (
            "from universalassistant.helpers.issue_registry import async_get",
            "tests.components.pylint_test.climate",
            (
                "async_get",
                "universalassistant.helpers.issue_registry",
                "ir",
                "ir",
                "async_get",
            ),
        ),
        (
            (
                "from universalassistant.helpers.issue_registry"
                " import async_get as async_get_issue_registry"
            ),
            "tests.components.pylint_test.climate",
            (
                "async_get",
                "universalassistant.helpers.issue_registry",
                "ir",
                "ir",
                "async_get",
            ),
        ),
    ],
)
def test_bad_namespace_import(
    linter: UnittestLinter,
    imports_checker: BaseChecker,
    import_node: str,
    module_name: str,
    expected_args: tuple[str, ...],
) -> None:
    """Ensure bad namespace imports are rejected."""

    node = astroid.extract_node(
        f"{import_node} #@",
        module_name,
    )
    imports_checker.visit_module(node.parent)

    with assert_adds_messages(
        linter,
        pylint.testutils.MessageTest(
            msg_id="universal-assistant-helper-namespace-import",
            node=node,
            args=expected_args,
            line=1,
            col_offset=0,
            end_line=1,
            end_col_offset=len(import_node),
        ),
    ):
        imports_checker.visit_importfrom(node)


@pytest.mark.parametrize(
    ("module_name", "import_string", "end_col_offset"),
    [
        (
            "universalassistant.components.pylint_test.sensor",
            "from universalassistant.components.other import DOMAIN as OTHER_DOMAIN",
            -1,
        ),
        (
            "universalassistant.components.pylint_test.sensor",
            "from universalassistant.components.other import DOMAIN",
            49,
        ),
    ],
)
def test_domain_alias(
    linter: UnittestLinter,
    imports_checker: BaseChecker,
    module_name: str,
    import_string: str,
    end_col_offset: int,
) -> None:
    """Ensure good imports pass through ok."""

    import_node = astroid.extract_node(
        f"{import_string}  #@",
        module_name,
    )
    imports_checker.visit_module(import_node.parent)

    expected_messages = []
    if end_col_offset > 0:
        expected_messages.append(
            pylint.testutils.MessageTest(
                msg_id="universal-assistant-import-constant-alias",
                node=import_node,
                args=("DOMAIN", "DOMAIN", "OTHER_DOMAIN"),
                line=1,
                col_offset=0,
                end_line=1,
                end_col_offset=end_col_offset,
            )
        )

    with assert_adds_messages(linter, *expected_messages):
        if import_string.startswith("import"):
            imports_checker.visit_import(import_node)
        else:
            imports_checker.visit_importfrom(import_node)


@pytest.mark.parametrize(
    ("module_name", "code"),
    [
        pytest.param(
            "universalassistant.components.pylint_test",
            """
            from .const import DOMAIN, SERVICE  # noqa: F401

            __all__ = ["DOMAIN"]
            """,
            id="noqa_with_all",
        ),
        pytest.param(
            "universalassistant.components.pylint_test",
            """
            from .const import (
                DOMAIN,
                SERVICE,  # noqa: F401
            )

            __all__ = ["DOMAIN"]
            """,
            id="per_name_noqa_with_all",
        ),
        pytest.param(
            "universalassistant.components.pylint_test",
            """
            from .const import DOMAIN, SERVICE  # noqa: E501, F401

            __all__ = ["DOMAIN"]
            """,
            id="combined_noqa_with_all",
        ),
        pytest.param(
            "universalassistant.components.pylint_test",
            """
            from . import CONSTANT, sensor  # noqa: F401

            __all__ = ["DOMAIN"]
            """,
            id="mixed_submodule_noqa_with_all",
        ),
        pytest.param(
            "universalassistant.components.pylint_test.sensor",
            """
            from .const import DOMAIN, SERVICE  # noqa: F401

            __all__ = ["DOMAIN"]
            """,
            id="noqa_with_all_in_submodule",
        ),
    ],
)
def test_bad_noqa_f401_with_all(
    linter: UnittestLinter,
    imports_checker: BaseChecker,
    tmp_path: Path,
    module_name: str,
    code: str,
) -> None:
    """Ensure `# noqa: F401` is reported in modules defining __all__."""
    (tmp_path / "sensor.py").touch()
    root_node = astroid.parse(
        textwrap.dedent(code), module_name, str(tmp_path / "__init__.py")
    )
    import_node = root_node.body[0]

    with assert_adds_messages(
        linter,
        pylint.testutils.MessageTest(
            msg_id="universal-assistant-noqa-f401-with-all",
            node=import_node,
            line=import_node.lineno,
            col_offset=import_node.col_offset,
            end_line=import_node.end_lineno,
            end_col_offset=import_node.end_col_offset,
        ),
    ):
        imports_checker.visit_module(root_node)


@pytest.mark.parametrize(
    ("module_name", "code"),
    [
        pytest.param(
            "universalassistant.components.pylint_test",
            """
            from .const import DOMAIN, SERVICE  # noqa: F401
            """,
            id="noqa_without_all",
        ),
        pytest.param(
            "universalassistant.components.pylint_test",
            """
            from .const import DOMAIN, SERVICE

            __all__ = ["DOMAIN", "SERVICE"]
            """,
            id="all_without_noqa",
        ),
        pytest.param(
            "universalassistant.components.pylint_test",
            """
            from . import sensor, switch  # noqa: F401

            __all__ = ["DOMAIN"]
            """,
            id="submodule_preload",
        ),
        pytest.param(
            "tests.components.pylint_test",
            """
            from .const import DOMAIN, SERVICE  # noqa: F401

            __all__ = ["DOMAIN"]
            """,
            id="test_module",
        ),
        pytest.param(
            "universalassistant.helpers.pylint_test",
            """
            from .const import DOMAIN, SERVICE  # noqa: F401

            __all__ = ["DOMAIN"]
            """,
            id="not_an_integration",
        ),
        pytest.param(
            "universalassistant.components.pylint_test",
            """
            __all__ = ["DOMAIN"]

            def check() -> bool:
                import pylint_test_library  # noqa: F401

                return True
            """,
            id="function_local_import",
        ),
        pytest.param(
            "universalassistant.components.pylint_test",
            """
            __all__ = ["DOMAIN"]

            class Check:
                from .const import SERVICE  # noqa: F401
            """,
            id="class_local_import",
        ),
    ],
)
def test_good_noqa_f401_with_all(
    linter: UnittestLinter,
    imports_checker: BaseChecker,
    tmp_path: Path,
    module_name: str,
    code: str,
) -> None:
    """Ensure allowed `# noqa: F401` usages are not reported."""
    (tmp_path / "sensor.py").touch()
    (tmp_path / "switch").mkdir()
    root_node = astroid.parse(
        textwrap.dedent(code), module_name, str(tmp_path / "__init__.py")
    )

    with assert_no_messages(linter):
        imports_checker.visit_module(root_node)


def test_good_noqa_f401_with_all_sibling_preload(
    linter: UnittestLinter,
    imports_checker: BaseChecker,
    tmp_path: Path,
) -> None:
    """Ensure preloading sibling submodules from an ordinary module passes."""
    (tmp_path / "sensor.py").touch()
    root_node = astroid.parse(
        textwrap.dedent(
            """
            from . import sensor  # noqa: F401

            __all__ = ["DOMAIN"]
            """
        ),
        "universalassistant.components.pylint_test.api",
        str(tmp_path / "api.py"),
    )

    with assert_no_messages(linter):
        imports_checker.visit_module(root_node)


def test_bad_noqa_f401_with_all_module_level_block(
    linter: UnittestLinter,
    imports_checker: BaseChecker,
    tmp_path: Path,
) -> None:
    """Ensure imports in module-level blocks are still reported."""
    root_node = astroid.parse(
        textwrap.dedent(
            """
            try:
                from .const import SERVICE  # noqa: F401
            except ImportError:
                pass

            __all__ = ["DOMAIN"]
            """
        ),
        "universalassistant.components.pylint_test",
        str(tmp_path / "__init__.py"),
    )
    import_node = root_node.body[0].body[0]

    with assert_adds_messages(
        linter,
        pylint.testutils.MessageTest(
            msg_id="universal-assistant-noqa-f401-with-all",
            node=import_node,
            line=import_node.lineno,
            col_offset=import_node.col_offset,
            end_line=import_node.end_lineno,
            end_col_offset=import_node.end_col_offset,
        ),
    ):
        imports_checker.visit_module(root_node)
