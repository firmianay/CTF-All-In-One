#!/usr/bin/python

import tempfile
import os
import string
import random


def randstr():
    return ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(10))

code = "require 'LFA'\n"
code += "syscall 1, 1, \"hello\\n\", 6\n\n"

max = 600 # 600 linex should be more than enough ;)

print "Enter your code, enter the string END_OF_PWN to finish "

while max:

    new_code = raw_input("code> ")
    if new_code == "END_OF_PWN":
        break
    code += new_code + "\n"
    max -= 1

name = "/tmp/%s" % randstr()

with open(name, "w+") as f:
    f.write(code)

flag = open("flag", "r")

os.dup2(flag.fileno(), 1023)
flag.close()
cmd = "timeout 40 ruby %s" % name
os.system(cmd)


