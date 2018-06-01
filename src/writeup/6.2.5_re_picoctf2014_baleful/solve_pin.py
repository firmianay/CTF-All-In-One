#!/usr/bin/env python

import os

def get_count(flag):
    cmd = "echo " + "\"" + flag + "\"" + " | ../../../pin -t obj-ia32/inscount0.so -o inscount.out -- ~/baleful_unpack"
    os.system(cmd)
    with open("inscount.out") as f:
        count = int(f.read().split(" ")[1])
    return count

charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-+*'"

flag = list("A" * 30)
p_count = get_count("".join(flag))
for i in range(30):
    for c in charset:
        flag[i] = c
        print("".join(flag))
        count = get_count("".join(flag))
        print("count: ", count)
        if count != p_count:
            break
    p_count = count
print("password: ", "".join(flag))
