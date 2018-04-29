.data

msg:
    .ascii "Hello 64-bit!\n"
    len = . - msg

.text
    .global _start

_start:
    movq  $1, %rdi
    movq  $msg, %rsi
    movq  $len, %rdx
    movq  $1, %rax
    syscall

    xorq  %rdi, %rdi
    movq  $60, %rax
    syscall
