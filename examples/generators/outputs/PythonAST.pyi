from __future__ import annotations
import sys
import typing

class AST:
    _attributes: typing.ClassVar[typing.Tuple[str, ...]]
    _fields: typing.ClassVar[typing.Tuple[str, ...]]
    def __init__(self, *args: typing.Any, **kwargs: typing.Any) -> None: ...

    # Allow any attribute access (taken from types.SingleNamespace)
    def __getattribute__(self, name: str) -> Any: ...
    def __setattr__(self, name: str, value: Any) -> None: ...
    def __delattr__(self, name: str) -> None: ...

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

class mod(AST): ...

class Module(mod):
    body: typing.List[stmt]
    if sys.version_info >= (3, 8):
        type_ignores: typing.List[type_ignore]

class Interactive(mod):
    body: typing.List[stmt]

class Expression(mod):
    body: expr

if sys.version_info <= (3, 8):
    class Suite(mod):
        body: typing.List[stmt]

class stmt(AST):
    lineno: int
    col_offset: int
    if sys.version_info >= (3, 8):
        end_lineno: typing.Optional[int]
        end_col_offset: typing.Optional[int]

class FunctionDef(stmt):
    name: identifier
    args: arguments
    body: typing.List[stmt]
    decorator_list: typing.List[expr]
    returns: typing.Optional[expr]
    if sys.version_info >= (3, 8):
        type_comment: typing.Optional[string]

class AsyncFunctionDef(stmt):
    name: identifier
    args: arguments
    body: typing.List[stmt]
    decorator_list: typing.List[expr]
    returns: typing.Optional[expr]
    if sys.version_info >= (3, 8):
        type_comment: typing.Optional[string]

class ClassDef(stmt):
    name: identifier
    bases: typing.List[expr]
    keywords: typing.List[keyword]
    body: typing.List[stmt]
    decorator_list: typing.List[expr]

class Return(stmt):
    value: typing.Optional[expr]

class Delete(stmt):
    targets: typing.List[expr]

class Assign(stmt):
    targets: typing.List[expr]
    value: expr
    if sys.version_info >= (3, 8):
        type_comment: typing.Optional[string]

class AugAssign(stmt):
    target: expr
    op: operator
    value: expr

class AnnAssign(stmt):
    target: expr
    annotation: expr
    value: typing.Optional[expr]
    simple: int

class For(stmt):
    target: expr
    iter: expr
    body: typing.List[stmt]
    orelse: typing.List[stmt]
    if sys.version_info >= (3, 8):
        type_comment: typing.Optional[string]

class AsyncFor(stmt):
    target: expr
    iter: expr
    body: typing.List[stmt]
    orelse: typing.List[stmt]
    if sys.version_info >= (3, 8):
        type_comment: typing.Optional[string]

class While(stmt):
    test: expr
    body: typing.List[stmt]
    orelse: typing.List[stmt]

class If(stmt):
    test: expr
    body: typing.List[stmt]
    orelse: typing.List[stmt]

class With(stmt):
    items: typing.List[withitem]
    body: typing.List[stmt]
    if sys.version_info >= (3, 8):
        type_comment: typing.Optional[string]

class AsyncWith(stmt):
    items: typing.List[withitem]
    body: typing.List[stmt]
    if sys.version_info >= (3, 8):
        type_comment: typing.Optional[string]

class Raise(stmt):
    exc: typing.Optional[expr]
    cause: typing.Optional[expr]

class Try(stmt):
    body: typing.List[stmt]
    handlers: typing.List[excepthandler]
    orelse: typing.List[stmt]
    finalbody: typing.List[stmt]

class Assert(stmt):
    test: expr
    msg: typing.Optional[expr]

class Import(stmt):
    names: typing.List[alias]

class ImportFrom(stmt):
    module: typing.Optional[identifier]
    names: typing.List[alias]
    level: typing.Optional[int]

class Global(stmt):
    names: typing.List[identifier]

