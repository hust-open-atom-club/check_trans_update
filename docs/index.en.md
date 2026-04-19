# Linux Doc zh_CN Translation Status

This site shows, for every page under `Documentation/` in the upstream Linux
kernel, whether a Chinese (`zh_CN`) translation exists and whether it is up to
date with the English original.

Data is regenerated **daily** by running
[`checktransupdate.py`](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/tools/docs/checktransupdate.py)
against the `docs-next` branch of the kernel tree, then rendered into static
pages by this repository's build step.

## Sections

- **[Needs translation](needs-translation.md)** — files with no zh_CN
  translation yet.
- **[Needs update](needs-update.md)** — files whose zh_CN translation is
  behind the English original, with the list of commits to resolve.

## Contributing translations

Before picking up a file from the lists above, read the kernel's
zh_CN translator how-to (written in Chinese). It covers file layout,
header format, review workflow, and common pitfalls:

- [zh_CN/how-to.rst](https://www.kernel.org/doc/Documentation/translations/zh_CN/how-to.rst)
