#pragma once

#include "./parser.hpp"
#include <iostream>
#include <string>

class Generator {
public:
    inline Generator(NodeExit root):
        m_root(std::move(root))
    {

    }

    [[nodiscard]] std::string generate() const {
        std::stringstream output;
        output << "section .text\n";
        output << "    global _start\n\n";

        output << "_start:\n";
        output << "    mov rax, 1\n";
        output << "    mov rbx, " << m_root.expr.int_lit.value.value() << "\n";
        output << "    int 0x80";
        return output.str();
    }

private:
    const NodeExit m_root;

};