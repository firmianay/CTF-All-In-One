# CTF-All-In-One（CTF 从入门到放弃）

*——“与其相信谣言，不如一直学习。”*

*GitHub 地址：https://github.com/firmianay/CTF-All-In-One*

*GitBook 地址：https://www.gitbook.com/book/firmianay/ctf-all-in-one/details*

---

- [前言](doc/0_preface.md)

- [一、基础知识篇](doc/1_basic.md)
  - [1.1 CTF 简介](doc/1.1_ctf.md)
  - [1.2 学习方法](doc/1.2_how_to_learn.md)
  - [1.3 Linux 基础](doc/1.3_linux_basic.md)
  - [1.4 Web 安全基础](doc/1.4_web_basic.md)
    - [1.4.1 HTML基础](doc/1.4.1_html_basic.md)
    - [1.4.2 HTTP协议基础](doc/1.4.2_http_basic.md)
    - [1.4.3 JavaScript基础](doc/1.4.3_javascript_basic.md)
    - [1.4.4 常见Web服务器基础](doc/1.4.4_webserver_basic.md)
    - [1.4.5 OWASP Top Ten Project漏洞基础](doc/1.4.5_owasp_basic.md)
    - [1.4.6 PHP源码审计基础](doc/1.4.6_php_basic.md)
  - [1.5 逆向工程基础](doc/1.5_reverse_basic.md)
    - [1.5.1 C 语言基础](doc/1.5.1_c_basic.md)
    - [1.5.2 x86/x86-64 汇编基础](doc/1.5.2_x86&x64.md)
    - [1.5.3 Linux ELF](doc/1.5.3_elf.md)
    - [1.5.4 Windows PE](doc/1.5.4_pe.md)
    - [1.5.5 静态链接](doc/1.5.5_static_link.md)
    - [1.5.6 动态链接](doc/1.5.6_dynamic_link.md)
    - [1.5.7 内存管理](doc/1.5.7_memory.md)
    - [1.5.8 glibc malloc](doc/1.5.8_glibc_malloc.md)
  - [1.6 密码学基础](doc/1.6_crypto_basic.md)
    - [1.6.1 初等数论](doc/1.6.1_number_theory.md)
    - [1.6.2 近世代数](doc/1.6.2_modern_algebra.md)
    - [1.6.3 流密码](doc/1.6.3_stream_cipher.md)
    - [1.6.4 分组密码](doc/1.6.4_block_cipher.md)
    - [1.6.5 公钥密码](doc/1.6.5_public-key_crypto.md)
    - [1.6.6 哈希函数](doc/1.6.6_hash.md)
    - [1.6.7 数字签名](doc/1.6.7_digital_signature.md)
  - [1.7 Android 安全基础](doc/1.7_android_basic.md)
    - [1.7.1 Android 环境搭建](doc/1.7.1_android_env.md)
    - [1.7.2 Dalvik 指令集](doc/1.7.2_dalvik.md)
    - [1.7.3 ARM 汇编基础](doc/1.7.3_arm.md)
    - [1.7.4 Android 常用工具](doc/1.7.4_android_tools.md)

- [二、工具篇](doc/2_tools.md)
  - [2.1 VM](doc/2.1_vm.md)
  - [2.2 gdb/peda](doc/2.2_gdb.md)
  - [2.3 ollydbg](doc/2.3_ollydbg.md)
  - [2.4 windbg](doc/2.4_windbg.md)
  - [2.5 radare2](doc/2.5_radare2.md)
  - [2.6 IDA Pro](doc/2.6_idapro.md)
  - [2.7 pwntools](doc/2.7_pwntools.md)
  - [2.8 zio](doc/2.8_zio.md)
  - [2.9 JEB](doc/2.9_jeb.md)
  - [2.10 metasploit](doc/2.10_metasploit.md)
  - [2.11 binwalk](doc/2.11_binwalk.md)
  - [2.12 Burp Suite](doc/2.12_burpsuite.md)

- [三、分类专题篇](doc/3_topics.md)
  - [3.1 Reverse](doc/3.1_reverse.md)
  - [3.2 Crypto](doc/3.2_crypto.md)
    - [3.2.1 古典密码](doc/3.2.1_classic_crypto.md)
  - [3.3 Pwn](doc/3.3_pwn.md)
    - [3.3.1 格式化字符串漏洞](doc/3.3.1_format_string.md)
    - [3.3.2 整数溢出](doc/3.3.2_integer_overflow.md)
    - [3.3.3 栈溢出](doc/3.3.3_stack_overflow.md)
    - [3.3.4 返回导向编程（ROP）](doc/3.3.4_rop.md)
    - [3.3.5 堆溢出](doc/3.3.5_heap_overflow.md)
  - [3.4 Web](doc/3.4_web.md)
  - [3.5 Misc](doc/3.5_misc.md)
  - [3.6 Mobile](doc/3.6_mobile.md)

