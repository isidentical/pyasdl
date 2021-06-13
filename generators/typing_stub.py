import ast
import textwrap
from argparse import ArgumentParser
from collections import defaultdict
from functools import partial
from pathlib import Path

import pyasdl

_BASE_CLASS = "AST"

_TYPING = ast.Name("typing", ast.Load())
_SYS_VERSION = ast.Attribute(ast.Name("sys"), "version_info", ast.Load())
_EMPTY_BODY = [ast.Constant(...)]
_DUMMY_CONDITION = ast.AST(test=ast.AST())


class StubGenerator(pyasdl.ASDLVisitor):
    def __init__(self):
        self.namespaces = defaultdict(list)

    def visit_Type(self, node):
        return self.visit(
            node.value,
            name=node.name,
            attributes=self.visit_all(node.value.attributes),
        )

    def visit_Sum(self, node, name, attributes):
        self._create_type(
            name, base=_BASE_CLASS, fields=attributes or _EMPTY_BODY
        )

        for constructor in node.types:
            if constructor.fields:
                fields = self.visit_all(constructor.fields)
            else:
                fields = _EMPTY_BODY

            self._create_type(constructor.name, base=name, fields=fields)

    def visit_Product(self, node, name, attributes):
        self._create_type(
            name,
            base=_BASE_CLASS,
            fields=[*self.visit_all(node.fields), *attributes],
        )

    def visit_Field(self, node):
        target = ast.Name(node.name, ast.Store())
        annotation = ast.Name(node.kind, ast.Load())
        if node.qualifier is not None:
            if node.qualifier is pyasdl.FieldQualifier.SEQUENCE:
                qualifier = "List"
            elif node.qualifier is pyasdl.FieldQualifier.OPTIONAL:
                qualifier = "Optional"
            else:
                raise ValueError(
                    f"Unexpected field qualifier: {node.qualifier}"
                )

            annotation = ast.Subscript(
                value=ast.Attribute(_TYPING, qualifier, ast.Load()),
                slice=annotation,
                ctx=ast.Load(),
            )
        return ast.AnnAssign(target, annotation, simple=1)

    def _create_type(self, name, base, fields):
        stub = ast.ClassDef(
            name=name,
            bases=[ast.Name(base, ast.Load())],
            keywords=[],
            body=fields,
            decorator_list=[],
        )
        self._add_stub(name, stub)

    def _add_stub(self, name, stub):
        self.namespaces[name].append((self.version, stub))


def by_version(item):
    version, _ = item
    return version


def group_fields(namespaces):
    fields = defaultdict(list)

    def _search_match(item):
        for field in fields:
            if ast.dump(field) == ast.dump(item):
                return field
        else:
            return item

    for version, namespace in namespaces:
        for item in namespace.body:
            fields[_search_match(item)].append(version)

    return fields


def with_guard(node, lowest, highest):
    if lowest is None:
        # sys.version_info <= highest
        assert highest is not None
        condition = ast.Compare(
            _SYS_VERSION, [ast.LtE()], [ast.Constant(highest)]
        )
    elif highest is None:
        # sys.version_info >= highest
        assert lowest is not None
        condition = ast.Compare(
            _SYS_VERSION, [ast.GtE()], [ast.Constant(lowest)]
        )
    else:
        # lowest <= sys.version_info <= highest
        condition = ast.Compare(
            ast.Constant(lowest),
            [ast.LtE()] * 2,
            [_SYS_VERSION, ast.Constant(highest)],
        )

    return ast.If(condition, body=[node], orelse=[])


def generate_guard(
    node,
    versions,
    all_asdl_versions,
    lowest_asdl_version,
    highest_asdl_version,
):
    if set(versions) == set(all_asdl_versions):
        return node
    elif max(versions) != highest_asdl_version:
        if min(versions) == lowest_asdl_version:
            lowest = None
        else:
            lowest = min(versions)
        return with_guard(node, lowest=lowest, highest=max(versions))
    elif min(versions) != lowest_asdl_version:
        if max(versions) == highest_asdl_version:
            highest = None
        else:
            highest = max(versions)
        return with_guard(node, lowest=min(versions), highest=highest)
    else:
        raise ValueError(f"Unexpected version chain: {versions}")


def unmarshal_low_level_versions(node):
    previous_condition = _DUMMY_CONDITION
    for item in node.body.copy():
        if (
            isinstance(item, ast.If)
            and ast.dump(item.test) == ast.dump(previous_condition.test)
            and not item.orelse
        ):
            previous_condition.body.extend(item.body)
            node.body.remove(item)
        elif isinstance(item, ast.If):
            previous_condition = item
        else:
            previous_condition = _DUMMY_CONDITION


