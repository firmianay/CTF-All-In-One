#!/usr/bin/env python

import os

def get_count(flag):
    cmd = "echo " + "\"" + flag + "\"" + " | ../../../pin -t obj-ia32/inscount0.so -o inscount.out -- ~/baleful_unpack"
    os.system(cmd)
    with open("inscount.out") as f:
        count = int(f.read().split(" ")[1])
    return count

flag = "A"
p_count = get_count(flag)
for i in range(50):
    flag += "A"
    count = get_count(flag)
    print("count: ", count)
    diff = count - p_count
    print("diff: ", diff)
    if diff != 794:
        break
    p_count = count
print("length of password: ", len(flag))
