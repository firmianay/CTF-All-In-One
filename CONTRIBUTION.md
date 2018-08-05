# 合作与贡献

随着信息安全的迅速发展，CTF 竞赛也在如火如荼的开展，有人说“今天的 ACM 就是明天的 CTF”，颇有几分道理。

市场上已经充斥着大量的 ACM 书籍，而 CTF 以其知识内容之分散、考察面之广泛、题目类型之多变，让许多新手不知所措，同时也加大了该方面书籍的编写难度。

此书本着开源之精神，以分享他人提高自己为目的，将是一本大而全的 CTF 领域指南。因本人能力和时间有限，不可能精通各个类别的知识，欢迎任何人提出任何建议，和我一起完成此书。

千万不要觉得自己是初学者就不敢提交 PR（issue），千万不要担心自己提交的 PR（issue） 会有问题，毕竟最后合并的人是我，背锅的也是我：）

如果还有其他想法，请直接给我发邮件 firmianay@gmail.com。

**You think you understand something until you try to teach it.**

-- 开始于 2017.7.15

## 规范

### 目录结构

```text
.
├── .gitignore
├── .travis.yml
├── build
│   └── ctf_all_in_one.pdf
├── CHANGELOG
├── CONTRIBUTION.md
├── doc
│   └── 1.1_ctf.md
├── FAQ.md
├── LICENSE
├── pic
│   └── 1.3_byte_order.png
├── README.md
├── slides
│   └── 01_fight-with-linux.pdf
├── src
│   ├── exploit
│   │   └── init
│   ├── others
│   │   └── 1.5.7_brk.c
│   └── writeup
│       └── 6.1.1_pwn_hctf2016_brop
├── SUMMARY.md
├── tex
│   └── init
└── THANKS
```

- `LICENSE`：开源协议。
- `README.md`：自述文件。
- `CHANGELOG`：变更日志。
- `CONTRIBUTION.md`：合作与贡献的相关内容。
- `SUMMARY.md`：GitBook 目录结构。
- `.gitignore`：忽略特殊文件。
- `.travis.yml`：Travis CI 配置文件。
- `FAQ.md`：常见问题解答。
- `THANKS`：致谢名单。
- `doc`：该目录包含书全部内容的 Markdown 文件。（文字）
- `tex`：该目录包含使用 LaTex 重写的内容。（PDF）
- `pic`：该目录包含所有 Markdown 中引用的所有图片文件。（图片）
- `src`：该目录包含书中示例和练习的二进制文件或源代码，分专题保存。（代码）
- `slides`：该目录包含以书为主要内容制作的幻灯片。(ppt)
- `build`：该目录包含使用 LaTeX 生成的 PDF 书籍。(pdf)

### 注意事项

- 在开始编写某一个内容之前，请先在下面的表格里注明，以避免重复和冲突。如果是已经完成的章节，则可以直接进行修改。
- 每个章节开头需要有一个目录，增加或删除内容时需要做相应的修改，GitHub 独特的页面跳转写法是：大写换小写，空格换“-”，然后删掉除下划线以外的其他字符。
- [中文文案排版指北](https://github.com/sparanoid/chinese-copywriting-guidelines)。
- 推荐使用 VSCode，安装插件 markdownlint，对格式进行[规范](https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md)。
- 可能用到的几个网站：[Graphviz](https://www.graphviz.org/)，[asciiflow](http://asciiflow.com/)，[asciinema](https://asciinema.org/)，[ProcessOn](https://www.processon.com)。
- 如果你新添加一个章节，需要在 **SUMMARY.md** 和章节所属部分相应的文件中添加条目。
- 新增第六章题解篇，收集各种好题的 Writeup，应力求详细，且能提供程序供实际操作，一个 md 只写一题，所有文件上传到目录 `src/writeup`，题目最好来自 [CTFs](https://github.com/ctfs)。
- 新增第七章实战篇，CTF 之后，总是要回到现实中，对真实存在的漏洞进行分析利用，还是一样力求详细，并提供程序复现，一个 md 写一个漏洞，所有文件上传到 `src/exploit`（程序太大的可附上网盘链接），参考 [exploit-db](https://www.exploit-db.com/)。
  - 考虑到真实漏洞的环境可能会很复杂，如果能做一个基于 docker 的环境，应该会很不错，这条就作为一个未来的计划。
- 新增第八章学术篇，目前某人也处在读研还是工作的纠结中，但看看论文总不会错，一个 md 一篇文章或一类文章都可以，风格随意（参考 [How to Read an Engineering Research Paper](http://cseweb.ucsd.edu/%7Ewgg/CSE210/howtoread.html)）。论文的 pdf 我会统一上传到百度网盘。
- 由于某人有强迫症，所以能用文本时绝不要截图:p，但有时候动图（gif）也是可以考虑的。
- 看了下 GitBook 导出的 PDF，排版有点不忍直视，计划转战 LaTeX（XeLaTeX），即提供 md 和 tex 两个版本，tex 版本放在目录 `tex/` 下。
- 有外国小哥哥邮件我希望提供了英文版，鉴于某人的英文水平，可能暂时不太现实，如果有人愿意承担这一部分工作，请告诉我。

| 章节            | 作者          | 进度   |
| ------------- | ----------- | ---- |
| 2.6_idapro.md | Sky3        | 未完成  |
| 开始使用Latex     | Sky3        | 未完成  |
| 1.4.6.md      | phantom0301 | 未完成  |
| 3.4.1.md      | phantom0301 | 未完成  |
| 3.4.2.md      | phantom0301 | 未完成  |
