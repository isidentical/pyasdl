# PyASDL

A new ASDL parser for Zephyr's ASDL format.

## Stub Generator Example
For understanding the parse tree and the visitors, you can check out 
the stub generator example. Basically it generates a typing stub for
the AST module itself (when the Python's ASDL is given) in a straight
forward way.

## Reference
- `parse(source: str, *, filename: str = "<pyasdl>") -> Module`
    Takes the source code (and optionally the filename, to be used in
    syntax errors) and outputs an `pyasdl.Module` instance that
    represents the AST of the given ASDL schema.

- `ASDLVisitor`
    A base class to be used with `visitor-pattern` applications. The
    interface is similiar with the `ast.NodeVisitor`.
    
    ```py
    import pyasdl as asdl

    class CollectNamesVisitor(asdl.ASDLVisitor):
        def __init__(self):
            self.names = set()

        def visit_Module(self, node: asdl.Module) -> None:
            self.names.add(node.name)

    visitor = DummyVisitor()
    for source in sources:
        tree = asdl.parse(source)
        visitor.visit(tree)
    print(visitor.names)
    ```

- `Module`
- `Type`
- `Sum`
- `Constructor`
- `FieldQualifier`
- `Field`
