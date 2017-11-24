.intel_syntax noprefix

.text
.globl syscall0, syscall1, syscall2, syscall3, syscall4, syscall5

syscall0:
    mov rax, rdi /* rax (syscall number) = function param 1 (rdi) */
    syscall        /* enter syscall */
    ret
 
syscall3:
    mov rax, rdi /* rax (syscall number) = function param 1 (rdi) */
    mov rdi, rsi /* rdi (syscall param 1) = func param 2 (rsi) */
    mov rsi, rdx /* rsi (syscall param 2) = func param 3 (rdx) */
    mov rdx, rcx /* rdx (syscall param 3) = func param 4 (rcx) */
    syscall        /* enter syscall */
    ret