class Nonlocal(stmt):
    names: typing.List[identifier]

class Expr(stmt):
    value: expr

class Pass(stmt): ...
class Break(stmt): ...
class Continue(stmt): ...

class expr(AST):
    lineno: int
    col_offset: int
    if sys.version_info >= (3, 8):
        end_lineno: typing.Optional[int]
        end_col_offset: typing.Optional[int]

class BoolOp(expr):
    op: boolop
    values: typing.List[expr]

class BinOp(expr):
    left: expr
    op: operator
    right: expr

class UnaryOp(expr):
    op: unaryop
    operand: expr

class Lambda(expr):
    args: arguments
    body: expr

class IfExp(expr):
    test: expr
    body: expr
    orelse: expr

class Dict(expr):
    keys: typing.List[expr]
    values: typing.List[expr]

class Set(expr):
    elts: typing.List[expr]

class ListComp(expr):
    elt: expr
    generators: typing.List[comprehension]

class SetComp(expr):
    elt: expr
    generators: typing.List[comprehension]

class DictComp(expr):
    key: expr
    value: expr
    generators: typing.List[comprehension]

class GeneratorExp(expr):
    elt: expr
    generators: typing.List[comprehension]

class Await(expr):
    value: expr

class Yield(expr):
    value: typing.Optional[expr]

class YieldFrom(expr):
    value: expr

class Compare(expr):
    left: expr
    ops: typing.List[cmpop]
    comparators: typing.List[expr]

class Call(expr):
    func: expr
    args: typing.List[expr]
    keywords: typing.List[keyword]

if sys.version_info <= (3, 7):
    class Num(expr):
        n: object

    class Str(expr):
        s: string

class FormattedValue(expr):
    value: expr
    if sys.version_info <= (3, 9):
        conversion: typing.Optional[int]
    format_spec: typing.Optional[expr]
    if sys.version_info >= (3, 10):
        conversion: int

class JoinedStr(expr):
    values: typing.List[expr]

if sys.version_info <= (3, 7):
    class Bytes(expr):
        s: bytes

    class NameConstant(expr):
        value: singleton

    class Ellipsis(expr): ...

class Constant(expr):
    value: constant
    if sys.version_info >= (3, 8):
        kind: typing.Optional[string]

class Attribute(expr):
    value: expr
    attr: identifier
    ctx: expr_context

class Subscript(expr):
    value: expr
    if sys.version_info <= (3, 8):
        slice: slice
    ctx: expr_context
    if sys.version_info >= (3, 9):
        slice: expr

class Starred(expr):
    value: expr
    ctx: expr_context

class Name(expr):
    id: identifier
    ctx: expr_context

class List(expr):
    elts: typing.List[expr]
    ctx: expr_context

class Tuple(expr):
    elts: typing.List[expr]
    ctx: expr_context

class expr_context(AST): ...
class Load(expr_context): ...
class Store(expr_context): ...
class Del(expr_context): ...

if sys.version_info <= (3, 8):
    class AugLoad(expr_context): ...
    class AugStore(expr_context): ...
    class Param(expr_context): ...
    class slice(AST): ...

if sys.version_info <= (3, 8):
    _SliceBase = slice
elif sys.version_info >= (3, 9):
    _SliceBase = expr

class Slice(_SliceBase):
    lower: typing.Optional[expr]
    upper: typing.Optional[expr]
    step: typing.Optional[expr]

if sys.version_info <= (3, 8):
    class ExtSlice(slice):
        dims: typing.List[slice]

    class Index(slice):
        value: expr

