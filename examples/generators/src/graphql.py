from argparse import ArgumentParser
from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path
from typing import List, Optional

import pyasdl

DEFAULT_INDENT = " " * 2
GRAPHQL_BASICS = {
    "int": "Int",
    "string": "String",
    "identifier": "String",
}


class Constraint(Enum):
    SEQUENCE = auto()
    NOT_NULLABLE = auto()


@dataclass
class QLUnion:
    name: str
    models: List[str]

    def __str__(self):
        return f"union {self.name} = " + " | ".join(self.models)


@dataclass
class QLEnum:
    name: str
    values: List[str]

    def __str__(self):
        lines = []
        lines.append(f"enum {self.name} {{")
        lines.extend(DEFAULT_INDENT + value for value in self.values)
        lines.append("}")
        return "\n".join(lines)


@dataclass
class QLField:
    name: str
    qualifier: str
    constraint: Optional[Constraint] = None

    @property
    def type(self):
        field_type = self.qualifier
        if self.constraint is Constraint.NOT_NULLABLE:
            return field_type + "!"
        elif self.constraint is Constraint.SEQUENCE:
            return "[" + field_type + "]"
        else:
            return field_type


@dataclass
class QLModel:
    name: str
    fields: List[QLField]

    def __str__(self):
        lines = []
        lines.append(f"type {self.name} {{")
        for field in self.fields:
            lines.append(DEFAULT_INDENT + f"{field.name}: {field.type}")
        lines.append("}")
        return "\n".join(lines)


def is_simple(sum_t: pyasdl.Sum) -> bool:
    for constructor in sum_t.types:
        if constructor.fields is not None:
            return False
    else:
        return True


class GraphQLGenerator(pyasdl.ASDLVisitor):
    def visit_Module(self, node):
        definitions = []
        for definition in node.body:
            definitions.extend(self.visit(definition))
        return definitions

    def visit_Type(self, node):
        # FIX-ME: attributes are ignored, need a better way
        # for storing location information
        yield from self.visit(node.value, name=node.name)

    def visit_Product(self, node, name):
        yield QLModel(name, self.visit_all(node.fields))

    def visit_Sum(self, node, name):
        constructor_names = [constructor.name for constructor in node.types]
        if is_simple(node):
            yield QLEnum(name, constructor_names)
        else:
            yield QLUnion(name, constructor_names)
            yield from self.visit_all(node.types)

    def visit_Constructor(self, node):
        return QLModel(node.name, self.visit_all(node.fields or ()))

    def visit_Field(self, node):
        qualifier = Constraint.NOT_NULLABLE
        if node.qualifier is pyasdl.FieldQualifier.SEQUENCE:
            qualifier = Constraint.SEQUENCE
        elif node.qualifier is pyasdl.FieldQualifier.OPTIONAL:
            qualifier = None
        return QLField(node.name, node.kind, qualifier)


def main():
    parser = ArgumentParser()
    parser.add_argument("file", type=Path)

    options = parser.parse_args()
    with open(options.file) as source:
        tree = pyasdl.parse(source.read())

    visitor = GraphQLGenerator()
    for ql_type in visitor.visit(tree):
        print(str(ql_type))


if __name__ == "__main__":
    main()
