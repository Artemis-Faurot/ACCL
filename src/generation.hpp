#pragma once

#include "./parser.hpp"
#include <iostream>
#include <string>

class Generator {
public:
    inline Generator(Node::Program program):
        m_program(std::move(program))
    {

    }

    [[nodiscard]] std::string gen_program() const {
        std::stringstream output;
        std::stringstream text;
        std::stringstream read;
        std::stringstream bss;
        text << "section .text\n";
        text << "    global _start\n\n";

        text << "_start:\n";

        for (const Node::Stmt& stmt : m_program.stmts) {
            
        }

        text << "    mov rax, 1\n";
        text << "    mov rbx, 0\n";
        text << "    int 0x80";
        return output.str();
    }

private:
    const Node::Program m_program;

};