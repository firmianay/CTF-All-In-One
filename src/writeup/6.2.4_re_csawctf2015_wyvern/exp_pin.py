#!/usr/bin/env python

import os

def get_count(flag):
    cmd = "echo " + "\"" + flag + "\"" + " | ../../../pin -t obj-intel64/wyvern.so -o inscount.out -- ~/wyvern "
    os.system(cmd)
    with open("inscount.out") as f:
        count = int(f.read().split(" ")[1])
    return count

charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-+*'"

flag = list("A" * 28)
count = 0
for i in range(28):
    for c in charset:
        flag[i] = c
        # print("".join(flag))
        count = get_count("".join(flag))
        # print(count)
        if count == i+2:
            break
    if count == 29:
        break;
print("".join(flag))
