#!/usr/bin/python

from typing import *
import os, sys
from argparse import ArgumentParser
from pathlib import PosixPath
import requests
import urllib
from urllib.request import urlretrieve
from urllib.parse import urlparse
import textwrap

from httpfs.common import SERVER_URL, build_confs_from_json

FSCONFS = build_confs_from_json()

# set agent to something convincing so that we don't get 403 Forbidden response while retrieving web image
opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
urllib.request.install_opener(opener)

# temporary directory to store downloaded remote url images
TMP_DIR = PosixPath('/tmp/typora-httpfs/')
os.makedirs(TMP_DIR, exist_ok=True)

## Paste the following command to Typora: ##
"""
python3 -m httpfs.client_typora.img_uploader -md "${filepath}" -ts
"""


def main(mdpath, targetpaths):
    try:

        ##==================================##
        ## Special Case Treatments needed
        ##

        # - case1) Typora's is testing the uploader (in Typora preferences UI)
        # - case2) image pasted into no markdown file with no path (== new & unsaved) --> send to defaault fs
        # - case3) Image pasted into markdowin file in a fsroot tree no governed by httpfs -> send to default fs

        if mdpath == "":
            parentDirs:List[PosixPath] = [PosixPath(targetpath).parent for targetpath in targetpaths]

            # case 1)
            if all(parentdir == PosixPath('/tmp') for parentdir in parentDirs):
                mdpath = str(FSCONFS['tmp'].fsroot) + '/'
            else:
                # case 2)
                mdpath = str(FSCONFS['default'].fsroot) + '/'


        ##==================================##
        ## if any targetpath provided is URL,
        ##   downloadt to local storage first
        ##

        ## - else, assumed to be local file paths, can just directly upload
        toBeDeleteds = [False]*len(targetpaths) # downloaded files are temporary and will be removed after uploading
        dontUploads = [False]*len(targetpaths)
        for idx, targetpath in enumerate(targetpaths):
            if ('http://' in targetpath) or ('https://' in targetpath):
                targetUrl = targetpath
                # if the URL is of the httpfs server, don't wan't to re-upload.
                if SERVER_URL in targetUrl:
                    dontUploads[idx] = True
                    continue

                urlparsed = urlparse(targetUrl)

                # download first
                fBasename = os.path.basename(urlparsed.path)

                # decode %NN encoding in filename
                decodedFBasename = urllib.parse.unquote(fBasename)
                targetpaths[idx], headers = urlretrieve(targetUrl, TMP_DIR/decodedFBasename)
                toBeDeleteds[idx] = True

        ##==================================##
        ## Find appropriate fs using mdpath provided
        ##

        fetched_fsname = None
        for fsname, fsconf in FSCONFS.items():
            if (str(fsconf.fsroot)+'/') in mdpath:
                fetched_fsname = fsname
                break

        ## case 3)
        if fetched_fsname is None:
            fetched_fsname = 'default'


        ##==================================##
        ## Upload Image File(s)
        ##

        # files to upload should be all in local storage by this point.

        url = f'{SERVER_URL}/{fetched_fsname}/'
        for dontUpload, toBeDeleted, targetpath in zip(dontUploads, toBeDeleteds, targetpaths):
            if dontUpload:
                # return as original URL as it is, but pretend as if it was uploaded to Typora, for upload standard compliance.
                print(targetpath)
            else:
                # encode filename into URL & UTF-8 safe filename
                fBasename = os.path.basename(targetpath)
                encodedFBasename = urllib.parse.quote(fBasename)
                with open(targetpath, 'rb') as f:
                    response = requests.post(url, files={'file': (encodedFBasename, f)})

                if response.ok:
                    # print URL uploaded to
                    print(response.text)
                else:
                    assert False, f'Received HTTP POST response: {response}'

                if toBeDeleted:
                    os.remove(targetpath)

    except Exception as err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        # XML style printing is for the sake of readability.
        errout = textwrap.dedent(f"""\
                                <ERROR>
                                <Exception>
                                File \"{fname}\", line {exc_tb.tb_lineno}, {exc_type}: {err}
                                </Exception>
                                <Arguments>
                                \"{args}\"
                                </Arguments>
                                </ERROR>""")
        raise RuntimeError(errout)

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-md", "--mdpath", nargs='?')
    parser.add_argument("-ts", "--targetpaths", nargs='+', help="image URL or image file path")

    args = parser.parse_args()
    main(args.mdpath, args.targetpaths)