# PyASDL

A yet another implementation for [Zephyr ASDL](https://www.cs.princeton.edu/~appel/papers/asdl97.pdf) format.

## API
### `parse(source: str, *, filename: str = "<pyasdl>") -> Module`

Parse the given `source` string, and return the AST in the shape of an `pyasdl.Module`. The
full format is defined in the [`grammar.asdl`](./pyasdl/static/grammar.asdl) file. The `filename`
can be optionally supplied, and will be displayed if there is any syntax error.

### `fetch_comments(source: str) -> Iterator[str]:`

Return an iterator of the ASDL comments in the given `source` string.

### `is_simple_sum(node: Sum) -> bool:`

Check whether if the given `node`'s all children lack any fields.


### Examples
Here is a list of example tools that process the given ASDL with `PyASDL`:
- [Typing Stub Generator](./examples/generators/src/typing_stub.py)
- [Python Class Generator](./examples/generators/src/python.py)
- [ESDL Generator](./examples/generators/src/edgedb.py)
- [GraphQL Converter](./examples/generators/src/graphql.py)
