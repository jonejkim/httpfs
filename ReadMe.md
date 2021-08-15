# httpfs – a Local HTTP File Server and Image Uploader for Markdown Image Link Management with Typora

## What is this?

***httpfs*** is a local HTTP file server with uploader (for Typora) that helps you manage image/file references in your markdown in your repository/directory more manageable, trackable, and private.

The short clip below is a quick preview on what httpfs tries to achieve with Markdown editing (shown markdown editor is [Typora](https://typora.io))

![Preview Video](./demo/preview.gif)

### Motivation
[Typora](https://typora.io), a GUI markdown editor, supports pasting images into the markdown files from clipboard or web URL to your markdown in WYSWYG ("What you see is what you get") manner, providing pasted images to be saved as original URL, or as local file path (relative/absolute) or [uploading to your image server of choice](https://support.typora.io/Upload-Image/).

My use cases of Typora was mostly having multiple `git` repositories full of markdown files ranging from personal memos, journals, study notes, etc. I was initially storing images in directories relative to the markdown file it was referencing. I soon encountered into some problems:

1. Notes I made in markdown often needed to be splitted, renamed, moved around in file tree hierarchy, and moving images referenced relatively along with it was often difficult. Tracking and fixing broken references to relatively stored images tedious, the more I needed to move around my files.

2. Option of saving to one absolute path was of no interest for me because I wanted to keep the images in each repository/tree only belong to that repository, and trackable. Typora did not provide this capability.

3. I did not want to use public image servers or subscribed web markdown-line solutions like Notion, because I wanted to have the files completely under my control, trackable within my own repository and gitlab.

### Solution

I created a simple local http server to be used in uploading images into a hidden directory at the root (`${REPO_ROOT}/.imgs/`) of my multiple markdown repositories, the same level where `.git` or `.vscode` directory is placed. I chose to call this solution ***httpfs*** for convenience.

With httpfs running along with Typora, pasting web image URL or image in clipbard will be automatically be to the httpfs server, which in turn will know which `.imgs` subdirectory of your repository to be stored into, based on where your markdown file you are editing is located.

 With this, I now am able to:

1. Keep images trackable in their relavant repository (optionally used with with git LFS for Large File Storage)

2. Can move around markdown files within the repo without worrying about breaking links.

3. Not rely on public cloud solutions and keep my images self contained within the repository and fully under my control.

It was written for my personal use initially, but I saw why not in sharing it for those who may find it useful.


## Just Get Me Started

### Requirements

- Operating System: Linux or POSIX compliant Operating Systems (was only tested on Manjaro/Arch Linux)
- Python3 and pip (3.8+, native installed rather than `conda` Python recommended)
- tmux (optional. for detaching terminal for the server process into background)
- (Was written and tested only in `bash` shell. I trust people using other than bash will already know enough to get it to work in their own shell.)

### Install
1. Download or `git clone` this repository to your local file system.
2. `bash install.sh` to install. This will `httpfs` as a editable/development pip package along with package requirements (detail in `setup.py`) and add executable scripts to your `~/.bashrc`
3. `source ~/.bashrc`
4. Launch server with command `httpfs-srv` or `httpfs-srv d` to detach with tmux.

### Image Uploader Setting in Typora:

The following are the settings for Typora. `Upload Image`, `Custom Command`, `Command` are essential, while checkboxes may be adjusted to your needs.

![](./demo/defaultDir/.imgs/typora_img_uploader1.png)

Copy/paste the following command into the `Command` text box:

```bash
python3 -m httpfs.client_typora.img_uploader -md "${filepath}" -ts
```

While `httpfs-srv` is running, press `Test Uploader`. If validation success as the following, you are ready to use.

![](./demo/defaultDir/.imgs/typora_img_uploader2.png)


For more details I recommend looking into the `demo` directory I have provided to run out of the box.

### Demo / Quick Tutorials

The entire `./demo` directory was designed to give quick tutorials on features/details of httpfs with live examples configured to work out of the box.

Open  `./demo/tutorial_0.md` preferrably with Typora, or other markdown viewers of your choice to get started.

### Uninstall

1. Run `bash uninstall.sh` and the script will remove all executables and `httpfs` pip package.
2. Delete the repository.

## Misc
### Targetted Scope of Usage

- This was written for use with **Typora** mainly, but I don't see why it can't be tweaked for other Markdown editors, or else.

- You are welcome tweak, write your won based on these scripts.

- Although I use it for image uploads mainly, the upload/download is not necessarily limited to images, but any other files. Hence why a file server.

### Security

- httpfs was written only for use with localhost (e.g. loopback ip address `127.0.0.1`), or perhaps a trusted Local Area Network use at most. I cannot warrant any security issues beyond this, nor have the time or need to go beyond this for my use cases. Please proceed with caution, and use it at your own risk.

- More security measures will need to be made if it is to be exposed to other computers within an untrusted LAN, or on the public internet. Please proceed at your own risk if you know what you are doing. These security measures will entail non-exahustive list of features like HTTPS/TLS encryption, dockerization, production level HTTP server (Apache, etc), adding authentication, etc.

### Unit Testing

Basic set of unit tests on communication between Typora uploader client `httpfs.client_typora.img_uploader` and `httpfs.server.server` has been written. You can execute the unit test by simply running `python3 -m httpfs.tests.run_unittest` while having the `httpfs-srv` running on another terminal. All should show `SUCCESS` if working properly.

### Repository Status & Contribution

The current code has been enough for covering my personal usage cases, and I do not plan on actively maintaining this repository unless I add more features or find major bugs and fixes down the road. Please feel free to contrubute/fork if you would like to.