# Linux 内核中文文档翻译状态

本网站跟踪 Linux 内核 `Documentation/` 下每个文档是否已有中文（`zh_CN`）翻译，
以及翻译是否与英文原文保持同步。

数据每日自动更新：运行
[`checktransupdate.py`](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/tools/docs/checktransupdate.py)
针对内核的 `docs-next` 分支进行扫描，再由本仓库的构建流程渲染为静态页面。

## 分类

- **[待翻译](needs-translation.md)** — 尚无中文翻译版本的文档。
- **[待更新](needs-update.md)** — 中文翻译版本落后于英文原文的文档，附上需要合入的提交列表。

## 贡献翻译

动手翻译前，强烈建议先阅读内核官方的中文翻译者指南。它介绍了文件布局、
页首格式、评审流程以及常见陷阱：

- [zh_CN/how-to.rst](https://www.kernel.org/doc/Documentation/translations/zh_CN/how-to.rst)
