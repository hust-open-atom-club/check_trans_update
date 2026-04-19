#!/bin/sh

if [ -e linux ];then
    git pull
else
    git clone --branch docs-next git://git.lwn.net/linux.git linux
fi

cd linux

./scripts/checktransupdate.py -l zh_CN > ../TODO_LIST 2>&1
