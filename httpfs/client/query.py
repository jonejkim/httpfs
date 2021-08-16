#!/usr/bin/python

from httpfs.common import build_confs_from_json
import sys

FSCONFS = build_confs_from_json()

if __name__ == '__main__':
    command = sys.argv[0]
    uri = sys.argv[1:]
    uri = ' '.join(uri) # in case of URIs with space with no quotation

    ## list all available fs and their configuration
    # - triggered by `httpfsq -fs` or `python3 -m httpfs.client.query -fs`
    if uri == "-fs":
        print(f'{"fsname":>12}   {"readonly"}   {"fsroot"} ')
        for fsconf in FSCONFS.values():
            print(f'{fsconf.fsname:>12} : {str(fsconf.readonly):>8} : {fsconf.fsroot:} ')
        exit()

    ## default query input can be either about:
    # - a local file path -> return corresponding URL
    # - a httpfs file URL -> return corresponding local file path
    if "file://" in uri:
        uri = uri.replace("file://", "")

    corresponding_uri = None
    for fsname, fsconf in FSCONFS.items():
        if fsconf.path_exists(uri):
            corresponding_uri = fsconf.path2url(uri)
            break
        elif fsconf.url_exists(uri):
            corresponding_uri = fsconf.url2path(uri)
            break

    if corresponding_uri is not None:
        print(corresponding_uri)
    else:
        print('No corresponding URI was found.')