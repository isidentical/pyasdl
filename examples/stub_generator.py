import ast
from argparse import ArgumentParser
from textwrap import dedent
from typing import Iterator

import pyasdl


class TestVisitor(pyasdl.ASDLVisitor):
    _BOOTSTRAP = ast.parse(
        dedent(
            """\
    from __future__ import annotations
    from typing import List, Optional, Union

    identifier = str
    string = Union[str, bytes]
    constant = Union[
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
        type(Ellipsis)
        # singletons
    ]

    class AST: ...
    """
        )
    ).body

    def visit_Module(self, node: pyasdl.Module) -> ast.Module:
        body = []
        for definition in node.body:
            body.extend(self.visit(definition))
        return ast.Module(body=self._BOOTSTRAP + body, type_ignores=[])

    def visit_Type(self, node: pyasdl.Type) -> Iterator[ast.ClassDef]:
        attributes = self.visit_all(node.value.attributes)

        if isinstance(node.value, pyasdl.Sum):
            yield self._create_type(node.name, "AST", attributes)
            for constructor in node.value.types:
                yield self._create_type(
                    constructor.name,
                    node.name,
                    self.visit_all(constructor.fields or ()),
                )

        elif isinstance(node.value, pyasdl.Product):
            yield self._create_type(
                node.name,
                "AST",
                [*self.visit_all(node.value.fields), *attributes],
            )
        else:
            raise TypeError(
                "Expected either a Product or a Sum, not: ",
                type(node.value).__name__,
            )

    def visit_Field(self, node: pyasdl.Field):
        target = ast.Name(node.name, ast.Store())
        annotation = ast.Name(node.kind, ast.Load())
        if node.qualifier is not None:
            if node.qualifier is pyasdl.FieldQualifier.SEQUENCE:
                qualifier = "List"
            elif node.qualifier is pyasdl.FieldQualifier.OPTIONAL:
                qualifier = "Optional"
            else:
                raise ValueError("Unexpected Field Qualifier")

            annotation = ast.Subscript(
                value=ast.Name(qualifier, ast.Load()),
                slice=annotation,
                ctx=ast.Load(),
            )
        return ast.AnnAssign(target, annotation, simple=1)

    def _create_type(self, name, base="AST", body=None):
        body = body or [ast.Expr(ast.Constant(...))]
        return ast.ClassDef(
            name=name,
            bases=[ast.Name(base, ast.Load())],
            keywords=[],
            body=body,
            decorator_list=[],
        )


def main():
    parser = ArgumentParser()
    parser.add_argument("file")
    options = parser.parse_args()

    with open(options.file) as f:
        tree = pyasdl.parse(f.read(), filename=options.file)

    visitor = TestVisitor()
    print(ast.unparse(visitor.visit(tree)))


if __name__ == "__main__":
    main()
