section .text
    global _start

_start:
    mov rax, 1
    mov rbx, 25
    int 0x80