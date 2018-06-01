#!/usr/bin/env python

import os

def get_count(flag):
    os.system("../../../pin -t obj-intel64/dont_panic.so -o inscount.out -- ~/dont_panic " + "\"" + flag + "\"")
    with open("inscount.out") as f:
        count = int(f.read().split(" ")[1])
    return count

charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-+*'"

flag = list("hxp{aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa}")
count = 0
while count != 42:
    for i in range(4, 41):  # only compare "a" in "hex{}"
        for c in charset:
            flag[i] = c
            # print("".join(flag))
            count = get_count("".join(flag))
            if count == i+2:
                break
    print("".join(flag))
