# PyASDL

A new ASDL parser for Zephyr's ASDL format.

## Stub Generator Example
For understanding the parse tree and the visitors, you can check out 
the stub generator example. Basically it generates a typing stub for
the AST module itself (when the Python's ASDL is given) in a straight
forward way.

## Usage

```py
import pyasdl

pyasdl.parse(<asdl source>)

class TestVisitor(pyasdl.ASDLVisitor):
    def visit_Module(self, node):
        print(f"Module name: {node.name}")
        self.generic_visit(node)
```
