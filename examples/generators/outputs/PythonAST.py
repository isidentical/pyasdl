from __future__ import annotations

import typing
from dataclasses import dataclass as _dataclass
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


class mod(AST):
    ...


@_dataclass
class Module(mod):
    body: list[stmt]
    type_ignores: list[type_ignore]


@_dataclass
class Interactive(mod):
    body: list[stmt]


@_dataclass
class Expression(mod):
    body: expr


@_dataclass
class FunctionType(mod):
    argtypes: list[expr]
    returns: expr


class stmt(AST):
    lineno: int
    col_offset: int
    end_lineno: int | None
    end_col_offset: int | None


@_dataclass
class FunctionDef(stmt):
    name: identifier
    args: arguments
    body: list[stmt]
    decorator_list: list[expr]
    returns: expr | None
    type_comment: string | None


@_dataclass
class AsyncFunctionDef(stmt):
    name: identifier
    args: arguments
    body: list[stmt]
    decorator_list: list[expr]
    returns: expr | None
    type_comment: string | None


@_dataclass
class ClassDef(stmt):
    name: identifier
    bases: list[expr]
    keywords: list[keyword]
    body: list[stmt]
    decorator_list: list[expr]


@_dataclass
class Return(stmt):
    value: expr | None


@_dataclass
class Delete(stmt):
    targets: list[expr]


@_dataclass
class Assign(stmt):
    targets: list[expr]
    value: expr
    type_comment: string | None


@_dataclass
class AugAssign(stmt):
    target: expr
    op: operator
    value: expr


@_dataclass
class AnnAssign(stmt):
    target: expr
    annotation: expr
    value: expr | None
    simple: int


@_dataclass
class For(stmt):
    target: expr
    iter: expr
    body: list[stmt]
    orelse: list[stmt]
    type_comment: string | None


@_dataclass
class AsyncFor(stmt):
    target: expr
    iter: expr
    body: list[stmt]
    orelse: list[stmt]
    type_comment: string | None


@_dataclass
class While(stmt):
    test: expr
    body: list[stmt]
    orelse: list[stmt]


@_dataclass
class If(stmt):
    test: expr
    body: list[stmt]
    orelse: list[stmt]


@_dataclass
class With(stmt):
    items: list[withitem]
    body: list[stmt]
    type_comment: string | None


@_dataclass
class AsyncWith(stmt):
    items: list[withitem]
    body: list[stmt]
    type_comment: string | None


@_dataclass
class Match(stmt):
    subject: expr
    cases: list[match_case]


@_dataclass
class Raise(stmt):
    exc: expr | None
    cause: expr | None


@_dataclass
class Try(stmt):
    body: list[stmt]
    handlers: list[excepthandler]
    orelse: list[stmt]
    finalbody: list[stmt]


@_dataclass
class TryStar(stmt):
    body: list[stmt]
    handlers: list[excepthandler]
    orelse: list[stmt]
    finalbody: list[stmt]


@_dataclass
class Assert(stmt):
    test: expr
    msg: expr | None


@_dataclass
class Import(stmt):
    names: list[alias]


@_dataclass
class ImportFrom(stmt):
    module: identifier | None
    names: list[alias]
    level: int | None


@_dataclass
class Global(stmt):
    names: list[identifier]


@_dataclass
class Nonlocal(stmt):
    names: list[identifier]


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
    end_lineno: int | None
    end_col_offset: int | None


@_dataclass
class BoolOp(expr):
    op: boolop
    values: list[expr]


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
    keys: list[expr]
    values: list[expr]


@_dataclass
class Set(expr):
    elts: list[expr]


@_dataclass
class ListComp(expr):
    elt: expr
    generators: list[comprehension]


@_dataclass
class SetComp(expr):
    elt: expr
    generators: list[comprehension]


@_dataclass
class DictComp(expr):
    key: expr
    value: expr
    generators: list[comprehension]


@_dataclass
class GeneratorExp(expr):
    elt: expr
    generators: list[comprehension]


@_dataclass
class Await(expr):
    value: expr


@_dataclass
class Yield(expr):
    value: expr | None


@_dataclass
class YieldFrom(expr):
    value: expr


@_dataclass
class Compare(expr):
    left: expr
    ops: list[cmpop]
    comparators: list[expr]


@_dataclass
class Call(expr):
    func: expr
    args: list[expr]
    keywords: list[keyword]


@_dataclass
class FormattedValue(expr):
    value: expr
    conversion: int
    format_spec: expr | None


@_dataclass
class JoinedStr(expr):
    values: list[expr]


@_dataclass
class Constant(expr):
    value: constant
    kind: string | None


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
    elts: list[expr]
    ctx: expr_context


@_dataclass
class Tuple(expr):
    elts: list[expr]
    ctx: expr_context


@_dataclass
class Slice(expr):
    lower: expr | None
    upper: expr | None
    step: expr | None


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
    ifs: list[expr]
    is_async: int


class excepthandler(AST):
    lineno: int
    col_offset: int
    end_lineno: int | None
    end_col_offset: int | None


@_dataclass
class ExceptHandler(excepthandler):
    type: expr | None
    name: identifier | None
    body: list[stmt]


@_dataclass
class arguments(AST):
    posonlyargs: list[arg]
    args: list[arg]
    vararg: arg | None
    kwonlyargs: list[arg]
    kw_defaults: list[expr]
    kwarg: arg | None
    defaults: list[expr]


@_dataclass
class arg(AST):
    arg: identifier
    annotation: expr | None
    type_comment: string | None
    lineno: int
    col_offset: int
    end_lineno: int | None
    end_col_offset: int | None


@_dataclass
class keyword(AST):
    arg: identifier | None
    value: expr
    lineno: int
    col_offset: int
    end_lineno: int | None
    end_col_offset: int | None


@_dataclass
class alias(AST):
    name: identifier
    asname: identifier | None
    lineno: int
    col_offset: int
    end_lineno: int | None
    end_col_offset: int | None


@_dataclass
class withitem(AST):
    context_expr: expr
    optional_vars: expr | None


@_dataclass
class match_case(AST):
    pattern: pattern
    guard: expr | None
    body: list[stmt]


class pattern(AST):
    lineno: int
    col_offset: int
    end_lineno: int
    end_col_offset: int


@_dataclass
class MatchValue(pattern):
    value: expr


@_dataclass
class MatchSingleton(pattern):
    value: constant


@_dataclass
class MatchSequence(pattern):
    patterns: list[pattern]


@_dataclass
class MatchMapping(pattern):
    keys: list[expr]
    patterns: list[pattern]
    rest: identifier | None


@_dataclass
class MatchClass(pattern):
    cls: expr
    patterns: list[pattern]
    kwd_attrs: list[identifier]
    kwd_patterns: list[pattern]


@_dataclass
class MatchStar(pattern):
    name: identifier | None


@_dataclass
class MatchAs(pattern):
    pattern: pattern | None
    name: identifier | None


@_dataclass
class MatchOr(pattern):
    patterns: list[pattern]


class type_ignore(AST):
    ...


@_dataclass
class TypeIgnore(type_ignore):
    lineno: int
    tag: string
