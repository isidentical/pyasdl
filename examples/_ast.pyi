from __future__ import annotations

from typing import List, Optional, Union

identifier = str
string = Union[str, bytes]
constant = Union[
    str,
    bytes,
    int,
    float,
    complex,
    bool,
    tuple,
    frozenset,
    None,
    type(Ellipsis),
]

class AST: ...
class mod(AST): ...

class Module(mod):
    body: List[stmt]
    type_ignores: List[type_ignore]

class Interactive(mod):
    body: List[stmt]

class Expression(mod):
    body: expr

class FunctionType(mod):
    argtypes: List[expr]
    returns: expr

class stmt(AST):
    lineno: int
    col_offset: int
    end_lineno: Optional[int]
    end_col_offset: Optional[int]

class FunctionDef(stmt):
    name: identifier
    args: arguments
    body: List[stmt]
    decorator_list: List[expr]
    returns: Optional[expr]
    type_comment: Optional[string]

class AsyncFunctionDef(stmt):
    name: identifier
    args: arguments
    body: List[stmt]
    decorator_list: List[expr]
    returns: Optional[expr]
    type_comment: Optional[string]

class ClassDef(stmt):
    name: identifier
    bases: List[expr]
    keywords: List[keyword]
    body: List[stmt]
    decorator_list: List[expr]

class Return(stmt):
    value: Optional[expr]

class Delete(stmt):
    targets: List[expr]

class Assign(stmt):
    targets: List[expr]
    value: expr
    type_comment: Optional[string]

class AugAssign(stmt):
    target: expr
    op: operator
    value: expr

class AnnAssign(stmt):
    target: expr
    annotation: expr
    value: Optional[expr]
    simple: int

class For(stmt):
    target: expr
    iter: expr
    body: List[stmt]
    orelse: List[stmt]
    type_comment: Optional[string]

class AsyncFor(stmt):
    target: expr
    iter: expr
    body: List[stmt]
    orelse: List[stmt]
    type_comment: Optional[string]

class While(stmt):
    test: expr
    body: List[stmt]
    orelse: List[stmt]

class If(stmt):
    test: expr
    body: List[stmt]
    orelse: List[stmt]

class With(stmt):
    items: List[withitem]
    body: List[stmt]
    type_comment: Optional[string]

class AsyncWith(stmt):
    items: List[withitem]
    body: List[stmt]
    type_comment: Optional[string]

class Raise(stmt):
    exc: Optional[expr]
    cause: Optional[expr]

class Try(stmt):
    body: List[stmt]
    handlers: List[excepthandler]
    orelse: List[stmt]
    finalbody: List[stmt]

class Assert(stmt):
    test: expr
    msg: Optional[expr]

class Import(stmt):
    names: List[alias]

class ImportFrom(stmt):
    module: Optional[identifier]
    names: List[alias]
    level: Optional[int]

class Global(stmt):
    names: List[identifier]

class Nonlocal(stmt):
    names: List[identifier]

class Expr(stmt):
    value: expr

class Pass(stmt): ...
class Break(stmt): ...
class Continue(stmt): ...

class expr(AST):
    lineno: int
    col_offset: int
    end_lineno: Optional[int]
    end_col_offset: Optional[int]

class BoolOp(expr):
    op: boolop
    values: List[expr]

class NamedExpr(expr):
    target: expr
    value: expr

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
    keys: List[expr]
    values: List[expr]

class Set(expr):
    elts: List[expr]

class ListComp(expr):
    elt: expr
    generators: List[comprehension]

class SetComp(expr):
    elt: expr
    generators: List[comprehension]

class DictComp(expr):
    key: expr
    value: expr
    generators: List[comprehension]

class GeneratorExp(expr):
    elt: expr
    generators: List[comprehension]

class Await(expr):
    value: expr

class Yield(expr):
    value: Optional[expr]

class YieldFrom(expr):
    value: expr

class Compare(expr):
    left: expr
    ops: List[cmpop]
    comparators: List[expr]

class Call(expr):
    func: expr
    args: List[expr]
    keywords: List[keyword]

class FormattedValue(expr):
    value: expr
    conversion: Optional[int]
    format_spec: Optional[expr]

class JoinedStr(expr):
    values: List[expr]

class Constant(expr):
    value: constant
    kind: Optional[string]

class Attribute(expr):
    value: expr
    attr: identifier
    ctx: expr_context

class Subscript(expr):
    value: expr
    slice: expr
    ctx: expr_context

class Starred(expr):
    value: expr
    ctx: expr_context

class Name(expr):
    id: identifier
    ctx: expr_context

class List(expr):
    elts: List[expr]
    ctx: expr_context

class Tuple(expr):
    elts: List[expr]
    ctx: expr_context

class Slice(expr):
    lower: Optional[expr]
    upper: Optional[expr]
    step: Optional[expr]

class expr_context(AST): ...
class Load(expr_context): ...
class Store(expr_context): ...
class Del(expr_context): ...
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
    ifs: List[expr]
    is_async: int

class excepthandler(AST):
    lineno: int
    col_offset: int
    end_lineno: Optional[int]
    end_col_offset: Optional[int]

class ExceptHandler(excepthandler):
    type: Optional[expr]
    name: Optional[identifier]
    body: List[stmt]

class arguments(AST):
    posonlyargs: List[arg]
    args: List[arg]
    vararg: Optional[arg]
    kwonlyargs: List[arg]
    kw_defaults: List[expr]
    kwarg: Optional[arg]
    defaults: List[expr]

class arg(AST):
    arg: identifier
    annotation: Optional[expr]
    type_comment: Optional[string]
    lineno: int
    col_offset: int
    end_lineno: Optional[int]
    end_col_offset: Optional[int]

class keyword(AST):
    arg: Optional[identifier]
    value: expr
    lineno: int
    col_offset: int
    end_lineno: Optional[int]
    end_col_offset: Optional[int]

class alias(AST):
    name: identifier
    asname: Optional[identifier]

class withitem(AST):
    context_expr: expr
    optional_vars: Optional[expr]

class type_ignore(AST): ...

class TypeIgnore(type_ignore):
    lineno: int
    tag: string
