# Tutorial 1

## about ***fs***

A ***fs*** in the keyword ***httpfs*** loosely stands for file system, or file server. It is a local directory that the httpfs server will manage upload/download. In my use cases, this usually corresponds to a root level of git repository with lots of markdown files of study notes and journal entries.

(***fs*** is probably not a file system nor file server in a rigorous sense, but I could not think of a better name at the time of programming, and still don't really.)

## `default` ***fs*** File Tree

This directory (`../defaultDir/`) is corresponds to `default` ***fs*** managed by the httpfs server.

Take a brief look of the file tree (omitting `.gitignore`):

```
.
├── .imgs
│   ├── example_01.svg
│   ├── example_02.svg
│   ├── example_03.svg
│   ├── typora_img_uploader1.png
│   └── typora_img_uploader2.png
├── .imgs.noref
└── tutorial_1.md // (we are viewing this file)
```

## `default` ***fs*** Server Configuration

This directory corresponds to the following entry of the `fsconf.json` (auto-generated from `fsconf-template.json`):
```json
[
    ...
    {
        "fsname" : "default",
        "fsroot": "{REPO_ROOT}/demo/defaultDir",
        "readonly": "False",
        ...
    },
    ...
]
```
The key-values consists of all essential configs required for a ***fs*** managed by the httpfs server:

- Key-value {"`fsname`": "`default`"} : This indicates the httpfs server URL you will use to access the content in this directory tree. ie. (http://127.0.0.1:9999/default/). They each ***fs*** is designed to have a dedicated `fsname` to prevent different directories of the directory name possibly conflicting. Please keep the characters simple and URL address encoding compliant (e.g. small case alphabets because cases are ignnored in URL, etc).

    "`default`" (this directory) is a reserved `fsname` value. `default` is for any image/file uploads that don't have its destination specified. Only `fsroot` value of this directory may be changed.

    "`tmp`" is another reserved `fsname` value. `tmp` ***fs*** is a Typora compliant configuration for upload testing UI in Typora's preferences menu (will see in next tutorial). No entries in this directory should be changed, unless not using Typora.

- Key-value {"`fsroot`": "`default`"} and its value is the absolute local file path (posix) of this directory, in which the server will manage read/write.

- key-value {"`readonly`": "`False`"} can only have one of two values:`"True"` or `"False"` (correpsonds to python boolean values typed out as in quotes). This indicates whether this ***fs*** is only for read (`"True"`) or read/write (`"False"`). Usage of read only state may be for archived directories not being changed anymore.

- (Optional) additional key-values such as {"`comment`":"..."} can be used to make notes because JSON does not support comments natively. All of other key values other than the above three will be ignored.


## Querying File Path / URL in ***fs*** to the httpfs server

`httpfsq` command, with a httpfs URL or local file absolute path as an input argument, will find you the corresponding local file path or httpfs URL. Following should work with the initial configuration of httpfs server:

```bash
# use your own full absolute path to this repository for REPO_ROOT variable here:
$ httpfsq /home/jonejkim/Local/repos/httpfs/demo/defaultDir/.imgs/example_01.svg
http://127.0.0.1:9999/default/.imgs/example_01.svg
## or equivalently with "file://"
$ httpfsq file:///home/jonejkim/Local/repos/httpfs/demo/defaultDir/.imgs/example_01.svg
http://127.0.0.1:9999/default/.imgs/example_01.svg
```

Feeding the output back into `httpfsq`:
```bash
$ httpfsq http://127.0.0.1:9999/default/.imgs/example_01.svg
/home/jonejkim/Local/repos/httpfs/demo/defaultDir/.imgs/example_01.svg
```

It can also print current list of of ***fs*** configurations in `fsconf.json` using `-fs` option:
```
$ httpfsq -fs
      fsname   readonly   fsroot
   myfsname3 :     True : /home/jonejkim/Local/repos/httpfs/demo/demoDir3
   myfsname2 :    False : /home/jonejkim/Local/repos/httpfs/demo/demoDir2
   myfsname1 :    False : /home/jonejkim/Local/repos/httpfs/demo/demoDir1
     default :    False : /home/jonejkim/Local/repos/httpfs/demo/defaultDir
         tmp :    False : /tmp
```

(Troubleshooting) if `httpfsq` doesnt work properly with the file path or URL you have provided, check that it is:
- a full absolute path
- posix path compliant (windows path not supported)
- if the path has any spaces. in this case you will need to surround your path with single or double quotes for the query program to not confuse space as separators for multiple arguments.
- Piping into `httpfq` (e.g. `echo  "http://127.0.0.1:9999/default/.imgs/example_01.svg" | httpfsq` ) is not supported. You are welcome to write it if you would like.
- Piping out from `httpfsq` works (e.g. copy to clipboard `httpfsq http://127.0.0.1:9999/default/.imgs/example_01.svg | xclip -selection clipboard`)

## `default` ***fs*** Image Gallery

The following images are attached via httpfs URLs to the images corresponding to  `.imgs` in this directory.

- if in Typora, images should be loaded successfully if the httpfs server is already running.

- if you are in VSCode's markdown viewer, you may need to allow loading insecure local contents minimally.

### file:///.../defaultDir/.imgs/example_01.svg
`![](http://127.0.0.1:9999/default/.imgs/example_01.svg)`
![](http://127.0.0.1:9999/default/.imgs/example_01.svg)

### file:///.../defaultDir/.imgs/example_02.svg
`![](http://127.0.0.1:9999/default/.imgs/example_02.svg)`
![](http://127.0.0.1:9999/default/.imgs/example_02.svg)

### file:///.../defaultDir/.imgs/example_03.svg
You may also tag with <img> tag in markdown.

`<img src="http://127.0.0.1:9999/default/.imgs/example_03.svg">`
<img src="http://127.0.0.1:9999/default/.imgs/example_03.svg">

## Uploading your own Images (for Typora users)

As httpfs was mainly written for usage along with Typora, it comes with a image uploader specifically written for automated image uploading within Typora. To use this feature, set your Typora image preference as the following:

![](http://127.0.0.1:9999/default/.imgs/typora_img_uploader1.png)

For `When Insert...` dropdown menu, select `Upload Image`. Apply the check boxes as it fits your need.

For `Image Uploader` dropdown menu, select `Custom Command`.

Copy/paste the following in to the `Commmand` textbox:

```sh
python3 -m httpfs.client_typora.img_uploader -md "${filepath}" -ts
```

- `-md` parameter is a markdown file currently being editted, so the uploader and httpfs server will know which ***fs*** it needs to uploade the image to. `"${filepath}"` is an argument that Typora will provide to the uploader.
- `-ts` parameter accepts number of target images that

Now click `Test Uploader` button and the following should appear if successful. If not, make sure you have your server up and running with `httpfs-srv` command.

![](http://127.0.0.1:9999/default/.imgs/typora_img_uploader2.png)

Now you can copy/paste images from clipboard or web URLs into Typora, and it should upload according to the configurations in `fsconf.json`. Uploading images with already existing file names will be renamed with added numeral suffix `_N` in the file name stem.

## Next

Proceed and open `../demofs1/tutorial_2.md` for next tutorial.