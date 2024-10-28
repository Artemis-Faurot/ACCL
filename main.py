from accl_generation import Generator
from accl_parser import Parser, NodeProgram
from accl_tokenizer import Tokenizer, Token
import sys

debug: bool = False
if debug: sys.argv.append("./file.accl")

def main():
    if len(sys.argv) != 2:
        raise Exception("Improper use of compiler: python3 main.py {file}.accl")
    file = open(sys.argv[1], 'r')
    contents: str = file.read()
    file.close()
    tokenizer: Tokenizer = Tokenizer(contents)
    tokens: list[Token] = tokenizer.tokenize()

    if debug: print(tokens)

    parser: Parser = Parser(tokens)
    program: NodeProgram or None = parser.parse_program() # type: ignore

    if debug: print(program)

    if not program:
        raise Exception("Invalid program")

    generator: Generator = Generator(program)

    file = open("./output/out.asm", 'w')
    file.write(generator.gen_prog())
    file.close()

if __name__ == "__main__":
    main()
