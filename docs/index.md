# Linux Documentation — zh_CN Translation Status

This site shows, for every page under `Documentation/` in the upstream Linux
kernel, whether a Chinese (`zh_CN`) translation exists and whether it is up to
date with the English original.

Data is regenerated **daily** by running
[`checktransupdate.py`](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/tools/docs/checktransupdate.py)
against the `docs-next` branch of the kernel tree, then rendered into static
pages by this repository's build step.

## Sections

- **[Needs translation](needs-translation.md)** — files with no zh_CN
  counterpart yet.
- **[Needs update](needs-update.md)** — files whose zh_CN translation is
  behind the English original, with the list of commits to resolve.

## Source

- Script: <https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/tools/docs/checktransupdate.py>
- Site generator: <https://github.com/mudongliang/check_trans_update>
