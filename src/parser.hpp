#pragma once

#include <variant>
#include <type_traits>

#include "./tokenization.hpp"

namespace Node {
    struct ExprIntLit {
        Token int_lit;
    };

    struct ExprIdentifier {
        Token identifier;
    };

    struct Expr {
        std::variant<ExprIntLit, ExprIdentifier> var;
    };

    struct StmtExit {
        Expr expr;
    };

    struct StmtLet {
        Token ident;
        Token type;
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
        } else if (peek().has_value() && peek().value().type == TokenType::identifier) {
            return Node::Expr { .var = Node::ExprIdentifier { .identifier = consume() } };
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
            } consume();

            std::optional<std::string> held_type;

            if (peek().has_value() && peek().value().type == TokenType::type) {
                held_type = peek().value().value;
                stmt_let = Node::StmtLet { .ident = stmt_let.ident, .type = consume() };
            } else {
                std::cerr << "Expected a type identifier" << std::endl;
                exit(EXIT_FAILURE);
            }

            if (!peek().has_value() || peek().value().type != TokenType::equals) {
                std::cerr << "Expected a = to set variable" << std::endl;
                exit(EXIT_FAILURE);
            } consume();

            if (peek().has_value()) {
                auto expr = parse_expr();
                if (held_type == "int" && std::holds_alternative<Node::ExprIntLit>(expr.value().var)) {
                    stmt_let.expr = expr.value();
                } else {
                    std::cerr << "Data type mismatch on variable declaration" << std::endl;
                    exit(EXIT_FAILURE);
                }
            } else {
                std::cerr << "Expected value to be assigned to the variable" << std::endl;
                exit(EXIT_FAILURE);
            }

            if (!peek().has_value() || peek().value().type != TokenType::semicolon) {
                std::cerr << "Expected a semicolon to end let statement" << std::endl;
                exit(EXIT_FAILURE);
            } consume();

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