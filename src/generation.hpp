#pragma once

#include "./parser.hpp"
#include <iostream>
#include <unordered_map>

class Generator {
public:
    inline explicit Generator(Node::Program program)
        : m_program(std::move(program))
    {}

    void gen_expr(const Node::Expr& expr) {
        struct ExprVisitor {
            Generator* gen;
            void operator()(const Node::ExprIntLit& expr_int_lit) const {
                gen->m_output << "    mov rbx, " << expr_int_lit.int_lit.value.value() << "\n";
                gen->push("rbx");
            }

            void operator()(const Node::ExprIdentifier& expr_identifier) const {
                if(gen->m_vars.find(expr_identifier.identifier.value.value()) == gen->m_vars.end()) {
                    std::cerr << "Undeclared identifier: " << expr_identifier.identifier.value.value() << std::endl;
                    exit(EXIT_FAILURE);
                }
                const auto& var = gen->m_vars.at(expr_identifier.identifier.value.value());
                std::stringstream offset;
                offset << "QWORD [rsp + " << (gen->m_stack_size - var.stack_loc - 1) * 8 << "]";
                gen->push(offset.str());
            }
        };

        ExprVisitor visitor { .gen = this };
        std::visit(visitor, expr.var);
    }

    void gen_stmt(const Node::Stmt& stmt) {
        struct StmtVisitor {
            Generator* gen;
            void operator()(const Node::StmtExit& stmt_exit) const {
                gen->gen_expr(stmt_exit.expr);
                gen->m_output << "    mov rax, 1\n";
                gen->pop("rbx");
                gen->m_output << "    int 0x80\n\n";
            }

            void operator()(const Node::StmtLet& stmt_let) const {
                if (gen->m_vars.find(stmt_let.ident.value.value()) != gen->m_vars.end()) {
                    std::cerr << "Identifier already used: " << stmt_let.ident.value.value() << std::endl;
                    exit(EXIT_FAILURE);
                }

                gen->m_vars.insert({ stmt_let.ident.value.value(), var { .stack_loc = gen->m_stack_size } });
                gen->gen_expr(stmt_let.expr);
            }
        };

        StmtVisitor visitor { .gen = this };
        std::visit(visitor, stmt.var);
    }

    [[nodiscard]] std::string gen_prog() {
        m_output << "section .text\n";
        m_output << "    global _start\n\n";

        m_output << "_start:\n";
        for(const Node::Stmt& stmt : m_program.stmts) {
            gen_stmt(stmt);
        }

        m_output << "    mov rax, 1\n";
        m_output << "    mov rbx, 0\n";
        m_output << "    int 0x80\n\n";
        return m_output.str();
    }

private:
    void push(const std::string& reg) {
        m_output << "    push " << reg << "\n\n";
        m_stack_size++;
    }

    void pop(const std::string& reg) {
        m_output << "    pop " << reg << "\n";
        m_stack_size--;
    }

    struct var {
        size_t stack_loc;
    };

    const Node::Program m_program;
    std::stringstream m_output;
    size_t m_stack_size = 0;
    std::unordered_map<std::string, var> m_vars {};
};