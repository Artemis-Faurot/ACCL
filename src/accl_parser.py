from accl_tokenizer import Token, TokenType
from typing import Union

class Node:
    class ExprIntLit:
        def __init__(self, int_lit: Token) -> None:
            self.int_lit: Token = int_lit

        def __repr__(self) -> str:
            return f"ExprIntLit:\n\tint_lit: {self.int_lit}\n"

    class ExprFloatLit:
        def __init__(self, float_lit: Token) -> None:
            self.float_lit: Token = float_lit

        def __repr__(self) -> str:
            return f"ExprFloatLit:\n\tfloat_lit: {self.float_lit}\n"

    class ExprCharLit:
        def __init__(self, char_lit: Token) -> None:
            self.char_lit: Token = char_lit

        def __repr__(self) -> str:
            return f"ExprCharLit:\n\tchar_lit: {self.char_lit}\n"

    class ExprStrLit:
        def __init__(self, str_lit: Token) -> None:
            self.str_lit: Token = str_lit

        def __repr__(self) -> str:
            return f"ExprStrLit:\n\tstr_lit: {self.str_lit}\n"

    class ExprFStrLit:
        def __init__(self, fstr_lit: Token) -> None:
            self.fstr_lit: Token = fstr_lit

        def __repr__(self) -> str:
            return f"ExprFStrLit:\n\tfstr_lit: {self.fstr_lit}\n"

    class ExprBoolLit:
        def __init__(self, bool_lit: Token) -> None:
            self.bool_lit: Token = bool_lit

        def __repr__(self) -> str:
            return f"ExprBoolLit:\n\tbool_lit: {self.bool_lit}\n"

    class ExprIdent:
        def __init__(self, ident: Token) -> None:
            self.ident: Token = ident

        def __repr__(self) -> str:
            return f"ExprIdent:\n\tident: {self.ident}\n"

    class Expr:
        def __init__(self, var: Union['Node.ExprIntLit',
        'Node.ExprFloatLit',
        'Node.ExprCharLit',
        'Node.ExprStrLit',
        'Node.ExprFStrLit',
        'Node.ExprBoolLit',
        'Node.ExprIdent']) -> None:
            self.var: Union['Node.ExprIntLit',
            'Node.ExprFloatLit',
            'Node.ExprCharLit',
            'Node.ExprStrLit',
            'Node.ExprFStrLit',
            'Node.ExprBoolLit',
            'Node.ExprIdent'] = var

        def __repr__(self) -> str:
            return f"Expr:\n\tvar: {self.var}\n"

    class StmtExit:
        def __init__(self, expr: 'Node.Expr') -> None:
            self.expr: 'Node.Expr' = expr

        def __repr__(self) -> str:
            return f"StmtExit:\n\texpr: {self.expr}\n"

    class StmtLet:
        def __init__(self, ident: Token, type: Token, expr: 'Node.Expr') -> None:
            self.ident: Token = ident
            self.type: Token = type
            self.expr: 'Node.Expr' = expr

        def __repr__(self) -> str:
            return f"StmtLet:\n\tident: {self.ident}\n\ttype: {self.type}\n\texpr: {self.expr}\n"

    class StmtPrint:
        def __init__(self, expr: 'Node.Expr') -> None:
            self.expr: 'Node.Expr' = expr

        def __repr__(self) -> str:
            return f"StmtPrint:\n\texpr: {self.expr}\n"

    class StmtError:
        def __init__(self, errmessage: 'Node.Expr', exit_code: 'Node.Expr') -> None:
            self.errmessage: 'Node.Expr' = errmessage
            self.exit_code: 'Node.Expr' = exit_code

        def __repr__(self) -> str:
            return f"StmtError:\n\terrmessage: {self.errmessage}\n\texit_code: {self.exit_code}\n"

    class Stmt:
        def __init__(self, var: Union['Node.StmtExit',
        'Node.StmtLet',
        'Node.StmtPrint',
        'Node.StmtError']) -> None:
            self.var: Union['Node.StmtExit',
            'Node.StmtLet',
            'Node.StmtPrint',
            'Node.StmtError'] = var

        def __repr__(self) -> str:
            return f"Stmt:\n\tvar: {self.var}\n"

    class Program:
        def __init__(self, stmts: list['Node.Stmt']) -> None:
            self.stmts: list['Node.Stmt'] = stmts

        def __repr__(self) -> str:
            return f"Program:\n\tstmts: {self.stmts}\n"


