from __future__ import annotations

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


@pytest.mark.parametrize(
    "generator, original_file, args",
    [
        (
            GENERATORS_DIR / "src" / "edgedb.py",
            GENERATORS_DIR / "outputs" / "PythonAST.edgeql",
            [LATEST_ASDL],
        ),
        (
            GENERATORS_DIR / "src" / "graphql.py",
            GENERATORS_DIR / "outputs" / "PythonAST.ql",
            [LATEST_ASDL],
        ),
        (
            GENERATORS_DIR / "src" / "python.py",
            GENERATORS_DIR / "outputs" / "PythonAST.py",
            [LATEST_ASDL],
        ),
        (
            GENERATORS_DIR / "src" / "typing_stub.py",
            GENERATORS_DIR / "outputs" / "PythonAST.pyi",
            ALL_ASDLS.values(),
        ),
    ],
)
def test_generators(tmp_path, generator, original_file, args):
    result = subprocess.check_output([sys.executable, generator, *args], text=True)

    result_file = (tmp_path / "result").with_suffix(original_file.suffix)
    result_file.write_text(result)
    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "pre_commit",
            "run",
            "--files",
            result_file,
        ]
    )
    assert original_file.read_text() == result_file.read_text()
