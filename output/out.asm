section .data
    float_0 dq 1.5
    char_0 db "A", 0
    string_0 db "Hello, World!", 0
    print_0 db "10", 0xa, 0
    print_1 db "1.5", 0xa, 0
    print_2 db "A", 0xa, 0
    print_3 db "Hello, World!", 0xa, 0
    print_4 db "True", 0xa, 0
    print_5 db "", 0xa, 0
    print_6 db "16", 0xa, 0
    print_7 db "8.7", 0xa, 0
    print_8 db "E", 0xa, 0
    print_9 db "Beans", 0xa, 0
    print_10 db "False", 0xa, 0

section .text
    global _start

_start:
    mov rax, 10
    push rax

    mov rax, QWORD [float_0]
    sub rsp, 8
    mov QWORD [rsp], rax
    lea rax, [char_0]
    push rax

    lea rax, [string_0]
    push rax

    mov rax, 1
    push rax

    push QWORD [rsp + 32]

    lea rax, [print_0]
    push rax

    pop rsi
    call length_function
    mov rax, 1
    mov rdi, 1
    syscall

    push QWORD [rsp + 32]

    lea rax, [print_1]
    push rax

    pop rsi
    call length_function
    mov rax, 1
    mov rdi, 1
    syscall

    push QWORD [rsp + 32]

    lea rax, [print_2]
    push rax

    pop rsi
    call length_function
    mov rax, 1
    mov rdi, 1
    syscall

    push QWORD [rsp + 32]

    lea rax, [print_3]
    push rax

    pop rsi
    call length_function
    mov rax, 1
    mov rdi, 1
    syscall

    push QWORD [rsp + 32]

    lea rax, [print_4]
    push rax

    pop rsi
    call length_function
    mov rax, 1
    mov rdi, 1
    syscall

    lea rax, [print_5]
    push rax

    pop rsi
    call length_function
    mov rax, 1
    mov rdi, 1
    syscall

    lea rax, [print_6]
    push rax

    pop rsi
    call length_function
    mov rax, 1
    mov rdi, 1
    syscall

    lea rax, [print_7]
    push rax

    pop rsi
    call length_function
    mov rax, 1
    mov rdi, 1
    syscall

    lea rax, [print_8]
    push rax

    pop rsi
    call length_function
    mov rax, 1
    mov rdi, 1
    syscall

    lea rax, [print_9]
    push rax

    pop rsi
    call length_function
    mov rax, 1
    mov rdi, 1
    syscall

    lea rax, [print_10]
    push rax

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