class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens: list[Token] = tokens
        self.index: int = 0

    def peek(self, offset: int = 0) -> Union[Token, None]:
        if self.index + offset >= len(self.tokens):
            return None
        else:
            return self.tokens[self.index + offset]

    def consume(self) -> Token:
        self.index += 1
        return self.tokens[self.index - 1]

    def expect(self, token: TokenType, errmessage: str = "") -> None:
        if self.peek() and self.peek().Type == token:
            self.consume()
        else:
            raise Exception(errmessage)

    def parse_expr(self) -> Node.Expr:
        if self.peek() and self.peek().Type == TokenType.IntLit:
            return Node.Expr(var=Node.ExprIntLit(int_lit=self.consume()))
        elif self.peek() and self.peek().Type == TokenType.FloatLit:
            return Node.Expr(var=Node.ExprFloatLit(float_lit=self.consume()))
        elif self.peek() and self.peek().Type == TokenType.CharLit:
            return Node.Expr(var=Node.ExprCharLit(char_lit=self.consume()))
        elif self.peek() and self.peek().Type == TokenType.StrLit:
            return Node.Expr(var=Node.ExprStrLit(str_lit=self.consume()))
        elif self.peek() and self.peek().Type == TokenType.FStrLit:
            return Node.Expr(var=Node.ExprFStrLit(fstr_lit=self.consume()))
        elif self.peek() and self.peek().Type == TokenType.BoolLit:
            return Node.Expr(var=Node.ExprBoolLit(bool_lit=self.consume()))
        elif self.peek() and self.peek().Type == TokenType.Ident:
            return Node.Expr(var=Node.ExprIdent(ident=self.consume()))
        else:
            raise Exception("Invalid Expression")

    def parse_stmt_exit(self) -> Node.StmtExit:
        self.consume()
        stmt_exit: Node.StmtExit = Node.StmtExit(expr=self.parse_expr())
        self.expect(token=TokenType.Semicolon, errmessage="Expected ; to end exit statement")
        return stmt_exit

    def parse_stmt_let(self) -> Node.StmtLet:
        self.consume()
        if self.peek() and self.peek().Type == TokenType.Ident:
            stmt_let_identifier: Token = self.consume()
        else:
            raise Exception("Expected identifier in let statement")

        self.expect(token=TokenType.Colon, errmessage="Expected : for type specification in let statement")

        if self.peek() and self.peek().Type == TokenType.DataType:
            held_type: str = self.peek().value
            stmt_let_type: Token = self.consume()
        else:
            raise Exception("Expected type in let statement")

        try:
            self.expect(token=TokenType.Equals, errmessage="Expected =/is to set variable in let statement")
        except:
            self.expect(token=TokenType.Is, errmessage="Expected =/is to set variable in let statement")

        if self.peek():
            node_expr = self.parse_expr()
            if held_type == "int" and type(node_expr.var) == Node.ExprIntLit or \
                    held_type == "float" and type(node_expr.var) == Node.ExprFloatLit or \
                    held_type == "char" and type(node_expr.var) == Node.ExprCharLit or \
                    held_type == "str" and type(node_expr.var) == Node.ExprStrLit or \
                    held_type == "str" and type(node_expr.var) == Node.ExprFStrLit or \
                    held_type == "bool" and type(node_expr.var) == Node.ExprBoolLit:
                stmt_let_expr = node_expr
            else:
                raise Exception("Data type mismatch on variable declaration")
        else:
            raise Exception("Expected value to be assigned to the variable")

        self.expect(token=TokenType.Semicolon, errmessage="Expected ; to end let statement")
        return Node.StmtLet(ident=stmt_let_identifier, type=stmt_let_type, expr=stmt_let_expr)

    def parse_stmt_print(self) -> Node.StmtPrint:
        self.consume()
        self.expect(token=TokenType.OpenParen, errmessage="Expected ( to begin print statement expression")

        if self.peek().Type != TokenType.CloseParen:
            node_expr: Node.Expr = self.parse_expr()
            stmt_print: Node.StmtPrint = Node.StmtPrint(expr=node_expr)
        else:
            node_expr: Node.Expr = Node.Expr(var=Node.ExprStrLit(str_lit=Token(Type=TokenType.StrLit, value="")))
            stmt_print: Node.StmtPrint = Node.StmtPrint(expr=node_expr)

        self.expect(token=TokenType.CloseParen, errmessage="Expected ) to close print statement")
        self.expect(token=TokenType.Semicolon, errmessage="Expected ; to end print statement")
        return stmt_print

    def parse_stmt_error(self) -> Node.StmtError:
        self.consume()
        self.expect(token=TokenType.OpenParen, errmessage="Expected open parenthesis to start error arguments")

        stmt_error: Node.StmtError = Node.StmtError(errmessage=Node.Expr(var=Node.ExprStrLit(str_lit= Token( Type=TokenType.StrLit, value=""))), exit_code= Node.Expr(var=Node.ExprIntLit(int_lit=Token(Type= TokenType.IntLit, value="1"))))

        if self.peek().Type != TokenType.CloseParen:
            errmessage: Node.Expr = self.parse_expr()
            if type(errmessage.var) != Node.ExprStrLit and type(errmessage.var != Node.ExprFStrLit) and \
                    type(errmessage.var) != Node.ExprIdent:
                raise Exception("Expected string for error message argument")
            else:
                stmt_error.errmessage = errmessage
            self.expect(token=TokenType.Comma, errmessage="Expected a comma to separate arguments")
            exit_code: Node.Expr = self.parse_expr()
            if type(exit_code.var) != Node.ExprIntLit and type(exit_code.var) != Node.ExprIdent:
                raise Exception("Expected integer literal for error exit code")
            else:
                stmt_error.exit_code = exit_code

        self.expect(token=TokenType.CloseParen, errmessage="Expected closing parenthesis to end error arguments")
        self.expect(token=TokenType.Semicolon, errmessage="Expected semicolon to end error statement")
        return stmt_error

    def parse_stmt(self) -> Node.Stmt:
        stmt_token: Token = self.peek()
        if stmt_token.Type == TokenType.Exit:
            node_stmt = self.parse_stmt_exit()
        elif stmt_token.Type == TokenType.Let:
            node_stmt = self.parse_stmt_let()
        elif stmt_token.Type == TokenType.Print:
            node_stmt = self.parse_stmt_print()
        elif stmt_token.Type == TokenType.Error:
            node_stmt = self.parse_stmt_error()
        else:
            raise Exception("Invalid Expression")
        return Node.Stmt(var=node_stmt)

    def parse_program(self) -> Node.Program:
        program: Node.Program = Node.Program(stmts=[])
        while self.peek():
            program.stmts.append(self.parse_stmt())
        return program