- [四、技巧篇](doc/4_tips.md)
  - [4.1]()
  - [4.2 Linux 命令行技巧](doc/4.2_Linux_terminal_tips.md)
  - [4.3 GCC 编译参数解析](doc/4.3_gcc_arg.md)
  - [4.4 GCC 堆栈保护技术](doc/4.4_gcc_sec.md)
  - [4.5 Z3 约束求解器](doc/4.5_z3.md)
  - [4.6 one-gadget RCE](doc/4.6_one-gadget_rce.md)
  - [4.7 通用 gadget](doc/4.7_common_gadget.md)
  - [4.8 使用 DynELF 泄露函数地址](doc/4.8_dynelf.md)
  - [4.9 给 ELF 文件打 patch](doc/4.9_patch_elf.md)
  - [4.10 给 PE 文件打 patch](doc/4.10_patch_pe.md)

- [五、高级篇](doc/5_advanced.md)
  - [5.1 Fuzz 测试](doc/5.1_fuzz.md)
  - [5.2 Pin 动态二进制插桩](doc/5.2_pin.md)
  - [5.3 angr 二进制自动化分析](doc/5.3_angr.md)
  - [5.4 符号执行](doc/5.4_symbolic.md)
  - [5.5 Triton 动态二进制分析框架](doc/5.5_triton.md)
  - [5.6 LLVM](doc/5.6_llvm.md)
  - [5.7 Capstone/Keystone](doc/5.7_cap-keystone.md)
  - [5.8 SAT/SMT](doc/5.8_sat-smt.md)
  - [5.9 反调试技术](doc/5.9_antidbg.md)
  - [5.10 反编译技术](doc/5.10_decompiling.md)
  - [5.11 RetDec 反编译器](doc/5.11_retdec.md)

- [六、题解篇](doc/6_writeup.md)
  - pwn
    - [6.1.1 pwn HCTF2016 brop](doc/6.1.1_pwn_hctf2016_brop.md)
    - [6.1.2 pwn NJCTF2017 pingme](doc/6.1.2_pwn_njctf2017_pingme.md)
    - [6.1.3 pwn XDCTF2015 pwn200](doc/6.1.3_pwn_xdctf2015_pwn200.md)
    - [6.1.4 pwn BackdoorCTF2017 Fun-Signals](doc/6.1.4_pwn_backdoorctf2017_fun_signals.md)
    - [6.1.5 pwn GreHackCTF2017 beerfighter](doc/6.1.5_pwn_grehackctf2017_beerfighter.md)
    - [6.1.6 pwn DefconCTF2015 fuckup](doc/6.1.6_pwn_defconctf2015_fuckup.md)
    - [6.1.7 pwn 0CTF2015 freenote](doc/6.1.7_pwn_0ctf2015_freenote.md)
    - [6.1.8 pwn DCTF2017 Flex](doc/6.1.8_pwn_dctf2017_flex.md)
    - [6.1.9 pwn RHme3 Exploitation](doc/6.1.9_rhme3_exploitation.md)
  - re
    - [6.2.1 re XHPCTF2017 dont_panic](doc/6.2.1_re_xhpctf2017_dont_panic.md)
    - [6.2.2 re ECTF2016 tayy](doc/6.2.2_re_ectf2016_tayy.md)
    - [6.2.3 re Codegate2017 angrybird](doc/6.2.3_re_codegate2017_angrybird.md)
    - [6.2.4 re CSAWCTF2015 wyvern](doc/6.2.4_re_csawctf2015_wyvern.md)
    - [6.2.5 re PicoCTF2014 Baleful](doc/6.2.5_re_picoctf2014_baleful.md)
    - [6.2.6 re SECCON2017 printf_machine](doc/6.2.6_re_seccon2017_printf_machine.md)

- [七、实战篇](doc/7_exploit.md)
  - CVE 分析
    - [7.1.1 [CVE-2017-11543] tcpdump 4.9.0 Buffer Overflow](doc/7.1.1_tcpdump_2017-11543.md)

- [八、附录](doc/8_appendix.md)
  - [8.1 更多 Linux 工具](doc/8.1_Linuxtools.md)
  - [8.2 更多 Windows 工具](doc/8.2_wintools.md)
  - [8.3 更多资源](doc/8.3_books&blogs.md)
  - [8.4 习题 write-up](doc/8.4_writeup.md)
  - [8.5 Linux x86-64 系统调用表](doc/8.5_syscall.md)
  - [8.6 幻灯片](doc/8.6_slides.md)


合作和贡献
---
请查看 [CONTRIBUTION.md](CONTRIBUTION.md)

LICENSE
---
CC BY-SA 4.0
