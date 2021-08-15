#!/usr/bin/python
from typing import *
import json
from pathlib import PosixPath
from urllib.parse import urlparse
from html.parser import HTMLParser
import requests
import markdown

from .constants import *


# Central class for accessing httpfs configurations
class HttpFs(object):

    def __init__(self, fsconf:dict):
        self.fsname = fsconf['fsname']
        self.readonly = fsconf['readonly']
        self.fsroot:PosixPath = fsconf['fsroot']
        self.uploadDir:PosixPath = fsconf['uploadDir']
        self.norefDir:PosixPath = fsconf['norefDir']
        self.fs_url = SERVER_URL + '/' + self.fsname

    def __list_xDir_fpaths(self, xDir:PosixPath, fname_only=False, asPathObj=False, recursive:bool=True) -> Union[List[str], List[PosixPath]]:

        if xDir != self.uploadDir and xDir != self.norefDir:
            raise Exception(f'bad argument xDir: {xDir} is not a writable subdirectory managed by this object\'s fsroot')

        if recursive:
          existing_posixpaths:List[PosixPath] = list(xDir.glob('**/*')) # '**/*' allows search into subdirectories manually made under '.imgs', not just tree depth 1
        else:
          existing_posixpaths:List[PosixPath] = list(filter(lambda item: not item.is_dir(), xDir.glob('*')))

        # output format as function of arguments
        if fname_only and asPathObj:
            raise Exception('argument input: ( not(fullpath) && asPathObj ) is not supported.')
        elif fname_only and not asPathObj:
            return [posixpath.name for posixpath in existing_posixpaths]
        elif not fname_only and asPathObj:
            return existing_posixpaths
        elif not fname_only and not asPathObj:
            return [str(posixpath) for posixpath in existing_posixpaths]

    def list_uploadDir_fpaths(self, fname_only=False, asPathObj=False, recursive:bool=True) -> Union[List[str], List[PosixPath]]:
        return self.__list_xDir_fpaths(self.uploadDir, fname_only, asPathObj, recursive)

    def list_norefDir_fpaths(self, fname_only=False, asPathObj=False, recursive:bool=True) -> Union[List[str], List[PosixPath]]:
        return self.__list_xDir_fpaths(self.norefDir, fname_only, asPathObj, recursive)

    def list_uploadDir_furls(self, recursive:bool=True) -> List[str]:
        return [self.path2url(path) for path in self.list_uploadDir_fpaths(recursive=recursive)]

    def list_norefDir_furls(self, recursive:bool=True) -> List[str]:
        return [self.path2url(path) for path in self.list_norefDir_fpaths(recursive=recursive)]

    def secure_unique_fname(self, desired_fname:str, xDir:PosixPath) -> str:
        # compares proposed filename with existing,
        # and ensures returning a non-duplicate filename
        # (by adding suffixes if there's existing duplicate)
        if xDir == self.uploadDir:
            existing_fnames:str = self.list_uploadDir_fpaths(fname_only=True, asPathObj=False)
        elif xDir == self.norefDir:
            existing_fnames:str = self.list_norefDir_fpaths(fname_only=True, asPathObj=False)
        else:
            raise Exception(f'bad argument xDir: {xDir} is not a writable subdirectory managed by this object\'s fsroot')

        initial_desired_fname = PosixPath(desired_fname)

        idx = 0
        while(True):
            if desired_fname in existing_fnames:
                desired_fname = initial_desired_fname.stem + f'_{idx}' + initial_desired_fname.suffix
                idx += 1
            else:
                break
        return desired_fname

    def list_md_refs(self, with_mdpaths=False) -> Union[List[str], List[Tuple[PosixPath,str]]]:
        # lists all references in md file except of the external web urls

        mds = self.fsroot.glob('**/*.md')

        mdpaths = []
        refs = []
        for md in mds:
            with open(md, 'r') as f:
                string = f.read()
                html = markdown.markdown(string)
            htmlparser = HTMLRefTagParser()
            try:
                htmlparser.feed(html)
            except Exception as e:
                print(f'Error: {e}, {md}')
            refs.extend(htmlparser.parsedrefs)
            mdpaths.extend([md]*len(htmlparser.parsedrefs))

        if with_mdpaths:
            return mdpaths, refs
        else:
            return refs

    def path2url(self, path:Union[PosixPath, str]) -> str:
        assert(self.path_valid(path)), f'{path} is not a valid path for {self.fsroot}'
        assert(self.path_exists(path)), f'{path} is not a member of {self.fsroot}'
        path = str(path).replace(str(self.fsroot), '')
        url = self.fs_url + str(path)
        assert(self.url_exists(url)), f'url {url} is not member of {self.fs_url}'
        return url

    def url2path(self, url:str) -> PosixPath:
        assert(self.url_valid(url)), f'{url} is not a valid url for {self.fs_url}'
        assert(self.url_exists(url)), f'{url} is not a member of {self.fs_url}'
        subpath = url.replace(self.fs_url+'/', '')
        posixpath = PosixPath(self.fsroot / subpath)
        assert(self.path_exists(posixpath)), f'posixpath {posixpath} is not member of {self.fsroot}'
        return posixpath

    def path_valid(self, path:Union[PosixPath, str]) -> bool:
        return (str(self.fsroot)+'/') in str(path)

    def url_valid(self, url:str) -> bool:
        return (self.fs_url+'/') in url

    def path_exists(self, path:Union[PosixPath, str]) -> bool:
        return self.path_valid(path) and PosixPath(path).exists()

    def url_exists(self, url:str) -> bool:
        # inquire directly to server
        return self.url_valid(url) and requests.get(url).ok


