from __future__ import annotations

import dataclasses
from dataclasses import dataclass
from enum import Enum, auto
from typing import List, Optional, Union


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
    value: Union[Sum, Product]


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
