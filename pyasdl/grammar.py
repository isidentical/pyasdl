from __future__ import annotations

import typing
from dataclasses import dataclass as _dataclass
from dataclasses import field as _field
from enum import Enum as _Enum
from enum import auto as _auto

identifier = str
string = typing.AnyStr
constant = typing.Union[
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


class AST:
    ...


@_dataclass
class Module(AST):
    name: string
    body: typing.List[Type] = _field(default_factory=list)


@_dataclass
class Type(AST):
    name: string
    value: type


class type(AST):
    ...


@_dataclass
class Sum(type):
    types: typing.List[Constructor] = _field(default_factory=list)
    attributes: typing.List[field] = _field(default_factory=list)


@_dataclass
class Product(type):
    fields: typing.List[field] = _field(default_factory=list)
    attributes: typing.List[field] = _field(default_factory=list)


@_dataclass
class Constructor(AST):
    name: string
    fields: typing.List[field] = _field(default_factory=list)


@_dataclass
class Field(AST):
    kind: string
    name: string
    qualifier: typing.Optional[field_qualifier] = _field(default=None)


class FieldQualifier(_Enum):
    OPTIONAL = _auto()
    SEQUENCE = _auto()
