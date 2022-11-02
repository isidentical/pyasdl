# @generated by generators/python.py from pyasdl/static/grammar.asdl

from __future__ import annotations

import typing
from dataclasses import dataclass as _dataclass
from dataclasses import field as _field
from enum import Enum as _Enum
from enum import auto as _auto

identifier = str
string = typing.Union[str, bytes]  # Can't use AnyStr before PEP 613 is supported
constant = typing.Union[  # type: ignore
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
    type(Ellipsis)  # type: ignore
    # singletons
]


class AST:
    ...


@_dataclass
class Module(AST):
    name: string
    body: list[Type] = _field(default_factory=list)


@_dataclass
class Type(AST):
    name: string
    value: type


class type(AST):
    ...


@_dataclass
class Sum(type):
    types: list[Constructor] = _field(default_factory=list)
    attributes: list[Field] = _field(default_factory=list)


@_dataclass
class Product(type):
    fields: list[Field] = _field(default_factory=list)
    attributes: list[Field] = _field(default_factory=list)


@_dataclass
class Constructor(AST):
    name: string
    fields: list[Field] = _field(default_factory=list)


@_dataclass
class Field(AST):
    kind: string
    name: string
    qualifier: FieldQualifier | None = _field(default=None)


class FieldQualifier(_Enum):
    OPTIONAL = _auto()
    SEQUENCE = _auto()
