#!/usr/bin/env python

#HXP CTF 2017 - dont_panic 100 pts
#Writeup link : https://rce4fun.blogspot.com/2017/11/hxp-ctf-2017-dontpanic-reversing-100.html
#Souhail Hammou
import gdb

CHAR_SUCCESS = 0x47B976
NOPE = 0x47BA23
gdb.execute("set pagination off")
gdb.execute("b*0x47B976") #Success for a given character
gdb.execute("b*0x47BA23") #Block displaying "Nope"
charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-+*{}'"
flag = list('A'*42) #junk
for i in range(0,len(flag)) :
	for c in charset:
		flag[i] = c
		# the number of times we need to hit the
		# success bp for the previous correct characters
		success_hits = i
		gdb.execute("r " + '"' + "".join(flag) + '"')
		while success_hits > 0 :
			gdb.execute('c')
			success_hits -= 1
		#we break either on success or on fail
		rip = int(gdb.parse_and_eval("$rip"))
		if rip == CHAR_SUCCESS:
			break #right one. To the next character
		if rip == NOPE: #added for clarity
			continue
print("".join(flag))
#flag : hxp{k3eP_C4lM_AnD_D0n't_P4n1c__G0_i5_S4F3}