# Markdown Image References Parsing (using html compiled from markdown)
class HTMLRefTagParser(HTMLParser):
        def __init__(self):
            super().__init__()
            self.parsedrefs = []

        def handle_starttag(self, tag, attrs):
            if tag == "img":
                img_uri = dict(attrs)["src"]
                self.parsedrefs.append(img_uri)
            elif tag == 'a':
                href_uri = dict(attrs)["href"]
                try:
                    # if fails attempt to convert to uri (ie. file://), it means it is likely of http:// or https:// format
                    # if attempt successful, append whether it is possible to check if the file path actually exists or not.
                    #   (e.g. Network Attached Storage, etc)
                    assert(PosixPath(href_uri).as_uri())
                    self.parsedrefs.append(href_uri)

                except Exception as e:
                    # if it is a httpfs server url, then append
                    if SERVER_URL in href_uri:
                        self.parsedrefs.append(href_uri)

def build_confs_from_json(fsconf_fpath:PosixPath=FSCONF_FPATH):

    confs = read_conf_json(fsconf_fpath)

    # convert raw string values into appropriate python datatype
    for conf in confs:

        # process readonly value to boolean
        if conf['readonly'] != 'True' and conf['readonly'] != 'False':
            raise ValueError('\'fsname \' {fsname} : property \'readonly\' must be \"True\" or \"False\", actual value: \"{readonly}\"'.format(fsname=conf['fsname'], readonly=conf['readonly']))

        conf['readonly'] = True if conf['readonly'] == 'True' else False

        # process fsroot value to PosixPath
        fsroot = PosixPath(conf['fsroot'])
        if not fsroot.exists():
            print('directory \'fsname \' {fsname} : fsroot path does not exist, therefore will be created.'.format(fsname=conf['fsname']))
            fsroot.mkdir(parents=True, exist_ok=True)

        conf['fsroot'] = fsroot

    # create upload/noref directories needed if managed fsroot will be writable by server
    for conf in confs:
        if conf['readonly']:
            conf['uploadDir'] = None
            conf['norefDir'] = None
            continue

        uploadDir = PosixPath(conf['fsroot']) / UPLOAD_SUBDIR_NAME
        uploadDir.mkdir(exist_ok=True)
        conf['uploadDir'] = uploadDir

        norefDir = PosixPath(conf['fsroot']) / NOREF_SUBDIR_NAME
        norefDir.mkdir(exist_ok=True)
        conf['norefDir'] = norefDir

    # construct dictionary of {key : value} => {fsname : httpfs object}
    fsconfs = dict()
    for conf in confs:
        httpfs = HttpFs(conf)
        fsconfs[httpfs.fsname] = httpfs

    return fsconfs


def read_conf_json(conf_path:PosixPath) -> dict:
    ## call server configuration json file into dict
    with open(conf_path.as_posix(), 'r') as f:
        string = f.read()
        confs = json.loads(string)
    return confs


