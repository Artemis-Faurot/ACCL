section .data
    float_2: dq 1.5
    string_0 db "Hello, World!", 0xa, 0

section .text
    global _start

_start:
    mov rax, 10
    push rax

    mov rax, qword [float_2]
    push rax

    lea rax, [string_0]
    push rax

    push QWORD [rsp + 0]

    pop rsi
    call length_function
    mov rax, 1
    mov rdi, 1
    syscall

    push QWORD [rsp + 0]

    pop rsi
    call length_function
    mov rax, 1
    mov rdi, 1
    syscall

    mov rax, 0
    push rax

    mov rax, 60
    pop rdi
    syscall

    mov rax, 60
    mov rdi, 0
    syscall

length_function:
    xor rdx, rdx
    mov rdx, 0

length_loop:
    cmp byte [rsi + rdx], 0
    je done_length
    inc rdx 
    jmp length_loop

done_length:
    mov rax, rdx
    ret