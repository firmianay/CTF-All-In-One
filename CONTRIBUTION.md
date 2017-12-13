# 合作与贡献
随着信息安全的迅速发展，CTF 竞赛也在如火如荼的开展，有人说“今天的 ACM 就是明天的 CTF”，颇有几分道理。

市场上已经充斥着大量的 ACM 书籍，而 CTF 以其知识内容之分散、考察面之广泛、题目类型之多变，让许多新手不知所措，同时也加大了该方面书籍的编写难度。

此书本着开源之精神，以分享他人提高自己为目的，将是一本大而全的 CTF 领域指南。因本人能力和时间有限，不可能精通竞赛中各个类别的知识，欢迎任何人提出建议或和我一起完成此书。

**You think you understand something until you try to teach it.**

-- 开始于 2017.7.17

### 规范
#### 目录结构
```
.
├── CONTRIBUTION.md
├── doc
│   └── 1.1_ctf.md
├── LICENSE
├── pic
│   └── 1.3_byte_order.png
├── README.md
├── slides
│   └── 01_fight-with-linux.pdf
├── src
│   ├── exploit
│   │   └── init
│   ├── Others
│   │   └── 1.5.7_brk.c
│   ├── Pwn
│   │   └── 3.3.1_goodlock_200
│   ├── Reverse
│   │   └── 2.2_serial_number_300
│   └── writeup
│       └── 6.1.1_pwn_hctf2016_brop
└── SUMMARY.md
```

- `LICENSE`：开源协议。
- `README.md`：自述文件。
- `CONTRIBUTION.md`：合作与贡献的相关内容。
- `SUMMARY.md`：gitbook 目录结构。
- `doc`：该文件夹包含书全部内容的 Markdown 文件。（文字）
- `pic`：该文件夹包含所有 Markdown 中引用的所有图片文件。（图片）
- `src`：该文件夹包含书中示例和练习的二进制文件或源代码，分专题保存。（代码）
- `slides`：该文件夹包含以书为主要内容制作的幻灯片。(ppt)

#### 注意事项
- 在开始编写某一个内容之前，请先在下面的表格里注明，以避免重复和冲突。如果是已经完成的章节，则可以直接进行修改。
- 每个章节开头需要有一个目录，增加或删除内容时需要做相应的修改，关于 GitHub 独特的页面跳转写法请参考 [Page Jumping in Github](https://github.com/firmianay/Life-long-Learner/blob/master/misc/github-tips.md#page-jumping-in-github)。
- [中文文案排版指北](https://github.com/sparanoid/chinese-copywriting-guidelines)
- 如果你新添加一个章节，需要在 **README.md**、**SUMMARY.md** 和章节所属部分相应的文件中添加条目。
- 新增第六章题解篇，收集各种好题的Writeup，应力求详细，且能提供程序供实际操作，一个md只写一题，所有文件上传到文件夹`src/writeup`，题目最好来自 [CTFs](https://github.com/ctfs)。
- 新增第七章实战篇，CTF之后，总是要回到现实中，对真实存在的漏洞进行分析利用，还是一样力求详细，并提供程序复现，一个md写一个漏洞，所有文件上传到`src/exploit`（程序太大的可附上网盘链接），参考 [exploit-db](https://www.exploit-db.com/)。
  - 考虑到真实漏洞的环境可能会很复杂，如果能做一个基于 docker 的环境，应该会很不错，这条就作为一个未来的计划。


| 章节              | 作者        | 进度   |
| --------------- | --------- | ---- |
| 2.10_binwalk.md | Sky3      | 未完成  |
| 2.12_burpsuite.md | phantom0301      | 未完成  |
| 1.4.*.md | phantom0301      | 未完成  |
