#!/bin/sh

## if running line by line manually:
thisdir=`pwd`

## if running as a script:
thisdir=$(realpath $(dirname "$0"))

pip uninstall httpfs

# make it executables
chmod u-x ${thisdir}/httpfs/shellexecs/httpfs-srv
chmod u-x ${thisdir}/httpfs/shellexecs/httpfsq
chmod u-x ${thisdir}/httpfs/shellexecs/httpfs-noref
chmod u-x ${thisdir}/httpfs/shellexecs/httpfs-unittest

# add to path, in .bashrc
sed -i 's/export PATH=.*httpfs\/httpfs\/shellexecs\/\:\$PATH//g' ~/.bashrc
source ~/.bashrc

echo ""
echo "Uninstallation Done. You may now remove this repository manually."