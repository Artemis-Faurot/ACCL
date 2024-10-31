from accl_parser import NodeProgram, NodeStmt, NodeExpr, NodeExprIntLit, NodeStmtExit, NodeStmtLet, NodeExprIdentifier, \
    NodeExprFloatLit, NodeExprCharLit, NodeExprStrLit, NodeExprFStrLit, NodeExprBoolLit, NodeStmtPrint
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
        self.float_amount: int = 0
        self.string_amount: int = 0
        self.fstring_amount: int = 0
        self.char_amount: int = 0
        self.vars: list = []
        self.var_values: list = []

        self.print_amount: int = 0
        self.hold_identifier_value = None

    # Expr visitors
    def visit_expr_int_lit(self, expr_int_lit: NodeExprIntLit):
        self.text.write(f"    mov rax, {expr_int_lit.int_lit.Value}\n")
        self.push("rax")
    def visit_expr_float_lit(self, expr_float_lit: NodeExprFloatLit):
        label = f"float_{self.float_amount}"
        self.float_amount += 1

        self.data.write(f"    {label} dq {expr_float_lit.float_lit.Value}\n")
        self.text.write(f"    mov rax, QWORD [{label}]\n")
        self.push_float("rax")
    def visit_expr_char_lit(self, expr_char_lit: NodeExprCharLit):
        char_value = expr_char_lit.char_lit.Value
        label = f"char_{self.char_amount}"
        self.char_amount += 1

        self.data.write(f'    {label} db "{char_value}", 0\n')
        self.text.write(f"    lea rax, [{label}]\n")
        self.push("rax")
    def visit_expr_str_lit(self, expr_str_lit: NodeExprStrLit):
        label = f"string_{self.string_amount}"
        self.string_amount += 1
        string_list = list(expr_str_lit.str_lit.Value)
        value_list = []
        a = i = 0
        if '\\' in string_list:
            while i <= len(string_list):
                try:
                    if string_list[i] == '\\' and string_list[i+1] == 'n':
                        del string_list[i]
                        del string_list[i]
                        value_list.append(''.join(string_list[a:i]))
                        a = i
                        i -= 1
                except:
                    value_list.append(''.join(string_list[a:i]))
                    break
                i += 1
        else:
            value_list.append(''.join(string_list))

        self.data.write(f'    {label} db ')
        for value in value_list:
            self.data.write(f'"{value}", 0xa,')
        self.data.write(" 0\n")
        self.text.write(f"    lea rax, [{label}]\n")
        self.push("rax")
    def visit_expr_fstr_lit(self, expr_fstr_lit: NodeExprFStrLit):
        label = f"string_{self.fstring_amount}"
        self.fstring_amount += 1
        fstring_list = list(expr_fstr_lit.fstr_lit.Value)
        new_string_list = []

        if '{' in fstring_list:
            pass # TODO VISIT_EXPR_FSTR_LIT
        else:
            for i in range(0, len(fstring_list)):
                new_string_list.append(fstring_list[i])

        value_list = []
        a = i = 0
        if '\\' in new_string_list:
            while i <= len(new_string_list):
                try:
                    if new_string_list[i] == '\\' and new_string_list[i + 1] == 'n':
                        del new_string_list[i]
                        del new_string_list[i]
                        value_list.append(''.join(new_string_list[a:i]))
                        a = i
                        i -= 1
                except:
                    value_list.append(''.join(new_string_list[a:i]))
                    break
                i += 1
        else:
            value_list.append(''.join(new_string_list))

        self.data.write(f'    {label} db ')
        for value in value_list:
            self.data.write(f'"{value}", 0xa,')
        self.data.write(" 0\n")
        self.text.write(f"    lea rax, [{label}]\n")
        self.push("rax")
    def visit_expr_bool_lit(self, expr_bool_lit: NodeExprBoolLit):
        if expr_bool_lit.bool_lit.Value == "True": psh: str = "1"
        else: psh: str = "0"
        self.text.write(f"    mov rax, {psh}\n")
        self.push("rax")
    def visit_expr_identifier(self, expr_identifier: NodeExprIdentifier) -> str or None: # type: ignore
        isin: bool = False
        for i in range(0, len(self.vars)):
            if expr_identifier.identifier.Value in self.vars[i]:
                isin = True
                var: Var = Var(i)
                offset: str = f"QWORD [rsp + {(self.stack_size - var.stackloc - 1) * 8}]"
                self.push(offset)
                return self.var_values[i]
        if isin is False:
            raise ValueError(f"Undeclared Identifier: {expr_identifier.identifier.Value}")

    # Stmt visitors
    def visit_stmt_exit(self, stmt_exit: NodeStmtExit):
        self.gen_expr(stmt_exit.expr)
        self.text.write("    mov rax, 60\n")
        self.pop("rdi")
        self.text.write("    syscall\n\n")
    def visit_stmt_let(self, stmt_let: NodeStmtLet):
        expr_type = type(stmt_let.expr.var).__name__
        for i in range(0, len(self.vars)):
            if stmt_let.identifier.Value in self.vars[i]: raise Exception(f"Identifier Already Used: {stmt_let.identifier.Value}")
        self.vars.append([stmt_let.identifier.Value,Var(stackloc= self.stack_size)])
        if expr_type == 'NodeExprIntLit': self.var_values.append(stmt_let.expr.var.int_lit.Value)
        elif expr_type == 'NodeExprFloatLit': self.var_values.append(stmt_let.expr.var.float_lit.Value)
        elif expr_type == 'NodeExprCharLit': self.var_values.append(stmt_let.expr.var.char_lit.Value)
        elif expr_type == 'NodeExprStrLit': self.var_values.append(stmt_let.expr.var.str_lit.Value)
        elif expr_type == 'NodeExprBoolLit': self.var_values.append(stmt_let.expr.var.bool_lit.Value)
        elif expr_type == 'NodeExprIdentifier':
            value: str = self.visit_expr_identifier(stmt_let.expr.var)
            self.var_values.append(value)
        self.gen_expr(stmt_let.expr)
    def visit_stmt_print(self, stmt_print: NodeStmtPrint):
        expr_type = type(stmt_print.expr.var).__name__
        label = f"print_{self.print_amount}"
        self.print_amount += 1

        if expr_type == 'NodeExprIntLit':
            int_value = stmt_print.expr.var.int_lit.Value

            self.data.write(f'    {label} db "{int_value}", 0xa, 0\n')
            self.text.write(f"    lea rax, [{label}]\n")
            self.push("rax")
        elif expr_type == 'NodeExprFloatLit':
            float_value = stmt_print.expr.var.float_lit.Value

            self.data.write(f'    {label} db "{float_value}", 0xa, 0\n')
            self.text.write(f"    lea rax, [{label}]\n")
            self.push("rax")
        elif expr_type == 'NodeExprCharLit':
            char_value = stmt_print.expr.var.char_lit.Value

            self.data.write(f'    {label} db "{char_value}", 0xa, 0\n')
            self.text.write(f"    lea rax, [{label}]\n")
            self.push("rax")
        elif expr_type == 'NodeExprStrLit':
            string_list = list(stmt_print.expr.var.str_lit.Value)
            value_list = []
            a = i = 0
            if '\\' in string_list:
                while i <= len(string_list):
                    try:
                        if string_list[i] == '\\' and string_list[i + 1] == 'n':
                            del string_list[i]
                            del string_list[i]
                            value_list.append(''.join(string_list[a:i]))
                            a = i
                            i -= 1
                    except:
                        value_list.append(''.join(string_list[a:i]))
                        break
                    i += 1
            else:
                value_list.append(''.join(string_list))

            self.data.write(f'    {label} db ')
            for value in value_list:
                self.data.write(f'"{value}", 0xa,')
            self.data.write(" 0\n")
            self.text.write(f"    lea rax, [{label}]\n")
            self.push("rax")
        elif expr_type == 'NodeExprFStrLit':
            pass # TODO PRINT FSTRING
        elif expr_type == 'NodeExprBoolLit':
            bool_value = stmt_print.expr.var.bool_lit.Value

            self.data.write(f'    {label} db "{bool_value}", 0xa, 0\n')
            self.text.write(f"    lea rax, [{label}]\n")
            self.push("rax")
        elif expr_type == 'NodeExprIdentifier':
            identifier_list = list(self.visit_expr_identifier(stmt_print.expr.var))
            newline_amount = 0
            value_list = []
            a = i = 0
            if '\\' in identifier_list:
                while i <= len(identifier_list):
                    try:
                        if identifier_list[i] == '\\' and identifier_list[i+1] == 'n':
                            del identifier_list[i]
                            del identifier_list[i]
                            value_list.append(''.join(identifier_list[a:i]))
                            newline_amount += 1
                            a = i
                            i -= 1
                    except:
                        value_list.append(''.join(identifier_list[a:i]))
                        break
                    i += 1
            else:
                value_list.append(''.join(identifier_list))

            self.data.write(f'    {label} db ')
            for value in value_list:
                self.data.write(f'"{value}", 0xa,')
                newline_amount -= 1
            for i in range(0, newline_amount):
                self.data.write(' 0xa,')
            self.data.write(" 0\n")
            self.text.write(f"    lea rax, [{label}]\n")
            self.push("rax")
        self.pop("rsi")

        self.text.write("    call length_function\n")
        self.text.write("    mov rax, 1\n")
        self.text.write("    mov rdi, 1\n")
        self.text.write("    syscall\n\n")

    # Visitor Dictionaries
    expr_visitor: dict = {
        'NodeExprIntLit': visit_expr_int_lit,
        'NodeExprFloatLit': visit_expr_float_lit,
        'NodeExprCharLit': visit_expr_char_lit,
        'NodeExprStrLit': visit_expr_str_lit,
        'NodeExprFStrLit': visit_expr_fstr_lit,
        'NodeExprBoolLit': visit_expr_bool_lit,
        'NodeExprIdentifier': visit_expr_identifier
    }

    stmt_visitor: dict = {
        'NodeStmtExit': visit_stmt_exit,
        'NodeStmtLet': visit_stmt_let,
        'NodeStmtPrint': visit_stmt_print
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

        self.vars.append(["EXIT_SUCCESS", Var(stackloc=self.stack_size)])
        self.var_values.append("0")
        self.text.write("    mov rax, 0\n")
        self.push("rax")

        self.vars.append(["EXIT_FAILURE", Var(stackloc=self.stack_size)])
        self.var_values.append("1")
        self.text.write("    mov rax, 1\n")
        self.push("rax")

        for stmt in self.program.stmts:
            self.gen_stmt(stmt)

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
        self.text.write("    ret\n\n")

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
    def push_float(self, reg: str):
        self.text.write(f"    sub rsp, 8\n")
        self.text.write(f"    mov QWORD [rsp], {reg}\n")
        self.stack_size += 1
