from __future__ import annotations

import typing
from dataclasses import dataclass as _dataclass
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


class mod(AST):
    ...


@_dataclass
class Module(mod):
    body: typing.List[stmt]
    type_ignores: typing.List[type_ignore]


@_dataclass
class Interactive(mod):
    body: typing.List[stmt]


@_dataclass
class Expression(mod):
    body: expr


@_dataclass
class FunctionType(mod):
    argtypes: typing.List[expr]
    returns: expr


class stmt(AST):
    lineno: int
    col_offset: int
    end_lineno: typing.Optional[int]
    end_col_offset: typing.Optional[int]


@_dataclass
class FunctionDef(stmt):
    name: identifier
    args: arguments
    body: typing.List[stmt]
    decorator_list: typing.List[expr]
    returns: typing.Optional[expr]
    type_comment: typing.Optional[string]


@_dataclass
class AsyncFunctionDef(stmt):
    name: identifier
    args: arguments
    body: typing.List[stmt]
    decorator_list: typing.List[expr]
    returns: typing.Optional[expr]
    type_comment: typing.Optional[string]


@_dataclass
class ClassDef(stmt):
    name: identifier
    bases: typing.List[expr]
    keywords: typing.List[keyword]
    body: typing.List[stmt]
    decorator_list: typing.List[expr]


@_dataclass
class Return(stmt):
    value: typing.Optional[expr]


@_dataclass
class Delete(stmt):
    targets: typing.List[expr]


@_dataclass
class Assign(stmt):
    targets: typing.List[expr]
    value: expr
    type_comment: typing.Optional[string]


@_dataclass
class AugAssign(stmt):
    target: expr
    op: operator
    value: expr


@_dataclass
class AnnAssign(stmt):
    target: expr
    annotation: expr
    value: typing.Optional[expr]
    simple: int


@_dataclass
class For(stmt):
    target: expr
    iter: expr
    body: typing.List[stmt]
    orelse: typing.List[stmt]
    type_comment: typing.Optional[string]


@_dataclass
class AsyncFor(stmt):
    target: expr
    iter: expr
    body: typing.List[stmt]
    orelse: typing.List[stmt]
    type_comment: typing.Optional[string]


@_dataclass
class While(stmt):
    test: expr
    body: typing.List[stmt]
    orelse: typing.List[stmt]


@_dataclass
class If(stmt):
    test: expr
    body: typing.List[stmt]
    orelse: typing.List[stmt]


@_dataclass
class With(stmt):
    items: typing.List[withitem]
    body: typing.List[stmt]
    type_comment: typing.Optional[string]


@_dataclass
class AsyncWith(stmt):
    items: typing.List[withitem]
    body: typing.List[stmt]
    type_comment: typing.Optional[string]


@_dataclass
class Raise(stmt):
    exc: typing.Optional[expr]
    cause: typing.Optional[expr]


@_dataclass
class Try(stmt):
    body: typing.List[stmt]
    handlers: typing.List[excepthandler]
    orelse: typing.List[stmt]
    finalbody: typing.List[stmt]


@_dataclass
class Assert(stmt):
    test: expr
    msg: typing.Optional[expr]


@_dataclass
class Import(stmt):
    names: typing.List[alias]


@_dataclass
class ImportFrom(stmt):
    module: typing.Optional[identifier]
    names: typing.List[alias]
    level: typing.Optional[int]


@_dataclass
class Global(stmt):
    names: typing.List[identifier]


@_dataclass
class Nonlocal(stmt):
    names: typing.List[identifier]


@_dataclass
class Expr(stmt):
    value: expr


@_dataclass
class Pass(stmt):
    ...


@_dataclass
class Break(stmt):
    ...


@_dataclass
class Continue(stmt):
    ...


class expr(AST):
    lineno: int
    col_offset: int
    end_lineno: typing.Optional[int]
    end_col_offset: typing.Optional[int]


@_dataclass
class BoolOp(expr):
    op: boolop
    values: typing.List[expr]


@_dataclass
class NamedExpr(expr):
    target: expr
    value: expr


@_dataclass
class BinOp(expr):
    left: expr
    op: operator
    right: expr


@_dataclass
class UnaryOp(expr):
    op: unaryop
    operand: expr


@_dataclass
class Lambda(expr):
    args: arguments
    body: expr


@_dataclass
class IfExp(expr):
    test: expr
    body: expr
    orelse: expr


@_dataclass
class Dict(expr):
    keys: typing.List[expr]
    values: typing.List[expr]


