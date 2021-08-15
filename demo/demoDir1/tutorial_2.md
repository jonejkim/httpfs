# Tutorial 2

## `myfsname1` **fs** Local File Tree

This directory (`../demoDir1/`) corresponds to `myfsname1` ***fs***.

File tree (omitting `.gitignore`):
```
.
├── .imgs
│   ├── example_04.svg
│   ├── example_05.svg
│   ├── example_06.svg
│   ├── example.md
│   ├── example.pdf
│   ├── example.txt
│   └── hello
│       └── example_06.svg
├── .imgs.noref
├── tutorial_2.md // (we are viewing this file)
└── world
    └── example_07.svg
```

## `mynamefs1` ***fs*** Server Configuration

This directory correspond to the following ***fs*** entry in `fsconfig.json`:

```json
[
    ...
    {
        "fsname": "myfsname1",
        "fsroot": "{REPO_ROOT}/demo/demoDir1",
        "readonly": "False",
        "comment": "...(abbreviated)..."
    },
    ...
]
```

## `mynamefs1` ***fs*** Image Gallery

The following are images saved to `.imgs/*`

In my use cases, a non `default` ***fs*** typically is also a top level of a `git` repository, and I use along with Git Large File Storage (`git lfs`) to have images saved as part of large file storage if needed.

### file:///.../.imgs/example_04.svg
`![](http://127.0.0.1:9999/myfsname1/.imgs/example_04.svg)`
![](http://127.0.0.1:9999/myfsname1/.imgs/example_04.svg)

### file:///.../.imgs/example_05.svg
`![](http://127.0.0.1:9999/myfsname1/.imgs/example_05.svg)`
![](http://127.0.0.1:9999/myfsname1/.imgs/example_05.svg)


## Lesson: Upload goes to `./imgs/*` only, while Download can be level of ***fs*** file tree.

### file:///.../.imgs/<u>hello</u>/example_06.svg
`![](http://127.0.0.1:9999/myfsname1/.imgs/hello/example_06.svg)`
![](http://127.0.0.1:9999/myfsname1/.imgs/hello/example_06.svg)

Notice that this image is part of `.imgs`, but a subdirectory below`.imgs/hello/`. Uploading via server will never write into this level. Only way to make this subdirectory is by you manually creating it on your local file system. However since this is the tree fs manages, it will still be obtainable through downlading.

Restricting the upload directory to `.imgs/*` and no other (ie. not even its subdirectory) is to keep the image upload/management linearly without depending on where the markdown file is, which its path may be relocated from time to time while image linked in it stays the unchanged.

### file:///.../<u>world</u>/example_07.svg
`![](http://127.0.0.1:9999/myfsname1/world/example_07.svg)`
![](http://127.0.0.1:9999/myfsname1/world/example_07.svg)

Notice that this image is located outside of the our usual `.imgs` directory, but still under the this ***fs*** file tree. Therefore this image will still be accessible via httpfs.

## Using httpfs for Non-images

Although majority of use my cases are intended for referencing images in markdown, httpfs use case is not only limited to it. You may access ***any*** other files as long as they are part of the ***fsroot*** the of the ***fs*** being managed. Following links are such examples:

[http://127.0.0.1:9999/myfsname1/.imgs/example.md](http://127.0.0.1:9999/myfsname1/.imgs/example.md)

[http://127.0.0.1:9999/myfsname1/.imgs/example.txt](http://127.0.0.1:9999/myfsname1/.imgs/example.txt)

[http://127.0.0.1:9999/myfsname1/.imgs/example.pdf](http://127.0.0.1:9999/myfsname1/.imgs/example.pdf)

However as opening non-images via HTTP with web browser for may trigger unnecessary download to your default Downloads directory, use it as you see the need.

## Cross-referencing to different ***fs***

Although we are currently in ***fs*** `fsname1`, you are not restricted from cross-referencing files in other ***fs***. Such as:

`![](http://127.0.0.1:9999/myfsname2/.imgs/example_10.svg)`
![](http://127.0.0.1:9999/myfsname2/.imgs/example_10.svg)

However I would not recommend doing this often as it defies the purpose (at least in my case of use) of having dedicated ***fs*** in each markdown intensive repository.

However two use cases may be healthy for cross-referencing.

Case 1) Cross-referencing to `default` ***fs***

because it is the uploading site speicifically designed for images unspecified of their destination ***fs***. Such as:

`![](http://127.0.0.1:9999/default/.imgs/example_03.svg)`
![](http://127.0.0.1:9999/default/.imgs/example_03.svg)

Case 2) ***fs*** declared specifically as `readonly`.

In my case, I use `readonly` ***fs*** for libraries of books, paper pdfs, video, media, etc. These type of directories don't get their file structure changed often, and content changes are mostly additive operation of files.

Examples are from `myfsname3` ***fs***, which are set to `readonly`:

[http://127.0.0.1:9999/myfsname3/books/mockBook.pdf](http://127.0.0.1:9999/myfsname3/books/mockBook.pdf)

[http://127.0.0.1:9999/myfsname3/papers/mockPaper.pdf](http://127.0.0.1:9999/myfsname3/papers/mockPaper.pdf)

## Next

Proceed and open `../demofs1/tutorial_2.md` for the final tutorial.