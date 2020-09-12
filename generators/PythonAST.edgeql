START MIGRATION TO {
    module default {
        abstract type mod {}
        type PyModule extending mod {
            multi link body -> stmt;
            multi link type_ignores -> type_ignore;
        }
        type Interactive extending mod {
            multi link body -> stmt;
        }
        type Expression extending mod {
            required link body -> expr;
        }
        type FunctionType extending mod {
            multi link argtypes -> expr;
            required link returns -> expr;
        }
        type Suite extending mod {
            multi link body -> stmt;
        }
        abstract type stmt {}
        type FunctionDef extending stmt {
            required property name -> str;
            required link args -> arguments;
            multi link body -> stmt;
            multi link decorator_list -> expr;
            link returns -> expr;
            property type_comment -> str;
        }
        type AsyncFunctionDef extending stmt {
            required property name -> str;
            required link args -> arguments;
            multi link body -> stmt;
            multi link decorator_list -> expr;
            link returns -> expr;
            property type_comment -> str;
        }
        type ClassDef extending stmt {
            required property name -> str;
            multi link bases -> expr;
            multi link keywords -> keyword;
            multi link body -> stmt;
            multi link decorator_list -> expr;
        }
        type Return extending stmt {
            link value -> expr;
        }
        type PyDelete extending stmt {
            multi link targets -> expr;
        }
        type Assign extending stmt {
            multi link targets -> expr;
            required link value -> expr;
            property type_comment -> str;
        }
        type AugAssign extending stmt {
            required link target -> expr;
            required property op -> operator;
            required link value -> expr;
        }
        type AnnAssign extending stmt {
            required link target -> expr;
            required link annotation -> expr;
            link value -> expr;
            required property simple -> bigint;
        }
        type PyFor extending stmt {
            required link target -> expr;
            required link iter -> expr;
            multi link body -> stmt;
            multi link orelse -> stmt;
            property type_comment -> str;
        }
        type AsyncFor extending stmt {
            required link target -> expr;
            required link iter -> expr;
            multi link body -> stmt;
            multi link orelse -> stmt;
            property type_comment -> str;
        }
        type While extending stmt {
            required link test -> expr;
            multi link body -> stmt;
            multi link orelse -> stmt;
        }
        type PyIf extending stmt {
            required link test -> expr;
            multi link body -> stmt;
            multi link orelse -> stmt;
        }
        type PyWith extending stmt {
            multi link items -> withitem;
            multi link body -> stmt;
            property type_comment -> str;
        }
        type AsyncWith extending stmt {
            multi link items -> withitem;
            multi link body -> stmt;
            property type_comment -> str;
        }
        type PyRaise extending stmt {
            link exc -> expr;
            link cause -> expr;
        }
        type Try extending stmt {
            multi link body -> stmt;
            multi link handlers -> excepthandler;
            multi link orelse -> stmt;
            multi link finalbody -> stmt;
        }
        type Assert extending stmt {
            required link test -> expr;
            link msg -> expr;
        }
        type PyImport extending stmt {
            multi link names -> alias;
        }
        type ImportFrom extending stmt {
            property py_module -> str;
            multi link names -> alias;
            property level -> bigint;
        }
        type PyGlobal extending stmt {
            multi property names -> str;
        }
        type Nonlocal extending stmt {
            multi property names -> str;
        }
        type Expr extending stmt {
            required link value -> expr;
        }
        type Pass extending stmt {}
        type Break extending stmt {}
        type Continue extending stmt {}
        abstract type expr {}
        type BoolOp extending expr {
            required property op -> boolop;
            multi link values -> expr;
        }
        type NamedExpr extending expr {
            required link target -> expr;
            required link value -> expr;
        }
        type BinOp extending expr {
            required link left -> expr;
            required property op -> operator;
            required link right -> expr;
        }
        type UnaryOp extending expr {
            required property op -> unaryop;
            required link operand -> expr;
        }
        type Lambda extending expr {
            required link args -> arguments;
            required link body -> expr;
        }
        type IfExp extending expr {
            required link test -> expr;
            required link body -> expr;
            required link orelse -> expr;
        }
        type Dict extending expr {
            multi link keys -> expr;
            multi link values -> expr;
        }
        type PySet extending expr {
            multi link elts -> expr;
        }
        type ListComp extending expr {
            required link elt -> expr;
            multi link generators -> comprehension;
        }
        type SetComp extending expr {
            required link elt -> expr;
            multi link generators -> comprehension;
        }
        type DictComp extending expr {
            required link key -> expr;
            required link value -> expr;
            multi link generators -> comprehension;
        }
        type GeneratorExp extending expr {
            required link elt -> expr;
            multi link generators -> comprehension;
        }
        type Await extending expr {
            required link value -> expr;
        }
        type Yield extending expr {
            link value -> expr;
        }
        type YieldFrom extending expr {
            required link value -> expr;
        }
        type Compare extending expr {
            required link left -> expr;
            multi property ops -> cmpop;
            multi link comparators -> expr;
        }
        type Call extending expr {
            required link func -> expr;
            multi link args -> expr;
            multi link keywords -> keyword;
        }
        type FormattedValue extending expr {
            required link value -> expr;
            property conversion -> bigint;
            link format_spec -> expr;
        }
        type JoinedStr extending expr {
            multi link values -> expr;
        }
        type Constant extending expr {
            required property value -> str;
            property kind -> str;
        }
        type Attribute extending expr {
            required link value -> expr;
            required property attr -> str;
            required property ctx -> expr_context;
        }
        type Subscript extending expr {
            required link value -> expr;
            required link slice -> slice;
            required property ctx -> expr_context;
        }
        type Starred extending expr {
            required link value -> expr;
            required property ctx -> expr_context;
        }
        type Name extending expr {
            required property py_id -> str;
            required property ctx -> expr_context;
        }
        type List extending expr {
            multi link elts -> expr;
            required property ctx -> expr_context;
        }
        type Tuple extending expr {
            multi link elts -> expr;
            required property ctx -> expr_context;
        }
        scalar type expr_context extending enum<'Load', 'Store', 'Del', 'AugLoad', 'AugStore', 'Param'> {}
        abstract type slice {}
        type Slice extending slice {
            link lower -> expr;
            link upper -> expr;
            link step -> expr;
        }
        type ExtSlice extending slice {
            multi link dims -> slice;
        }
        type Index extending slice {
            required link value -> expr;
        }
        scalar type boolop extending enum<'And', 'Or'> {}
        scalar type operator extending enum<'Add', 'Sub', 'Mult', 'MatMult', 'Div', 'Mod', 'Pow', 'LShift', 'RShift', 'BitOr', 'BitXor', 'BitAnd', 'FloorDiv'> {}
        scalar type unaryop extending enum<'Invert', 'Not', 'UAdd', 'USub'> {}
        scalar type cmpop extending enum<'Eq', 'NotEq', 'Lt', 'LtE', 'Gt', 'GtE', 'Is', 'IsNot', 'In', 'NotIn'> {}
        type comprehension {
            required link target -> expr;
            required link iter -> expr;
            multi link ifs -> expr;
            required property is_async -> bigint;
        }
        abstract type excepthandler {}
        type ExceptHandler extending excepthandler {
            link type -> expr;
            property name -> str;
            multi link body -> stmt;
        }
        type arguments {
            multi link posonlyargs -> arg;
            multi link args -> arg;
            link vararg -> arg;
            multi link kwonlyargs -> arg;
            multi link kw_defaults -> expr;
            link kwarg -> arg;
            multi link defaults -> expr;
        }
        type arg {
            required property arg -> str;
            link annotation -> expr;
            property type_comment -> str;
        }
        type keyword {
            property arg -> str;
            required link value -> expr;
        }
        type alias {
            required property name -> str;
            property asname -> str;
        }
        type withitem {
            required link context_expr -> expr;
            link optional_vars -> expr;
        }
        abstract type type_ignore {}
        type TypeIgnore extending type_ignore {
            required property lineno -> bigint;
            required property tag -> str;
        }
    }
};
POPULATE MIGRATION;
COMMIT MIGRATION;
