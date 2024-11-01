from curses.ascii import isalpha, isdigit, isalnum
from enum import Enum

class TokenType(Enum):
    # Literals
    IntegerLiteral = 0
    FloatLiteral = 1
    CharacterLiteral = 2
    StringLiteral = 3
    FStringLiteral = 4
    BooleanLiteral = 5

    Identifier = 6
    DataType = 7

    # Keywords
    Let = 8
    Is = 9
    Exit = 10
    Print = 11
    Error = 24

    # Symbols
    Equals = 12
    BinaryOperator = 13     # + - * / %
    OpenParen = 14          # (
    CloseParen = 15         # )
    OpenBracket = 16        # [
    CloseBracket = 17       # ]
    OpenBrace = 18          # {
    CloseBrace = 19         # }
    Colon = 20
    Semicolon = 21
    Comma = 22
    Dot = 23

class Token:
    def __init__(self, Type: TokenType, Value: str = ""):
        self.Type = Type
        self.Value = Value

    def __repr__(self):
        if self.Value != "":
            return f"Token(Type= {self.Type}, Value= {self.Value})\n"
        elif self.Type == TokenType.Semicolon:
            return f"Token(Type= {self.Type})\n\n"
        elif self.Type == TokenType.OpenBrace:
            return f"Token(Type= {self.Type})\n\n"
        else:
            return f"Token(Type= {self.Type})\n"

class Tokenizer:
    def __init__(self, src: str):
        self.src: str = src
        self.index: int = 0

    def tokenize(self) -> list[Token]:
        tokens: list[Token] = []
        buffer: str = ""

        while self.peek() is not None:
            if isalpha(self.peek()):
                while self.peek() is not None and isalnum(self.peek()) or self.peek() is not None and self.peek() == "_":
                    buffer += self.consume()
                    if buffer == "exit" and not isalnum(self.peek()):
                        tokens.append(Token(Type= TokenType.Exit))
                        buffer = ""
                    elif buffer == "let" and not isalnum(self.peek()):
                        tokens.append(Token(Type= TokenType.Let))
                        buffer = ""
                    elif buffer == "print" and not isalnum(self.peek()):
                        tokens.append(Token(Type= TokenType.Print))
                        buffer = ""
                    elif buffer == "is" and not isalnum(self.peek()):
                        tokens.append(Token(Type= TokenType.Is))
                        buffer = ""
                    elif buffer == "error" and not isalnum(self.peek()):
                        tokens.append(Token(Type= TokenType.Error))
                        buffer = ""
                    elif buffer == "int" and not isalnum(self.peek()) or buffer == "float" and not isalnum(self.peek()) or buffer == "char" and not isalnum(self.peek()) or buffer == "str" and not isalnum(self.peek()) or buffer == "bool":
                        tokens.append(Token(Type= TokenType.DataType, Value= buffer))
                        buffer = ""
                    elif buffer == "True" and not isalnum(self.peek()) or buffer == "False" and not isalnum(self.peek()):
                        tokens.append(Token(Type= TokenType.BooleanLiteral, Value= buffer))
                        buffer = ""
                    elif buffer == 'f' and self.peek() == '"':
                        self.consume()
                        buffer = ""
                        while self.peek() != '"' and self.peek():
                            buffer += self.consume()
                        if not self.peek() or self.peek() != '"':
                            raise Exception("Expected \" to end fstring declaration")
                        self.consume()
                        tokens.append(Token(Type= TokenType.FStringLiteral, Value= buffer))
                        buffer = ""
                if buffer != "":
                    tokens.append(Token(Type= TokenType.Identifier, Value= buffer))
                    buffer = ""
            elif isdigit(self.peek()):
                buffer += self.consume()
                isfloat = False
                while self.peek() is not None and isdigit(self.peek()) or self.peek() is not None and self.peek() == ".":
                    if self.peek() == "." and not isfloat:
                        isfloat = True
                        buffer += self.consume()
                        if not self.peek() or not isdigit(self.peek()):
                            raise ValueError("Float variables must have at least one digit behind dot")
                    elif self.peek() == "." and isfloat:
                        raise ValueError("Float variables should only have one dot")
                    buffer += self.consume()
                if isfloat:
                    tokens.append(Token(Type= TokenType.FloatLiteral, Value= buffer))
                    buffer = ""
                else:
                    tokens.append(Token(Type= TokenType.IntegerLiteral, Value= buffer))
                    buffer = ""
            elif self.peek() == '\'':
                self.consume()
                if self.peek(1) != '\'':
                    raise ValueError("Char variable must contain one char")
                buffer = self.consume()
                if self.peek() != '\'':
                    raise Exception("Expected ' to end char declaration")
                self.consume()
                tokens.append(Token(Type= TokenType.CharacterLiteral, Value= buffer))
                buffer = ""
            elif self.peek() == '"':
                self.consume()
                while self.peek() != '"' and self.peek():
                    buffer += self.consume()
                if not self.peek() or self.peek() != '"':
                    raise Exception("Expected \" to end str declaration")
                self.consume()
                tokens.append(Token(Type= TokenType.StringLiteral, Value= buffer))
                buffer = ""
            elif self.peek() == ';':
                self.consume()
                tokens.append(Token(Type= TokenType.Semicolon))
            elif self.peek() == ':':
                self.consume()
                tokens.append(Token(Type= TokenType.Colon))
            elif self.peek() == '(':
                self.consume()
                tokens.append(Token(Type= TokenType.OpenParen))
            elif self.peek() == ')':
                self.consume()
                tokens.append(Token(Type= TokenType.CloseParen))
            elif self.peek() == '[':
                self.consume()
                tokens.append(Token(Type= TokenType.OpenBracket))
            elif self.peek() == ']':
                self.consume()
                tokens.append(Token(Type= TokenType.CloseBracket))
            elif self.peek() == '{':
                self.consume()
                tokens.append(Token(Type= TokenType.OpenBrace))
            elif self.peek() == '}':
                self.consume()
                tokens.append(Token(Type= TokenType.CloseBrace))
            elif self.peek() == '+' or self.peek() == '-' or self.peek() == '*' or self.peek() == '/' or self.peek() == '%':
                buffer = self.consume()
                tokens.append(Token(Type= TokenType.BinaryOperator, Value= buffer))
                buffer = ""
            elif self.peek() == '=':
                self.consume()
                tokens.append(Token(Type= TokenType.Equals))
            elif self.peek() == ',':
                self.consume()
                tokens.append(Token(Type= TokenType.Comma))
            elif self.peek() == '.':
                self.consume()
                tokens.append(Token(Type= TokenType.Dot))
            elif self.peek() == ' ' or self.peek() == '\n' or self.peek() == '\t':
                self.consume()
            else:
                raise Exception("Found unrecognized character while lexing:", self.peek())
        self.index = 0
        return tokens

    def peek(self, offset: int = 0) -> str or None: # type: ignore
        if self.index + offset >= len(self.src):
            return None
        else:
            offset += self.index
            return self.src[offset]

    def consume(self) -> str:
        self.index += 1
        return self.src[self.index - 1]

