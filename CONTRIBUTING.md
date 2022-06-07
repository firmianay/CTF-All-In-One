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
├── CONTRIBUTING.md
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
- `CONTRIBUTING.md`：合作与贡献的相关内容。
- `SUMMARY.md`：GitBook 目录结构。
- `.gitignore`：忽略特殊文件。
- `FAQ.md`：常见问题解答。
- `THANKS`：致谢名单。
- `doc`：该目录包含书全部内容的 Markdown 文件。（文字）
- `pic`：该目录包含所有 Markdown 中引用的所有图片文件。（图片）
- `src`：该目录包含书中示例和练习的二进制文件或源代码，分专题保存。（代码）
- `slides`：该目录包含以书为主要内容制作的幻灯片。(ppt)

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


## 其他说明

*对最后一个 PDF 版本（ 2018.07.15 ）的说明*

《CTF All-In-One》满一周年了，正好也是世界杯决赛的日子，或许应该纪念一下。

去年有段时间我就在想，应该给大学生涯留下点什么，然后某天我在读《Reverse Engineering for Beginners》的时候，突然就萌生了像作者一样写一本开源书的想法。当时就很激动，CTF for Beginners，听起来不错，然后又一想，CTF 这么多内容，全包含进来是不是用 All-In-One 更好一点，然后就有了这本书。书的结构经过几次大改，现在有点像博客式的连载，但章节之间也会有一些关联。理想很丰满现实很骨感，一年过去了仅有四个 contributer，内容虽然超过 1700 页，但也只覆盖了二进制的一部分，或许把书名换成《Binary for Beginners》会更匹配一点（这一条在我的计划中）。当然 482 个 star 和 95 个 fork 的成绩似乎也还说得过去。

写东西确实很辛苦，生怕哪里写错或者表述不清楚误导了别人（虽然还是错了不少...）。特别是在调试漏洞的时候，为了将每个步骤及内存的情况清晰地展现出来，花费了非常多的时间。当然辛苦的同时自己也得到了许多东西，从学习到总结再到分享，本身就是一个自我提高的过程。然后还认识了一些朋友，能够交流一些技术问题，其中有一个看不懂中文的小哥，问我能否提供英文版，我当然是很感动然后拒绝了他（能力有限…）。大概一个月前，在 ASU 做科研的 Fish 师傅说看了我写的东西，问我是否有打算出国深造，无奈作为学渣绩点太低。如果列表里出国的同学有对自动化二进制程序分析感兴趣的，赶紧抱紧 Fish 师傅大腿（angr 的作者之一）。

这本书未来还会继续更新，速度就不好说了，希望有更多的朋友参与进来。

最后，克罗地亚加油！！！

例行描述：
1、距离上次 release 已有三个月。
2、总共 1795 页，增加约 30%。
3、增加的内容主要是题解和论文笔记。
4、我好菜啊QAQ。

## 致谢

- 感谢内容贡献者及我室友：skyel1u
- 感谢 XDSEC，把我引上了安全这条路，认识了很多志同道合的小伙伴
- 感谢 GitHub 上的朋友，是你们的 star 给我写作的动力
