# Tutorial 0 - Launching httpfs Server

Once installed using `setup.sh` script in the root of repository, start the httpfs server by typing command in bash (or tweak to be used other shells of your choice):

```bash
$ httpfs-srv
```
You should see terminal output running Flask server like the following:
```
 * Serving Flask app 'server' (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://127.0.0.1:9999/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * ...

```

(Optionally), if you want to detach the process from terminal foreground to let server run in the background, I have already coded that capability using terminal multiplexer `tmux` (needs to be installed if your system doesn't have it).
```bash
$ httpfs-srv d # d for detach
```
Once launched you can typically press `ctrl+b` then `ctrl+d` to detach.

To reattach execute `tmux a` implicitly or `tmux a -t httpfs-srv` explicit with the tmux session.

## Understanding what httpfs Server is managing

httpfs server manages only the directories you have configured in `httpfs/fsconf.json`.

Upon initial installation, the `fsconf.json` will be having httpfs server to dictate the three subdirectories in this demo directory.

### File Retrieval (HTTP GET method)

For retrieval of files via HTTP GET method, the mapping looks as the following:

- `fsname`: `default`,  `fsroot`: `./defaultDir/**/*`

    --- retrieval ---> `http://127.0.0.1:9999/default/**/*`

- `fsname`: `myfsname1`,  `fsroot`: `./demoDir1/**/*`

    --- retrieval ---> `http://127.0.0.1:9999/myfsname1/**/*`

- `fsname`: `myfsname2`,  `fsroot`: `./demoDir2/**/*`

    --- retrieval ---> `http://127.0.0.1:9999/myfsname2/**/*`

Where `**/*` indicates the entire tree under recursively. Demo of this is shown in `./demoDir1/tutorial_2.md`

### File Upload (HTTP POST method)

For uploading of files via HTTP POST method, server will only post to the following subset of the file tree mentioned above:

- `fsname`: `default`,  `fsroot`: `./defaultDir/.imgs/*`

    --- corresponding to ---> `http://127.0.0.1:9999/default/.imgs/*`

- `fsname`: `myfsname1`,  `fsroot`: `./demoDir1/.imgs/*`

    --- corresponding to ---> `http://127.0.0.1:9999/myfsname1/.imgs/*`

- `fsname`: `myfsname2`,  `fsroot`: `./demoDir2/.imgs/*`

    --- corresponding to ---> `http://127.0.0.1:9999/myfsname2/.imgs/*`

Where single wildcard `*` in `.imgs/*` indicates only the top level of `.imgs` directory only (ie. no files in subdirectories of `.imgs`). Demo of this is shown in `./demoDir1/tutorial_2.md`

## Next

Now proceed to next tutorial by opening `./defaultDir/tutorial_1.md` with your editor of choice (e.g. Typora, VSCode, etc)

Following is a simplified overview of this demo directory:
```
.
├── defaultDir
│   ├── .imgs
│   │   └── ...
│   ├── .imgs.noref
│   └── tutorial_1.md
├── demoDir1
│   ├── .imgs
│   │   └── hello
│   │       └── ...
│   ├── .imgs.noref
│   ├── tutorial_2.md
│   └── world
│       └── ...
├── demoDir2
│   ├── .imgs
│   │   ├── ...
│   │   └── foobar
│   │       └── ...
│   ├── .imgs.noref
│   │   └── .gitignore
│   └── tutorial_3.md
├── demoDir3
│   ├── books
│   │   └── ...
│   └── papers
│       └── ...
└── tutorial_0.md
```

