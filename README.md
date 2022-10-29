# PyASDL

A pure Python implementation of the [Zephyr ASDL](https://www.cs.princeton.edu/~appel/papers/asdl97.pdf) format.

## API

### `parse(source, *, filename = ...) -> Module`

Parse the given `source` string, and return the AST in the shape of an `pyasdl.Module`. The
full format is defined in the [`grammar.asdl`](./pyasdl/static/grammar.asdl) file. The `filename`
can be optionally supplied, and will be used if any syntax errors found during the parsing process.

### `fetch_comments(source) -> Iterator[str]`

Iterate over all the comments (in the shape of `-- comment`) in the given ASDL source string.

### `is_simple_sum(node) -> bool`

Check whether if the given `node` is an enum (or simple sum) (e.g. a sum where none
of the members has constructor fields).

### Examples

Here is a list of example tools that process the given ASDL with `PyASDL`:

- [Typing Stub Generator](./examples/generators/src/typing_stub.py)
- [Python Class Generator](./examples/generators/src/python.py)
- [ESDL Generator](./examples/generators/src/edgedb.py)
- [GraphQL Converter](./examples/generators/src/graphql.py)
