# s3fileshipper
It uses inotify to watch a directory and sends the file to S3

It relies on the excellent [PyInotify project](https://github.com/dsoprea/PyInotify) by [Dustin Oprea](https://github.com/dsoprea)

Simple as.

# Getting started
## Without docker
Install requirements <br>
`pip3 install -r`

Set a recursive watch path - s3fileshipper watches this path
`export RECURSIVE_WATCH_PATH=/tmp`

Run the app <br>
`python3 app/main.py`

## With docker
Build the image <br>
`docker build . -t s3fileshipper`

Run the image in detached mode <br>
`docker run -d --name fileshipper --env-file ./env.list s3fileshipper`

Observe the logs <br>
`docker logs fileshipper`


# Incompatibilites
iNotify is incompatible with macOS
It only runs in Linux platforms