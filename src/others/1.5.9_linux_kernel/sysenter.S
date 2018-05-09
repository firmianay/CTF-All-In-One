.data

msg:
    .ascii "Hello sysenter!\n"
    len = . - msg

.text
    .globl _start

_start:
    movl $len, %edx
    movl $msg, %ecx
    movl $1, %ebx
    movl $4, %eax

    pushl $sysenter_ret
    pushl %ecx
    pushl %edx
    pushl %ebp
    movl %esp, %ebp
    sysenter

sysenter_ret:    
    movl $0, %ebx
    movl $1, %eax

    pushl $sysenter_ret
    pushl %ecx
    pushl %edx
    pushl %ebp
    movl %esp, %ebp
    sysenter
