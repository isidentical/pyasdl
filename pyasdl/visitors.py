from __future__ import annotations

from typing import Any, cast

from pyasdl.grammar import AST


class Visitor:
    def __call__(self, node: AST, *args, **kwargs) -> Any:
        ...


class ASDLVisitor:
    def visit(self, node: AST, *args, **kwargs) -> Any:
        visitor = self.find_visitor(type(node).__name__)
        return visitor(node, *args, **kwargs)

    def visit_all(self, nodes: list[AST], *args, **kwags) -> list[Any]:
        return [self.visit(node, *args, **kwags) for node in nodes]

    def generic_visit(self, node: AST, *args, **kwags) -> AST:
        for value in vars(node).values():
            if isinstance(value, AST):
                self.visit(value)
            elif isinstance(value, list):
                self.visit_all(value)
        return node

    def find_visitor(self, name: str) -> Visitor:
        visitor = f"visit_{name}"
        if hasattr(self, visitor):
            func = getattr(self, visitor)
        else:
            func = self.generic_visit
        return cast(Visitor, func)
