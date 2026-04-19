# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository purpose

This repo publishes a daily-refreshed static site showing the zh_CN translation status of the Linux kernel documentation. The status checker itself — `checktransupdate.py` — also lives upstream in the kernel tree at `tools/docs/checktransupdate.py`. What this repo contains:

- A local copy of [checktransupdate.py](checktransupdate.py) that carries a bug fix not yet merged upstream (handles translations whose origin English file was merged into the branch *after* the translation was authored). The build pipeline overlays this local copy onto the cloned kernel tree before running the checker; once the fix lands upstream, this local copy can be deleted.
- A site generator ([build_site.py](build_site.py) + [mkdocs.yml](mkdocs.yml)) that turns the checker's output into a GitHub Pages site.
- Upstream-bound docs mirrors: [en/checktransupdate.rst](en/checktransupdate.rst) and [zh_CN/checktransupdate.rst](zh_CN/checktransupdate.rst) — edited here and flowed upstream into `Documentation/doc-guide/`.
- A harness ([gen_todolist.sh](gen_todolist.sh)) that clones the kernel tree, overlays the local checker, and regenerates `TODO_LIST` locally (for previewing the site build).

The checker reports which Linux kernel translation files (e.g. `Documentation/translations/zh_CN/...`) are out-of-date relative to their English originals, by walking `git log` — no translation content is parsed.

## Commands

Regenerate [TODO_LIST](TODO_LIST) (clones LWN's `docs-next` branch into `./linux/`, runs the in-tree checker):

```sh
./gen_todolist.sh
```

Note: [gen_todolist.sh](gen_todolist.sh) clones `git://git.lwn.net/linux.git --branch docs-next` into `./linux/` (gitignored), copies [checktransupdate.py](checktransupdate.py) over `linux/tools/docs/checktransupdate.py` (to apply the local patch), then invokes `./linux/tools/docs/checktransupdate.py`. The CI workflow follows the same pattern.

Run the checker directly against a Linux kernel tree (when the script lives at `<linux>/tools/docs/checktransupdate.py`):

```sh
./tools/docs/checktransupdate.py --help
./tools/docs/checktransupdate.py -l zh_CN
./tools/docs/checktransupdate.py Documentation/translations/zh_CN/dev-tools/testing-overview.rst
./tools/docs/checktransupdate.py --log DEBUG -l zh_CN   # verbose
```

Build and preview the static site locally:

```sh
pip install -r requirements.txt
python3 build_site.py --todo TODO_LIST --out docs
mkdocs serve
```

Run the parser tests:

```sh
pytest tests/ -v
```

There is no linter config in this repo; run `pytest tests/ -v` for the parser tests and `mkdocs build` to build the static site.

## How the script works (the non-obvious parts)

- **Path assumption.** The script derives `linux_path` as `os.path.dirname(__file__)/../..`, i.e. it assumes it lives at `<linux>/tools/docs/checktransupdate.py`. It `chdir`s to `linux_path` before running `git log`, so it will not work correctly if invoked from an arbitrary location or if the tree structure differs.
- **Origin-path convention.** `get_origin_path` strips the `translations/<locale>/` segment from a translated path: `Documentation/translations/zh_CN/foo/bar.rst` → `Documentation/foo/bar.rst`. The script relies on this two-level layout — changing the translation directory structure will break it.
- **"Tracked" origin commit.** For each translated file, `get_origin_from_trans` walks backwards through the English file's history from the translation's commit hash until it finds an English commit whose `author_date` is ≤ the translation's `author_date`. That commit is treated as the English revision the translation was based on; commits between it and HEAD (filtered to exclude `Merge tag` commits) are what needs updating.
- **Dates are compared by author date**, not commit date — this matters when rebases/cherry-picks shift commit dates.
- **Locale validation.** `-l <locale>` is rejected unless `<linux>/Documentation/translations/<locale>/` exists on disk.
- **Missing translations.** When run without explicit files, the script walks `Documentation/` (excluding `translations/` and `output/`) for `*.rst` files and reports any whose corresponding translation is absent. `--no-print-missing-translations` suppresses this.
- **Logging.** All output goes through the `logging` module with a custom dmesg-style formatter, and is written both to stdout and to `checktransupdate.log` (configurable via `--logfile`). `gen_todolist.sh` captures stdout+stderr into `TODO_LIST` via `> TODO_LIST 2>&1`.

## Site pipeline

[build_site.py](build_site.py) parses [TODO_LIST](TODO_LIST) into two markdown pages (`docs/needs-translation.md`, `docs/needs-update.md`, both gitignored), which [mkdocs.yml](mkdocs.yml) turns into a static site. A daily cron in [.github/workflows/deploy.yml](.github/workflows/deploy.yml) re-runs the whole pipeline — clones the Linux docs tree, runs `checktransupdate.py`, rebuilds, and deploys to GitHub Pages.

The parser tolerates unrecognized records (`logging.error` lines from `checktransupdate.py`, records with zero valid commits after merge-tag filtering). They are logged and collected into `result.skipped`, not included on the site.

## Keeping in sync with upstream

Changes to [en/checktransupdate.rst](en/checktransupdate.rst) and [zh_CN/checktransupdate.rst](zh_CN/checktransupdate.rst) are intended to flow upstream into the kernel's `Documentation/doc-guide/`. Keep them consistent when editing either one — the translation must describe the same feature set as the original.

The local [checktransupdate.py](checktransupdate.py) is a temporary overlay, not a permanent mirror. It exists solely to carry a fix upstream hasn't accepted yet. Edits should be submitted to `tools/docs/checktransupdate.py` upstream; once they merge, refresh this copy from upstream or delete it (and the overlay step in [gen_todolist.sh](gen_todolist.sh) and [.github/workflows/deploy.yml](.github/workflows/deploy.yml)).

[README.md](README.md) is this repo's GitHub landing page and is **not** a sync target for the upstream docs. It can intentionally diverge — e.g., omit feature lists that are already documented in the kernel's docs.
