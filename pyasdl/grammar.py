from __future__ import annotations

import re
import token as _token
import tokenize as _tokenize
from dataclasses import dataclass, field
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
    attributes: List[Field] = field(default_factory=list)


@dataclass
class Product(Node):
    fields: List[Field]
    attributes: List[Field] = field(default_factory=list)


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


def add_comment_type(prefix):
    _tokenize.EXACT_TOKEN_TYPES[prefix] = _token.COMMENT
    _tokenize.PseudoToken = _tokenize.Whitespace + _tokenize.group(
        re.escape(prefix),
        _tokenize.PseudoExtras,
        _tokenize.Number,
        _tokenize.Funny,
        _tokenize.ContStr,
        _tokenize.Name,
    )
