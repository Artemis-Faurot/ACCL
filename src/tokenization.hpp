#pragma once

#include <iostream>
#include <vector>
#include <optional>

enum class TokenType { _exit, _return, _let, _const, _class, _enum, _struct, int_lit, str_lit, identifier, type, _bool, equals, colon, semicolon, openparen, closeparen };

struct Token {
    TokenType type;
    std::optional<std::string> value {};
};

class Tokenizer {
public:
    inline explicit Tokenizer(const std::string& src)
        : m_src(std::move(src))
    {
        
    }

    inline std::vector<Token> tokenize() {
        std::vector<Token> tokens;
        std::string buffer;
        while (peek().has_value()) {
            if (std::isalpha(peek().value())) {
                buffer.push_back(consume());
                while (peek().has_value() && std::isalnum(peek().value())) {
                    buffer.push_back(consume());
                }
                if (buffer == "exit") {
                    tokens.push_back({ .type = TokenType::_exit });
                    buffer.clear();
                    continue;
                } else if (buffer == "return") {
                    tokens.push_back({ .type = TokenType::_return });
                    buffer.clear();
                    continue;
                } else if (buffer == "let") {
                    tokens.push_back({ .type = TokenType::_let });
                    buffer.clear();
                    continue;
                } else if (buffer == "const") {
                    tokens.push_back({ .type = TokenType::_const });
                    buffer.clear();
                    continue;
                } else if (buffer == "class") {
                    tokens.push_back({ .type = TokenType::_class });
                    buffer.clear();
                    continue;
                } else if (buffer == "enum") {
                    tokens.push_back({ .type = TokenType::_enum });
                    buffer.clear();
                    continue;
                } else if (buffer == "struct") {
                    tokens.push_back({ .type = TokenType::_struct });
                    buffer.clear();
                    continue;
                } else if (buffer == "int" || buffer == "float" || buffer == "char" || buffer == "str" || buffer == "bool") {
                    tokens.push_back({ .type = TokenType::type, .value = buffer });
                    buffer.clear();
                    continue;
                } else if (buffer == "true" || buffer == "false") {
                    tokens.push_back({ .type = TokenType::_bool, .value = buffer});
                    buffer.clear();
                    continue;
                } else {
                    tokens.push_back({ .type = TokenType::identifier, .value = buffer });
                    buffer.clear();
                    continue;
                }
            } else if (std::isdigit(peek().value())) {
                buffer.push_back(consume());
                while (peek().has_value() && std::isdigit(peek().value())) {
                    buffer.push_back(consume());
                }
                tokens.push_back({ .type = TokenType::int_lit, .value = buffer });
                buffer.clear();
                continue;
            } else if (peek().value() == ';') {
                consume();
                tokens.push_back({ .type = TokenType::semicolon });
                continue;
            } else if (peek().value() == ':') {
                consume();
                tokens.push_back({ .type = TokenType::colon });
                continue;
            } else if (std::isspace(peek().value())) {
                consume();
                continue;
            } else if (peek().value() == '(') {
                consume();
                tokens.push_back({ .type = TokenType::openparen });
                continue;
            } else if (peek().value() == ')') {
                consume();
                tokens.push_back({ .type = TokenType::closeparen });
                continue;
            } else if (peek().value() == '=') {
                consume();
                tokens.push_back({ .type = TokenType::equals });
                continue;
            } else if (peek().value() == '"' || peek().value() == '\'') {
                consume();
                while (peek().has_value() && peek().value() != '"' || peek().has_value() && peek().value() != '\'') {
                    buffer.push_back(consume());
                }
                if (peek().value() == '"' || peek().value() == '\'') {
                    consume();
                } else {
                    std::cerr << "Missing quote at the end of string literal" << std::endl;
                    exit(EXIT_FAILURE);
                }
                tokens.push_back({ .type = TokenType::str_lit, .value = buffer });
                buffer.clear();
                continue;
            } else {
                std::cerr << "Unrecognized character found while lexing: " << peek().value() << std::endl;
                exit(EXIT_FAILURE);
            }
        }
        m_index = 0;
        return tokens;
    }
private:
    [[nodiscard]] std::optional<char> peek(int offset = 0) const {
        if (m_index + offset >= m_src.length()) {
            return {};
        } else {
            return m_src.at(m_index + offset);
        }
    }

    inline char consume() {
        return m_src.at(m_index++);
    }

    const std::string m_src;
    size_t m_index = 0;
};