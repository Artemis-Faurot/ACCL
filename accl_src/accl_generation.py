from accl_parser import NodeProgram, NodeStmt, NodeExpr, NodeExprIntLit, NodeStmtExit, NodeStmtLet, NodeExprIdentifier, \
    NodeExprFloatLit, NodeExprCharLit, NodeExprStrLit, NodeExprBoolLit, NodeStmtPrint
import io

class Var:
    def __init__(self, stackloc: int):
        self.stackloc: int = stackloc

class Generator:
    def __init__(self, program: NodeProgram):
        self.program: NodeProgram = program

        self.data = io.StringIO()
        self.text = io.StringIO()

        self.output = io.StringIO()

        self.stack_size: int = 0
        self.string_amount: int = 0
        self.vars: list = []

    # Expr visitors
    def visit_expr_int_lit(self, expr_int_lit: NodeExprIntLit):
        self.text.write(f"    mov rax, {expr_int_lit.int_lit.Value}\n")
        self.push("rax")

    def visit_expr_float_lit(self, expr_float_lit: NodeExprFloatLit):
        ... # TODO VISIT_EXPR_FLOAT_LIT

    def visit_expr_char_let(self, expr_char_lit: NodeExprCharLit):
        ... # TODO VISIT_EXPR_CHAR_LIT

    def visit_expr_str_lit(self, expr_str_lit: NodeExprStrLit):
        string_value = expr_str_lit.str_lit.Value
        label = f"string_{self.string_amount}"
        self.string_amount += 1

        self.data.write(f'    {label} db "{string_value}", 0xa, 0\n')
        self.text.write(f"    lea rax, [{label}]\n")
        self.push("rax")

    def visit_expr_bool_lit(self, expr_bool_lit: NodeExprBoolLit):
        if expr_bool_lit.bool_lit.Value == "True": psh: str = "1"
        else: psh: str = "0"
        self.text.write(f"    mov rax, {psh}\n")
        self.push("rax")

    def visit_expr_identifier(self, expr_identifier: NodeExprIdentifier):
        isin: bool = False
        for i in range(0, len(self.vars)):
            if expr_identifier.identifier.Value in self.vars[i]:
                isin = True
                var: Var = Var(i)
                offset: str = f"QWORD [rsp + {(self.stack_size - var.stackloc - 1) * 8}]"
                self.push(offset)
        if isin is False:
            raise ValueError(f"Undeclared Identifier: {expr_identifier.identifier.Value}")

    # Stmt visitors
    def visit_stmt_exit(self, stmt_exit: NodeStmtExit):
        self.gen_expr(stmt_exit.expr)
        self.text.write("    mov rax, 60\n")
        self.pop("rdi")
        self.text.write("    syscall\n\n")

    def visit_stmt_let(self, stmt_let: NodeStmtLet):
        if stmt_let.identifier.Value in self.vars:
            raise Exception(f"Identifier Already Used: {stmt_let.identifier.Value}")
        self.vars.append([stmt_let.identifier.Value,Var(stackloc= self.stack_size)])
        self.gen_expr(stmt_let.expr)

    def visit_stmt_print(self, stmt_print: NodeStmtPrint):
        self.gen_expr(stmt_print.expr)
        self.pop("rsi")

        self.text.write("    call length_function\n")

        self.text.write("    mov rax, 1\n")
        self.text.write("    mov rdi, 1\n")
        self.text.write("    syscall\n\n")

    # Visitor Dictionaries
    expr_visitor: dict = {
        'NodeExprIntLit': visit_expr_int_lit,
        'NodeExprStrLit': visit_expr_str_lit,
        'NodeExprBoolLit': visit_expr_bool_lit,
        'NodeExprIdentifier': visit_expr_identifier
    }

    stmt_visitor: dict = {
        'NodeStmtExit': visit_stmt_exit,
        'NodeStmtLet' : visit_stmt_let,
        'NodeStmtPrint' : visit_stmt_print
    }

    # Generators
    def gen_expr(self, expr: NodeExpr):
        self.expr_visitor[type(expr.var).__name__](self, expr.var)
    def gen_stmt(self, stmt: NodeStmt):
        self.stmt_visitor[type(stmt.var).__name__](self, stmt.var)
    def gen_prog(self) -> str:
        self.data.write("section .data\n")

        self.text.write("\nsection .text\n")
        self.text.write("    global _start\n\n")

        self.text.write("_start:\n")
        for stmt in self.program.stmts:
            self.gen_stmt(stmt)

        self.text.write("    mov rax, 60\n")
        self.text.write("    mov rdi, 0\n")
        self.text.write("    syscall\n\n")

        self.text.write("length_function:\n")
        self.text.write("    xor rdx, rdx\n")
        self.text.write("    mov rdx, 0\n\n")

        self.text.write("length_loop:\n")
        self.text.write("    cmp byte [rsi + rdx], 0\n")
        self.text.write("    je done_length\n")
        self.text.write("    inc rdx \n")
        self.text.write("    jmp length_loop\n\n")

        self.text.write("done_length:\n")
        self.text.write("    mov rax, rdx\n")
        self.text.write("    ret")

        self.output.write(self.data.getvalue())
        self.output.write(self.text.getvalue())

        return self.output.getvalue()

    # Push and Pop
    def push(self, reg: str):
        self.text.write(f"    push {reg}\n\n")
        self.stack_size += 1
    def pop(self, reg: str):
        self.text.write(f"    pop {reg}\n")
        self.stack_size -= 1
