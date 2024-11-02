from accl_generation import Generator
from accl_parser import Parser, Node
from accl_tokenizer import Tokenizer, Token
import sys
import os
import subprocess as s

def main():
    if len(sys.argv) != 2:
        raise Exception("Improper use of compiler: python3 main.py {file}.accl")
    file = open(sys.argv[1], 'r')
    contents: str = file.read()
    file.close()
    tokenizer: Tokenizer = Tokenizer(contents)
    tokens: list[Token] = tokenizer.tokenize()

    parser: Parser = Parser(tokens)
    program: Node.Program = parser.parse_program() # type: ignore

    generator: Generator = Generator(program)

    file = open("./output/out.asm", 'w')
    file.write(generator.gen_prog())
    file.close()

    os.system("nasm -felf64 ./output/out.asm -o ./output/out.o")
    os.system(f"gcc -static -nostdlib -m64 ./output/out.o -o ./{sys.argv[1].removesuffix('.accl')}")
    os.system("rm -rf ./output")
    print("Running program . . .\n")
    result = s.run(f"./{sys.argv[1].removesuffix('.accl')}")
    print(f"Program exited with code: {result.returncode}")

if __name__ == "__main__":
    main()
