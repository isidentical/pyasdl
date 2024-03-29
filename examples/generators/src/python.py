from __future__ import annotations

import ast
import textwrap
from argparse import ArgumentParser
from pathlib import Path

import pyasdl

_BASE_CLASS = "AST"

_FIELD = ast.Name("_field", ast.Load())
_TYPING = ast.Name("typing", ast.Load())
_ELLIPSIS = [ast.Constant(Ellipsis, kind=None)]
_AUTO_CALL = ast.Call(ast.Name("_auto", ast.Load()), args=[], keywords=[])


class PythonGenerator(pyasdl.ASDLVisitor):
    def __init__(self, with_defaults):
        self.definitions = []
        self.with_defaults = with_defaults

    def visit_Type(self, node):
        self.visit(
            node.value,
            name=node.name,
            attributes=self.visit_all(node.value.attributes),
        )

    def visit_Sum(self, node, name, attributes):
        if pyasdl.is_simple_sum(node):
            self._create_enum(
                name=name,
                fields=[constructor.name for constructor in node.types],
            )
        else:
            self._create_class(
                name=name, base=_BASE_CLASS, body=attributes or _ELLIPSIS
            )
            self.visit_all(node.types, base=name)

    def visit_Constructor(self, node, base):
        self._create_dataclass(
            name=node.name,
            base=base,
            body=self.visit_all(node.fields) if node.fields else _ELLIPSIS,
        )

    def visit_Product(self, node, name, attributes):
        self._create_dataclass(
            name=name,
            base=_BASE_CLASS,
            body=self.visit_all(node.fields) + attributes,
        )

    def visit_Field(self, node):
        target = ast.Name(node.name, ast.Store())
        annotation = ast.Name(node.kind, ast.Load())
        if node.qualifier is not None:
            if node.qualifier is pyasdl.FieldQualifier.SEQUENCE:
                qualifier = "List"
                default = ast.Call(
                    _FIELD,
                    [],
                    [ast.keyword("default_factory", ast.Name("list", ast.Load()))],
                )
            elif node.qualifier is pyasdl.FieldQualifier.OPTIONAL:
                qualifier = "Optional"
                default = ast.Call(
                    _FIELD, [], [ast.keyword("default", ast.Constant(None))]
                )
            else:
                raise ValueError(f"Unexpected field qualifier: {node.qualifier}")

            annotation = ast.Subscript(
                value=ast.Attribute(_TYPING, qualifier, ast.Load()),
                slice=annotation,
                ctx=ast.Load(),
            )
        else:
            # no-default!
            default = None

        if not self.with_defaults:
            default = None

        return ast.AnnAssign(target, annotation, default, simple=1)

    def _create_class(self, name, base, body, decorators=()):
        cls = ast.ClassDef(
            name=name,
            body=body,
            bases=[ast.Name(base, ast.Load())],
            keywords=[],
            decorator_list=[
                ast.Name(decorator, ast.Load()) for decorator in decorators
            ],
        )
        self.definitions.append(cls)

    def _create_dataclass(self, name, base, body):
        return self._create_class(name, base, body, decorators=("_dataclass",))

    def _create_enum(self, name, fields):
        return self._create_class(
            name,
            "_Enum",
            [ast.Assign([ast.Name(field, ast.Load())], _AUTO_CALL) for field in fields],
        )

    def generate(self, tree):
        self.visit(tree)
        return ast.Module(self.definitions, type_ignores=[])


def main():
    parser = ArgumentParser()
    parser.add_argument("file", type=Path)
    parser.add_argument("--with-defaults", action="store_true")
    parser.add_argument("-o", "--out", default=1)
    options = parser.parse_args()

    with open(options.file) as stream:
        tree = pyasdl.parse(stream.read())

    generator = PythonGenerator(with_defaults=options.with_defaults)
    stub = generator.generate(tree)
    with open(options.out, "w") as stream:
        stream.write("from __future__ import annotations\n\n")
        stream.write("import typing\n")
        stream.write(
            "from dataclasses import dataclass as _dataclass, field as _field\n"
        )
        stream.write("from enum import Enum as _Enum, auto as _auto\n")
        stream.write("identifier = str\n")
        stream.write(
            "string = typing.Union[str, bytes] # Can't use AnyStr before PEP"
            " 613 is supported\n"
        )
        stream.write(
            textwrap.dedent(
                """\
        constant = typing.Union[ # type: ignore
            str,
            bytes,
            # strings
            int,
            float,
            complex,
            # numbers
            bool,
            # other
            tuple,
            frozenset,
            # sequences
            None,
            type(Ellipsis) # type: ignore
            # singletons
        ]\n
        """
            )
        )
        stream.write("class AST: ...\n")
        stream.write(ast.unparse(ast.fix_missing_locations(stub)))
        stream.write("\n")


if __name__ == "__main__":
    main()
