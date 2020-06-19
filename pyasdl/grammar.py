from __future__ import annotations

import dataclasses
from dataclasses import dataclass
from enum import Enum, auto


class AST:
    pass


class Node(AST):
    pass


class Leaf(AST):
    pass


@dataclass
class Module(Node):
    name: str
    body: List[Type]


@dataclass
class Type(Node):
    name: str
    value: Node


@dataclass
class Sum(Node):
    types: List[Constructor]
    attributes: List[Field] = dataclasses.field(default_factory=list)


@dataclass
class Product(Node):
    fields: List[Field]
    attributes: List[Field] = dataclasses.field(default_factory=list)


@dataclass
class Constructor(Node):
    name: str
    fields: Optional[List[Field]] = None


class FieldQualifier(Enum):
    OPTIONAL = auto()
    SEQUENCE = auto()

    def __repr__(self):
        return f"FieldQualifier.{self.name}"


@dataclass
class Field(Leaf):
    kind: str
    name: str
    qualifier: Optional[FieldQualifier] = None


class ASDLVisitor:
    def visit(self, node: AST) -> None:
        if visitor := getattr(self, f"visit_{type(node).__name__}", None):
            visitor(node)
        else:
            self.generic_visit(node)

    def generic_visit(self, node: AST) -> None:
        def traverse(node):
            if isinstance(node, AST):
                self.visit(node)

        if not dataclasses.is_dataclass(node):
            return None

        # vars() preffered over dataclasses.asdict since it
        # recursively converts all values to dict instead of
        # only the give node.
        for field, value in vars(node).items():
            if isinstance(value, list):
                for item in value:
                    traverse(item)
            else:
                traverse(value)
