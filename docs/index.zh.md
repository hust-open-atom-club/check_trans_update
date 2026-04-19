# Linux 内核文档 — zh_CN 翻译状态

本网站跟踪 Linux 内核 `Documentation/` 下每个文档是否已有中文（`zh_CN`）翻译，
以及翻译是否与英文原文保持同步。

数据每日自动更新：运行
[`checktransupdate.py`](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/tools/docs/checktransupdate.py)
针对内核的 `docs-next` 分支进行扫描，再由本仓库的构建流程渲染为静态页面。

## 分类

- **[待翻译](needs-translation.md)** — 尚无中文版本的文档。
- **[待更新](needs-update.md)** — 中文版本落后于英文原文的文档，附上需要合入的提交列表。

## 来源

- 脚本: <https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/tools/docs/checktransupdate.py>
- 网站生成器: <https://github.com/hust-open-atom-club/check_trans_update>
