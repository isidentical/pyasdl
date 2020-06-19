from argparse import ArgumentParser

import pyasdl


class TestVisitor(pyasdl.ASDLVisitor):
    def visit_Module(self, node):
        print(f"Module name: {node.name}")
        self.generic_visit(node)

    def visit_Type(self, node):
        print(
            f"Definiton of '{node.name}' is a {type(node.value).__name__.lower()}"
        )


def main():
    parser = ArgumentParser()
    parser.add_argument("file")
    options = parser.parse_args()

    with open(options.file) as f:
        tree = pyasdl.parse(f.read(), filename=options.file)

    visitor = TestVisitor()
    visitor.visit(tree)


if __name__ == "__main__":
    main()
