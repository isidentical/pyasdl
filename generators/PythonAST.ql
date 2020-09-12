union mod = Module | Interactive | Expression | FunctionType
type Module {
  body: [stmt]
  type_ignores: [type_ignore]
}
type Interactive {
  body: [stmt]
}
type Expression {
  body: expr!
}
type FunctionType {
  argtypes: [expr]
  returns: expr!
}
union stmt = FunctionDef | AsyncFunctionDef | ClassDef | Return | Delete | Assign | AugAssign | AnnAssign | For | AsyncFor | While | If | With | AsyncWith | Raise | Try | Assert | Import | ImportFrom | Global | Nonlocal | Expr | Pass | Break | Continue
type FunctionDef {
  name: identifier!
  args: arguments!
  body: [stmt]
  decorator_list: [expr]
  returns: expr
  type_comment: string
}
type AsyncFunctionDef {
  name: identifier!
  args: arguments!
  body: [stmt]
  decorator_list: [expr]
  returns: expr
  type_comment: string
}
type ClassDef {
  name: identifier!
  bases: [expr]
  keywords: [keyword]
  body: [stmt]
  decorator_list: [expr]
}
type Return {
  value: expr
}
type Delete {
  targets: [expr]
}
type Assign {
  targets: [expr]
  value: expr!
  type_comment: string
}
type AugAssign {
  target: expr!
  op: operator!
  value: expr!
}
type AnnAssign {
  target: expr!
  annotation: expr!
  value: expr
  simple: int!
}
type For {
  target: expr!
  iter: expr!
  body: [stmt]
  orelse: [stmt]
  type_comment: string
}
type AsyncFor {
  target: expr!
  iter: expr!
  body: [stmt]
  orelse: [stmt]
  type_comment: string
}
type While {
  test: expr!
  body: [stmt]
  orelse: [stmt]
}
type If {
  test: expr!
  body: [stmt]
  orelse: [stmt]
}
type With {
  items: [withitem]
  body: [stmt]
  type_comment: string
}
type AsyncWith {
  items: [withitem]
  body: [stmt]
  type_comment: string
}
type Raise {
  exc: expr
  cause: expr
}
type Try {
  body: [stmt]
  handlers: [excepthandler]
  orelse: [stmt]
  finalbody: [stmt]
}
type Assert {
  test: expr!
  msg: expr
}
type Import {
  names: [alias]
}
type ImportFrom {
  module: identifier
  names: [alias]
  level: int
}
type Global {
  names: [identifier]
}
type Nonlocal {
  names: [identifier]
}
type Expr {
  value: expr!
}
type Pass {
}
type Break {
}
type Continue {
}
union expr = BoolOp | NamedExpr | BinOp | UnaryOp | Lambda | IfExp | Dict | Set | ListComp | SetComp | DictComp | GeneratorExp | Await | Yield | YieldFrom | Compare | Call | FormattedValue | JoinedStr | Constant | Attribute | Subscript | Starred | Name | List | Tuple | Slice
type BoolOp {
  op: boolop!
  values: [expr]
}
type NamedExpr {
  target: expr!
  value: expr!
}
type BinOp {
  left: expr!
  op: operator!
  right: expr!
}
type UnaryOp {
  op: unaryop!
  operand: expr!
}
type Lambda {
  args: arguments!
  body: expr!
}
type IfExp {
  test: expr!
  body: expr!
  orelse: expr!
}
type Dict {
  keys: [expr]
  values: [expr]
}
type Set {
  elts: [expr]
}
type ListComp {
  elt: expr!
  generators: [comprehension]
}
type SetComp {
  elt: expr!
  generators: [comprehension]
}
type DictComp {
  key: expr!
  value: expr!
  generators: [comprehension]
}
type GeneratorExp {
  elt: expr!
  generators: [comprehension]
}
type Await {
  value: expr!
}
type Yield {
  value: expr
}
type YieldFrom {
  value: expr!
}
type Compare {
  left: expr!
  ops: [cmpop]
  comparators: [expr]
}
type Call {
  func: expr!
  args: [expr]
  keywords: [keyword]
}
type FormattedValue {
  value: expr!
  conversion: int
  format_spec: expr
}
type JoinedStr {
  values: [expr]
}
type Constant {
  value: constant!
  kind: string
}
type Attribute {
  value: expr!
  attr: identifier!
  ctx: expr_context!
}
type Subscript {
  value: expr!
  slice: expr!
  ctx: expr_context!
}
type Starred {
  value: expr!
  ctx: expr_context!
}
type Name {
  id: identifier!
  ctx: expr_context!
}
type List {
  elts: [expr]
  ctx: expr_context!
}
type Tuple {
  elts: [expr]
  ctx: expr_context!
}
type Slice {
  lower: expr
  upper: expr
  step: expr
}
enum expr_context {
  Load
  Store
  Del
}
enum boolop {
  And
  Or
}
enum operator {
  Add
  Sub
  Mult
  MatMult
  Div
  Mod
  Pow
  LShift
  RShift
  BitOr
  BitXor
  BitAnd
  FloorDiv
}
enum unaryop {
  Invert
  Not
  UAdd
  USub
}
enum cmpop {
  Eq
  NotEq
  Lt
  LtE
  Gt
  GtE
  Is
  IsNot
  In
  NotIn
}
type comprehension {
  target: expr!
  iter: expr!
  ifs: [expr]
  is_async: int!
}
union excepthandler = ExceptHandler
type ExceptHandler {
  type: expr
  name: identifier
  body: [stmt]
}
type arguments {
  posonlyargs: [arg]
  args: [arg]
  vararg: arg
  kwonlyargs: [arg]
  kw_defaults: [expr]
  kwarg: arg
  defaults: [expr]
}
type arg {
  arg: identifier!
  annotation: expr
  type_comment: string
}
type keyword {
  arg: identifier
  value: expr!
}
type alias {
  name: identifier!
  asname: identifier
}
type withitem {
  context_expr: expr!
  optional_vars: expr
}
union type_ignore = TypeIgnore
type TypeIgnore {
  lineno: int!
  tag: string!
}
