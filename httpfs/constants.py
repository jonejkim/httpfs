#!/usr/bin/python
from pathlib import PosixPath

## HTTP Image/File Server URL
HOST = '127.0.0.1' # localhost/loopback address by default
PORT = '9999'

SERVER_URL = 'http://'+ HOST + ':' +  PORT

# where configurations should be found
FSCONF_FPATH = PosixPath(__file__).parent / 'fsconf.json'
FSCONF_TEMPLATE_FPATH = PosixPath('.').absolute() / 'httpfs' / 'fsconf-template.json'

# name of the subdirectory under fsroot where images are uploaded to by HTTPFS server.
UPLOAD_SUBDIR_NAME = '.imgs'
NOREF_SUBDIR_NAME = '.imgs.noref'

