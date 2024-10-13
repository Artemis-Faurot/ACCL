#pragma once

#include <iostream>
#include <vector>
#include <optional>

enum class TokenType { 
    _exit,
    _let, 
    int_lit,
    identifier, 
    type, 
    equals, 
    colon, 
    semicolon, 
    openparen, 
    closeparen 
};

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
            if (std::isalpha(peek().value()) || peek().value() == '_') {
                buffer.push_back(consume());
                while (peek().has_value() && std::isalnum(peek().value()) ||
                        peek().has_value() && peek().value() == '_') {
                    buffer.push_back(consume());
                }
                if (buffer == "exit") {
                    tokens.push_back({ .type = TokenType::_exit });
                    buffer.clear();
                    continue;
                } else if (buffer == "let") {
                    tokens.push_back({ .type = TokenType::_let });
                    buffer.clear();
                    continue;
                } else if (buffer == "int" || buffer == "float" || buffer == "char" || buffer == "str" || buffer == "bool") {
                    tokens.push_back({ .type = TokenType::type, .value = buffer });
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
            } else {
                std::cerr << "Found unrecognized character while lexing" << std::endl;
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