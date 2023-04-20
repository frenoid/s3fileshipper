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

Be sure to set your AWS credentials in ENV. See [Environment variables to configure the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-envvars.html)

Run the app <br>
`python3 app/main.py`

## With docker
Build the image <br>
`docker build . -t s3fileshipper`

Run the image in detached mode <br>
`docker run -d --name fileshipper --env-file ./env.list s3fileshipper`

Observe the logs <br>
`docker logs fileshipper`

# How it works
iNotify listens for IN_CLOSE_WRITE events and excludes directory events. When the event occurs, it uploads the files to S3. If you update the file, the file in S3 will be overwritten.

# Incompatibilites
iNotify is incompatible with macOS
It only runs in Linux platforms