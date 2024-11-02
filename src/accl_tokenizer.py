from curses.ascii import isalpha, isdigit, isalnum
from enum import Enum

class TokenType(Enum):
    # Literals
    IntLit = 0
    FloatLit = 1
    CharLit = 2
    StrLit = 3
    FStrLit = 4
    BoolLit = 5

    Ident = 6
    DataType = 7

    # Symbols
    OpenParen = 8
    CloseParen = 9
    OpenBracket = 10
    CloseBracket = 11
    OpenBrace = 12
    CloseBrace = 13
    Semicolon = 14
    Equals = 15
    Colon = 16
    Comma = 17

    # Keywords
    Exit = 18
    Is = 19
    Let = 20
    Print = 21
    Error = 22


class Token:
    def __init__(self, Type: TokenType, value: str = "") -> None:
        self.Type: TokenType = Type
        self.value: str = value

    def __repr__(self) -> str:
        if self.value != "":
            return f"Token(Type= {self.Type}, Value= {self.value})\n"
        elif self.Type == TokenType.Semicolon or self.Type == TokenType.OpenBrace:
            return f"Token(Type= {self.Type})\n\n"
        else:
            return f"Token(Type= {self.Type})\n"


class Tokenizer:
    def __init__(self, src: str) -> None:
        self.src: str = src
        self.index: int = 0

        self.buffer: str = ""
        self.tokens: list[Token] = []

    def peek(self, offset: int = 0) -> str:
        if self.index + offset >= len(self.src):
            return ""
        else:
            return self.src[offset + self.index]

    def consume(self) -> str:
        self.index += 1
        return self.src[self.index - 1]

    def check_keywords(self) -> None:
        types: list[str] = ["int", "float", "char", "str", "bool"]
        bools: list[str] = ["true", "false"]
        if self.buffer == "exit" and not isalnum(self.peek()):
            self.tokens.append(Token(Type=TokenType.Exit))
            self.buffer = ""
        elif self.buffer == "is" and not isalnum(self.peek()):
            self.tokens.append(Token(Type=TokenType.Is))
            self.buffer = ""
        elif self.buffer == "let" and not isalnum(self.peek()):
            self.tokens.append(Token(Type=TokenType.Let))
            self.buffer = ""
        elif self.buffer == "print" and not isalnum(self.peek()):
            self.tokens.append(Token(Type=TokenType.Print))
            self.buffer = ""
        elif self.buffer == "error" and not isalnum(self.peek()):
            self.tokens.append(Token(Type=TokenType.Error))
            self.buffer = ""
        elif self.buffer in types and not isalnum(self.peek()):
            self.tokens.append(Token(Type=TokenType.DataType, value=self.buffer))
            self.buffer = ""
        elif self.buffer in bools and not isalnum(self.peek()):
            self.tokens.append(Token(Type=TokenType.BoolLit, value=self.buffer))
            self.buffer = ""
        elif self.buffer == "f" and self.peek() == '"':
            self.consume()
            while self.peek() or self.peek() != '"':
                self.buffer += self.consume()
            if not self.peek() or self.peek() != '"':
                raise Exception("Expected \" to end fstring")
            self.consume()
            self.tokens.append(Token(Type=TokenType.FStrLit, value=self.buffer))
            self.buffer = ""

    def check_symbols(self) -> None:
        if self.peek() == "(":
            self.consume()
            self.tokens.append(Token(Type=TokenType.OpenParen))
        elif self.peek() == ")":
            self.consume()
            self.tokens.append(Token(Type=TokenType.CloseParen))
        elif self.peek() == "[":
            self.consume()
            self.tokens.append(Token(Type=TokenType.OpenBracket))
        elif self.peek() == "]":
            self.consume()
            self.tokens.append(Token(Type=TokenType.CloseBracket))
        elif self.peek() == "{":
            self.consume()
            self.tokens.append(Token(Type=TokenType.OpenBrace))
        elif self.peek() == "}":
            self.consume()
            self.tokens.append(Token(Type=TokenType.CloseBrace))
        elif self.peek() == ";":
            self.consume()
            self.tokens.append(Token(Type=TokenType.Semicolon))
        elif self.peek() == "=":
            self.consume()
            self.tokens.append(Token(Type=TokenType.Equals))
        elif self.peek() == ":":
            self.consume()
            self.tokens.append(Token(Type=TokenType.Colon))
        elif self.peek() == ",":
            self.consume()
            self.tokens.append(Token(Type=TokenType.Comma))
        elif self.peek() == " " or self.peek() == "\n" or self.peek() == "\t":
            self.consume()
        else:
            raise Exception("Found unrecognized character while lexing:", self.peek())

    def tokenize(self) -> list[Token]:
        while self.peek() != "":
            if isalpha(self.peek()):
                while self.peek() != "" and isalnum(self.peek()) or \
                        self.peek() != "" and self.peek() == "_":
                    self.buffer += self.consume()
                    self.check_keywords()
                if self.buffer != "":
                    self.tokens.append(Token(Type=TokenType.Ident, value=self.buffer))
                    self.buffer = ""
            elif isdigit(self.peek()):
                self.buffer += self.consume()
                canfloat = False
                isfloat = False
                while self.peek() != "" and isdigit(self.peek()) or \
                        self.peek() != "" and self.peek() == ".":
                    if self.peek() == "." and canfloat and not isfloat:
                        isfloat = True
                        self.buffer += self.consume()
                        if not self.peek() or not isdigit(self.peek()):
                            raise ValueError("Floats must have at least one digit after .")
                    elif self.peek() == "." and isfloat:
                        raise ValueError("Float variables should only have one .")
                    elif self.peek() == "." and not canfloat:
                        raise ValueError("Float variables should have at least one digit before .")
                    else:
                        self.buffer += self.consume()
                        canfloat = True
                if isfloat:
                    self.tokens.append(Token(Type=TokenType.FloatLit, value=self.buffer))
                    self.buffer = ""
                else:
                    self.tokens.append(Token(Type=TokenType.IntLit, value=self.buffer))
                    self.buffer = ""
            elif self.peek() == "'":
                self.consume()
                if isalnum(self.peek(1)):
                    raise ValueError("Char must only be one character")
                self.buffer = self.consume()
                if not self.peek() or self.peek() != "'":
                    raise ValueError("Expected ' to end char")
                self.consume()
                self.tokens.append(Token(Type=TokenType.CharLit, value=self.buffer))
                self.buffer = ""
            elif self.peek() == '"':
                self.consume()
                while self.peek() and self.peek() != '"':
                    self.buffer += self.consume()
                if not self.peek() or self.peek() != '"':
                    raise ValueError("Expected \" to end str")
                self.consume()
                self.tokens.append(Token(Type=TokenType.StrLit, value=self.buffer))
                self.buffer = ""
            else:
                self.check_symbols()

        self.index = 0
        return self.tokens