class boolop(AST): ...
class And(boolop): ...
class Or(boolop): ...
class operator(AST): ...
class Add(operator): ...
class Sub(operator): ...
class Mult(operator): ...
class MatMult(operator): ...
class Div(operator): ...
class Mod(operator): ...
class Pow(operator): ...
class LShift(operator): ...
class RShift(operator): ...
class BitOr(operator): ...
class BitXor(operator): ...
class BitAnd(operator): ...
class FloorDiv(operator): ...
class unaryop(AST): ...
class Invert(unaryop): ...
class Not(unaryop): ...
class UAdd(unaryop): ...
class USub(unaryop): ...
class cmpop(AST): ...
class Eq(cmpop): ...
class NotEq(cmpop): ...
class Lt(cmpop): ...
class LtE(cmpop): ...
class Gt(cmpop): ...
class GtE(cmpop): ...
class Is(cmpop): ...
class IsNot(cmpop): ...
class In(cmpop): ...
class NotIn(cmpop): ...

class comprehension(AST):
    target: expr
    iter: expr
    ifs: typing.List[expr]
    is_async: int

class excepthandler(AST):
    lineno: int
    col_offset: int
    if sys.version_info >= (3, 8):
        end_lineno: typing.Optional[int]
        end_col_offset: typing.Optional[int]

class ExceptHandler(excepthandler):
    type: typing.Optional[expr]
    name: typing.Optional[identifier]
    body: typing.List[stmt]

class arguments(AST):
    args: typing.List[arg]
    vararg: typing.Optional[arg]
    kwonlyargs: typing.List[arg]
    kw_defaults: typing.List[expr]
    kwarg: typing.Optional[arg]
    defaults: typing.List[expr]
    if sys.version_info >= (3, 8):
        posonlyargs: typing.List[arg]

class arg(AST):
    arg: identifier
    annotation: typing.Optional[expr]
    lineno: int
    col_offset: int
    if sys.version_info >= (3, 8):
        type_comment: typing.Optional[string]
        end_lineno: typing.Optional[int]
        end_col_offset: typing.Optional[int]

class keyword(AST):
    arg: typing.Optional[identifier]
    value: expr
    if sys.version_info >= (3, 9):
        lineno: int
        col_offset: int
        end_lineno: typing.Optional[int]
        end_col_offset: typing.Optional[int]

class alias(AST):
    name: identifier
    asname: typing.Optional[identifier]
    if sys.version_info >= (3, 10):
        lineno: int
        col_offset: int
        end_lineno: typing.Optional[int]
        end_col_offset: typing.Optional[int]

class withitem(AST):
    context_expr: expr
    optional_vars: typing.Optional[expr]

if sys.version_info >= (3, 8):
    class FunctionType(mod):
        argtypes: typing.List[expr]
        returns: expr

    class NamedExpr(expr):
        target: expr
        value: expr

    class type_ignore(AST): ...

    class TypeIgnore(type_ignore):
        lineno: int
        tag: string

if sys.version_info >= (3, 10):
    class Match(stmt):
        subject: expr
        cases: typing.List[match_case]

    class match_case(AST):
        pattern: pattern
        guard: typing.Optional[expr]
        body: typing.List[stmt]

    class pattern(AST):
        lineno: int
        col_offset: int
        end_lineno: int
        end_col_offset: int

    class MatchValue(pattern):
        value: expr

    class MatchSingleton(pattern):
        value: constant

    class MatchSequence(pattern):
        patterns: typing.List[pattern]

    class MatchMapping(pattern):
        keys: typing.List[expr]
        patterns: typing.List[pattern]
        rest: typing.Optional[identifier]

    class MatchClass(pattern):
        cls: expr
        patterns: typing.List[pattern]
        kwd_attrs: typing.List[identifier]
        kwd_patterns: typing.List[pattern]

    class MatchStar(pattern):
        name: typing.Optional[identifier]

    class MatchAs(pattern):
        pattern: typing.Optional[pattern]
        name: typing.Optional[identifier]

    class MatchOr(pattern):
        patterns: typing.List[pattern]

if sys.version_info >= (3, 11):
    class TryStar(stmt):
        body: typing.List[stmt]
        handlers: typing.List[excepthandler]
        orelse: typing.List[stmt]
        finalbody: typing.List[stmt]
