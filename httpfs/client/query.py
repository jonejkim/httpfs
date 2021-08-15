#!/usr/bin/python

# input a local absolute file path. if it is in httpfs, return the corresponding valid httpfs url for it
from httpfs.common import build_confs_from_json
import sys

FSCONFS = build_confs_from_json()

if __name__ == '__main__':
    command = sys.argv[0]
    uri = sys.argv[1:]
    uri = ' '.join(uri)
    # print(filepath)

    # print(f'[      Input      ]: {uri}')

    if "file://" in uri:
        uri = uri.replace("file://", "")

    corresponding_uri = None
    for fsname, httpfs in FSCONFS.items():
        if httpfs.path_exists(uri):
            corresponding_uri = httpfs.path2url(uri)
            break
        elif httpfs.url_exists(uri):
            corresponding_uri = httpfs.url2path(uri)
            break

    if corresponding_uri is not None:
        print(corresponding_uri)
    else:
        print('No corresponding URI was found.')