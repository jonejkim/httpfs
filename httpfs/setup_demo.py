#!/usr/bin/python
import json
from pathlib import PosixPath
from .constants import FSCONF_TEMPLATE_FPATH
from .common import read_conf_json

thisdir = PosixPath(__file__).parent.absolute()

confs = read_conf_json(FSCONF_TEMPLATE_FPATH)

for conf in confs:
    if conf['fsname'] == 'myfsname3':
        conf['fsroot'] = str(thisdir.parent/'demo/demoDir3')
    if conf['fsname'] == 'myfsname2':
        conf['fsroot'] = str(thisdir.parent/'demo/demoDir2')
    if conf['fsname'] == 'myfsname1':
        conf['fsroot'] = str(thisdir.parent/'demo/demoDir1')
    if conf['fsname'] == 'default':
        conf['fsroot'] = str(thisdir.parent/'demo/defaultDir')

with open(thisdir / 'fsconf.json', 'w') as f:
    json.dump(confs, indent=4, fp=f)
