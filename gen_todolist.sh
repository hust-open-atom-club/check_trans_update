#!/bin/sh

if [ -e linux ]; then
    git -C linux pull
else
    git clone --branch docs-next git://git.lwn.net/linux.git linux
fi

./linux/tools/docs/checktransupdate.py -l zh_CN > TODO_LIST 2>&1
