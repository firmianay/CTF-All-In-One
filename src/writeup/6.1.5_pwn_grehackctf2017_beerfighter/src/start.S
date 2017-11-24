.intel_syntax noprefix

.text
.globl _start

_start:
xor rbp, rbp /* rbp = 0 */
pop rdi /* rdi = argc */
mov rsi, rsp /*rsi = (char*) argv[] */
and rsp, -16 /* last 4 bytes of rsp to 0 */

call main

mov rdi, rax /* syscall param 1 = return value of main */
mov rax, 60 /* SYS_exit */
syscall

ret
