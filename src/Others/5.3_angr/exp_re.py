from __future__ import print_function
str_list = ["Dufhbmf", "pG`imos", "ewUglpt"]
passwd = []
for i in range(12):
    passwd.append(chr(ord(str_list[i % 3][2 * (i / 3)]) - 1))
print(''.join(passwd))
