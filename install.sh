#!/bin/bash

# if running line by line manually:
thisdir=`pwd`

## if running as a script:
thisdir=$(realpath $(dirname "$0"))

pip install -e ${thisdir}

# make it executables
chmod u+x ${thisdir}/httpfs/shellexecs/httpfs-srv
chmod u+x ${thisdir}/httpfs/shellexecs/httpfsq
chmod u+x ${thisdir}/httpfs/shellexecs/httpfs-noref
chmod u+x ${thisdir}/httpfs/shellexecs/httpfs-unittest

# add to path, in .bashrc
cat << EOF >> ~/.bashrc
export PATH=${thisdir}/httpfs/shellexecs/:\$PATH
EOF
source ~/.bashrc

# setup demo configurations
python3 -m httpfs.setup_demo

# configure start server upon boot
echo ""
echo "Done Installation. Complete by running: "
echo "\$ source ~/.bashrc"
echo ""
echo "Then you may start httpfs server with command: "
echo "\$ httpfs-srv"
echo ""
echo "With basic sanity unit-testing the with: "
echo "\$ httpfs-unittest"
echo ""
echo "In Typora Image Uploader settings, add the following command with required settings:"
echo "\$ python3 -m httpfs.client_typora.img_uploader -md \"\${filepath}\" -ts"
echo ""
echo "For more details, please take a look at the ./demo directory while the server is running."
echo ""