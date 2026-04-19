# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository purpose

A single Python 3 script, [checktransupdate.py](checktransupdate.py), that has been upstreamed into the Linux kernel (at `Documentation/doc-guide/checktransupdate.rst` / `scripts/checktransupdate.py`). This repo is the author's working copy; the companion files here are documentation ([checktransupdate.rst](checktransupdate.rst), [zh_CN/checktransupdate.rst](zh_CN/checktransupdate.rst)), a harness to regenerate the tracked [TODO_LIST](TODO_LIST), and the generated TODO_LIST itself.

The script reports which Linux kernel translation files (e.g. `Documentation/translations/zh_CN/...`) are out-of-date relative to their English originals, by walking `git log` — no translation content is parsed.

## Commands

Regenerate [TODO_LIST](TODO_LIST) (clones/updates a `linux/` checkout, checks out `docs-next`, runs the script):

```sh
./gen_todolist.sh
```

Note: [gen_todolist.sh](gen_todolist.sh) clones `https://mirrors.hust.edu.cn/git/lwn.git` into `./linux/` (gitignored) and then invokes `./scripts/checktransupdate.py` **from within that checkout** — it relies on the upstreamed copy in the kernel tree, not on [checktransupdate.py](checktransupdate.py) at the repo root. If you've modified the local script and want to test it, copy it into `linux/scripts/` before running.

Run the script directly against a Linux kernel tree:

```sh
# from inside a Linux kernel checkout, with the script placed at scripts/
./scripts/checktransupdate.py --help
./scripts/checktransupdate.py -l zh_CN
./scripts/checktransupdate.py Documentation/translations/zh_CN/dev-tools/testing-overview.rst
./scripts/checktransupdate.py --log DEBUG -l zh_CN   # verbose
```

There are no tests, no linter config, and no build step in this repo.

## How the script works (the non-obvious parts)

- **Path assumption.** The script derives `linux_path` as `os.path.dirname(__file__)/..`, i.e. it assumes it lives at `<linux>/scripts/checktransupdate.py`. It `chdir`s to `linux_path` before running `git log`, so it will not work correctly if invoked from an arbitrary location or if the tree structure differs.
- **Origin-path convention.** `get_origin_path` strips the `translations/<locale>/` segment from a translated path: `Documentation/translations/zh_CN/foo/bar.rst` → `Documentation/foo/bar.rst`. The script relies on this two-level layout — changing the translation directory structure will break it.
- **"Tracked" origin commit.** For each translated file, `get_origin_from_trans` walks backwards through the English file's history from the translation's commit hash until it finds an English commit whose `author_date` is ≤ the translation's `author_date`. That commit is treated as the English revision the translation was based on; commits between it and HEAD (filtered to exclude `Merge tag` commits) are what needs updating.
- **Dates are compared by author date**, not commit date — this matters when rebases/cherry-picks shift commit dates.
- **Locale validation.** `-l <locale>` is rejected unless `<linux>/Documentation/translations/<locale>/` exists on disk.
- **Missing translations.** When run without explicit files, the script walks `Documentation/` (excluding `translations/` and `output/`) for `*.rst` files and reports any whose corresponding translation is absent. `--no-print-missing-translations` suppresses this.
- **Logging.** All output goes through the `logging` module with a custom dmesg-style formatter, and is written both to stdout and to `checktransupdate.log` (configurable via `--logfile`). `gen_todolist.sh` captures stdout+stderr into `TODO_LIST` via `> ../TODO_LIST 2>&1`.

## Keeping in sync with upstream

Changes to [checktransupdate.py](checktransupdate.py) / [checktransupdate.rst](checktransupdate.rst) / [zh_CN/checktransupdate.rst](zh_CN/checktransupdate.rst) are intended to flow upstream to the Linux kernel tree (`scripts/checktransupdate.py` and `Documentation/doc-guide/`). Keep the three documentation files (English `.rst`, zh_CN `.rst`, and [README.md](README.md)) consistent when editing any of them.
