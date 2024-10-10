#pragma once

#include <variant>

#include "./tokenization.hpp"

namespace Node {
    struct ExprIntLit {
        Token int_lit;
    };

    struct ExprStrLit {
        Token str_lit;
    };

    struct ExprType {
        Token type;
    };

    struct ExprIdent {
        Token ident;
    };

    struct Expr {
        std::variant<ExprIntLit, ExprStrLit, ExprType, ExprIdent> var;
    };

    struct StmtExit {
        Expr expr;
    };

    struct StmtLet {
        Token ident;
        Expr expr;
    };

    struct Stmt {
        std::variant<StmtExit, StmtLet> var;
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
            return Node::Expr { .var = Node::ExprIntLit { .int_lit = consume() } };
        } else if (peek().has_value() && peek().value().type == TokenType::str_lit) {
            return Node::Expr { .var = Node::ExprStrLit { .str_lit = consume() } };
        } else if (peek().has_value() && peek().value().type == TokenType::identifier) {
            return Node::Expr { .var = Node::ExprIdent { .ident = consume() } };
        } else if (peek().has_value() && peek().value().type == TokenType::type) {
            return Node::Expr { .var = Node::ExprType { .type = consume() } };
        } else {
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
        } else if (peek().has_value() && peek().value().type == TokenType::_let
                    && peek(1).has_value() && peek(1).value().type == TokenType::identifier
                    && peek(2).has_value() && peek(2).value().type == TokenType::colon
                    && peek(3).has_value() && peek(2).value().type == TokenType::type
                    && peek(4).has_value() && peek(4).value().type == TokenType::equals) {
            consume();
            
            Node::StmtLet stmt_let;
        }
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