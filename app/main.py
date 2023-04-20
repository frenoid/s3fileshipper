from os import getenv
import boto3
import inotify.adapters
import logging
import sys

logging.basicConfig(stream=sys.stdout,
                    level=logging.DEBUG,
                    format="%(asctime)s %(message)s",
                    datefmt="%m/%d/%Y &I:%M:%S %p")



def main():
    logging.info("Start inotify")
    RECURSIVE_WATCH_PATH: str = getenv("RECURSIVE_WATCH_PATH", None)

    if RECURSIVE_WATCH_PATH is None:
        logging.info("Watches are None")
        logging.info("RECURSIVE_WATCH_PATH must be non-empty")
        sys.exit(1)

    AWS_ACCESS_KEY_ID = getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = getenv("AWS_SECRET_ACCESS_KEY")
    S3_BUCKET = getenv("S3_BUCKET")
    S3_KEY_PREFIX = getenv("S3_KEY_PREFIX")
    S3_ENDPOINT = getenv("S3_ENDPOINT", None)
    
    s3_client = boto3.client("s3")

    logging.info("Recursively watching: {}".format(RECURSIVE_WATCH_PATH))
    i = inotify.adapters.InotifyTree(RECURSIVE_WATCH_PATH)

    with open("/tmp/test_file", "w") as f:
        f.write("data data data")
        pass
    with open("/tmp/norman", "w") as f:
        f.write("data data data")
        pass
    with open("/tmp/file1.txt", "w") as f:
        f.write("data data data")
        pass

    for event in i.event_gen(yield_nones=False):
        (_, type_names, path, filename) = event
        logging.info("PATH=[{}] FILENAME=[{}] EVENT_TYPES={}".format(path, filename, type_names))

        if "IN_CLOSE_WRITE" in type_names:
            logging.info("Uploading file {}/{}".format(path, filename))
            reponse = s3_client.upload_file("{}/{}".format(path, filename),
                                            S3_BUCKET,
                                            "{}/{}".format(S3_KEY_PREFIX, filename))

if __name__ == "__main__":
    main()
