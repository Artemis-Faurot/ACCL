#pragma once

#include <variant>

#include "./tokenization.hpp"

namespace Node {
    struct Expr {
        std::optional<Token> int_lit;
        std::optional<Token> float_lit;
        std::optional<Token> str_lit;
        std::optional<Token> _bool;
        std::optional<Token> type;
        std::optional<Token> ident;
    };

    struct StmtExit {
        Expr expr;
    };

    struct StmtLet {
        Token ident;
        Expr type;
        Expr expr;
    };

    struct StmtDef {
        Token ident;
        std::vector<Expr> exprs;
        Expr type;
        std::vector<Stmt> stmts;
    };

    struct Stmt {
        std::variant<StmtExit, StmtLet, StmtDef> var;
    };

    struct Program {
        std::vector<Stmt> stmts;
    };
}

class Parser {
public:
    inline explicit Parser(std::vector<Token> tokens):
        m_tokens(std::move(tokens))
    {

    }

    std::optional<Node::Expr> parse_expr() {
        if (peek().has_value() && peek().value().type == TokenType::int_lit) {
            return Node::Expr { .int_lit = consume() };
        } else if (peek().has_value() && peek().value().type == TokenType::float_lit) {
            return Node::Expr { .float_lit = consume() };
        } else if (peek().has_value() && peek().value().type == TokenType::str_lit) {
            return Node::Expr { .str_lit = consume() };
        } else if (peek().has_value() && peek().value().type == TokenType::_bool) {
            return Node::Expr { ._bool = consume() };
        } else if (peek().has_value() && peek().value().type == TokenType::type) {
            return Node::Expr { .type = consume() };
        } else if (peek().has_value() && peek().value().type == TokenType::identifier) {
            return Node::Expr { .ident = consume() };
        }  else {
            return {};
        }
    }

    std::optional<Node::Stmt> parse_stmt() {
        if (peek().has_value() && peek().value().type == TokenType::_exit) {
            consume();
            Node::StmtExit stmt_exit;
            if (auto node_expr = parse_expr()) {
                stmt_exit = { .expr = node_expr.value() };
            } else {
                std::cerr << "Invalid Expression" << std::endl;
                exit(EXIT_FAILURE);
            }

            if (peek().has_value() || peek().value().type == TokenType::semicolon) {
                consume();
            } else {
                std::cerr << "Expected ';' after exit statement" << std::endl;
                exit(EXIT_FAILURE);
            }

            return Node::Stmt { .var = stmt_exit };
        } else if (peek().has_value() && peek().value().type == TokenType::_let) {
            consume();
            Node::StmtLet stmt_let;
            if (peek().has_value() && peek().value().type == TokenType::identifier) {
                stmt_let = Node::StmtLet { .ident = consume() };
            } else {
                std::cerr << "Expected an identifier after let declaration" << std::endl;
                exit(EXIT_FAILURE);
            }

            if (!peek().has_value() || peek().value().type != TokenType::colon) {
                std::cerr << "Expected a colon to type the identifier" << std::endl;
                exit(EXIT_FAILURE);
            } else {
                consume();
            }

            std::optional<std::string> held_type;

            if (peek().has_value() && peek().value().type == TokenType::type) {
                auto type = parse_expr();
                held_type = type.value().type.value().value;
                stmt_let = Node::StmtLet { .ident = stmt_let.ident, .type = type.value() };
            } else {
                std::cerr << "Expected a type identifier" << std::endl;
                exit(EXIT_FAILURE);
            }

            if (!peek().has_value() || peek().value().type != TokenType::equals) {
                std::cerr << "Expected a = to set variable" << std::endl;
                exit(EXIT_FAILURE);
            } else {
                consume();
            }

            if (peek().has_value()) {
                auto expr = parse_expr();
                if (held_type == "int" && expr.value().int_lit ||
                    held_type == "float" && expr.value().float_lit ||
                    held_type == "str" && expr.value().str_lit ||
                    held_type == "bool" && expr.value()._bool) {
                    stmt_let.expr = expr.value();
                } else {
                    std::cerr << "Data type mismatch on variable declaration" << std::endl;
                    exit(EXIT_FAILURE);
                }
            } else {
                std::cerr << "Invalid expression" << std::endl;
                exit(EXIT_FAILURE);
            }

            if (!peek().has_value() || peek().value().type != TokenType::semicolon) {
                std::cerr << "Expected a semicolon after expression" << std::endl;
                exit(EXIT_FAILURE);
            } else {
                consume();
            }

            return Node::Stmt { .var = stmt_let };
        } else {
            return {};
        }
    }

    std::optional<Node::Program> parse_prog() {
        Node::Program program;
        while (peek().has_value()) {
            if (auto stmt = parse_stmt()) {
                program.stmts.push_back(stmt.value());
            } else {
                std::cerr << "Invalid statement" << std::endl;
                exit(EXIT_FAILURE);
            }
        }
        return program;
    }

private:
    [[nodiscard]] std::optional<Token> peek(int offset = 0) const {
        if (m_index + offset >= m_tokens.size()) {
            return {};
        } else {
            return m_tokens.at(m_index + offset);
        }
    }

    inline Token consume() {
        return m_tokens.at(m_index++);
    }

    const std::vector<Token> m_tokens;
    size_t m_index = 0;
};