import argparse
import io
import re
import tokenize

from pegen.tokenizer import Tokenizer
from pyasdl.parser import GeneratedParser as _ASDLParser

# Since the pegen.tokenizer.Tokenizer uses .type instead of .exact_type
# it is not trivial to change the default comment behavior. A workaround
# way is sanitizing the input before passing it into the real parser

COMMENT_PATTERN = re.compile(r"--.*?\n")


def parse(source, *, filename="<pyasdl>"):
    source = re.sub(COMMENT_PATTERN, str(), source)

    buffer_ = io.StringIO(source)
    tokengen = tokenize.generate_tokens(buffer_.readline)
    tokenizer = Tokenizer(tokengen)
    parser = _ASDLParser(tokenizer)
    tree = parser.start()

    if tree is None:
        raise parser.make_syntax_error(filename)
    return tree


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    options = parser.parse_args()

    with open(options.file) as f:
        content = f.read()

    print(parse(content))


if __name__ == "__main__":
    main()