@_dataclass
class Set(expr):
    elts: typing.List[expr]


@_dataclass
class ListComp(expr):
    elt: expr
    generators: typing.List[comprehension]


@_dataclass
class SetComp(expr):
    elt: expr
    generators: typing.List[comprehension]


@_dataclass
class DictComp(expr):
    key: expr
    value: expr
    generators: typing.List[comprehension]


@_dataclass
class GeneratorExp(expr):
    elt: expr
    generators: typing.List[comprehension]


@_dataclass
class Await(expr):
    value: expr


@_dataclass
class Yield(expr):
    value: typing.Optional[expr]


@_dataclass
class YieldFrom(expr):
    value: expr


@_dataclass
class Compare(expr):
    left: expr
    ops: typing.List[cmpop]
    comparators: typing.List[expr]


@_dataclass
class Call(expr):
    func: expr
    args: typing.List[expr]
    keywords: typing.List[keyword]


@_dataclass
class FormattedValue(expr):
    value: expr
    conversion: typing.Optional[int]
    format_spec: typing.Optional[expr]


@_dataclass
class JoinedStr(expr):
    values: typing.List[expr]


@_dataclass
class Constant(expr):
    value: constant
    kind: typing.Optional[string]


@_dataclass
class Attribute(expr):
    value: expr
    attr: identifier
    ctx: expr_context


@_dataclass
class Subscript(expr):
    value: expr
    slice: expr
    ctx: expr_context


@_dataclass
class Starred(expr):
    value: expr
    ctx: expr_context


@_dataclass
class Name(expr):
    id: identifier
    ctx: expr_context


@_dataclass
class List(expr):
    elts: typing.List[expr]
    ctx: expr_context


@_dataclass
class Tuple(expr):
    elts: typing.List[expr]
    ctx: expr_context


@_dataclass
class Slice(expr):
    lower: typing.Optional[expr]
    upper: typing.Optional[expr]
    step: typing.Optional[expr]


class expr_context(_Enum):
    Load = _auto()
    Store = _auto()
    Del = _auto()


class boolop(_Enum):
    And = _auto()
    Or = _auto()


class operator(_Enum):
    Add = _auto()
    Sub = _auto()
    Mult = _auto()
    MatMult = _auto()
    Div = _auto()
    Mod = _auto()
    Pow = _auto()
    LShift = _auto()
    RShift = _auto()
    BitOr = _auto()
    BitXor = _auto()
    BitAnd = _auto()
    FloorDiv = _auto()


class unaryop(_Enum):
    Invert = _auto()
    Not = _auto()
    UAdd = _auto()
    USub = _auto()


class cmpop(_Enum):
    Eq = _auto()
    NotEq = _auto()
    Lt = _auto()
    LtE = _auto()
    Gt = _auto()
    GtE = _auto()
    Is = _auto()
    IsNot = _auto()
    In = _auto()
    NotIn = _auto()


@_dataclass
class comprehension(AST):
    target: expr
    iter: expr
    ifs: typing.List[expr]
    is_async: int


class excepthandler(AST):
    lineno: int
    col_offset: int
    end_lineno: typing.Optional[int]
    end_col_offset: typing.Optional[int]


@_dataclass
class ExceptHandler(excepthandler):
    type: typing.Optional[expr]
    name: typing.Optional[identifier]
    body: typing.List[stmt]


@_dataclass
class arguments(AST):
    posonlyargs: typing.List[arg]
    args: typing.List[arg]
    vararg: typing.Optional[arg]
    kwonlyargs: typing.List[arg]
    kw_defaults: typing.List[expr]
    kwarg: typing.Optional[arg]
    defaults: typing.List[expr]


@_dataclass
class arg(AST):
    arg: identifier
    annotation: typing.Optional[expr]
    type_comment: typing.Optional[string]
    lineno: int
    col_offset: int
    end_lineno: typing.Optional[int]
    end_col_offset: typing.Optional[int]


@_dataclass
class keyword(AST):
    arg: typing.Optional[identifier]
    value: expr
    lineno: int
    col_offset: int
    end_lineno: typing.Optional[int]
    end_col_offset: typing.Optional[int]


@_dataclass
class alias(AST):
    name: identifier
    asname: typing.Optional[identifier]


@_dataclass
class withitem(AST):
    context_expr: expr
    optional_vars: typing.Optional[expr]


class type_ignore(AST):
    ...


@_dataclass
class TypeIgnore(type_ignore):
    lineno: int
    tag: string
