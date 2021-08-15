#!/usr/bin/python
from typing import *
from flask import Flask, request, send_from_directory
from urllib.request import url2pathname as url2pathname
# from flask.helpers import send_file
# from werkzeug.utils import secure_filename

from httpfs.common import build_confs_from_json, HOST, PORT, SERVER_URL, UPLOAD_SUBDIR_NAME

FSCONFS = build_confs_from_json()

app = Flask(__name__)

@app.route('/<string:fsname>/', methods=['POST'])
def fs(fsname):
    # uploading/writing through HTTP POST is always stored exactly into `/fsname/.imgs/` - ie. no subdirectories.
    # for subdirectories e.g. `/fsname/.imgs/notes0/`, create them manually. HTTP GET on them will still be possible.
    if request.method == 'POST':
        if fsname in FSCONFS.keys():
            httpfs = FSCONFS[fsname]

            if httpfs.readonly:
                return False

            f = request.files['file'] # fetch inbound file

            # find & avoid duplicate filename
            desired_fname:str = url2pathname(f.filename)
            unique_fname:str = httpfs.secure_unique_fname(desired_fname, httpfs.uploadDir)
            savepath = httpfs.uploadDir / unique_fname
            f.save(savepath)

            # return accessible URL
            urlpath = SERVER_URL + '/' + fsname + f'/{UPLOAD_SUBDIR_NAME}/' + unique_fname
            return urlpath

@app.route('/<string:fsname>/<path:fpath>', methods=['GET'])
def download(fsname, fpath):
    # retrieving is allowed on the entire subdirectories recursively under `/fsname/`
    if request.method == 'GET':
        return send_from_directory(directory=FSCONFS[fsname].fsroot, path=fpath)

if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=True)