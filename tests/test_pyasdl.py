import ast
import subprocess
import sys
from pathlib import Path

import pytest

import pyasdl
from pyasdl import *

EXAMPLES_DIR = Path(__file__).parent.parent / "examples"
GENERATORS_DIR = EXAMPLES_DIR / "generators"
ASDL_DIR = EXAMPLES_DIR / "cpython"

ALL_ASDLS = {
    # Python-<version>.asdl
    int(file.stem.split("-")[1]): file
    for file in ASDL_DIR.iterdir()
    if file.suffix == ".asdl"
}
LATEST_ASDL = ALL_ASDLS[max(ALL_ASDLS)]


def test_asdl_generation():
    with open(EXAMPLES_DIR / "example.asdl") as stream:
        parsed_ast = pyasdl.parse(stream.read(), filename="example.asdl")

    expected_ast = Module(
        name="Test",
        body=[
            Type(
                name="type1",
                value=Sum(
                    types=[
                        Constructor(
                            name="Type1",
                            fields=[
                                Field(kind="int", name="id", qualifier=None),
                                Field(
                                    kind="constant",
                                    name="name",
                                    qualifier=None,
                                ),
                            ],
                        )
                    ],
                    attributes=[],
                ),
            ),
            Type(
                name="base_type",
                value=Sum(
                    types=[
                        Constructor(name="Type2", fields=[]),
                        Constructor(
                            name="Type3",
                            fields=[
                                Field(
                                    kind="identifier",
                                    name="name",
                                    qualifier=None,
                                )
                            ],
                        ),
                    ],
                    attributes=[],
                ),
            ),
            Type(
                name="operators",
                value=Sum(
                    types=[
                        Constructor(name="Add", fields=[]),
                        Constructor(name="Sub", fields=[]),
                    ],
                    attributes=[],
                ),
            ),
        ],
    )
    assert parsed_ast == expected_ast


regular_equality = lambda result, original: result == original


def ast_based_equality(result, original):
    def nuke_imports(tree):
        # isort changes the AST (re-orders imports), so
        # for a better equalivance we'll remove all
        # imports.

        for node in tree.body.copy():
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                tree.body.remove(node)

    tree_1, tree_2 = ast.parse(result), ast.parse(original)
    nuke_imports(tree_1)
    nuke_imports(tree_2)
    return ast.dump(tree_1, indent=4) == ast.dump(tree_2, indent=4)


@pytest.mark.parametrize(
    "generator, original_file, args, equality_func",
    [
        (
            GENERATORS_DIR / "src" / "edgedb.py",
            GENERATORS_DIR / "outputs" / "PythonAST.edgeql",
            [LATEST_ASDL],
            regular_equality,
        ),
        (
            GENERATORS_DIR / "src" / "graphql.py",
            GENERATORS_DIR / "outputs" / "PythonAST.ql",
            [LATEST_ASDL],
            regular_equality,
        ),
        (
            GENERATORS_DIR / "src" / "python.py",
            GENERATORS_DIR / "outputs" / "PythonAST.py",
            [LATEST_ASDL],
            ast_based_equality,
        ),
        (
            GENERATORS_DIR / "src" / "typing_stub.py",
            GENERATORS_DIR / "outputs" / "PythonAST.pyi",
            ALL_ASDLS.values(),
            ast_based_equality,
        ),
    ],
)
def test_generators(generator, original_file, args, equality_func):
    original = original_file.read_text()
    result = subprocess.check_output(
        [sys.executable, generator, *args], text=True
    )
    assert equality_func(original, result)
