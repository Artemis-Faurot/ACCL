from src.accl_tokenizer import Tokenizer, Token
import sys

sys.argv.append("main.accl")

def main():
    if len(sys.argv) != 2:
        raise Exception("Improperuse of compiler: python 3 main.py {file}.accl")
    file = open(sys.argv[1], 'r')
    contents: str = file.read()
    file.close()
    tokenizer: Tokenizer = Tokenizer(contents)
    tokens: list[Token] = tokenizer.tokenize()

    print(tokens)

if __name__ == "__main__":
    main()