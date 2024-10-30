from accl_tokenizer import Token, TokenType
from typing import Union

class NodeExprIntLit:
    def __init__(self, int_lit: Token):
        self.int_lit: Token = int_lit

    def __repr__(self):
        return f"NodeExprIntLit:\n\tint_lit: {self.int_lit}\n"
class NodeExprFloatLit:
    def __init__(self, float_lit: Token):
        self.float_lit: Token = float_lit

    def __repr__(self):
        return f"NodeExprFloatLit:\n\tfloat_lit: {self.float_lit}\n"
class NodeExprCharLit:
    def __init__(self, char_lit: Token):
        self.char_lit: Token = char_lit

    def __repr__(self):
        return f"NodeExprCharLit:\n\tchar_lit: {self.char_lit}\n"
class NodeExprStrLit:
    def __init__(self, str_lit: Token):
        self.str_lit: Token = str_lit

    def __repr__(self):
        return f"NodeExprStrLit:\n\tstr_lit: {self.str_lit}\n"
class NodeExprFStrLit:
    def __init__(self, fstr_lit: Token):
        self.fstr_lit: Token = fstr_lit

    def __repr__(self):
        return f"NodeExprFStrLit:\n\tfstr_lit: {self.fstr_lit}\n"
class NodeExprBoolLit:
    def __init__(self, bool_lit: Token):
        self.bool_lit: Token = bool_lit

    def __repr__(self):
        return f"NodeExprBoolLit:\n\tbool_lit: {self.bool_lit}\n"
class NodeExprIdentifier:
    def __init__(self, identifier: Token):
        self.identifier: Token = identifier

    def __repr__(self):
        return f"NodeExprIdentifier:\n\tidentifier: {self.identifier}\n"
class NodeExpr:
    def __init__(self, var: Union['NodeExprIntLit',
            'NodeExprFloatLit',
            'NodeExprCharLit',
            'NodeExprStrLit',
            'NodeExprFStrLit',
            'NodeExprBoolLit',
            'NodeExprIdentifier']):
        self.var: Union['NodeExprIntLit',
            'NodeExprFloatLit',
            'NodeExprCharLit',
            'NodeExprStrLit',
            'NodeExprFStrLit',
            'NodeExprBoolLit',
            'NodeExprIdentifier'] = var

    def __repr__(self):
        return f"NodeExpr:\n\tvar: {self.var}\n"

class NodeStmtExit:
    def __init__(self, expr: NodeExpr):
        self.expr: NodeExpr = expr

    def __repr__(self):
        return f"NodeStmtExit:\n\texpr: {self.expr}\n"
class NodeStmtLet:
    def __init__(self, Identifier: Token, Type: Token, Expr: NodeExpr):
        self.identifier: Token = Identifier
        self.type: Token = Type
        self.expr: NodeExpr = Expr

    def __repr__(self):
        return f"NodeStmtLet:\n\tidentifier: {self.identifier}\n\ttype: {self.type}\n\texpr: {self.expr}\n"
class NodeStmtPrint:
    def __init__(self, expr: NodeExpr):
        self.expr: NodeExpr = expr

    def __repr__(self):
        return f"NodeStmtPrint:\n\texpr: {self.expr}\n"
class NodeStmtReassignment:
    def __init_(self, Identifier: Token, Expr: NodeExpr):
        self.identifier: Token = Identifier
        self.expr: NodeExpr = Expr

    def __repr__(self):
        return f"NodeStmtReassignment:\n\tidentifier: {self.identifier}\n\texpr: {self.expr}\n"
class NodeStmtReturn:
    def __init__(self, expr: NodeExpr):
        self.expr: NodeExpr = expr

    def __repr__(self):
        return f"NodeStmtReturn:\n\texpr: {self.expr}\n"
class NodeStmtDef:
    def __init__(self,
                 Identifier: Token,
                 Parameters: list[NodeStmtLet],
                 ReturnType: Token,
                 Stmts: list['NodeStmt', NodeStmtReturn]):
        self.identifier: Token = Identifier
        self.parameters: list[NodeStmtLet] = Parameters
        self.returnType: Token = ReturnType
        self.stmts: list['NodeStmt', NodeStmtReturn] = Stmts

    def __repr__(self):
        return f"NodeStmtDef:\n\tidentifier: {self.identifier}\n\tparameters: {self.parameters}\n\treturn type: {self.returnType}\n\tstmts: {self.stmts}\n"
class NodeStmtIf:
    def __init__(self):
        pass # TODO NODESTMTIF
class NodeStmtWhile:
    def __init__(self):
        pass # TODO NODESTMTWHILE
class NodeStmtFor:
    def __init__(self):
        pass # TODO NODESTMTFOR
class NodeStmt:
    def __init__(self, var: Union['NodeStmtExit',
            'NodeStmtReturn',
            'NodeStmtLet',
            'NodeStmtReassignment',
            'NodeStmtDef',
            'NodeStmtPrint']):
        self.var: Union['NodeStmtExit',
            'NodeStmtReturn',
            'NodeStmtLet',
            'NodeStmtReassignment',
            'NodeStmtDef',
            'NodeStmtPrint'] = var

    def __repr__(self):
        return f"NodeStmt:\n\tvar: {self.var}\n"

class NodeProgram:
    def __init__(self, stmts: list[NodeStmt]):
        self.stmts: list[NodeStmt] = stmts

    def __repr__(self):
        return f"NodeProgram:\n\tstmts: {self.stmts}\n"

