#!/bin/sh

if [ -e linux ]; then
    git -C linux pull
else
    git clone --branch docs-next git://git.lwn.net/linux.git linux
fi

# Overlay the repo's copy of checktransupdate.py onto the tree; ours
# carries a fix not yet merged upstream (see commit history).
cp checktransupdate.py linux/tools/docs/checktransupdate.py

./linux/tools/docs/checktransupdate.py -l zh_CN > TODO_LIST 2>&1
