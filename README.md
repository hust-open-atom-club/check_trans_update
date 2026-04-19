[![加入飞书外部群](https://img.shields.io/badge/加入飞书外部群-HCTT%20SIG-0078d7?style=flat-square&labelColor=444444)](https://applink.feishu.cn/client/chat/chatter/add_by_link?link_token=4e3g0475-2966-40c7-a713-3fcf43893a67)
[![Deploy](https://github.com/hust-open-atom-club/check_trans_update/actions/workflows/deploy.yml/badge.svg)](https://github.com/hust-open-atom-club/check_trans_update/actions/workflows/deploy.yml)

**Live site:** <https://hust-open-atom-club.github.io/check_trans_update/>

# Checking for needed translation updates

This script helps track the translation status of the documentation in
different locales, i.e., whether the documentation is up-to-date with
the English counterpart.

## How it works

It uses the `git log` command to track the latest English commit from the
translation commit (ordered by author date) and the latest English commit on
HEAD. If they differ, the file is considered out-of-date, and the commits
that need to be resolved are collected and reported.

## Static site

Translation status is published as a static site built with MkDocs (Material
theme) and deployed to GitHub Pages daily.

### Local preview

```sh
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# regenerate TODO_LIST if needed:
./gen_todolist.sh

python3 build_site.py --todo TODO_LIST --out docs
mkdocs serve
```
