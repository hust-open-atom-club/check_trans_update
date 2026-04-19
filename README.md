[![加入飞书外部群](https://img.shields.io/badge/加入飞书外部群-HCTT%20SIG-0078d7?style=flat-square&labelColor=444444)](https://applink.feishu.cn/client/chat/chatter/add_by_link?link_token=4e3g0475-2966-40c7-a713-3fcf43893a67)
[![Deploy](https://github.com/mudongliang/check_trans_update/actions/workflows/deploy.yml/badge.svg)](https://github.com/mudongliang/check_trans_update/actions/workflows/deploy.yml)

**Live site:** <https://mudongliang.github.io/check_trans_update/>

# Checking for needed translation updates

This script helps track the translation status of the documentation in
different locales, i.e., whether the documentation is up-to-date with
the English counterpart.

## How it works

It uses ``git log`` command to track the latest English commit from the
translation commit (order by author date) and the latest English commits
from HEAD. If any differences occur, the file is considered as out-of-date,
then commits that need to be updated will be collected and reported.

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

Features implemented

-  check all files in a certain locale
-  check a single file or a set of files
-  provide options to change output format
-  track the translation status of files that have no translation

## Usage

```
./scripts/checktransupdate.py --help
```

Please refer to the output of argument parser for usage details.

Samples

-  ``./scripts/checktransupdate.py -l zh_CN``
   This will print all the files that need to be updated in the zh_CN locale.
-  ``./scripts/checktransupdate.py Documentation/translations/zh_CN/dev-tools/testing-overview.rst``
   This will only print the status of the specified file.

Then the output is something like:

```
Documentation/dev-tools/kfence.rst
No translation in the locale of zh_CN

Documentation/translations/zh_CN/dev-tools/testing-overview.rst
commit 42fb9cfd5b18 ("Documentation: dev-tools: Add link to RV docs")
1 commits needs resolving in total
```
