#pragma once

#include <variant>
#include <type_traits>

#include "./tokenization.hpp"

namespace Node {
    struct ExprIntLit {
        Token int_lit;
    };

    struct ExprFloatLit {
        Token float_lit;
    };

    struct ExprStrLit {
        Token str_lit;
    };

    struct ExprBool {
        Token _bool;
    };

    struct ExprType {
        Token type;
    };

    struct ExprIdentifier {
        Token identifier;
    };

    struct Expr {
        std::variant<ExprIntLit, ExprFloatLit, ExprStrLit, ExprBool, ExprType, ExprIdentifier> var;
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
            return Node::Expr { .var = Node::ExprIntLit { .int_lit = consume() } };
        } else if (peek().has_value() && peek().value().type == TokenType::float_lit) {
            return Node::Expr { .var = Node::ExprFloatLit { .float_lit = consume() } };
        } else if (peek().has_value() && peek().value().type == TokenType::str_lit) {
            return Node::Expr { .var = Node::ExprStrLit { .str_lit = consume() } };
        } else if (peek().has_value() && peek().value().type == TokenType::_bool) {
            return Node::Expr { .var = Node::ExprBool { ._bool = consume() } };
        } else if (peek().has_value() && peek().value().type == TokenType::type) {
            return Node::Expr { .var = Node::ExprType { .type = consume() } };
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
            } else {
                consume();
            }

            std::optional<std::string> held_type;

            if (peek().has_value() && peek().value().type == TokenType::type) {
                held_type = peek().value().value;
                auto type = parse_expr();
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
                if (held_type == "int" && std::is_same<decltype(expr.value().var),  Node::ExprIntLit>::value ||
                    held_type == "float" && std::is_same<decltype(expr.value().var), Node::ExprFloatLit>::value ||
                    held_type == "str" && std::is_same<decltype(expr.value().var), Node::ExprStrLit>::value ||
                    held_type == "bool" && std::is_same<decltype(expr.value().var), Node::ExprBool>::value) {
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