def unmarshal_top_level_versions(guarded_node):
    # This code will remove reduntant conditions
    # when the class is already protected by the same
    # condition. E.g:
    # if sys.version <= (3, 7):
    #   class Test(AST):
    #       if sys.version <= (3, 7):
    #           foo: int
    #       if sys.version <= (3, 6):
    #           bar: str
    #
    # will become
    # if sys.version <= (3, 7):
    #   class Test(AST):
    #       foo: int
    #       if sys.version <= (3, 6):
    #           bar: str

    if not isinstance(guarded_node, ast.If):
        return unmarshal_low_level_versions(guarded_node)

    assert isinstance(guarded_node.body[0], ast.ClassDef)
    original_class = guarded_node.body[0]
    for index, item in enumerate(original_class.body.copy()):
        if isinstance(item, ast.If) and ast.dump(item.test) == ast.dump(
            guarded_node.test
        ):
            original_class.body[index] = item.body[0]

    return unmarshall_low_level_versions(original_class)


def generate_stubs(asdls):
    asdls.sort(key=by_version)

    all_asdl_versions = [version for version, _ in asdls]
    _guard_generator = partial(
        generate_guard,
        all_asdl_versions=all_asdl_versions,
        lowest_asdl_version=all_asdl_versions[0],
        highest_asdl_version=all_asdl_versions[-1],
    )

    stub_generator = StubGenerator()
    for stub_generator.version, tree in asdls:
        stub_generator.visit(tree)

    body = []
    for name, namespaces in stub_generator.namespaces.items():
        namespaces.sort(key=by_version)
        latest_stub_version, latest_stub = namespaces[-1]

        latest_stub.body = [
            _guard_generator(field, versions)
            for field, versions in group_fields(namespaces).items()
        ]

        all_stub_versions = []
        all_stub_bases = defaultdict(list)
        for version, stub in namespaces:
            all_stub_versions.append(version)
            all_stub_bases[stub.bases[0].id].append(version)

        if len(all_stub_bases) > 1:
            base_name = ast.Name(f"_{name}Base", ast.Store())
            base_switch = top_level_switch = None
            for base, base_versions in all_stub_bases.items():
                base_assign = ast.Assign(
                    [base_name], ast.Name(base, ast.Load())
                )
                guarded_base_assign = _guard_generator(
                    base_assign, base_versions
                )
                if base_switch is None:
                    base_switch = top_level_switch = guarded_base_assign
                else:
                    base_switch.orelse.append(guarded_base_assign)
                    base_switch = guarded_base_assign

            body.append(top_level_switch)
            latest_stub.bases = [base_name]

        latest_stub = _guard_generator(latest_stub, all_stub_versions)
        unmarshal_top_level_versions(latest_stub)
        body.append(latest_stub)

    module = ast.Module(body, type_ignores=[])
    unmarshal_low_level_versions(module)
    return module


def retrive_version(source):
    for comment in pyasdl.fetch_comments(source):
        comment = comment.lstrip()
        if comment.startswith("version="):
            comment = comment.replace("version=", "")
            tuple_version = comment.replace(".", ",")
            return ast.literal_eval(tuple_version)
    else:
        raise ValueError("No version= tag found in the given ASDL file")


def main():
    parser = ArgumentParser()
    parser.add_argument("files", type=Path, nargs="+")

    options = parser.parse_args()

    asdls = []
    for file in options.files:
        with open(file) as stream:
            source = stream.read()
            version = retrive_version(source)
            asdls.append((version, pyasdl.parse(source)))

    stub = generate_stubs(asdls)
    print("from __future__ import annotations")
    print("import sys")
    print("import typing")
    print(
        textwrap.dedent(
            """\
    class AST:
        _attributes: typing.ClassVar[typing.Tuple[str, ...]]
        _fields: typing.ClassVar[typing.Tuple[str, ...]]
        def __init__(self, *args: typing.Any, **kwargs: typing.Any) -> None: ...

        # Allow any attribute access (taken from types.SingleNamespace)
        def __getattribute__(self, name: str) -> Any: ...
        def __setattr__(self, name: str, value: Any) -> None: ...
        def __delattr__(self, name: str) -> None: ...
    """
        )
    )
    print("identifier = str")
    print("string = typing.AnyStr")
    print(
        textwrap.dedent(
            """\
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
    """
        )
    )
    print(ast.unparse(ast.fix_missing_locations(stub)))


if __name__ == "__main__":
    main()
