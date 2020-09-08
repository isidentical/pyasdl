from __future__ import annotations

from typing import Any, Callable, List

from pyasdl.grammar import AST

VisitorType = Callable[["ASDLVisitor", AST], Any]


class ASDLVisitor:
    def visit(self, node: AST) -> Any:
        visitor = self.find_visitor(type(node).__name__)
        return visitor(node)

    def visit_all(self, nodes: List[AST]) -> List[Any]:
        return [self.visit(node) for node in nodes]

    def generic_visit(self, node: AST) -> AST:
        for value in vars(node).values():
            if isinstance(value, AST):
                self.visit(value)
            elif isinstance(value, list):
                self.visit_all(value)
        return node

    def find_visitor(self, name: str) -> VisitorType:
        visitor = f"visit_{name}"
        if hasattr(self, visitor):
            return getattr(self, visitor)
        else:
            return self.generic_visit
