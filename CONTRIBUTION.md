# 合作与贡献
随着信息安全的迅速发展，CTF 竞赛也在如火如荼的开展，有人说“今天的 ACM 就是明天的 CTF”，颇有几分道理。

市场上已经充斥着大量的 ACM 书籍，而 CTF 以其知识内容之分散、考察面之广泛、题目类型之多变，让许多新手不知所措，同时也加大了该方面书籍的编写难度。

此书本着开源之精神，以分享他人提高自己为目的，将是一本大而全的 CTF 领域指南。因本人能力和时间有限，不可能精通竞赛中各个类别的知识，欢迎任何人提出建议或和我一起完成此书。

-- 开始于 2017.7.17

### 规范
#### 目录结构
```
.
.
├── CONTRIBUTION.md
├── doc
│   ├── 1.1_ctf.md
│   └── 6_appendix.md
├── LICENSE
├── pic
│   ├── 1.3_byte_order.png
│   └── 5.2_pin_arch.png
├── ppt
│   └── 01_fight-with-linux.pdf
├── README.md
├── src
│   ├── Others
│   │   ├── 1.5.7_stack.c
│   │   └── 5.2_pin.c
│   └── Reverse
│       ├── 5.2_baleful
│       └── xxd_crackme
└── SUMMARY.md
```

- `LICENSE`：开源协议。
- `README.md`：自述文件。
- `CONTRIBUTION.md`：合作与贡献的相关内容。
- `SUMMARY.md`：gitbook 目录结构。
- `doc`：该文件夹包含书全部内容的 Markdown 文件。（文字）
- `pic`：该文件夹包含所有 Markdown 中引用的所有图片文件。（图片）
- `src`：该文件夹包含书中示例和练习的二进制文件或源代码，分专题保存。（代码）
- `ppt`：该文件夹包含以书为主要内容制作的 PPT。(分享)

#### 注意事项
- 在开始编写某一个内容之前，请先在下面的表格里注明，以避免重复和冲突。如果是已经完成的章节，则可以直接进行修改。
- 每个章节开头需要有一个目录，增加或删除内容时需要做相应的修改，关于 GitHub 独特的页面跳转写法请参考 [Page Jumping in Github](https://github.com/firmianay/Life-long-Learner/blob/master/misc/github-tips.md#page-jumping-in-github)。
- [中文文案排版指北](https://github.com/sparanoid/chinese-copywriting-guidelines)
- 如果你新添加一个章节，需要在 **README.md**、**SUMMARY.md** 和章节所属部分相应的文件中添加条目。


| 章节              | 作者        | 进度   |
| --------------- | --------- | ---- |
| 3.3.4_rop.md    | firmianay | 未完成  |
| 2.10_binwalk.md | Sky3      | 未完成  |
