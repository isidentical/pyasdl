# PyASDL

A new ASDL parser for Zephyr's ASDL format.

## Usage

```py
import pyasdl

pyasdl.parse(<asdl source>)

class TestVisitor(pyasdl.ASDLVisitor):
    def visit_Module(self, node):
        print(f"Module name: {node.name}")
        self.generic_visit(node)
```
