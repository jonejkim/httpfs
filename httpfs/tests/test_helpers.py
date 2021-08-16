#!/usr/bin/python
import os, sys
from pathlib import PosixPath
from typing import List
import subprocess

testfiles_dir = PosixPath(__file__).parent / 'testfiles'

def runUploadTest(testName, md, ts, printResult=True):
    printTestName(testName)
    cmd = makeUploadCmd(md, ts)
    code, _, _ = run_subprocess([*cmd])
    if printResult:
        printTestResult(code)
    return code

def makeUploadCmd (md:str, ts:List[str]):
    return 'python3', '-m', 'httpfs.client_typora.img_uploader', '-md', md, '-ts' , *ts

def printTestName(testName):
    testNameLine =  f'== TEST: {testName} =='
    divider = '='*len(testNameLine)
    print('')
    print(f'{divider}')
    print(f'{testNameLine}')
    print(f'{divider}')
    print('')

def printTestResult(code):
    print('[RESULT]:')
    if code == 0:
        print('SUCCESS')

    else:
        print('FAIL')

def run_subprocess(cmd):
    # code reference, modified: https://code-maven.com/python-capture-stdout-stderr-exit

    cmdprint = ' '.join(cmd)
    print(f'[cmd]:\n{cmdprint}\n')

    # turn off output buffering for child process
    os.environ['PYTHONUNBUFFERED'] = "1"
    # run
    proc = subprocess.Popen(cmd,
                            stdout = subprocess.PIPE,
                            stderr = subprocess.PIPE,
                            universal_newlines = True,
                            )
    stdout = []
    stderr = []

    # check if terminated then fetch exitcode/stdout/stderr
    while proc.poll() is None:
        stdout = proc.stdout.readlines()

        stderr = proc.stderr.readlines()

    proc.stdout.close()
    proc.stderr.close()
    proc.terminate()

    stdout = ''.join(stdout)
    stderr = ''.join(stderr)

    print(f'[stdout]:\n{stdout}')
    print(f'[stderr]:\n{stderr}')
    print(f'[code]:\n{proc.returncode}')

    return proc.returncode, stdout, stderr
