#!/bin/sh

if [ -e linux ];then
    git pull
else
    git clone https://mirrors.hust.edu.cn/git/lwn.git linux
fi

cd linux

git checkout docs-next

./scripts/checktransupdate.py -l zh_CN > ../TODO_LIST 2>&1
