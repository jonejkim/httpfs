#!/usr/bin/python
import sys
from typing import *
from pathlib import PosixPath
class Bcolors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# core_dir = PosixPath('.').parent.absolute() / 'core'
core_dir = PosixPath(__file__).parent.parent / 'core'
sys.path.append(str(core_dir))

from httpfs.common import FsConf, UPLOAD_SUBDIR_NAME, build_confs_from_json

FSCONFS = build_confs_from_json()

printlist = lambda lst: [print(entry) for entry in lst]

def printbig(string:str):
    testNameLine =  f'== {string} =='
    divider = '='*len(testNameLine)
    print('')
    print(f'{divider}')
    print(f'{testNameLine}')
    print(f'{divider}')
    print('')


if __name__ == '__main__':

    for fsname, fsconf in FSCONFS.items():
        printbig(f'fsroot name: {fsname} at {fsconf.fsroot}')

        if fsconf.readonly:
            print(f'(skipping {fsconf.fsname} at {fsconf.fsroot} as it is readonly (ie. not writable to {UPLOAD_SUBDIR_NAME} directory)')
            continue
        elif fsconf.fsname == 'default':
            print(f'(skipping {fsconf.fsname} at {fsconf.fsroot} as it is reserved for default routing for image uploading for unspecified fsname.)')
            continue
        elif fsconf.fsname == 'tmp':
            print(f'(skipping {fsconf.fsname} at {fsconf.fsroot} as it is reserved for Typora upload testing only.)')
            continue


        all_uploaded = fsconf.list_uploadDir_furls(recursive=False)
        all_refereds = fsconf.list_md_refs()


        print(f'##====[ listA: URLs in ${str(fsconf.uploadDir)}/* ]====##')
        print(f'length: {len(all_uploaded)}', end='\n\n')
        printlist(all_uploaded)
        print('', end='\n\n')

        print(f'##====[ listB: URL+URI referenced in {str(fsconf.fsroot)}/**/*.md ]====##')
        print(f'length: {len(all_refereds)}', end='\n\n')
        printlist(all_refereds)
        print('', end='\n\n')

        print('##====[ listD: set(listA) - set(listB) ]====##')
        not_refereds = set(all_uploaded) - set(all_refereds)
        print(f'length: {len(not_refereds)}', end='\n\n')
        printlist(not_refereds)
        print('', end='\n\n')

        print('##====[ listP: listD mapped to equivalent posix paths ]====##')
        posixpaths = [fsconf.url2path(noref) for noref in not_refereds]
        print(f'length: {len(posixpaths)}', end='\n\n')
        printlist(posixpaths)
        print('', end='\n\n')

        print('')

        if len(posixpaths) == 0:
            print('There are files with no reference to be relocated. Proceeding to next available httpfs.')
            continue

        def relocate(posixpaths:PosixPath, fsconf:FsConf, dryrun:bool):
            renamedPath_pairs = []
            for posixpath in posixpaths:
                # secure new unique filename for conflicting ones instead of overwrite
                desired_fname = posixpath.name
                unique_fname:str = fsconf.secure_unique_fname(desired_fname , fsconf.norefDir)
                renamedPath = fsconf.norefDir / unique_fname

                if not dryrun:
                    renamedPath = posixpath.rename(renamedPath)

                renamedPath_pairs.append([posixpath, renamedPath])

            return renamedPath_pairs


        print('[INPUT REQUIRED]')
        print(f'For fs of fsname : \"{fsconf.fsname}\", located at \"{str(fsconf.fsroot)}\",')
        print(f'files in {str(fsconf.uploadDir.name)}/* with no markdown files referencing (shown in listP above) will be relocated to {str(fsconf.norefDir.name)}/*')

        userInp_dryrun = input(f'Dry run first? [y/n]: ')
        print('')
        if userInp_dryrun.lower() == 'y':
            renamedPath_pairs = relocate(posixpaths, fsconf, dryrun=True)

            print(f'##====[ (DRY RUN) listR: listP relocated to {fsconf.norefDir}/* ]====##')
            print(f'length: {len(renamedPath_pairs)}', end='\n\n')
            for originalPath, renamedPath in renamedPath_pairs:
                print(f'{originalPath.parent.parent}/{Bcolors.BOLD}{Bcolors.YELLOW}{originalPath.parent.name}{Bcolors.ENDC}/{originalPath.name}')
                print(f'-> {renamedPath.parent.parent}/{Bcolors.BOLD}{Bcolors.RED}{renamedPath.parent.name}{Bcolors.ENDC}/{renamedPath.name}')
            print('', end='\n\n')

        elif userInp_dryrun.lower() == 'n':
            pass

        else:
            raise Exception('Bad input: must be one of \'y\' or \'n\'')

        userInp_proceed = input(f'Proceed relocating? [y/n]: ')
        if userInp_proceed.lower() == 'y':
            renamedPath_pairs = relocate(posixpaths, fsconf, dryrun=False)

            print(f'##====[ listR: listP relocated to {fsconf.norefDir}/* ]====##')
            print(f'length: {len(renamedPath_pairs)}', end='\n\n')
            for originalPath, renamedPath in renamedPath_pairs:
                print(f'{originalPath.parent.parent}/{Bcolors.BOLD}{originalPath.parent.name}{Bcolors.ENDC}/{originalPath.name}')
                print(f'-> {renamedPath.parent.parent}/{Bcolors.BOLD}{renamedPath.parent.name}{Bcolors.ENDC}/{renamedPath.name}')
            print('', end='\n\n')

        elif userInp_proceed.lower() == 'n':
            pass

        else:
            raise Exception('Bad input: must be one of \'y\' or \'n\'')

    print('\nEnd of the script.', end='\n\n')
