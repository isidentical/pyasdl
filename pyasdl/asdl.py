import argparse
import io
import tokenize as _tokenize
from typing import Iterator

from pegen.tokenizer import Tokenizer
from pyasdl.grammar import Module, Sum
from pyasdl.parser import GeneratedParser as _ASDLParser

__all__ = ["parse", "fetch_comments", "is_simple_sum"]
# Since the pegen.tokenizer.Tokenizer uses .type instead of .exact_type
# it is not trivial to change the default comment behavior. A workaround
# way is sanitizing the input before passing it into the real parser

COMMENT_PATTERN = _tokenize.Whitespace + r"--.*?\n"
_tokenize.PseudoToken = _tokenize.Whitespace + _tokenize.group(
    COMMENT_PATTERN,
    _tokenize.PseudoExtras,
    _tokenize.Number,
    _tokenize.Funny,
    _tokenize.ContStr,
    _tokenize.Name,
)


def tokenize(
    source: str, ignore_comments: bool = True
) -> Iterator[_tokenize.TokenInfo]:
    # A wrapper around tokenize.generate_tokens to pass comment tokens
    source_buffer = io.StringIO(source)
    for token in _tokenize.generate_tokens(source_buffer.readline):
        if token.string.startswith("--") and ignore_comments:
            continue
        yield token


def parse(source: str, *, filename: str = "<pyasdl>") -> Module:
    tokenizer = Tokenizer(tokenize(source))
    parser = _ASDLParser(tokenizer)
    tree = parser.start()

    if tree is None:
        raise parser.make_syntax_error(filename)
    return tree


def fetch_comments(source: str):
    for token in tokenize(source, ignore_comments=False):
        if token.string.startswith("--"):
            yield token.string[2:]


def is_simple_sum(node):
    assert isinstance(node, Sum)
    return (
        all(len(constructor.fields) == 0 for constructor in node.types)
        and len(node.attributes) == 0
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    options = parser.parse_args()

    with open(options.file) as f:
        content = f.read()

    print(parse(content))


if __name__ == "__main__":
    main()
