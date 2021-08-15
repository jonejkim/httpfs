# Tutorial 3 (Finale)

## `myfsname2` **fs** File Tree

This directory (`../demoDir2/`) corresponds to `myfsname2` ***fs***.

File tree (omitting `.gitignore`):
```
.
├── .imgs
│   ├── example_08.svg
│   ├── example_11.svg
│   ├── example_12.svg
│   ├── example_13.txt
│   └── foobar
│       ├── example_09.svg
│       └── example_10.svg
├── .imgs.noref
└── tutorial_3.md
```

## `mynamefs2` ***fs*** Server Configuration

This directory correspond to the following ***fs*** entry in `fsconfig.json`:
```
    {
        "fsname" : "myfsname2",
        "fsroot" : "{REPO_ROOT}/demo/demoDir2",
        "readonly": "False"
    },
```

## `mynamefs2` ***fs*** Image Gallery

### file:///.../.imgs/example_08.svg
`![](http://127.0.0.1:9999/myfsname2/.imgs/example_08.svg)`
![](http://127.0.0.1:9999/myfsname2/.imgs/example_08.svg)


### file:///.../.imgs/<u>foobar</u>/example_09.svg
`![](http://127.0.0.1:9999/myfsname2/.imgs/foobar/example_09.svg)`
![](http://127.0.0.1:9999/myfsname2/.imgs/foobar/example_09.svg)

## No Reference Remover `httpfs-noref` Demo

Notice for the following files:

- .imgs/<u>foobar</u>/example_10.svg
- .imgs/example_11.svg
- .imgs/example_12.svg
- .imgs/example_13.txt

In common they are part of this ***fs***, but I have not referenced into this markdown using syntax `![](http://...)` nor `<img src="http://...">` syntax. These are considered images with no markdown files referencing them, and some images are no longer needed and get dereferenced over time, and you wish to remove them to make more space or clean up the repository.

`httpfs-noref` is the shell command for no-reference removing script to achieve this. Executing this command, it inspect the entire list of registered ***fs*** to find out which images/files in `.imgs/*` in each ***fs*** are no longer being referenced by any of the markdown files in the same ***fs***.

Exceptions are for `tmp` and `default`, and ***fs*** with `readonly` property `True`.

Here is an example execution with demo configurations:
```
$ httpfs-noref
```
Output (fragment 1)

Self explanatory.
```
===============================================================================
== fsroot name: myfsname3 at /home/jonejkim/Local/repos/httpfs/demo/demoDir3 ==
===============================================================================

(skipping myfsname3 at /home/jonejkim/Local/repos/httpfs/demo/demoDir3 as it is readonly (ie. not writable to .imgs directory)
```

Output (fragment 2)

***fs*** `myfsname3` our current directory, and is not set to be `readonly`.

Notice all files mentioned ahead are detected for no-reference, except for .imgs/<u>foobar</u>/example_10.svg (because it is in subdirectory of `.imgs/*`)

```
===============================================================================
== fsroot name: myfsname2 at /home/jonejkim/Local/repos/httpfs/demo/demoDir2 ==
===============================================================================

##====[ listA: URLs in $/home/jonejkim/Local/repos/httpfs/demo/demoDir2/.imgs/* ]====##
length: 4

http://127.0.0.1:9999/myfsname2/.imgs/example_12.svg
http://127.0.0.1:9999/myfsname2/.imgs/example_11.svg
http://127.0.0.1:9999/myfsname2/.imgs/example_13.txt
http://127.0.0.1:9999/myfsname2/.imgs/example_08.svg

##====[ listB: URL+URI referenced in /home/jonejkim/Local/repos/httpfs/demo/demoDir2/**/*.md ]====##
length: 2

http://127.0.0.1:9999/myfsname2/.imgs/example_08.svg
http://127.0.0.1:9999/myfsname2/.imgs/foobar/example_09.svg

##====[ listD: set(listA) - set(listB) ]====##
length: 3

http://127.0.0.1:9999/myfsname2/.imgs/example_12.svg
http://127.0.0.1:9999/myfsname2/.imgs/example_11.svg
http://127.0.0.1:9999/myfsname2/.imgs/example_13.txt

##====[ listP: listD mapped to equivalent posix paths ]====##
length: 3

/home/jonejkim/Local/repos/httpfs/demo/demoDir2/.imgs/example_12.svg
/home/jonejkim/Local/repos/httpfs/demo/demoDir2/.imgs/example_11.svg
/home/jonejkim/Local/repos/httpfs/demo/demoDir2/.imgs/example_13.txt

[INPUT REQUIRED]
For fs of fsname : "myfsname2", located at "/home/jonejkim/Local/repos/httpfs/demo/demoDir2",
files in .imgs/* with no markdown files referencing (shown in listP above) will be relocated to .imgs.noref/*
Dry run first? [y/n]: y

##====[ (DRY RUN) listR: listP relocated to /home/jonejkim/Local/repos/httpfs/demo/demoDir2/.imgs.noref/* ]====##
length: 3

/home/jonejkim/Local/repos/httpfs/demo/demoDir2/.imgs/example_12.svg
-> /home/jonejkim/Local/repos/httpfs/demo/demoDir2/.imgs.noref/example_12.svg
/home/jonejkim/Local/repos/httpfs/demo/demoDir2/.imgs/example_11.svg
-> /home/jonejkim/Local/repos/httpfs/demo/demoDir2/.imgs.noref/example_11.svg
/home/jonejkim/Local/repos/httpfs/demo/demoDir2/.imgs/example_13.txt
-> /home/jonejkim/Local/repos/httpfs/demo/demoDir2/.imgs.noref/example_13.txt

Proceed relocating? [y/n]: n
```

Output (fragment 3)

Self explanatory.
```

===============================================================================
== fsroot name: myfsname1 at /home/jonejkim/Local/repos/httpfs/demo/demoDir1 ==
===============================================================================

##====[ listA: URLs in $/home/jonejkim/Local/repos/httpfs/demo/demoDir1/.imgs/* ]====##
length: 5

http://127.0.0.1:9999/myfsname1/.imgs/example.md
http://127.0.0.1:9999/myfsname1/.imgs/example_04.svg
http://127.0.0.1:9999/myfsname1/.imgs/example.txt
http://127.0.0.1:9999/myfsname1/.imgs/example.pdf
http://127.0.0.1:9999/myfsname1/.imgs/example_05.svg

##====[ listB: URL+URI referenced in /home/jonejkim/Local/repos/httpfs/demo/demoDir1/**/*.md ]====##
length: 11

http://127.0.0.1:9999/myfsname1/.imgs/example_04.svg
http://127.0.0.1:9999/myfsname1/.imgs/example_05.svg
http://127.0.0.1:9999/myfsname1/.imgs/hello/example_06.svg
http://127.0.0.1:9999/myfsname1/world/example_07.svg
http://127.0.0.1:9999/myfsname1/.imgs/example.md
http://127.0.0.1:9999/myfsname1/.imgs/example.txt
http://127.0.0.1:9999/myfsname1/.imgs/example.pdf
http://127.0.0.1:9999/myfsname2/.imgs/example_10.svg
http://127.0.0.1:9999/default/.imgs/example_03.svg
http://127.0.0.1:9999/myfsname3/books/mockBook.pdf
http://127.0.0.1:9999/myfsname3/papers/mockPaper.pdf

##====[ listD: set(listA) - set(listB) ]====##
length: 0

##====[ listP: listD mapped to equivalent posix paths ]====##
length: 0


There are files with no reference to be relocated. Proceeding to next available httpfs.

```

Output (fragment 4)

Self explanatory.
```
===============================================================================
== fsroot name: default at /home/jonejkim/Local/repos/httpfs/demo/defaultDir ==
===============================================================================

(skipping default at /home/jonejkim/Local/repos/httpfs/demo/defaultDir as it is reserved for default routing for image uploading for unspecified fsname.)
```

Output (fragment 5)

Self explanatory.
```
==============================
== fsroot name: tmp at /tmp ==
==============================

(skipping tmp at /tmp as it is reserved for Typora upload testing only.)

End of the script.
```

After relocation, you may manually verify the content of `.imgs.noref` to confirm you no longer need, and manually delete them.

If there are already existing filenames in the `.imgs.noref`, the file name will be renamed with suffix `_N` added to the file name stem.

## End of Tutorial

This ends the tutorial for httpfs. I hope whoever finds this small program will find it useful.