class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens: list[Token] = tokens
        self.index: int = 0

    def parse_expr(self) -> NodeExpr or None: # type: ignore
        token: Token = self.peek()
        if token and token.Type == TokenType.IntegerLiteral:
            return NodeExpr(var= NodeExprIntLit(int_lit= self.consume()))
        elif token and token.Type == TokenType.FloatLiteral:
            return NodeExpr(var= NodeExprFloatLit(float_lit= self.consume()))
        elif token and token.Type == TokenType.CharacterLiteral:
            return NodeExpr(var= NodeExprCharLit(char_lit= self.consume()))
        elif token and token.Type == TokenType.StringLiteral:
            return NodeExpr(var= NodeExprStrLit(str_lit= self.consume()))
        elif token and token.Type == TokenType.FStringLiteral:
            return NodeExpr(var= NodeExprFStrLit(fstr_lit= self.consume()))
        elif token and token.Type == TokenType.BooleanLiteral:
            return NodeExpr(var= NodeExprBoolLit(bool_lit= self.consume()))
        elif token and token.Type == TokenType.Identifier:
            return NodeExpr(var= NodeExprIdentifier(identifier= self.consume()))
        else:
            return None

    def parse_stmt(self) -> NodeStmt or None: # type: ignore
        token: Token = self.peek()
        if token and token.Type == TokenType.Exit:
            self.consume()
            node_expr = self.parse_expr()
            if node_expr:
                stmt_exit: None or NodeStmtExit = NodeStmtExit(expr= node_expr) # type: ignore
            else:
                raise ValueError("Invalid Expression")

            self.expect(token= TokenType.Semicolon, errmessage= "Expected ; to end exit statement")
            return NodeStmt(var= stmt_exit)
        elif token and token.Type == TokenType.Let:
            self.consume()
            if self.peek() and self.peek().Type == TokenType.Identifier:
                stmt_let_identifier: Token = self.consume()
            else:
                raise Exception("Expected Identifier following let statement")

            self.expect(token= TokenType.Colon, errmessage= "Expected colon for type declaration")

            if self.peek() and self.peek().Type == TokenType.DataType:
                held_type: str = self.peek().Value
                stmt_let_type: Token = self.consume()
            else:
                raise Exception("Expected type in variable declaration")

            try:
                self.expect(token= TokenType.Equals, errmessage= "Expected =/is to set variable")
            except:
                self.expect(token= TokenType.Is, errmessage= "Expected =/is to set variable")

            if self.peek():
                node_expr = self.parse_expr()
                if held_type == "int" and type(node_expr.var).__name__ == "NodeExprIntLit" or \
                        held_type == "float" and type(node_expr.var).__name__ == "NodeExprFloatLit" or \
                        held_type == "char" and type(node_expr.var).__name__ == "NodeExprCharLit" or \
                        held_type == "str" and type(node_expr.var).__name__ == "NodeExprStrLit" or \
                        held_type == "bool" and type(node_expr.var).__name__ == "NodeExprBoolLit":
                    stmt_let_expr = node_expr
                else:
                    raise Exception("Data type mismatch on variable declaration")
            else:
                raise Exception("Expected value to be assigned to the variable")

            self.expect(token= TokenType.Semicolon, errmessage= "Expected a ; to end let statement")
            stmt_let: NodeStmtLet = NodeStmtLet(Identifier= stmt_let_identifier, Type= stmt_let_type, Expr= stmt_let_expr)
            return NodeStmt(var= stmt_let)
        elif token and token.Type == TokenType.Print:
            self.consume()
            self.expect(token= TokenType.OpenParen, errmessage= "Expected ( to begin print statement")

            stmt_print = None
            if self.peek().Type != TokenType.CloseParen:
                node_expr: NodeExpr = self.parse_expr()
                stmt_print = NodeStmtPrint(expr= node_expr)

            self.expect(token=TokenType.CloseParen, errmessage="Expected ) to close print statement")
            self.expect(token= TokenType.Semicolon, errmessage= "Expected ; to end print statement")
            if stmt_print:
                return NodeStmt(var= stmt_print)
            else:
                return None
        elif token and token.Type == TokenType.Identifier:
            pass # TODO PARSE REASSIGNMENT/CALL STATEMENT
        elif token and token.Type == TokenType.If:
            pass # TODO PARSE IF STATEMENT
        elif token and token.Type == TokenType.While:
            pass # TODO PARSE WHILE LOOP STATEMENT
        elif token and token.Type == TokenType.For:
            pass # TODO PARSE FOR LOOP STATEMENT
        elif token and token.Type == TokenType.Def:
            pass # TODO PARSE FUNCTION DEF STATEMENT

    def parse_program(self):
        program: NodeProgram = NodeProgram(stmts=[])
        while self.peek():
            stmt = self.parse_stmt()
            if stmt:
                program.stmts.append(stmt)
            else:
                raise Exception("Invalid Statement")
        return program

    def peek(self, offset: int = 0) -> Token or None: # type: ignore
        if self.index + offset >= len(self.tokens):
            return None
        else:
            offset += self.index
            return self.tokens[offset]

    def consume(self) -> Token:
        self.index += 1
        return self.tokens[self.index - 1]

    def expect(self, token: TokenType, errmessage: str = ""):
        token_: Token = self.peek()
        if token_ and token_.Type == token:
            self.consume()
        else:
            raise Exception(errmessage)
